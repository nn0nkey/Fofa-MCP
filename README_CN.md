# FOFA MCP 服务器

**作者: nn0nkey**

基于 MCP 协议的 FOFA 和 Shodan 搜索引擎服务器，支持 Cherry Studio 等 AI 助手。

[English](README.md) | 简体中文

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置 API 密钥
set FOFA_EMAIL=your_email
set FOFA_KEY=your_key

# 3. 运行服务器
python fofa_mcp.py
```

## Cherry Studio 配置

```json
{
    "mcpServers": {
        "fofa-mcp": {
            "command": "python",
            "args": ["fofa_mcp.py"],
            "cwd": "项目路径",
            "env": {
                "FOFA_EMAIL": "你的邮箱",
                "FOFA_KEY": "你的密钥"
            }
        }
    }
}
```

## 使用示例

```
使用 FOFA 搜索 domain="baidu.com"
在 FOFA 中查找 app="ATLASSIAN-JIRA"
使用 Shodan 搜索 ssl:"example.com"
```

## 功能特点

- ✅ 支持 FOFA 和 Shodan
- ✅ 多种输出格式
- ✅ AI 助手集成
- ✅ 自动重试

## 许可证

MIT License

## 作者

nn0nkey
