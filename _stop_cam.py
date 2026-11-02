import urllib.request, json

BASE = "http://127.0.0.1:8000"

def req(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    r = urllib.request.Request(BASE+path, data=data, headers={"Content-Type":"application/json"}, method=method)
    try:
        with urllib.request.urlopen(r, timeout=20) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except Exception as e:
        return None, str(e)

print("== detect ==")
st, body = req("GET", "/api/cameras/detect")
print(st, body)

for cid in ["0", "camera_0", "1", "Camera 0"]:
    st, body = req("POST", f"/api/cameras/{cid}/stop-stream")
    print(f"== stop {cid} -> {st} {body}")
