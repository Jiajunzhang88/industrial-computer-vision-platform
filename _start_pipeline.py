import requests
resp = requests.post('http://127.0.0.1:8000/api/pipeline/start')
print(f'Status: {resp.status_code}')
print(f'Response: {resp.text}')
