import json, base64, numpy as np, cv2
from ultralytics import YOLO

model = YOLO(r"models\model_2\weights\best.pt")

def test(img, conf):
    res = model(img, conf=conf, iou=0.45)
    boxes = res[0].boxes
    return [(res[0].names[int(b.cls[0].item())], round(float(b.conf[0].item()),3)) for b in boxes]

# 训练集里的 reverse 图
for fn in ["coin_01_reverse.png", "coin_03_reverse.png", "coin_05_reverse.png", "coin_07_reverse.png"]:
    img = cv2.imread(f"_train_imgs/{fn}")
    for conf in (0.25, 0.1):
        d = test(img, conf)
        print(f"{fn} conf={conf}: {d}")
