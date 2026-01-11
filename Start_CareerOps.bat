@echo off
echo ==========================================
echo       CAREEROPS AUTOMATION ECOSYSTEM
echo ==========================================

echo 1. Starting Dashboard...
start "My Dashboard" cmd /k "python app.py"

echo 2. Starting Public Tunnel...
start "Public Tunnel" cmd /k "ngrok http 5000"

echo 3. Starting Job Alerts (Hyderabad Data Roles)...
start "Job Alerts" cmd /k "python job_alerts.py"

echo.
echo ==========================================
echo    ALL SYSTEMS ONLINE. LEAVE WINDOWS OPEN.
echo ==========================================
pause
