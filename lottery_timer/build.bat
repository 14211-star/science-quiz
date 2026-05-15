@echo off
chcp 65001 >nul
echo [1/2] Starting PyInstaller...
pyinstaller --onefile --windowed --name "TeacherHelper" --clean --noconfirm main.py
if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    pause
    exit /b %ERRORLEVEL%
)
echo [2/2] Build success!
pause