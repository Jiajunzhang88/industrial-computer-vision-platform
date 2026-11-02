from fastapi import APIRouter, Depends, HTTPException, Response, Request, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from ..services.camera import camera_service
from ..services.settings import SettingsService
from sqlalchemy.orm import Session
from ..dependencies import get_db
import logging
import numpy as np
import cv2
import base64

logger = logging.getLogger(__name__)

# 处理请求模型
class ProcessingRequest(BaseModel):
    camera_id: Optional[str] = None      # 摄像头ID
    operation_id: int                    # 操作ID
    operation_type: str = "operation"    # 操作类型：'operation' 或 'pipeline'

router = APIRouter(
    prefix="/api/cameras",
    tags=["cameras"]
)

@router.get("/detect", response_model=List[Dict])
def detect_cameras():
    """检测系统中可用的摄像头"""
    return camera_service.detect_cameras()

@router.get("/{camera_id}/stream")
def stream_camera(
    camera_id: str,
    operation_id: Optional[int] = None,
    operation_type: str = "operation",
    db: Session = Depends(get_db)
):
    """
    统一的摄像头流端点，支持普通流和处理流
    
    参数:
    - camera_id: 摄像头ID（数字或格式为camera_X）
    - operation_id: 可选，操作或流水线ID。如果提供则返回处理流，否则返回普通流
    - operation_type: 'operation'(默认) 或 'pipeline'，仅当operation_id存在时有效
    
    返回:
    - 摄像头的MJPEG流（原始或经过处理）
    """
    try:
        # 规范化摄像头ID
        if not camera_id.startswith("camera_") and camera_id.isdigit():
            camera_id = f"camera_{camera_id}"
        
        logger.info(f"Stream request - camera: {camera_id}, operation: {operation_id}, type: {operation_type}")
        
        # 确保摄像头是打开的
        with camera_service._cameras_lock:
            if camera_id not in camera_service._cameras:
                device_id = camera_id.replace("camera_", "")
                try:
                    device_id = int(device_id)
                except ValueError:
                    device_id = device_id  # 保持字符串格式
                    
                if not camera_service.open_camera(camera_id, device_id):
                    logger.error(f"Failed to open camera {camera_id}")
                    raise HTTPException(status_code=404, detail=f"无法打开摄像头 {camera_id}")
            
            # 确保摄像头在流式传输
            if not camera_service._cameras[camera_id].is_streaming:
                if not camera_service.start_stream(camera_id):
                    logger.error(f"Failed to start camera stream {camera_id}")
                    raise HTTPException(status_code=500, detail=f"无法启动摄像头流 {camera_id}")
        
        # 普通流 - 无操作参数
        if operation_id is None:
            logger.info(f"Providing regular stream for camera {camera_id}")
            return StreamingResponse(
                camera_service.get_mjpeg_frame_generator(camera_id),
                media_type="multipart/x-mixed-replace; boundary=frame"
            )
        
        # 处理流 - 验证操作参数
        if not isinstance(operation_id, int) or operation_id <= 0:
            raise HTTPException(status_code=422, detail=f"无效的操作ID: {operation_id}")
            
        if operation_type not in ["operation", "pipeline"]:
            raise HTTPException(status_code=422, detail=f"无效的操作类型: {operation_type}")
            
        # 验证操作是否存在
        if operation_type == "operation":
            from ..services.cv_operation import CVOperationService
            operation_service = CVOperationService(db)
            operation = operation_service.get_operation(operation_id)
            if not operation:
                raise HTTPException(status_code=404, detail=f"未找到指定的操作 (ID: {operation_id})")
        elif operation_type == "pipeline":
            from ..services.pipeline import PipelineService
            pipeline_service = PipelineService(db)
            pipeline = pipeline_service.get_pipeline(operation_id)
            if not pipeline:
                raise HTTPException(status_code=404, detail=f"未找到指定的流水线 (ID: {operation_id})")
        
        # 获取或启动处理流
        stream_key = camera_service.get_processed_stream_key(camera_id, operation_id, operation_type)
        with camera_service._streams_lock:
            if stream_key not in camera_service._processed_streams:
                if not camera_service.start_processed_stream(camera_id, operation_id, operation_type, db):
                    raise HTTPException(status_code=500, detail="无法启动处理流")
        
        # 返回处理后的流
        logger.info(f"Providing processed stream for camera {camera_id} with operation {operation_id}")
        return StreamingResponse(
            camera_service.get_processed_mjpeg_frame_generator(camera_id, operation_id, operation_type, db),
            media_type="multipart/x-mixed-replace; boundary=processedframe"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Stream error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"视频流错误: {str(e)}")

