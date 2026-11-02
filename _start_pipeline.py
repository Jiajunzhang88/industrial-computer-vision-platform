import requests
resp = requests.post('http://127.0.0.1:8000/api/pipeline/start')
print(f'Start: {resp.status_code} - {resp.text}')

# 等 6 秒看结果
import time
time.sleep(6)

resp2 = requests.get('http://127.0.0.1:8000/api/pipeline/live')
data = resp2.json()
print(f'\nLive: running={data["running"]}, interval={data["interval"]}')
if data['latest']:
    latest = data['latest']
    print(f'Timestamp: {latest["timestamp"]}')
    print(f'Detections: {len(latest.get("detections", []))} 个物体')
    for d in latest.get('detections', [])[:3]:
        print(f'  - {d.get("class", "?")}: conf={d.get("confidence", 0):.3f}')
else:
    print('No latest result yet')
