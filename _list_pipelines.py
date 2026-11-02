import requests, json
resp = requests.get('http://127.0.0.1:8000/api/pipelines/')
print(f'Status: {resp.status_code}')
data = resp.json()
print(f'数量: {len(data)}')
print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