@router.get("/{camera_id}/snapshot")
def get_camera_snapshot(
    camera_id: str, 
    operation_id: Optional[int] = None,
    operation_type: str = "operation",
    return_json: bool = False,
    db: Session = Depends(get_db)
):
    """获取摄像头的单帧快照，可选择应用处理操作
    
    参数:
    - camera_id: 摄像头ID
    - operation_id: 可选，操作ID或流水线ID
    - operation_type: 操作类型，'operation'(默认)或'pipeline'
    - return_json: 是否返回JSON格式数据，包含识别文字和置信度
    """
    try:
        # 规范化摄像头ID
        if not camera_id.startswith("camera_") and camera_id.isdigit():
            camera_id = f"camera_{camera_id}"
        
        logger.info(f"快照请求 - 摄像头: {camera_id}, 操作: {operation_id}, 类型: {operation_type}, 返回JSON: {return_json}")
        
        # 确保摄像头是打开的
        with camera_service._cameras_lock:
            if camera_id not in camera_service._cameras:
                device_id = camera_id.replace("camera_", "")
                try:
                    device_id = int(device_id)
                except ValueError:
                    pass  # 保持原始字符串
                    
                if not camera_service.open_camera(camera_id, device_id):
                    raise HTTPException(status_code=404, detail="无法打开摄像头")
        
        # 获取帧
        success, frame_data = camera_service.get_frame(camera_id)
        if not success or not frame_data:
            raise HTTPException(status_code=500, detail="无法获取摄像头帧")
        
        # 如果未指定操作，直接返回原始帧
        if operation_id is None:
            if return_json:
                # 将原始帧转为base64
                base64_data = base64.b64encode(frame_data).decode('utf-8')
                return {
                    "image": f"data:image/jpeg;base64,{base64_data}",
                    "text": "",
                    "confidence": 0,
                    "passed": False
                }
            else:
                return Response(content=frame_data, media_type="image/jpeg")
        
        # 验证操作参数
        if not isinstance(operation_id, int) or operation_id <= 0:
            raise HTTPException(status_code=422, detail=f"无效的操作ID: {operation_id}")
            
        if operation_type not in ["operation", "pipeline"]:
            raise HTTPException(status_code=422, detail=f"无效的操作类型: {operation_type}")
        
        # 如果需要返回JSON格式，但请求处理后的数据
        if return_json:
            try:
                # 使用带详情的处理方法，同时拿到图像和结构化输出参数
                processed_frame, outputs = camera_service.apply_operation_to_frame_with_details(
                    frame_data, operation_id, operation_type, db
                )

                if not processed_frame:
                    processed_frame = frame_data

                # 如果 outputs 里已经带了画好检测框的 base64 图（YOLO fallback 路径），优先用它
                annotated_b64 = None
                detections = []
                if outputs:
                    if isinstance(outputs.get("image"), str) and outputs["image"]:
                        annotated_b64 = outputs.pop("image")
                    if isinstance(outputs.get("detections"), list):
                        detections = outputs.pop("detections")

                # 将处理后的图像转为base64
                base64_data = base64.b64encode(processed_frame).decode('utf-8')

                # 从结构化输出中提取 confidence / passed / 可读 text
                confidence = 0.0
                text_parts = []
                passed = False
                for k, v in (outputs or {}).items():
                    kl = str(k).lower()
                    if kl in ('confidence', 'score', 'probability', 'conf'):
                        try:
                            confidence = float(v)
                        except (TypeError, ValueError):
                            pass
                    elif kl in ('passed', 'is_passed', 'ok', 'success', 'is_ok'):
                        passed = bool(v)
                    elif v is not None:
                        text_parts.append(f"{k}: {v}")
                text = ", ".join(text_parts) if text_parts else ""

                # 保存报警图和日志到 record 目录（在原始帧上画检测框后保存）
                try:
                    from datetime import datetime as _dt
                    import os as _os
                    import cv2 as _cv2
                    _root = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))))
                    _alarm_dir = _os.path.join(_root, "record", "alarm_png")
                    _log_dir = _os.path.join(_root, "record", "log")
                    _os.makedirs(_alarm_dir, exist_ok=True)
                    _os.makedirs(_log_dir, exist_ok=True)
                    _ts = _dt.now().strftime("%Y%m%d_%H%M%S_%f")
                    # 解码原始帧，在上面画检测框
                    _nparr = np.frombuffer(processed_frame, np.uint8)
                    _img = _cv2.imdecode(_nparr, _cv2.IMREAD_COLOR)
                    if _img is not None and detections:
                        for _d in detections:
                            _bbox = _d.get("bbox", [0,0,0,0])
                            _x1, _y1, _x2, _y2 = [int(v) for v in _bbox]
                            _cv2.rectangle(_img, (_x1, _y1), (_x2, _y2), (0, 255, 0), 2)
                            _label = f"{_d.get('class_name','')} {_d.get('confidence',0)*100:.1f}%"
                            _cv2.putText(_img, _label, (_x1, max(_y1-5, 10)), _cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
                    _, _jpeg = _cv2.imencode(".jpg", _img)
                    _img_path = _os.path.join(_alarm_dir, f"alarm_{_ts}.jpg")
                    with open(_img_path, "wb") as _f:
                        _f.write(_jpeg.tobytes())
                    _log_path = _os.path.join(_log_dir, f"detection_{_dt.now().strftime('%Y%m%d')}.log")
                    with open(_log_path, "a", encoding="utf-8") as _lf:
                        _lf.write(f"[{_dt.now().strftime('%Y-%m-%d %H:%M:%S')}] camera={camera_id} op={operation_id} type={operation_type} text={text} confidence={confidence:.4f} dets={len(detections)}\n")
                except Exception as _save_err:
                    logger.warning(f"保存报警图/日志失败: {_save_err}")

                return {
                    "image": f"data:image/jpeg;base64,{annotated_b64}" if annotated_b64 else f"data:image/jpeg;base64,{base64_data}",
                    "text": text,
                    "confidence": confidence,
                    "passed": passed,
                    "detections": detections,
                    "outputs": outputs or {}
                }

            except Exception as e:
                logger.error(f"JSON处理图像失败: {str(e)}")
                # 处理失败，返回原始图像和错误信息
                base64_data = base64.b64encode(frame_data).decode('utf-8')
                return {
                    "image": f"data:image/jpeg;base64,{base64_data}",
                    "text": "",
                    "confidence": 0,
                    "passed": False,
                    "error": str(e)
                }
                
        # 使用原有的处理流程返回图像数据
        processed_frame = camera_service.apply_operation_to_frame(frame_data, operation_id, operation_type, db)
        if not processed_frame:
            logger.warning(f"操作处理失败，返回原始帧 - 摄像头: {camera_id}, 操作: {operation_id}")
            return Response(content=frame_data, media_type="image/jpeg")
        
        logger.info(f"成功应用操作到快照 - 摄像头: {camera_id}, 操作: {operation_id}")
        return Response(content=processed_frame, media_type="image/jpeg")
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"获取快照错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取快照错误: {str(e)}")

