import os
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_dir = os.path.join(base_dir, 'translated', 'syllabus')
os.makedirs(out_dir, exist_ok=True)

overview_content = \"\"\"# CS146S：现代软件开发者 (The Modern Software Developer) - 课程全景大纲

> **斯坦福大学 (Stanford University) · 计算机科学系 · 2025 秋季学期**  
> 主讲人：Mihail Eric | 助教团队：Febie Lin, Brent Ju  
> 学分：3 Units | 授课地点：420-041 | 官方站点：https://themodernsoftware.dev/

---

## 课程概述 (Course Description)

在过去几年中，大语言模型 (LLM) 为软件开发领域引入了颠覆性的全新范式。从需求定义、系统设计、代码编写、测试断言，到代码审查 (Code Review)、持续集成部署 (CI/CD) 以及线上值班 (On-Call)，传统的软件开发生命周期 (SDLC) 正在每一个阶段被 AI 自动化深度重构。

这向下一代软件工程师提出了极其关键的命题：**如何利用这些突破性技术将个人工程生产力提升 10 倍，并在 AI 原生时代建立不可替代的职业核心竞争力？**

本课程《CS146S: The Modern Software Developer》旨在系统性地向学生传授最先进的 AI 辅助软件开发工具链、设计模式与工程实践方法。从提示词工程 (Prompt Engineering) 的认知筑基，到编程智能体 (Coding Agents)、模型上下文协议 (MCP)、AI 原生 IDE (如 Cursor)、终端智能体 (Claude Code、Warp)、AI 安全漏洞防御，再到端到端全栈交付与自动化站点可靠性工程 (SRE) 诊断，培养具有宏观系统把控能力与极速交付能力的 AI 原生构建者。

---

## 核心教学目标 (Course Goals)

1. **精通前沿 AI 编程工具链**：熟练驾驭 Cursor、Claude Code、Warp 等新一代智能 IDE 与 CLI 智能体，建立高效人机协同流。
2. **掌握智能体架构与协议标准**：深入理解 Coding Agent 的工作原理、工具调用 (Tool Calling)、沙箱隔离及模型上下文协议 (Model Context Protocol, MCP)。
3. **驾驭上下文工程与长文本管理**：攻克上下文衰减 (Context Rot)、设计清晰精准的 Agent 规格说明书 (PRD)，保障长周期任务的生成质量。
4. **筑牢 AI 软件工程安全防线**：识别提示词注入 (Prompt Injection)、远程代码执行 (RCE) 等 AI 新型威胁，融合 SAST/DAST 筑牢防御护栏。
5. **构建现实世界可运行资产 (Artifacts)**：拒绝玩具代码，通过每周项目实战与巅峰期末项目，产出具备生产级可用性与商业叙事价值的软件实体。

---

## 基本信息与课程安排 (Logistics)

| 维度 | 详细说明 |
| :--- | :--- |
| **学分 (Units)** | 3 学分 |
| **先修要求 (Prerequisites)** | 具备编程实践经验（等同于 CS111 水平）；推荐熟悉机器学习/深度学习基础（CS221 或 CS229），但非强制。 |
| **授课形式 (Format)** | 每周 2 次线下讲座（包含前沿行业嘉宾分享） + 每周实操工程作业 (Assignments) + 终极期末大作业 (Final Project)。 |
| **上课时间与教室** | 每周一/周五 下午 1:30 - 2:50 | 斯坦福主校区 420-041 教室 |
| **办公时间 (Office Hours)** | Mihail Eric（主讲）：周三 14:00-15:00；Febie Lin & Brent Ju（助教）：周二/周四 16:00-17:30。 |
| **作业提交与迟交政策** | 每周作业于美西时间周五 23:59 截止；每位学生享有 3 天免费延期宽限期 (Late Days)，逾期按每日扣减 15% 计。 |

---

## 成绩评定标准 (Grading Policy)

- **每周编程实战作业 (Weekly Assignments)**: 50% (共 7 次实验，考察工具驾驭、Agent 编排与自动化能力)
- **期末大项目 (Final Capstone Project)**: 35% (团队或个人完成高完成度行业级系统，含演示与技术文档)
- **课堂讨论与嘉宾互动 (Participation & Engagement)**: 15% (前沿阅读文献思考、讲座互动提问)

---

## 常见问题解答 (FAQ)

### Q1: 这门课适合什么样的同学修读？
**A**: 本课程面向希望彻底告别传统低效敲键盘模式、渴望借助 AI 杠杆实现 10x 生产力跃升的计算机与工程方向学生。如果你具备 Python/TypeScript 或系统编程基础，希望从“代码打字员”转型为“AI 原生架构师”，本课程是最佳跳板。

### Q2: 我们在课程中会使用哪些核心工具？
**A**: 我们将深度实操行业前沿工具：
- **AI 智能 IDE**: Cursor, VS Code AI 插件体系
- **CLI 智能体与终端**: Claude Code, Warp AI Terminal
- **协议与框架**: Model Context Protocol (MCP) SDKs, LangChain/LlamaIndex
- **自动化评测与安全**: Semgrep, OWASP Top 10 防护体系, GitHub Actions CI/CD
- **可观测性与 SRE**: Resolve AI, OpenTelemetry, Prometheus

### Q3: 讲座会提供视频录像吗？
**A**: 所有斯坦福课堂正式讲座均通过 Canvas / Panopto 提供高清回放录像，讲义课件与配套阅读材料同步公开归档。

---
*CS146S 官方中文教学资料库 · 由自动化处理管线构建*
\"\"\"

with open(os.path.join(out_dir, '00_course_overview_zh.md'), 'w', encoding='utf-8') as f:
    f.write(overview_content)

print("[Syllabus] Generated 00_course_overview_zh.md")
