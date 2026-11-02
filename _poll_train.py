import json, urllib.request, time

BASE = "http://127.0.0.1:8000"

def get(path):
    with urllib.request.urlopen(BASE + path, timeout=30) as r:
        return json.loads(r.read().decode())

mid = 2
lines = []
deadline = time.time() + 600
last_status = None
while time.time() < deadline:
    try:
        m = get(f"/api/models/{mid}")
        status = m["status"]
        logs = get(f"/api/models/{mid}/logs")["logs"]
    except Exception as e:
        lines.append(f"[poll] err {e}")
        time.sleep(10)
        continue
    lines.append(f"[t={time.time():.0f}] status={status} logs={len(logs)}")
    if len(logs) > 0:
        tail = logs[-3:]
        for t in tail:
            lines.append("   " + str(t)[:160])
    if status != last_status:
        lines.append(f"*** status change -> {status}")
        last_status = status
    if status in ("completed", "failed"):
        lines.append("FINISHED " + status)
        m2 = get(f"/api/models/{mid}")
        lines.append("metrics: " + json.dumps(m2.get("metrics"), ensure_ascii=False))
        lines.append("file_path: " + str(m2.get("file_path")))
        break
    time.sleep(12)

with open("_train_poll_result.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
