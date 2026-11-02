import requests, time

# 等 10 秒
time.sleep(10)

resp = requests.get('http://127.0.0.1:8000/api/pipeline/live')
data = resp.json()
print(f'running={data["running"]}, interval={data["interval"]}')
if data['latest']:
    latest = data['latest']
    print(f'\n最新结果:')
    print(f'  时间: {latest["timestamp"]}')
    dets = latest.get('detections', [])
    print(f'  检测到 {len(dets)} 个物体:')
    for d in dets[:5]:
        print(f'    - {d.get("class", "?")}: conf={d.get("confidence", 0):.3f}, bbox={d.get("bbox", [])}')
else:
    print('还没有结果')
