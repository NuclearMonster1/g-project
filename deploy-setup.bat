@echo off
set "NODE_DIR=C:\Program Files\nodejs"
set "PATH=%NODE_DIR%;%PATH%"
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\deploy.ps1" -Setup -SyncEnv %*
if errorlevel 1 (
    echo.
    echo Setup failed.
    pause
    exit /b 1
)
pause
