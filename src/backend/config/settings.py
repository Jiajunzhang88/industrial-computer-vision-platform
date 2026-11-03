"""
后端集中配置
所有路径均相对于项目根目录启动（python -m uvicorn src.backend.main:app）
"""
import os

# ===== 应用 =====
APP_TITLE = "Industrial Monitoring System API"
APP_VERSION = "1.0.0"
APP_HOST = "0.0.0.0"
APP_PORT = 8000

# ===== CORS =====
CORS_ORIGINS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# ===== 目录路径（相对项目根目录）=====
UPLOADS_DIR = "uploads"
DIST_DIR = "dist"
DATABASE_URL = "sqlite:///./industrial_ocr.db"

# ===== 实时检测默认参数 =====
PIPELINE_INTERVAL = 5       # 秒
PIPELINE_MODEL_ID = 1
PIPELINE_CONF_THRES = 0.5
PIPELINE_IOU_THRES = 0.7

# ===== 报警记录目录 =====
RECORD_DIR = "record"
ALARM_IMAGES_DIR = os.path.join(RECORD_DIR, "alarm_png")
LOGS_DIR = os.path.join(RECORD_DIR, "log")