@router.get("/{camera_id}/status")
def get_camera_status(camera_id: str):
    """获取摄像头状态"""
    return camera_service.get_camera_status(camera_id)

@router.post("/{camera_id}/stop-stream")
def stop_camera_stream(camera_id: str):
    """停止摄像头流处理"""
    # 规范化摄像头ID
    if not camera_id.startswith("camera_") and camera_id.isdigit():
        camera_id = f"camera_{camera_id}"
        
    try:
        # 首先收集需要停止的流
        streams_to_stop = []
        with camera_service._streams_lock:
            # 找到与该摄像头相关的所有处理流
            for stream_key, stream in list(camera_service._processed_streams.items()):
                if stream.camera_id == camera_id:
                    streams_to_stop.append((stream.operation_id, stream.operation_type))
        
        # 在锁外停止收集到的流
        success = False
        for operation_id, operation_type in streams_to_stop:
            if camera_service.stop_processed_stream(camera_id, operation_id, operation_type):
                success = True
        
        if success:
            return {"status": "success", "message": "成功停止视频流处理"}
        else:
            # 如果没有找到正在处理的流，也认为是成功的
            return {"status": "success", "message": "没有正在处理的流可停止"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"停止流处理错误: {str(e)}")

@router.get("/config-urls")
def get_camera_urls(request: Request, camera_id: Optional[str] = None):
    """获取摄像头的完整URL配置，包括操作参数说明"""
    base_url = str(request.base_url).rstrip('/')
    
    # 创建URL配置函数
    def create_url_config(camera_id: str):
        # 基本URL
        config = {
            "stream_url": f"{base_url}/api/cameras/{camera_id}/stream",
            "snapshot_url": f"{base_url}/api/cameras/{camera_id}/snapshot",
            "status_url": f"{base_url}/api/cameras/{camera_id}/status",
            # 带操作的URL示例
            "with_operation": {
                "stream": f"{base_url}/api/cameras/{camera_id}/stream?operation_id=1&operation_type=operation",
                "snapshot": f"{base_url}/api/cameras/{camera_id}/snapshot?operation_id=1&operation_type=operation"
            },
            "parameters": {
                "operation_id": "操作或流水线的ID (可选)",
                "operation_type": "操作类型: 'operation' (默认) 或 'pipeline'"
            }
        }
        return config
    
    if camera_id:
        # 为特定摄像头生成URL
        return create_url_config(camera_id)
    else:
        # 获取所有摄像头的URL配置
        camera_urls = {}
        for cam_id in camera_service.cameras.keys():
            camera_urls[cam_id] = create_url_config(cam_id)
        return camera_urls

