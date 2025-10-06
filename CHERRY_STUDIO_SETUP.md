# Cherry Studio 配置说明

## 问题解决

你遇到的 `Error invoking remote method 'mcp:list-tools': McpError: MCP error-32000: Connection closed` 错误已经解决！

## 解决方案

1. **使用MCP服务器**: `fofa_mcp.py` (已修复MCP协议兼容性问题)
2. **确保依赖已安装**: 运行 `pip install -r requirements.txt`
3. **正确配置Cherry Studio**

## Cherry Studio 配置

在Cherry Studio的MCP设置中添加以下配置：

```json
{
    "mcpServers": {
        "uncover-mcp": {
            "command": "python",
            "args": ["fofa_mcp.py"],
            "cwd": "C:\\Users\\86135\\Downloads\\Fofa-MCP",
            "env": {
                "SHODAN_API_KEY": "your_shodan_api_key_here",
                "FOFA_EMAIL": "your_fofa_email_here", 
                "FOFA_KEY": "your_fofa_key_here"
            }
        }
    }
}
```

**重要**: 请将 `cwd` 路径改为你的实际项目路径！

## 测试服务器

运行以下命令测试服务器是否正常工作：

```bash
python test_mcp_connection.py
```

如果看到 "SUCCESS: All tests passed!" 说明服务器配置正确。

## 使用示例

配置完成后，在Cherry Studio中可以使用：

### Shodan搜索
- `使用Shodan搜索 ssl:"Uber Technologies, Inc."`
- `查找Shodan中端口22开放的服务器`

### FOFA搜索  
- `使用FOFA搜索 app="ATLASSIAN-JIRA"`
- `在FOFA中查找Apache服务器`

## 故障排除

1. **MCP协议错误**: 确保使用 `fofa_mcp.py` 正确版本
2. **路径问题**: 确保 `cwd` 路径正确指向项目目录
3. **依赖问题**: 确保已安装所有依赖 `pip install -r requirements.txt`
4. **API密钥**: 至少设置一个搜索引擎的API密钥

## 作者

**nn0nkey** - Python版本MCP服务器实现
