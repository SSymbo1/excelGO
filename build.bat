@echo off
setlocal enabledelayedexpansion

echo [INFO] Starting build process...
if not exist excelGO.spec (
    echo [ERROR] Build struct file not found!
    pause
    exit /b 1
)
:: 清理旧构建
if exist build (
    echo [INFO] Cleaning build directory...
    rmdir /s /q build
)
if exist dist (
    echo [INFO] Cleaning dist directory...
    rmdir /s /q dist
)
:: 执行打包
echo [INFO] Running PyInstaller...
call .venv\Scripts\activate
pyinstaller --clean excelGO.spec
:: 错误处理
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Build failed with code %ERRORLEVEL%
    echo [WARN] Please check the build environment!
    pause
    exit /b %ERRORLEVEL%
)
:: 清理临时文件
echo [INFO] Cleaning up...
if exist build (
    rmdir /s /q build
)
echo [INFO] Build complete!
pause