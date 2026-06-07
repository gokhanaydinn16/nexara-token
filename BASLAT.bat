@echo off
title NEXARA Dashboard
color 0B
echo.
echo  ====================================
echo   NEXARA Kontrol Paneli Baslatiliyor
echo  ====================================
echo.
echo  Tarayici aciliyor: http://localhost:8501
echo.

start http://localhost:8501
"C:\Users\gokha\Desktop\nexara-token\dashboard\venv\Scripts\streamlit.exe" run "C:\Users\gokha\Desktop\nexara-token\dashboard\app.py" --server.port 8501

pause
