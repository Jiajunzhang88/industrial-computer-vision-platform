"""
全局变量和共享数据存储模块
"""

# 模型训练日志存储
TRAINING_LOGS = {}

# 正在运行的训练进程 {model_id: subprocess.Popen}
TRAINING_PROCESSES = {}