@router.post("/process-image")
async def process_image(
    image: UploadFile = File(...),
    operation_id: str = Form(None),
    operation_type: str = Form("operation"),
    db: Session = Depends(get_db)
):
    """处理上传的图像
    
    参数:
    - operation_id: 操作ID或流水线ID
    - operation_type: 操作类型，'operation'(默认)或'pipeline'
    - image: 上传的图像文件
    
    返回:
    - JSON结果，包含处理后的图像(base64)、识别文字和置信度
    """
    try:
        logger.info(f"图像处理请求 - 操作: {operation_id}, 类型: {operation_type}")
        
        # 读取上传的图像数据
        image_data = await image.read()
        if not image_data:
            raise HTTPException(status_code=400, detail="无法读取上传的图像数据")
            
        # 将operation_id从字符串转换为整数
        try:
            if operation_id is not None:
                operation_id = int(operation_id)
                logger.info(f"转换后的operation_id: {operation_id}")
            else:
                logger.warning("请求中没有提供operation_id参数")
                raise HTTPException(status_code=422, detail="缺少操作ID参数")
        except ValueError:
            logger.error(f"无效的operation_id值: {operation_id}")
            raise HTTPException(status_code=422, detail=f"无效的操作ID: {operation_id}")
            
        # 验证操作参数
        if not isinstance(operation_id, int) or operation_id <= 0:
            raise HTTPException(status_code=422, detail=f"无效的操作ID: {operation_id}")
            
        if operation_type not in ["operation", "pipeline"]:
            raise HTTPException(status_code=422, detail=f"无效的操作类型: {operation_type}")
        
        # 导入所需服务
        from ..services.cv_operation import CVOperationService
        from ..services.pipeline import PipelineService
        
        # 解码输入图像
        nparr = np.frombuffer(image_data, np.uint8)
        input_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if input_image is None:
            raise HTTPException(status_code=400, detail="无法解码图像数据")
        
        # 应用操作或流水线
        result = {}
        if operation_type == "operation":
            operation_service = CVOperationService(db)
            operation = operation_service.get_operation(operation_id)
            if not operation:
                raise HTTPException(status_code=404, detail=f"未找到指定的操作 (ID: {operation_id})")
                
            # 获取图像输入参数名
            input_param_name = None
            for param in operation.input_params:
                if param['type'] == 'image' or 'image' in param['name'].lower():
                    input_param_name = param['name']
                    break
                    
            if not input_param_name:
                raise HTTPException(status_code=400, detail="操作没有图像输入参数")
                
            # 应用操作
            result = operation_service.apply_operation(operation_id, {input_param_name: input_image})
            
        elif operation_type == "pipeline":
            pipeline_service = PipelineService(db)
            pipeline = pipeline_service.get_pipeline(operation_id)
            if not pipeline:
                raise HTTPException(status_code=404, detail=f"未找到指定的流水线 (ID: {operation_id})")
                
            # 获取图像输入参数名
            input_param_name = None
            for param in pipeline.input_params:
                if param['type'] == 'image' or 'image' in param['name'].lower():
                    input_param_name = param['name']
                    break
                    
            if not input_param_name:
                raise HTTPException(status_code=400, detail="流水线没有图像输入参数")
                
            # 应用流水线
            pipeline_result = pipeline_service.apply_pipeline(operation_id, {input_param_name: input_image})
            result = pipeline_result.get('outputParams', {})
        
        # 提取处理结果
        response_data = {
            "passed": False,
            "text": "",
            "confidence": 0
        }
        
        # 处理image类型参数并转换为base64
        for key, value in result.items():
            if isinstance(value, np.ndarray):
                # 这是图像参数，转为base64
                success, buffer = cv2.imencode('.jpg', value)
                if success:
                    base64_data = base64.b64encode(buffer).decode('utf-8')
                    response_data["image"] = f"data:image/jpeg;base64,{base64_data}"
            elif key.lower() in ('text', 'result_text', 'recognized_text', 'detected_text'):
                # 提取识别文字
                response_data["text"] = str(value)
            elif key.lower() in ('confidence', 'score', 'probability', 'accuracy'):
                # 提取置信度
                try:
                    conf_value = float(value)
                    # 确保置信度在0-100范围内
                    if 0 <= conf_value <= 1:
                        response_data["confidence"] = conf_value * 100
                    else:
                        response_data["confidence"] = min(100, max(0, conf_value))
                except (ValueError, TypeError):
                    pass
            elif key.lower() in ('passed', 'is_passed', 'valid', 'is_valid'):
                # 提取通过/失败状态
                response_data["passed"] = bool(value)
        
        # 如果没有图像，提供错误信息
        if "image" not in response_data:
            # 尝试将原始图像作为结果返回
            success, buffer = cv2.imencode('.jpg', input_image)
            if success:
                base64_data = base64.b64encode(buffer).decode('utf-8')
                response_data["image"] = f"data:image/jpeg;base64,{base64_data}"
            else:
                raise HTTPException(status_code=500, detail="无法获取处理结果图像")
        
        logger.info(f"成功应用操作到上传图像 - 操作: {operation_id}")
        return response_data
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"处理图像错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理图像错误: {str(e)}")


