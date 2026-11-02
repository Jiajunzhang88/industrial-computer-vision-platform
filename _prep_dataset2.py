import cv2, numpy as np, os, json, random, uuid, urllib.request, http.client

random.seed(7)
IMG_SIZE = 640
OUT_DIR = "_train_imgs2"
os.makedirs(OUT_DIR, exist_ok=True)

def make_coin(side, cx, cy, r):
    img = np.full((IMG_SIZE, IMG_SIZE, 3), 235, np.uint8)
    cv2.circle(img, (cx, cy), r, (150, 150, 150), -1)
    cv2.circle(img, (cx, cy), r, (60, 60, 60), 5)
    if side == 'obverse':
        # 极高纹理密度：密集同心环 + 放射线 + 圆点 + 铭文
        for rr in range(int(r*0.20), int(r*0.98), max(3, int(r*0.05))):
            cv2.circle(img, (cx, cy), rr, (85, 85, 85), 1)
        for a in range(0, 360, 8):
            x2 = cx + int(r*np.cos(np.radians(a))); y2 = cy + int(r*np.sin(np.radians(a)))
            cv2.line(img, (cx, cy), (x2, y2), (95, 95, 95), 1)
        for a in range(0, 360, 24):
            for rr in (int(r*0.5), int(r*0.75)):
                x = cx + int(rr*np.cos(np.radians(a))); y = cy + int(rr*np.sin(np.radians(a)))
                cv2.circle(img, (x, y), max(3, r//14), (70, 70, 70), -1)
        cv2.circle(img, (cx, cy), int(r*0.12), (90, 90, 90), -1)
    else:
        # 大面积留白 + 中央大面值 + 底部小字
        cv2.putText(img, "1", (cx-int(r*0.42), cy+int(r*0.30)), cv2.FONT_HERSHEY_SIMPLEX, r*0.045, (70, 70, 70), r//10)
        cv2.putText(img, "REPUBLIC", (cx-int(r*0.5), cy+int(r*0.62)), cv2.FONT_HERSHEY_SIMPLEX, r*0.012, (90, 90, 90), 1)
    return img

samples = []
for i in range(32):
    side = 'obverse' if i % 2 == 0 else 'reverse'
    r = random.randint(70, 150)
    cx = random.randint(70 + r, IMG_SIZE - 70 - r)
    cy = random.randint(70 + r, IMG_SIZE - 70 - r)
    fn = f"coin_{i:02d}_{side}.png"
    cv2.imwrite(os.path.join(OUT_DIR, fn), make_coin(side, cx, cy, r))
    bbox = [int(cx - r - 4), int(cy - r - 4), int(2*r + 8), int(2*r + 8)]
    samples.append((fn, side, bbox))
print("generated", len(samples))

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
    conn = http.client.HTTPConnection("127.0.0.1", 8000, timeout=90)
    conn.request("POST", f"/api/annotation/datasets/{dataset_id}/images",
                 body=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    resp = conn.getresponse()
    data = json.loads(resp.read().decode())
    conn.close()
    if resp.status != 200:
        raise RuntimeError(f"upload failed {resp.status}: {data}")
    return data

ds = jcall("POST", "/api/annotation/datasets", {"name": "硬币正反面数据集V2", "type": "ocr"})
dsid = ds["id"]
print("dataset", dsid)
imgs = upload_images(dsid, [s[0] for s in samples])
id_by_fn = {im["filename"]: im["id"] for im in imgs}
for fn, side, bbox in samples:
    x, y, w, h = bbox
    anno = {"annotations": [{"id": "1",
        "body": [{"type": "TextualBody", "value": side}],
        "target": {"selector": {"type": "RECTANGLE", "geometry": {"x": x, "y": y, "w": w, "h": h}}}
    }]}
    jcall("POST", f"/api/annotation/images/{id_by_fn[fn]}/annotation", anno)
print("annotated", len(samples))

model = jcall("POST", "/api/models/", {
    "name": "硬币正反面识别模型V2",
    "architecture": "yolo_v8",
    "dataset_id": dsid,
    "parameters": {"epochs": 30, "batch_size": 16, "img_size": 640,
                   "conf_thres": 0.25, "iou_thres": 0.45}
})
mid = model["id"]
jcall("POST", f"/api/models/{mid}/train")
print("MODEL_ID", mid)
