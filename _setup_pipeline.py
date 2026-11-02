import json, urllib.request, urllib.error

BASE = "http://127.0.0.1:8000"

def call(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers={"Content-Type": "application/json"}, method=method)
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())

# ---- 更新3个操作为流水线兼容签名 ----
op1 = {"outputType": "image", "code": '''def process(img, cv2, np):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray)'''}

op2 = {"outputType": "image", "code": '''def process(img, cv2, np):
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return img
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    cx, cy = x + w // 2, y + h // 2
    half = max(8, int(min(w, h) * 0.30))
    return img[cy-half:cy+half, cx-half:cx+half]'''}

op3 = {"outputType": "text", "code": '''def process(img, cv2, np):
    edges = cv2.Canny(img, 50, 150)
    density = float(cv2.countNonZero(edges)) / max(img.size, 1)
    return {"side": "正面" if density > 0.05 else "反面", "edge_density": round(density, 4)}'''}

for oid, payload in ((1, op1), (2, op2), (3, op3)):
    call("PUT", f"/api/cv/operations/{oid}", payload)
    print("UPDATED op", oid, "-> outputType", payload["outputType"])

# ---- 创建流水线 ----
pipeline = {
    "name": "硬币正反面识别",
    "description": "预处理 -> 定位主图案 -> 正反面判定",
    "metadata": {
        "nodes": [
            {"id": "start", "type": "start", "name": "开始", "position": {"x": 0, "y": 0}},
            {"id": "op1", "type": "operation", "name": "硬币预处理", "operation_id": 1, "position": {"x": 200, "y": 0}},
            {"id": "op2", "type": "operation", "name": "提取主图案", "operation_id": 2, "position": {"x": 420, "y": 0}},
            {"id": "op3", "type": "operation", "name": "正反面判定", "operation_id": 3, "position": {"x": 640, "y": 0}},
            {"id": "end", "type": "end", "name": "结束", "position": {"x": 860, "y": 0},
             "config": {"outputMappings": {"side": "node:op3:side", "edge_density": "node:op3:edge_density"}}}
        ],
        "edges": [
            {"id": "e1", "source": "start", "target": "op1", "type": "normal"},
            {"id": "e2", "source": "op1", "target": "op2", "type": "normal"},
            {"id": "e3", "source": "op2", "target": "op3", "type": "normal"},
            {"id": "e4", "source": "op3", "target": "end", "type": "normal"}
        ]
    },
    "inputParams": [{"name": "image", "type": "image", "description": "输入硬币图像", "required": True}],
    "outputParams": [
        {"name": "side", "type": "text", "description": "正面/反面", "required": True},
        {"name": "edge_density", "type": "number", "description": "边缘密度", "required": True}
    ]
}
created = call("POST", "/api/pipelines/", pipeline)
pid = created["id"]
print("CREATED pipeline", pid, created["name"])

# ---- 应用测试 ----
coins = json.load(open("test_coins.json"))
for label, b64 in coins.items():
    res = call("POST", f"/api/pipelines/{pid}/apply", {"inputParams": {"image": b64}, "enableLog": True})
    out = res["outputParams"]
    print(f"[{label}] side={out.get('side')} edge_density={out.get('edge_density')}")
    logs = res.get("logs") or []
    for lg in logs[-3:]:
        print("   log:", str(lg)[:120])
print("DONE")
