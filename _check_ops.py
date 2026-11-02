import requests, json

# 查看所有 CV 操作
resp = requests.get('http://127.0.0.1:8000/api/cv/operations/')
data = resp.json()
print(f'CV 操作数量: {len(data)}')
for op in data:
    print(f'  ID: {op["id"]}, 名称: {op["name"]}, 类型: {op.get("operationType", "?")}')

# 查看 pipeline 工程 1 的详细配置
print('\nPipeline 工程 1:')
resp2 = requests.get('http://127.0.0.1:8000/api/pipelines/1')
p = resp2.json()
print(json.dumps(p, indent=2, ensure_ascii=False)[:3000])
