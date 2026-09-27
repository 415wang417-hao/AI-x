# 第四周：Claude Code 与终端智能体开发流 (Claude Code & Agentic Coding Workflows)

> **斯坦福 CS146S** · 教学周期：10月13日 - 10月17日 · 主讲：Mihail Eric

---

## 一、核心主题与教学要点 (Topics)

- **Claude Code 深度拆解：子进程架构、原生终端集成、测试驱动自动化与自动修复循环**
- **Anthropic 内部使用规范与最佳实践：Prompt 缓存 (Prompt Caching) 与多轮工具循环**
- **伴随式智能体 (Companion Agent) 协作流：任务翻译官、调试伙伴与 AAR 引导体系**
- **如何设计面向复杂工程的自动化分步执行防线**

## 二、必读前沿文献与技术资料 (Reading Materials)

| 资料标题 (Title) | 类别/来源 | 深度内容指引与核心洞察 |
| :--- | :---: | :--- |
| [How Anthropic Uses Claude Code (Research Paper)](../papers/how-anthropic-uses-claude-code_zh.md) | 核心读物 | Anthropic 官方研究白皮书：内部工程团队如何全面转向 Claude Code 驱动日常开发 |
| [Claude Code Best Practices (Anthropic Docs)](../articles/claude-code-best-practices.html) | 核心读物 | 官方权威指南：高效利用 Claude Code 进行大仓阅读、单元测试自愈与安全执行 |
| [Peeking Under the Hood of Claude Code](../articles/peeking-under-the-hood-of-claude-code.html) | 核心读物 | 核心架构逆向解密：进程间通讯、本地沙箱与 Prompt 编排底层 |

## 三、本周工程实践作业 (Assignment)

> **Assignment 4: Autonomous Bug Fixing with Claude Code —— 利用 Claude Code 自动化定位并修复一个复杂 Web 仓库中的 5 个回归缺陷，全量通过 CI 测试并生成 PR 审查摘要。**

## 四、课程讲座与嘉宾安排 (Lectures)

- 周一 10/13: Claude Code 系统架构与内部工程实现全景 (讲座 Slides)
- 周五 10/17: 真实业务代码库中的终端智能体高级编排技巧 (讲座 Slides)

## 五、本周核心心智模型 (Key Takeaways)

💡 **核心认知**：将代码编辑器退居二线，让终端成为高带宽、多步自治的 Agent 运行中枢；依靠测试反馈驱动闭环进化。

---
*CS146S 官方中文教学资料库 · 由自动化处理管线构建并经专业术语审查通过*
