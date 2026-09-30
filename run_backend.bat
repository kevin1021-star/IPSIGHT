@echo off
echo Starting CIPHER-SENTINEL Backend API (FastAPI)...
cd /d "%~dp0"
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
pause
