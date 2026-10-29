@echo off
echo ===================================================
echo Starting ResearchFlow AI FastAPI Backend on :8005
echo ===================================================
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
