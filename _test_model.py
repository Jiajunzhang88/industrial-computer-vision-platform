import requests, json

# 1. 从摄像头抓拍
print("正在从摄像头抓拍...")
snap = requests.get("http://127.0.0.1:8000/api/cameras/0/snapshot?return_json=true", timeout=10)
snap_data = snap.json()
print(f"抓拍状态: {snap.status_code}")

# 2. 提取图片 base64
image_base64 = snap_data.get("image_base64") or snap_data.get("frame") or snap_data.get("image")
if not image_base64:
    print(f"抓拍返回字段: {list(snap_data.keys())}")
    raise SystemExit("无法获取图片数据")

# 如果是 data:image/... 开头的 dataURL，直接用
if not image_base64.startswith("data:"):
    image_base64 = f"data:image/jpeg;base64,{image_base64}"

# 3. 调测试 API
print("正在识别...")
resp = requests.post("http://127.0.0.1:8000/api/models/1/test",
    json={
        "image_base64": image_base64,
        "conf_thres": 0.5,
        "iou_thres": 0.7,
        "max_det": 300,
        "agnostic_nms": False,
        "imgsz": 640
    }, timeout=30)
data = resp.json()
print(f"状态码: {resp.status_code}")
print(f"检测到 {len(data.get('detections', []))} 个目标:")
for d in data.get('detections', []):
    print(f"  完整对象: {d}")
    print(f"  类别={d['class_name']}, 置信度={d['confidence']:.3f}")

# 保存标注后的图片供查看
import base64
if data.get("image"):
    img_b64 = data["image"].split(",")[-1] if "," in data["image"] else data["image"]
    with open("_test_result.jpg", "wb") as f:
        f.write(base64.b64decode(img_b64))
    print("标注图已保存: _test_result.jpg")
