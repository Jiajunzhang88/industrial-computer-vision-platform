import requests
import traceback

try:
    resp = requests.get('http://127.0.0.1:8000/api/cameras/0/snapshot?return_json=true', timeout=10)
    print('Snapshot status:', resp.status_code)
    data = resp.json()
    img_b64 = data.get('image', '')
    print('Image length:', len(img_b64))
    
    if not img_b64.startswith('data:'):
        img_b64 = f'data:image/jpeg;base64,{img_b64}'
    
    apply_resp = requests.post('http://127.0.0.1:8000/api/pipelines/2/apply',
        json={
            'inputParams': {'image': img_b64},
            'enableLog': True
        }, timeout=30)
    print('Apply status:', apply_resp.status_code)
    print('Response text:', apply_resp.text[:1000])
except Exception as e:
    print('Error:', e)
    traceback.print_exc()
