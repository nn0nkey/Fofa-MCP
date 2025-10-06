#!/bin/bash

echo "========================================"
echo "Uncover MCP Server - Python版本"
echo "作者: nn0nkey"
echo "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

# 检查依赖是否安装
echo "检查依赖..."
if ! python3 -c "import mcp" &> /dev/null; then
    echo "安装依赖..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误: 依赖安装失败"
        exit 1
    fi
fi

# 检查环境变量
echo "检查API密钥配置..."
if [ -z "$SHODAN_API_KEY" ]; then
    echo "警告: 未设置SHODAN_API_KEY环境变量"
fi
if [ -z "$FOFA_EMAIL" ]; then
    echo "警告: 未设置FOFA_EMAIL环境变量"
fi
if [ -z "$FOFA_KEY" ]; then
    echo "警告: 未设置FOFA_KEY环境变量"
fi

echo
echo "启动服务器..."
echo "按Ctrl+C停止服务器"
echo

python3 fofa_mcp.py
