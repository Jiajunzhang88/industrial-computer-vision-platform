import requests, json

# 新建 pipeline 工程
pipeline_data = {
    "name": "硬币正反面实时检测",
    "description": "从摄像头获取数据，每5秒用YOLO模型检测一次",
    "metadata": {
        "nodes": [
            {
                "id": "start",
                "type": "start",
                "name": "开始",
                "operationId": None,
                "config": None,
                "position": {"x": 0, "y": 0}
            },
            {
                "id": "op1",
                "type": "operation",
                "name": "YOLO模型检测",
                "operationId": 1,
                "config": {
                    "params": {
                        "image": {"source": "input:image"}
                    }
                },
                "position": {"x": 220, "y": 0}
            },
            {
                "id": "end",
                "type": "end",
                "name": "结束",
                "operationId": None,
                "config": {
                    "outputMappings": {
                        "side": "node:op1:side",
                        "confidence": "node:op1:confidence"
                    }
                },
                "position": {"x": 440, "y": 0}
            }
        ],
        "edges": [
            {"id": "e1", "source": "start", "target": "op1", "type": "normal"},
            {"id": "e2", "source": "op1", "target": "end", "type": "normal"}
        ]
    },
    "inputParams": [
        {
            "name": "image",
            "type": "image",
            "description": "输入硬币图像",
            "default": None,
            "required": True
        }
    ],
    "outputParams": [
        {
            "name": "side",
            "type": "text",
            "description": "正面(A)/反面(B)",
            "default": None,
            "required": True
        },
        {
            "name": "confidence",
            "type": "number",
            "description": "置信度",
            "default": None,
            "required": True
        }
    ]
}

resp = requests.post('http://127.0.0.1:8000/api/pipelines/', json=pipeline_data)
print(f'Status: {resp.status_code}')
if resp.status_code == 200:
    data = resp.json()
    print(f'创建成功! ID: {data["id"]}')
    print(f'名称: {data["name"]}')
else:
    print(f'创建失败: {resp.text}')
