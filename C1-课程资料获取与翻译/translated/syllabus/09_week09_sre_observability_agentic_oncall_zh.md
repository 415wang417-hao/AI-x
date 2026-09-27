# 第九周：SRE 可观测性与智能体线上值班 (SRE, Observability & Agentic On-Call)

> **斯坦福 CS146S** · 教学周期：11月17日 - 11月21日 · 主讲：Mihail Eric

---

## 一、核心主题与教学要点 (Topics)

- **站点可靠性工程 (Site Reliability Engineering, SRE) 核心原则：SLI、SLO、SLA 与错误预算**
- **可观测性三支柱：指标 (Metrics)、日志 (Logs) 与分布式链路追踪 (Traces / Spans)**
- **智能体介入线上值班 (On-Call)：告警自动化降噪、根本原因分析 (RCA) 与快速自愈**
- **基于 Resolve AI 与 Kubernetes 的自动化故障排查多智能体架构**

## 二、必读前沿文献与技术资料 (Reading Materials)

| 资料标题 (Title) | 类别/来源 | 深度内容指引与核心洞察 |
| :--- | :---: | :--- |
| [Introduction to Site Reliability Engineering (Google)](../articles/sre-introduction.html) | 核心读物 | 谷歌 SRE 经典开篇：将软件工程思维应用于系统运维的核心哲学 |
| [Observability Basics: Traces, Spans, Metrics (Last9)](../articles/observability-basics.html) | 核心读物 | 通俗易懂拆解现代分布式系统中的遥测数据与可观测性基石 |
| [The Role of Multi-Agent Systems in AI-Native Engineering (Resolve AI)](../articles/multi-agent-systems-ai-native.html) | 核心读物 | 深度解析多智能体系统如何在复杂的微服务拓扑中协同进行故障诊断 |
| [Top 5 Benefits of Agentic AI in On-Call Engineering (Resolve AI)](../articles/benefits-agentic-ai-oncall.html) | 核心读物 | 告别半夜惊魂：AI 智能体如何在分钟级完成故障定位与一键止血 |
| [Kubernetes Troubleshooting with AI Agents (Resolve AI)](../articles/kubernetes-troubleshooting-ai.html) | 核心读物 | 实战案例：AI 智能体如何排查 CrashLoopBackOff、OOMKilled 等云原生顽疾 |

## 三、本周工程实践作业 (Assignment)

> **Assignment 8: Automated Incident Response Agent —— 模拟微服务雪崩故障环境，编写一个自动化排查 Agent，通过查询 Prometheus 与 OpenTelemetry 链路日志在 3 分钟内输出止血方案与事后复盘报告 (AAR)。**

## 四、课程讲座与嘉宾安排 (Lectures)

- 周一 11/17: 现代 SRE 架构与可观测性数据流解剖 (讲座 Slides)
- 周五 11/21: 智能体值班革命：从规则告警到自治排障系统 (讲座 Slides)

## 五、本周核心心智模型 (Key Takeaways)

💡 **核心认知**：软件上线只是生命周期的开端。可观测性让系统透明，而 Agentic SRE 正在将原本需要数小时的复杂故障排查压缩为秒级确定性响应。

---
*CS146S 官方中文教学资料库 · 由自动化处理管线构建并经专业术语审查通过*
