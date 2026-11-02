import requests
import base64
import cv2
import numpy as np

# 1. 从摄像头抓拍
print("1. 从摄像头抓拍...")
resp = requests.get('http://127.0.0.1:8000/api/cameras/0/snapshot?return_json=true', timeout=10)
snap_data = resp.json()
img_b64 = snap_data.get('image_base64') or snap_data.get('frame') or snap_data.get('image')
if not img_b64:
    print("错误：没有抓拍图片")
    exit(1)
print(f"抓拍成功，图片长度: {len(img_b64)}")

# 2. 调用 pipeline 执行接口
print("\n2. 调用 pipeline 执行接口...")
if not img_b64.startswith('data:'):
    img_b64 = f'data:image/jpeg;base64,{img_b64}'

apply_resp = requests.post('http://127.0.0.1:8000/api/pipelines/2/apply',
    json={
        'inputParams': {'image': img_b64},
        'enableLog': True
    }, timeout=30)

print(f"状态码: {apply_resp.status_code}")
apply_data = apply_resp.json()
print(f"\n执行结果:")
print(f"输出参数: {apply_data.get('outputParams', {})}")
print(f"\n执行日志:")
for log in apply_data.get('logs', []):
    print(f"  [{log.get('level', 'INFO')}] {log.get('message', '')}")
