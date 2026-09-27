# 第二周：编程智能体解剖学与模型上下文协议 MCP (The Anatomy of Coding Agents & MCP)

> **斯坦福 CS146S** · 教学周期：9月29日 - 10月3日 · 主讲：Mihail Eric

---

## 一、核心主题与教学要点 (Topics)

- **编程智能体 (Coding Agent) 架构解密：感知、推理规划、工具调用 (Tool Calling) 与沙箱执行闭环**
- **模型上下文协议 (Model Context Protocol, MCP) 规范详解：Resources、Prompts 与 Tools 架构**
- **构建工业级 MCP Server：基于 TypeScript / Python SDK 暴露数据源与执行接口**
- **智能体工具设计最佳实践：如何编写清晰的工具描述与防误调契约**

## 二、必读前沿文献与技术资料 (Reading Materials)

| 资料标题 (Title) | 类别/来源 | 深度内容指引与核心洞察 |
| :--- | :---: | :--- |
| [MCP Introduction (Stytch)](../articles/mcp-introduction.html) | 核心读物 | 全景剖析模型上下文协议的诞生背景与核心架构 |
| [Sample MCP Server Implementations](https://github.com/modelcontextprotocol/servers) | 核心读物 | Anthropic 官方开源的参考级 MCP 服务端实现仓库 |
| [MCP Server Authentication (Cloudflare)](../articles/mcp-server-authentication.html) | 核心读物 | 在云原生与无服务器架构下构建安全的远程 MCP 鉴权网关 |
| [Writing Effective Tools for Agents (Anthropic)](../articles/writing-effective-tools-for-agents.html) | 核心读物 | Anthropic 官方工程团队总结的智能体工具设计七大黄金法则 |
| [APIs Don't Make Good MCP Tools](../articles/mcp-food-for-thought.html) | 核心读物 | 深度思辨：为何不能简单将 REST API 包装为 Agent 工具以及如何进行抽象重构 |
| [Devin: Coding Agents 101](../articles/devin-coding-agents-101.html) | 核心读物 | Cognition 团队分享构建全自主软件工程师智能体的工程实战洞察 |

## 三、本周工程实践作业 (Assignment)

> **Assignment 2: Building an MCP-Powered Agent —— 独立编写一个集成 GitHub API 与本地 SQLite 数据库的 MCP Server，并接入 Claude 实现自动化代码审查与元数据打标。**

## 四、课程讲座与嘉宾安排 (Lectures)

- 周一 09/29: 智能体工作流与工具调用机制深度剖析 (讲座 Slides)
- 周五 10/03: 模型上下文协议 (MCP) 深度拆解与企业级落地架构 (讲座 Slides)

## 五、本周核心心智模型 (Key Takeaways)

💡 **核心认知**：Agent 区别于单纯 Chatbot 的核心在于工具调用与状态闭环；MCP 正在成为 AI 与物理软件系统通信的工业级通用总线标准。

---
*CS146S 官方中文教学资料库 · 由自动化处理管线构建并经专业术语审查通过*
