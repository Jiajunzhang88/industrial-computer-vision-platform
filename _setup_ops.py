import json, urllib.request

BASE = "http://127.0.0.1:8000"

def post(path, payload):
    req = urllib.request.Request(BASE + path, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def get(path):
    with urllib.request.urlopen(BASE + path, timeout=30) as r:
        return json.loads(r.read().decode())

# ---- 操作1：硬币预处理 ----
op1_code = '''def process(image, **params):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    return {"image": enhanced}'''

# ---- 操作2：提取硬币中心主图案 ----
op2_code = '''def process(image, **params):
    _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return {"image": image, "found": False}
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    cx, cy = x + w // 2, y + h // 2
    half = max(8, int(min(w, h) * 0.30))
    roi = image[cy-half:cy+half, cx-half:cx+half]
    return {"image": roi, "found": True}'''

# ---- 操作3：正反面判定 ----
op3_code = '''def process(image, **params):
    edges = cv2.Canny(image, 50, 150)
    density = float(cv2.countNonZero(edges)) / max(image.size, 1)
    side = "正面" if density > 0.05 else "反面"
    return {"side": side, "edge_density": round(density, 4)}'''

img_param = [{"name": "image", "type": "image", "description": "输入图像", "required": True}]

ops = [
    {"name": "硬币预处理", "description": "灰度化+中值滤波+CLAHE增强", "code": op1_code,
     "inputParams": img_param, "outputParams": [{"name": "image", "type": "image", "description": "处理后的灰度图", "required": True}]},
    {"name": "提取硬币主图案", "description": "定位最大轮廓并提取中心ROI", "code": op2_code,
     "inputParams": img_param, "outputParams": [{"name": "image", "type": "image", "description": "中心主图案", "required": True}, {"name": "found", "type": "boolean", "description": "是否定位到硬币", "required": True}]},
    {"name": "正反面判定", "description": "基于主图案边缘密度判定正反面", "code": op3_code,
     "inputParams": img_param, "outputParams": [{"name": "side", "type": "text", "description": "正面/反面", "required": True}, {"name": "edge_density", "type": "number", "description": "边缘密度", "required": True}]},
]

created = []
for op in ops:
    r = post("/api/cv/operations/", op)
    created.append(r)
    print("CREATED OP", r["id"], r["name"])

# ---- 应用测试 ----
coins = json.load(open("test_coins.json"))
for label, b64 in coins.items():
    for op in created:
        res = post(f"/api/cv/operations/{op['id']}/apply", {"inputParams": {"image": b64}})
        out = res["result"]
        keys = list(out.keys())
        print(f"[{label}] op{op['id']} -> {keys}")
        if "side" in out:
            print(f"    RESULT side={out['side']} density={out['edge_density']}")
    print("---")
