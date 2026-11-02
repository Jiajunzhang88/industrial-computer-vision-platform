import json, urllib.request, time

BASE = "http://127.0.0.1:8000"

def get(path):
    with urllib.request.urlopen(BASE + path, timeout=30) as r:
        return json.loads(r.read().decode())

mid = 3
lines = []
deadline = time.time() + 700
last_status = None
while time.time() < deadline:
    try:
        m = get(f"/api/models/{mid}")
        status = m["status"]
    except Exception as e:
        lines.append(f"[poll] err {e}")
        time.sleep(12)
        continue
    lines.append(f"[t={time.time():.0f}] status={status}")
    if status != last_status:
        lines.append(f"*** status -> {status}")
        last_status = status
    if status in ("completed", "failed"):
        lines.append("FINISHED " + status)
        lines.append("metrics: " + json.dumps(m.get("metrics"), ensure_ascii=False))
        lines.append("file_path: " + str(m.get("file_path")))
        break
    time.sleep(15)

with open("_poll3_result.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
