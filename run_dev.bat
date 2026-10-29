@echo off
echo ===================================================
echo Launching ResearchFlow AI (Full Stack)
echo ===================================================
start "ResearchFlow Backend" cmd /k "run_backend.bat"
start "ResearchFlow Frontend" cmd /k "run_frontend.bat"
echo Services launching in background windows:
echo - Backend: http://localhost:8005
echo - Frontend: http://localhost:3005
echo - API Docs: http://localhost:8005/docs
