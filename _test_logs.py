import json, urllib.request, sys

def call(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request("http://127.0.0.1:8000" + path, data=data, headers={"Content-Type": "application/json"}, method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

coins = json.load(open("test_coins.json"))
out_lines = []
for label, b64 in coins.items():
    try:
        res = call("POST", "/api/pipelines/1/apply", {"inputParams": {"image": b64}, "enableLog": True})
        out = res["outputParams"]
        logs = res.get("logs") or []
        err = [l for l in logs if l.get("type") == "ERROR"]
        out_lines.append(f"[{label}] side={out.get('side')} density={out.get('edge_density')} ERROR_logs={len(err)}")
    except Exception as e:
        out_lines.append(f"[{label}] failed: {e}")
out_lines.append("DONE")
with open("_logs_result.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))
