@echo off

:: 每次使用pip安装或移除依赖后，运行此脚本
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
    pip freeze >requirements.txt
    echo [INFO] Requirements dumped to requirements.txt.
    pause
) else (
    echo [ERROR] Python 3 is either uninstalled or not in the environment variable.
    echo [WARN] Please install Python 3 and add it to the environment variable.
    pause
)