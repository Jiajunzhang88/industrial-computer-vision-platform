import requests, base64, os, json

val_dir = r"I:\git\industrial-computer-vision-platform\data\datasets\dataset_4\val\images"
imgs = [f for f in os.listdir(val_dir) if f.endswith(('.jpg','.png','.jpeg'))]
print(f"验证集共 {len(imgs)} 张图")

for img_name in imgs:
    img_path = os.path.join(val_dir, img_name)
    with open(img_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    data_url = f"data:image/jpeg;base64,{b64}"
    
    resp = requests.post("http://127.0.0.1:8000/api/models/1/test", 
        json={"image_base64": data_url, "conf_thres": 0.25, "iou_thres": 0.45}, timeout=30)
    data = resp.json()
    dets = data.get("detections", [])
    print(f"{img_name}: {len(dets)} 个目标")
    for d in dets:
        print(f"  类别={d.get('class_name')}, 置信度={d.get('confidence'):.3f}")
