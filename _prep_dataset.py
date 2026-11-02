import cv2, numpy as np, os, json, random, uuid, urllib.request, http.client

random.seed(42)
IMG_SIZE = 640
OUT_DIR = "_train_imgs"
os.makedirs(OUT_DIR, exist_ok=True)

def make_coin(side, cx, cy, r):
    """side: 'obverse'(复杂纹样) / 'reverse'(稀疏数字)"""
    img = np.full((IMG_SIZE, IMG_SIZE, 3), 220, np.uint8)
    cv2.circle(img, (cx, cy), r, (140, 140, 140), -1)
    cv2.circle(img, (cx, cy), r, (70, 70, 70), 4)
    if side == 'obverse':
        for rr in range(int(r*0.35), int(r*0.95), int(r*0.14)+1):
            cv2.circle(img, (cx, cy), rr, (90, 90, 90), 2)
        for a in range(0, 360, 20):
            x = cx + int(r*0.6*np.cos(np.radians(a)))
            y = cy + int(r*0.6*np.sin(np.radians(a)))
            cv2.circle(img, (x, y), int(r*0.10), (100, 100, 100), -1)
    else:
        cv2.putText(img, "1", (cx-int(r*0.3), cy+int(r*0.35)), cv2.FONT_HERSHEY_SIMPLEX, r*0.012, (60, 60, 60), max(2, r//12))
    return img

samples = []  # (filename, side, bbox)
for i in range(20):
    side = 'obverse' if i % 2 == 0 else 'reverse'
    r = random.randint(50, 120)
    cx = random.randint(60 + r, IMG_SIZE - 60 - r)
    cy = random.randint(60 + r, IMG_SIZE - 60 - r)
    fn = f"coin_{i:02d}_{side}.png"
    img = make_coin(side, cx, cy, r)
    cv2.imwrite(os.path.join(OUT_DIR, fn), img)
    bbox = [int(cx - r - 3), int(cy - r - 3), int(2*r + 6), int(2*r + 6)]
    samples.append((fn, side, bbox))
print("generated", len(samples), "images")

# ---- HTTP helpers ----
BASE = "http://127.0.0.1:8000"

def jcall(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers={"Content-Type": "application/json"}, method=method)
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())

def upload_images(dataset_id, files):
    boundary = "----WebKitFormBoundary" + uuid.uuid4().hex
    parts = []
    for fn in files:
        with open(os.path.join(OUT_DIR, fn), "rb") as f:
            content = f.read()
        parts.append(b"--" + boundary.encode())
        parts.append(f'Content-Disposition: form-data; name="files"; filename="{fn}"'.encode())
        parts.append(b"Content-Type: image/png")
        parts.append(b"")
        parts.append(content)
    parts.append(b"--" + boundary.encode() + b"--")
    body = b"\r\n".join(parts)
    conn = http.client.HTTPConnection("127.0.0.1", 8000, timeout=60)
    conn.request("POST", f"/api/annotation/datasets/{dataset_id}/images",
                 body=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    resp = conn.getresponse()
    data = json.loads(resp.read().decode())
    conn.close()
    if resp.status != 200:
        raise RuntimeError(f"upload failed {resp.status}: {data}")
    return data

# ---- 1. 创建数据集 ----
ds = jcall("POST", "/api/annotation/datasets", {"name": "硬币正反面数据集", "type": "ocr"})
dsid = ds["id"]
print("dataset id", dsid)

# ---- 2. 上传图片 ----
fnames = [s[0] for s in samples]
imgs = upload_images(dsid, fnames)
id_by_fn = {im["filename"]: im["id"] for im in imgs}
print("uploaded", len(imgs), "images")

# ---- 3. 保存标注 ----
for fn, side, bbox in samples:
    x, y, w, h = bbox
    anno = {"annotations": [{
        "id": "1",
        "body": [{"type": "TextualBody", "value": side}],
        "target": {"selector": {"type": "RECTANGLE", "geometry": {"x": x, "y": y, "w": w, "h": h}}}
    }]}
    jcall("POST", f"/api/annotation/images/{id_by_fn[fn]}/annotation", anno)
print("annotated", len(samples), "images")

# ---- 4. 创建模型 ----
model = jcall("POST", "/api/models/", {
    "name": "硬币正反面识别模型",
    "architecture": "yolo_v8",
    "dataset_id": dsid,
    "parameters": {"epochs": 30, "batch_size": 16, "img_size": 640,
                   "conf_thres": 0.25, "iou_thres": 0.45}
})
mid = model["id"]
print("created model id", mid)

# ---- 5. 启动训练 ----
res = jcall("POST", f"/api/models/{mid}/train")
print("training started, status", res["status"])
print("MODEL_ID", mid)
