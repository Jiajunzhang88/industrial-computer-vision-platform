import requests, time

# 测试 pipeline live
resp = requests.get('http://127.0.0.1:8000/api/pipeline/live')
data = resp.json()
print(f'running: {data["running"]}')
print(f'interval: {data["interval"]}')
print(f'latest: {data["latest"]}')

# 等 10 秒
print('\n等 10 秒...')
time.sleep(10)

resp2 = requests.get('http://127.0.0.1:8000/api/pipeline/live')
data2 = resp2.json()
print(f'\n10 秒后:')
print(f'running: {data2["running"]}')
if data2['latest']:
    print(f'timestamp: {data2["latest"]["timestamp"]}')
    print(f'detections: {len(data2["latest"].get("detections", []))} 个')
else:
    print('latest: None')
