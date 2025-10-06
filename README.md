# FOFA MCP Server

**作者: nn0nkey**

基于 [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) 的 FOFA 和 Shodan 搜索引擎服务器实现，用于快速发现互联网上暴露的主机。

## ✨ 功能特点

- 🔍 支持 **FOFA** 和 **Shodan** 搜索引擎
- 🎯 多种结果格式输出 (ip:port, host, ip, port)
- 🤖 与 AI 助手自然交互（支持 Cherry Studio 等 MCP 客户端）
- 🔄 支持结果数量限制
- 🛡️ 自动重试机制
- 🌐 完全兼容 MCP 协议

## 📦 安装

1. **克隆项目**
```bash
git clone https://github.com/yourusername/Fofa-MCP.git
cd Fofa-MCP
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置 API 密钥**

设置以下环境变量（至少需要设置一个搜索引擎的API密钥）：

```bash
# Windows
set SHODAN_API_KEY=your_shodan_api_key_here
set FOFA_EMAIL=your_fofa_email_here
set FOFA_KEY=your_fofa_key_here

# Linux/Mac
export SHODAN_API_KEY=your_shodan_api_key_here
export FOFA_EMAIL=your_fofa_email_here
export FOFA_KEY=your_fofa_key_here
```

## 🚀 使用方法

### 在 Cherry Studio 中使用

在 Cherry Studio 的 MCP 配置中添加：

```json
{
    "mcpServers": {
        "fofa-mcp": {
            "command": "python",
            "args": ["fofa_mcp.py"],
            "cwd": "/path/to/Fofa-MCP",
            "env": {
                "SHODAN_API_KEY": "your_shodan_api_key_here",
                "FOFA_EMAIL": "your_fofa_email_here",
                "FOFA_KEY": "your_fofa_key_here"
            }
        }
    }
}
```

### 直接运行

```bash
# Windows
start_server.bat

# Linux/Mac
./start_server.sh

# 或直接运行
python fofa_mcp.py
```

## 📝 使用示例

我想查询百度的10个ip

<img width="1561" height="630" alt="image" src="https://github.com/user-attachments/assets/af32de0a-b2bf-44ac-9bc9-84729bea8e5f" />


### 工具参数

- `query` (必需): 搜索查询语句
- `limit` (可选): 限制结果数量，默认 100
- `field` (可选): 返回字段格式
  - `ip:port` (默认): 返回 "IP:端口" 格式
  - `host`: 返回主机名
  - `ip`: 返回 IP 地址
  - `port`: 返回端口号

## 🔑 API 密钥获取

### Shodan
1. 访问 [Shodan 官网](https://www.shodan.io/)
2. 注册账户
3. 在账户设置中获取 API 密钥

### FOFA
1. 访问 [FOFA 官网](https://fofa.info/)
2. 注册账户
3. 在个人中心获取 API 密钥（Email 和 Key）

## 🛠️ 技术栈

- Python 3.7+
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Requests
- asyncio

## 📄 文件说明

- `fofa_mcp.py` - MCP 服务器主程序
- `requirements.txt` - Python 依赖
- `config.json.example` - Cherry Studio 配置示例
- `start_server.bat` - Windows 启动脚本
- `start_server.sh` - Linux/Mac 启动脚本
- `CHERRY_STUDIO_SETUP.md` - Cherry Studio 详细配置说明

## ⚠️ 注意事项

- 本工具仅供安全研究和合法用途使用
- 请遵守相关法律法规和搜索引擎的使用条款
- 建议合理使用 API 配额，避免频繁请求
- 某些搜索结果可能需要付费 API 密钥

## 🐛 故障排除

### 常见问题

1. **"未设置 API 密钥"错误**
   - 检查环境变量是否正确设置
   - 确认 API 密钥有效

2. **"搜索错误"**
   - 检查网络连接
   - 验证查询语句格式
   - 确认 API 配额未超限

3. **MCP 连接错误**
   - 确认使用最新版本的 `fofa_mcp.py`
   - 检查 Python 版本 >= 3.7
   - 确认所有依赖已正确安装

## 📜 许可证

本项目采用 MIT 许可证

## 👤 作者

**nn0nkey**

基于 [projectdiscovery/uncover](https://github.com/projectdiscovery/uncover) 项目，使用 Python 重新实现

## 🙏 致谢

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Project Discovery - Uncover](https://github.com/projectdiscovery/uncover)
- [FOFA](https://fofa.info/)
- [Shodan](https://www.shodan.io/)

## 🔗 相关链接

- [MCP 文档](https://modelcontextprotocol.io/docs)
- [Cherry Studio](https://github.com/kangfenmao/cherry-studio)
- [FOFA API 文档](https://fofa.info/api)
- [Shodan API 文档](https://developer.shodan.io/)

---

如果这个项目对你有帮助，欢迎 ⭐ Star！
