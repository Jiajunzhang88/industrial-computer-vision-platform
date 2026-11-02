import json, urllib.request

BASE = "http://127.0.0.1:8000"

def call(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers={"Content-Type": "application/json"}, method=method)
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())

# ---- 更新3个操作为 apply_operation 兼容签名（返回 dict） ----
op1 = {"outputType": "image", "code": '''def process(image, **params):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return {"image": clahe.apply(gray)}'''}

op2 = {"outputType": "image", "code": '''def process(image, **params):
    _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return {"image": image, "found": False}
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    cx, cy = x + w // 2, y + h // 2
    half = max(8, int(min(w, h) * 0.30))
    return {"image": image[cy-half:cy+half, cx-half:cx+half], "found": True}'''}

op3 = {"outputType": "text", "code": '''def process(image, **params):
    edges = cv2.Canny(image, 50, 150)
    density = float(cv2.countNonZero(edges)) / max(image.size, 1)
    return {"side": "正面" if density > 0.05 else "反面", "edge_density": round(density, 4)}'''}

for oid, payload in ((1, op1), (2, op2), (3, op3)):
    call("PUT", f"/api/cv/operations/{oid}", payload)
    print("UPDATED op", oid)

# ---- 删除旧流水线并重建（带 config.params 传递图像） ----
try:
    call("DELETE", "/api/pipelines/1")
    print("DELETED old pipeline 1")
except Exception as e:
    print("delete pipeline 1:", e)

pipeline = {
    "name": "硬币正反面识别",
    "description": "预处理 -> 定位主图案 -> 正反面判定",
    "metadata": {
        "nodes": [
            {"id": "start", "type": "start", "name": "开始", "position": {"x": 0, "y": 0}},
            {"id": "op1", "type": "operation", "name": "硬币预处理", "operation_id": 1, "position": {"x": 220, "y": 0},
             "config": {"params": {"image": {"source": "input:image"}}}},
            {"id": "op2", "type": "operation", "name": "提取主图案", "operation_id": 2, "position": {"x": 440, "y": 0},
             "config": {"params": {"image": {"source": "node:op1:image"}}}},
            {"id": "op3", "type": "operation", "name": "正反面判定", "operation_id": 3, "position": {"x": 660, "y": 0},
             "config": {"params": {"image": {"source": "node:op2:image"}}}},
            {"id": "end", "type": "end", "name": "结束", "position": {"x": 880, "y": 0},
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
print("CREATED pipeline", pid)

# ---- 应用测试 ----
coins = json.load(open("test_coins.json"))
for label, b64 in coins.items():
    try:
        res = call("POST", f"/api/pipelines/{pid}/apply", {"inputParams": {"image": b64}, "enableLog": False})
        out = res["outputParams"]
        print(f"[{label}] side={out.get('side')} edge_density={out.get('edge_density')}")
    except Exception as e:
        print(f"[{label}] apply failed: {e}")
print("DONE")
