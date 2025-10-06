# GitHub 发布准备清单

## ✅ 文件准备完成

### 核心文件
- [x] `fofa_mcp.py` - 主程序文件
- [x] `requirements.txt` - Python 依赖
- [x] `.gitignore` - Git 忽略文件

### 文档文件
- [x] `README.md` - 英文说明文档
- [x] `README_CN.md` - 中文说明文档
- [x] `LICENSE` - MIT 许可证
- [x] `CHERRY_STUDIO_SETUP.md` - Cherry Studio 配置指南

### 配置文件
- [x] `config.json.example` - 配置示例
- [x] `start_server.bat` - Windows 启动脚本
- [x] `start_server.sh` - Linux/Mac 启动脚本

## 📋 发布前检查

### 1. 删除不需要的文件
```bash
# 删除原始 Go 项目文件夹
rm -rf uncover-mcp-main

# 或者在 Windows 中
rmdir /s /q uncover-mcp-main
```

### 2. 测试服务器
```bash
# 测试导入
python -c "from fofa_mcp import UncoverMCPServer; print('Import OK')"

# 测试运行（Ctrl+C 退出）
python fofa_mcp.py
```

### 3. 初始化 Git 仓库
```bash
git init
git add .
git commit -m "Initial commit: FOFA MCP Server by nn0nkey"
```

### 4. 创建 GitHub 仓库
1. 访问 https://github.com/new
2. 仓库名称: `Fofa-MCP` 或 `fofa-mcp-server`
3. 描述: FOFA and Shodan MCP Server for AI Assistants
4. 选择 Public
5. 不要初始化 README（我们已经有了）

### 5. 推送到 GitHub
```bash
git remote add origin https://github.com/yourusername/Fofa-MCP.git
git branch -M main
git push -u origin main
```

## 🎯 建议的仓库设置

### Topics (标签)
- `mcp`
- `model-context-protocol`
- `fofa`
- `shodan`
- `ai-assistant`
- `cherry-studio`
- `python`
- `security-tools`

### 仓库描述
```
🔍 FOFA and Shodan MCP Server - AI-powered internet asset discovery tool supporting Cherry Studio and other MCP clients | 基于 MCP 协议的 FOFA 和 Shodan 搜索服务器
```

### README 徽章（可选）
在 README.md 顶部添加：
```markdown
![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![MCP](https://img.shields.io/badge/MCP-compatible-orange.svg)
```

## 📝 首次发布说明

### Release v1.0.0
```markdown
# FOFA MCP Server v1.0.0

首次发布！🎉

## 功能特点
- ✅ 支持 FOFA 和 Shodan 搜索引擎
- ✅ 完全兼容 MCP 协议
- ✅ 支持 Cherry Studio 等 AI 助手
- ✅ 多种输出格式
- ✅ 自动重试机制

## 安装使用
请参考 README.md 文档

## 作者
nn0nkey

## 致谢
基于 projectdiscovery/uncover 项目，使用 Python 重新实现
```

## ⚠️ 注意事项

1. **不要提交敏感信息**
   - 确保 `.gitignore` 已正确配置
   - 不要提交真实的 API 密钥
   - 检查所有配置示例文件

2. **更新 README 中的链接**
   - 将 `yourusername` 替换为你的 GitHub 用户名
   - 更新项目路径

3. **测试文档**
   - 检查所有链接是否有效
   - 确保代码示例正确
   - 验证配置示例可用

## 🚀 发布后

1. 在 GitHub 上创建第一个 Release
2. 添加仓库描述和标签
3. 在社交媒体分享
4. 考虑提交到 MCP 服务器列表

祝发布顺利！🎊
