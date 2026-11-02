@echo off
cd /d I:\git\industrial-computer-vision-platform
set PATH=I:\git\industrial-computer-vision-platform\.venv\Scripts;%PATH%
.venv\Scripts\python.exe -m uvicorn src.backend.main:app --host 127.0.0.1 --port 8000
