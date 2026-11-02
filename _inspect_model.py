import json
from ultralytics import YOLO

model = YOLO(r"models\model_2\weights\best.pt")
print("model.names:", model.names)

coins = json.load(open("test_coins.json"))
import base64, numpy as np, cv2
for label, b64 in coins.items():
    img_bytes = base64.b64decode(b64)
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    res = model(img, conf=0.25, iou=0.45)
    boxes = res[0].boxes
    print(f"[{label}] shape={img.shape} detections={len(boxes)}")
    for b in boxes:
        print("   cls_id=", int(b.cls[0].item()), "name=", res[0].names[int(b.cls[0].item())], "conf=", round(float(b.conf[0].item()),3))
