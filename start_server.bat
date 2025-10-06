@echo off
chcp 65001 >nul
echo ========================================
echo Uncover MCP Server - Python版本
echo 作者: nn0nkey
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖...
python -c "import mcp" >nul 2>&1
if errorlevel 1 (
    echo 安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)

REM 检查环境变量
echo 检查API密钥配置...
if "%SHODAN_API_KEY%"=="" (
    echo 警告: 未设置SHODAN_API_KEY环境变量
)
if "%FOFA_EMAIL%"=="" (
    echo 警告: 未设置FOFA_EMAIL环境变量
)
if "%FOFA_KEY%"=="" (
    echo 警告: 未设置FOFA_KEY环境变量
)

echo.
echo 启动服务器...
echo 按Ctrl+C停止服务器
echo.

python fofa_mcp.py

pause