@router.post("/force-release")
def force_release_camera():
    """
    强制释放摄像头：先停止本系统所有相机流，
    再结束常见占用摄像头的应用进程（Windows相机、Teams、Zoom、OBS等）。
    调用前需经用户确认。
    """
    import subprocess

    # 1. 释放本系统已打开的摄像头
    try:
        camera_service.close_all_cameras()
        logger.info("已停止本系统所有摄像头流")
    except Exception as e:
        logger.error(f"停止本系统摄像头失败: {str(e)}")

    # 2. 结束常见占用摄像头的应用进程
    targets = [
        "WindowsCamera",   # Windows 相机应用
        "ms-teams",        # Microsoft Teams
        "Teams",           # Teams (standalone)
        "zoom",            # Zoom
        "obs64",           # OBS Studio 64位
        "obs32",           # OBS Studio 32位
    ]
    killed = []
    for name in targets:
        try:
            r = subprocess.run(
                ["taskkill", "/IM", f"{name}.exe", "/F", "/T"],
                capture_output=True, text=True, timeout=15
            )
            if r.returncode == 0:
                killed.append(name)
                logger.info(f"已结束摄像头占用进程: {name}")
        except Exception as e:
            logger.warning(f"结束进程 {name} 失败: {str(e)}")

    if killed:
        logger.info(f"强制释放完成，结束进程: {killed}")
    else:
        logger.info("强制释放完成，未发现占用摄像头的常见进程")

    return {"success": True, "killed": killed}


# ============ 报警图片记录 ============
import os as _os_record
from datetime import datetime as _dt_record

def _get_record_dir(sub: str) -> str:
    _root = _os_record.path.dirname(_os_record.path.dirname(_os_record.path.dirname(_os_record.path.dirname(_os_record.path.abspath(__file__)))))
    _dir = _os_record.path.join(_root, "record", sub)
    _os_record.makedirs(_dir, exist_ok=True)
    return _dir

@router.get("/record/alarm_images")
def list_alarm_images(limit: int = 50):
    """返回最近的报警图片文件名列表（新的在前）"""
    _dir = _get_record_dir("alarm_png")
    files = [f for f in _os_record.listdir(_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    files.sort(reverse=True)
    return {"images": files[:limit]}

@router.get("/record/alarm_images/{filename}")
def get_alarm_image(filename: str):
    """返回指定报警图片"""
    # 防目录穿越
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    _dir = _get_record_dir("alarm_png")
    path = _os_record.path.join(_dir, filename)
    if not _os_record.path.exists(path):
        raise HTTPException(status_code=404, detail="Not found")
    with open(path, "rb") as f:
        content = f.read()
    return Response(content=content, media_type="image/jpeg")
