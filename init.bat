@echo off

:: 检查 Python 是否在环境变量中
python -V >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo [INFO] Python 3 is already installed.
    :: 检查是否存在虚拟环境 .venv
    if not exist .venv (
        echo [INFO] Creating virtual environment...
        python -m venv .venv
    )
    :: 激活虚拟环境
    call .venv\Scripts\activate
    :: 检查是否存在 requirements.txt 并安装依赖
    if exist requirements.txt (
        echo [INFO] Installing dependencies...
        pip install -r requirements.txt
    ) else (
        echo [ERROR] requirements.txt is not found.
        pause
    )
    echo [INFO] Project initialization complete!
    pause
) else (
    echo [ERROR] Python 3 is either uninstalled or not in the environment variable.
    echo [WARN] Please install Python 3 and add it to the environment variable.
    pause
)
