import json, urllib.request

BASE = "http://127.0.0.1:8000"

def call(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers={"Content-Type": "application/json"}, method=method)
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())

coins = json.load(open("test_coins.json"))
for label, b64 in coins.items():
    res = call("POST", "/api/pipelines/1/apply", {"inputParams": {"image": b64}, "enableLog": False})
    out = res["outputParams"]
    print(f"[{label}] side={out.get('side')} edge_density={out.get('edge_density')}")
print("DONE")
