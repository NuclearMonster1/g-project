@echo off
set "NODE_DIR=C:\Program Files\nodejs"
set "PATH=%NODE_DIR%;%PATH%"
cd /d "%~dp0"
echo Node:
"%NODE_DIR%\node.exe" --version
echo.
echo Vercel login (OAuth Device Flow)
echo   1. A code and URL will appear below
echo   2. Open the URL in any browser and enter the code
echo   3. Verify location, IP, and time before approving
echo.
"%NODE_DIR%\npx.cmd" vercel login
if errorlevel 1 (
    echo.
    echo Login failed or was cancelled.
    pause
    exit /b 1
)
echo.
echo Login successful. Run deploy-setup.bat next.
pause
