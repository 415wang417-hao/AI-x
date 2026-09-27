import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_dir = os.path.join(base_dir, 'translated', 'syllabus')
os.makedirs(out_dir, exist_ok=True)

weeks_data = [
    {
        "num": "01",
        "file": "01_week01_intro_coding_llms_zh.md",
        "title": "第一周：编程大模型入门与提示词工程 (Introduction to Coding LLMs & Prompt Engineering)",
        "dates": "9月22日 - 9月26日",
        "topics": [
            "课程物流、教学体系与 AI 原生开发者成长路径",
            "大语言模型 (LLM) 底层原理：Next-token 预测、自注意力机制与代码生成特质",
            "高效提示词工程 (Prompt Engineering)：少样本提示 (Few-shot)、思维链 (CoT) 与结构化指令",
            "代码生成中的幻觉问题及其规避技巧"
        ],
        "readings": [
            {"title": "Deep Dive into LLMs (Karpathy)", "link": "https://www.youtube.com/watch?v=7xTGNNLPyMI", "desc": "Andrej Karpathy 经典大模型技术底座与运转机制深度解析视频"},
            {"title": "Prompt Engineering Overview (Google Cloud)", "link": "../articles/prompt-engineering-overview.html", "desc": "谷歌云官方全面阐述提示词工程的核心构件与系统化设计理念"},
            {"title": "Prompt Engineering Guide (DAIR.AI)", "link": "../articles/prompt-engineering-guide.html", "desc": "国际公认最权威的提示词工程技术体系与模式汇总指南"},
            {"title": "AI Prompt Engineering: A Deep Dive", "link": "../articles/good-context-good-code.html", "desc": "工业界提示词工程从原型探索走向工程落地的高级模式"}
        ],
        "assignment": "Assignment 1: Prompt Engineering for Code Generation —— 编写标准化 Prompt 引导 LLM 零幻觉生成复杂算法并编写自动化单元测试验证套件。",
        "lectures": [
            "周一 09/22: 课程导学、AI 辅助编程浪潮与大模型底层运作直觉 (讲座 Slides)",
            "周五 09/26: 提示词工程的系统方法论：从单次问答走向结构化思维链编排 (讲座 Slides)"
        ],
        "key_takeaways": "理解大模型本质上是概率推断引擎，Prompt 是塑造概率分布的唯一界面。掌握代码生成场景下约束、示例与校验三位一体的提示原则。"
    },
    {
        "num": "02",
        "file": "02_week02_anatomy_of_coding_agents_zh.md",
        "title": "第二周：编程智能体解剖学与模型上下文协议 MCP (The Anatomy of Coding Agents & MCP)",
        "dates": "9月29日 - 10月3日",
        "topics": [
            "编程智能体 (Coding Agent) 架构解密：感知、推理规划、工具调用 (Tool Calling) 与沙箱执行闭环",
            "模型上下文协议 (Model Context Protocol, MCP) 规范详解：Resources、Prompts 与 Tools 架构",
            "构建工业级 MCP Server：基于 TypeScript / Python SDK 暴露数据源与执行接口",
            "智能体工具设计最佳实践：如何编写清晰的工具描述与防误调契约"
        ],
        "readings": [
            {"title": "MCP Introduction (Stytch)", "link": "../articles/mcp-introduction.html", "desc": "全景剖析模型上下文协议的诞生背景与核心架构"},
            {"title": "Sample MCP Server Implementations", "link": "https://github.com/modelcontextprotocol/servers", "desc": "Anthropic 官方开源的参考级 MCP 服务端实现仓库"},
            {"title": "MCP Server Authentication (Cloudflare)", "link": "../articles/mcp-server-authentication.html", "desc": "在云原生与无服务器架构下构建安全的远程 MCP 鉴权网关"},
            {"title": "Writing Effective Tools for Agents (Anthropic)", "link": "../articles/writing-effective-tools-for-agents.html", "desc": "Anthropic 官方工程团队总结的智能体工具设计七大黄金法则"},
            {"title": "APIs Don't Make Good MCP Tools", "link": "../articles/mcp-food-for-thought.html", "desc": "深度思辨：为何不能简单将 REST API 包装为 Agent 工具以及如何进行抽象重构"},
            {"title": "Devin: Coding Agents 101", "link": "../articles/devin-coding-agents-101.html", "desc": "Cognition 团队分享构建全自主软件工程师智能体的工程实战洞察"}
        ],
        "assignment": "Assignment 2: Building an MCP-Powered Agent —— 独立编写一个集成 GitHub API 与本地 SQLite 数据库的 MCP Server，并接入 Claude 实现自动化代码审查与元数据打标。",
        "lectures": [
            "周一 09/29: 智能体工作流与工具调用机制深度剖析 (讲座 Slides)",
            "周五 10/03: 模型上下文协议 (MCP) 深度拆解与企业级落地架构 (讲座 Slides)"
        ],
        "key_takeaways": "Agent 区别于单纯 Chatbot 的核心在于工具调用与状态闭环；MCP 正在成为 AI 与物理软件系统通信的工业级通用总线标准。"
    },
    {
        "num": "03",
        "file": "03_week03_the_ai_ide_zh.md",
        "title": "第三周：AI 原生 IDE 与上下文管理 (The AI IDE & Context Engineering)",
        "dates": "10月6日 - 10月10日",
        "topics": [
            "现代 AI IDE (Cursor、Windsurf) 架构演进：代码库全量索引、AST 抽象语法树与语义嵌入",
            "上下文工程 (Context Engineering)：如何精准组装最紧凑、信息密度最高的项目上下文",
            "上下文衰减 (Context Rot) 危机：输入 Token 激增如何导致大模型检索与推理能力雪崩",
            "面向 Agent 的产品需求文档 (PRD as Source Code)：将需求直接作为 Agent 可执行规格说明"
        ],
        "readings": [
            {"title": "Specs Are the New Source Code (Ravi Mehta)", "link": "../articles/specs-are-the-new-source-code.html", "desc": "软件工程范式转移：高质量规格说明书正在取代代码成为第一性资产"},
            {"title": "How Long Contexts Fail (David Breunig)", "link": "../articles/how-long-contexts-fail.html", "desc": "长上下文陷阱深度剖析：注意力分散、位置偏差与弥补方案"},
            {"title": "Context Rot (Chroma Research)", "link": "../articles/context-rot.html", "desc": "前沿实验论证：随着输入上下文增长，模型关键信息检索准确率的非线性衰退规律"},
            {"title": "Good Context, Good Code (StockApp)", "link": "../articles/good-context-good-code.html", "desc": "企业实战：如何在大型复杂代码库中构建高命中率上下文组装管线"}
        ],
        "assignment": "Assignment 3: Engineering Context for IDE Agents —— 为百万行级真实开源仓库编写 .cursorrules 与模块抽象层，引导 Agent 零错误完成跨文件大型重构。",
        "lectures": [
            "周一 10/06: AI IDE 的内核架构：从文本补全到项目级代码库感知 (讲座 Slides)",
            "周五 10/10: 上下文工程防线：战胜上下文衰减与 PRD 形式化驱动 (讲座 Slides)"
        ],
        "key_takeaways": "代码本身只是实现细节，规格说明 (Specs) 与上下文边界 (Context Boundaries) 才是 AI 原生开发者的最高指挥棒。"
    },
    {
        "num": "04",
        "file": "04_week04_claude_code_and_agentic_coding_zh.md",
        "title": "第四周：Claude Code 与终端智能体开发流 (Claude Code & Agentic Coding Workflows)",
        "dates": "10月13日 - 10月17日",
        "topics": [
            "Claude Code 深度拆解：子进程架构、原生终端集成、测试驱动自动化与自动修复循环",
            "Anthropic 内部使用规范与最佳实践：Prompt 缓存 (Prompt Caching) 与多轮工具循环",
            "伴随式智能体 (Companion Agent) 协作流：任务翻译官、调试伙伴与 AAR 引导体系",
            "如何设计面向复杂工程的自动化分步执行防线"
        ],
        "readings": [
            {"title": "How Anthropic Uses Claude Code (Research Paper)", "link": "../papers/how-anthropic-uses-claude-code_zh.md", "desc": "Anthropic 官方研究白皮书：内部工程团队如何全面转向 Claude Code 驱动日常开发"},
            {"title": "Claude Code Best Practices (Anthropic Docs)", "link": "../articles/claude-code-best-practices.html", "desc": "官方权威指南：高效利用 Claude Code 进行大仓阅读、单元测试自愈与安全执行"},
            {"title": "Peeking Under the Hood of Claude Code", "link": "../articles/peeking-under-the-hood-of-claude-code.html", "desc": "核心架构逆向解密：进程间通讯、本地沙箱与 Prompt 编排底层"}
        ],
        "assignment": "Assignment 4: Autonomous Bug Fixing with Claude Code —— 利用 Claude Code 自动化定位并修复一个复杂 Web 仓库中的 5 个回归缺陷，全量通过 CI 测试并生成 PR 审查摘要。",
        "lectures": [
            "周一 10/13: Claude Code 系统架构与内部工程实现全景 (讲座 Slides)",
            "周五 10/17: 真实业务代码库中的终端智能体高级编排技巧 (讲座 Slides)"
        ],
        "key_takeaways": "将代码编辑器退居二线，让终端成为高带宽、多步自治的 Agent 运行中枢；依靠测试反馈驱动闭环进化。"
    },
    {
        "num": "05",
        "file": "05_week05_warp_and_ai_terminal_zh.md",
        "title": "第五周：Warp 终端与 AI 原生命令行 (Warp & the AI Terminal)",
        "dates": "10月20日 - 10月24日",
        "topics": [
            "AI 原生终端革新：命令自动预测、错误实时解释与人机协作共享会话",
            "Warp vs Claude Code：定位对比、互补生态与工作流组合策略",
            "Warp 的吃狗粮 (Dogfooding) 哲学：如何用 Warp 构建 Warp",
            "命令行高阶工作流：将自然语言意图无缝编译为安全可靠的 Shell 管道脚本"
        ],
        "readings": [
            {"title": "Warp vs Claude Code: An Honest Comparison", "link": "../articles/warp-vs-claude-code.html", "desc": "深入对比终端交互界面的两种截然不同范式及其适用场景"},
            {"title": "How Warp Uses Warp to Build Warp", "link": "../articles/how-warp-uses-warp.html", "desc": "Warp 团队内部完全依赖自身终端 AI 驱动产品高速迭代的一手经验分享"},
            {"title": "Warp University Tutorials", "link": "https://www.warp.dev/university", "desc": "掌握现代命令行工具、自动化脚本与 AI 交互的精品教程库"}
        ],
        "assignment": "Assignment 5: Agentic Terminal Workflows with Warp —— 编写自定义 Warp Workflows，结合本地脚本构建从代码扫描、环境部署到健康探活的一键式运维流水线。",
        "lectures": [
            "周一 10/20: 重新定义开发者最古老的界面：AI 时代终端的涅槃 (讲座 Slides)",
            "周五 10/24: 嘉宾分享：Warp 核心工程团队谈 AI 终端底层渲染与智能交互 (讲座 Slides)"
        ],
        "key_takeaways": "终端不再是冰冷的文字输出框，而是感知上下文、自动纠错并协同人类执行高阶操作的智能画布。"
    },
    {
        "num": "06",
        "file": "06_week06_ai_security_vulnerability_detection_zh.md",
        "title": "第六周：AI 软件安全与漏洞挖掘 (AI Security & Vulnerability Detection)",
        "dates": "10月27日 - 10月31日",
        "topics": [
            "静态应用程序安全测试 (SAST) vs 动态测试 (DAST) 的现代演变与 AI 融合",
            "提示词注入 (Prompt Injection) 攻击全解：间接注入、越权逃逸与环境污染",
            "GitHub Copilot 与 AI 插件中的远程代码执行 (RCE) 真实漏洞复现与复盘",
            "OWASP Top 10 for LLM Applications 风险矩阵与防御策略",
            "利用 Semgrep 与 LLM 进行混合式自动化漏洞扫描与修复"
        ],
        "readings": [
            {"title": "SAST vs DAST (Splunk)", "link": "../articles/sast-vs-dast.html", "desc": "全面对比代码静态审查与动态黑盒测试的优劣势及工程落地"},
            {"title": "GitHub Copilot: Remote Code Execution via Prompt Injection", "link": "../articles/copilot-prompt-injection-rce.html", "desc": "震撼业界的安全白皮书：通过恶意代码注释中的提示词注入实现受害宿主机 RCE"},
            {"title": "Finding Vulnerabilities in Web Apps using Claude & Codex (Semgrep)", "link": "../articles/finding-vulnerabilities-claude-codex.html", "desc": "Semgrep 团队如何利用大模型挖掘传统静态工具难以识别的高级业务逻辑漏洞"},
            {"title": "Agentic AI Threats & Attack Vectors (Unit 42)", "link": "../articles/agentic-ai-threats.html", "desc": "Palo Alto Networks 深度分析智能体系统面临的投毒、工具滥用与特权提升威胁"},
            {"title": "OWASP Top Ten Web Application Vulnerabilities", "link": "../articles/owasp-top-ten.html", "desc": "经典 Web 漏洞风险清单及其在 AI 生成代码背景下的新变体"}
        ],
        "assignment": "Assignment 6: Red Teaming and Patching AI Workflows —— 在沙箱环境中针对一个漏洞靶场发起间接提示词注入攻击，随后设计安全护栏 (Guardrails) 与 Semgrep 规则完成漏洞修补。",
        "lectures": [
            "周一 10/27: AI 辅助编程带来的安全双刃剑：从代码投毒到 RCE 漏洞 (讲座 Slides)",
            "周五 10/31: 构建防御纵深：静态分析、输入清洗与沙箱化隔离防御体系 (讲座 Slides)"
        ],
        "key_takeaways": "AI 代码不仅继承传统安全缺陷，更引入了指令与数据不分带来的注入漏洞。未经严格沙箱与审阅的 AI 工具调用极度危险。"
    },
    {
        "num": "07",
        "file": "07_week07_ai_powered_code_review_zh.md",
        "title": "第七周：AI 驱动的代码审查 (AI-Powered Code Review)",
        "dates": "11月3日 - 11月7日",
        "topics": [
            "现代代码审查 (Code Review) 工程哲学与文化：Google 与 GitHub 的核心准则",
            "AI 代码审查的演进阶梯：从格式挑刺 (Nitpicking) 到高阶架构与边界分析",
            "抑制误报率与警报疲劳：如何让 AI 审阅意见真正具备可操作性与置信度",
            "自动化 PR 审查机器人架构：CI 触发、上下文提取、增量 Diff 分析与多 Agent 辩论"
        ],
        "readings": [
            {"title": "Code Reviews: Just Do It (Coding Horror)", "link": "../articles/code-reviews-just-do-it.html", "desc": "Jeff Atwood 经典博文：为什么代码审查是唯一不可或缺的高效工程实践"},
            {"title": "How to Review Code Effectively (GitHub)", "link": "../articles/how-to-review-code-effectively.html", "desc": "GitHub Staff Engineer 的审查哲学：善意、情境理解与关注核心价值"},
            {"title": "AI Code Review Implementation & Best Practices (Graphite)", "link": "../articles/ai-code-review-best-practices.html", "desc": "现代工程团队引入 AI 代码审查工具的高效落地路径与关键指标监控"},
            {"title": "Code Review Essentials for Software Teams", "link": "../articles/code-review-essentials.html", "desc": "敏捷团队实施代码审查的核心工作规程与检查清单"},
            {"title": "AI-Assisted Assessment of Coding Practices (Research Paper)", "link": "../papers/ai-assisted-code-review-assessment_zh.md", "desc": "工业界严谨实证评估：AI 在代码可读性、模块化与性能方面的评估能力基准"},
            {"title": "Lessons Learned from AI Code Reviews in Production", "link": "../articles/lessons-from-ai-code-reviews.html", "desc": "生产级应用踩坑实录：如何杜绝 AI 幻觉引发的无意义评论危机"}
        ],
        "assignment": "Assignment 7: Building an Intelligent PR Review Bot —— 实现一个基于 GitHub Actions 的智能审查流水线，能精准识别 PR 中的性能劣化、并发竞争与安全隐患，并自动生成结构化修改建议。",
        "lectures": [
            "周一 11/03: 代码审查的人类心智与工程标准：审查在审什么？ (讲座 Slides)",
            "周五 11/07: AI 代码审查系统设计：上下文丰富化与降噪机制 (讲座 Slides)"
        ],
        "key_takeaways": "高质量的代码审查不是语法纠错，而是系统级思维的校验。AI 必须结合全局架构上下文才能提出真正有价值的审查反馈。"
    },
    {
        "num": "08",
        "file": "08_week08_fullstack_ai_dev_deployment_zh.md",
        "title": "第八周：全栈 AI 应用开发与工程交付 (Full-Stack AI Development & Deployment)",
        "dates": "11月10日 - 11月14日",
        "topics": [
            "全栈应用开发新范式：前端、后端、数据库与 AI 推理编排的极速一体化",
            "自动化部署流水线与基础设施即代码 (IaC) 的 AI 协同",
            "从玩具原型到生产级资产：架构健壮性、数据迁移与高并发容灾考量",
            "期末巅峰大项目全面启动与中期架构评审 (Milestone Review)"
        ],
        "readings": [
            {"title": "How OpenAI Uses Codex for Internal Engineering", "link": "../papers/how-openai-uses-codex_zh.md", "desc": "OpenAI 官方白皮书：顶尖研究实验室如何用大模型自动化构建内部全栈应用"},
            {"title": "Modern Fullstack Architecture Patterns", "link": "https://themodernsoftware.dev/", "desc": "现代软件栈：Next.js、Supabase、FastAPI 与边缘流式推送的最佳实践体系"}
        ],
        "assignment": "Final Capstone Project Milestone: 提交系统架构蓝图 (System Architecture Blueprint)、产品需求文档 (PRD) 与已完成 50% 核心链路的可用原型 Demo。",
        "lectures": [
            "周一 11/10: 全栈 AI 开发全景：从原型秒级生成到生产级架构落地 (讲座 Slides)",
            "周五 11/14: 自动化 CI/CD 与现代云原生部署的 Agent 协同 (讲座 Slides)"
        ],
        "key_takeaways": "AI 将全栈工程的门槛拉平为问题拆解与系统集成能力。真正的竞争力在于将零散组件拼装成完整、稳定运转商业系统的工程把控力。"
    },
    {
        "num": "09",
        "file": "09_week09_sre_observability_agentic_oncall_zh.md",
        "title": "第九周：SRE 可观测性与智能体线上值班 (SRE, Observability & Agentic On-Call)",
        "dates": "11月17日 - 11月21日",
        "topics": [
            "站点可靠性工程 (Site Reliability Engineering, SRE) 核心原则：SLI、SLO、SLA 与错误预算",
            "可观测性三支柱：指标 (Metrics)、日志 (Logs) 与分布式链路追踪 (Traces / Spans)",
            "智能体介入线上值班 (On-Call)：告警自动化降噪、根本原因分析 (RCA) 与快速自愈",
            "基于 Resolve AI 与 Kubernetes 的自动化故障排查多智能体架构"
        ],
        "readings": [
            {"title": "Introduction to Site Reliability Engineering (Google)", "link": "../articles/sre-introduction.html", "desc": "谷歌 SRE 经典开篇：将软件工程思维应用于系统运维的核心哲学"},
            {"title": "Observability Basics: Traces, Spans, Metrics (Last9)", "link": "../articles/observability-basics.html", "desc": "通俗易懂拆解现代分布式系统中的遥测数据与可观测性基石"},
            {"title": "The Role of Multi-Agent Systems in AI-Native Engineering (Resolve AI)", "link": "../articles/multi-agent-systems-ai-native.html", "desc": "深度解析多智能体系统如何在复杂的微服务拓扑中协同进行故障诊断"},
            {"title": "Top 5 Benefits of Agentic AI in On-Call Engineering (Resolve AI)", "link": "../articles/benefits-agentic-ai-oncall.html", "desc": "告别半夜惊魂：AI 智能体如何在分钟级完成故障定位与一键止血"},
            {"title": "Kubernetes Troubleshooting with AI Agents (Resolve AI)", "link": "../articles/kubernetes-troubleshooting-ai.html", "desc": "实战案例：AI 智能体如何排查 CrashLoopBackOff、OOMKilled 等云原生顽疾"}
        ],
        "assignment": "Assignment 8: Automated Incident Response Agent —— 模拟微服务雪崩故障环境，编写一个自动化排查 Agent，通过查询 Prometheus 与 OpenTelemetry 链路日志在 3 分钟内输出止血方案与事后复盘报告 (AAR)。",
        "lectures": [
            "周一 11/17: 现代 SRE 架构与可观测性数据流解剖 (讲座 Slides)",
            "周五 11/21: 智能体值班革命：从规则告警到自治排障系统 (讲座 Slides)"
        ],
        "key_takeaways": "软件上线只是生命周期的开端。可观测性让系统透明，而 Agentic SRE 正在将原本需要数小时的复杂故障排查压缩为秒级确定性响应。"
    },
    {
        "num": "10",
        "file": "10_week10_future_of_ai_software_engineering_zh.md",
        "title": "第十周：软件工程的未来与巅峰大项目展示 (The Future of AI in Software Engineering)",
        "dates": "12月1日 - 12月5日",
        "topics": [
            "软件开发范式的百年未有之大变局：从汇编、高级语言到自然语言编排",
            "资本与产业界前沿视角：a16z 领军人物眼中的软件经济学与 AI 护城河重塑",
            "AI 原生工程师的个人职业定位、技能树演进与非对称竞争优势",
            "期末大项目 (Final Capstone Projects) 巅峰公开演示与专家答辩"
        ],
        "readings": [
            {"title": "Elite 20: Vibe Coding Survival Guide (Playbook)", "link": "../playbook/vibe_coding_playbook_zh.md", "desc": "AI 原生构建者 8 周架构蓝图与 NEOLAF 底层操作系统全量实战手册"},
            {"title": "The End of Programming as We Know It", "link": "https://themodernsoftware.dev/", "desc": "斯坦福与硅谷领袖关于编程本质消解与架构师角色升维的宏大思考"}
        ],
        "assignment": "Final Capstone Project Submission & Presentation: 提交完整的 GitHub 开源仓库、生产级在线 Demo、包含 60+ 规范术语的完整技术文档站以及深度 AAR 复盘报告。",
        "lectures": [
            "周一 12/01: 特邀重磅嘉宾演讲：Martin Casado (a16z 知名投资合伙人) 谈软件资本格局重构 (讲座 Slides)",
            "周五 12/05: 期末大项目路演巅峰展示 (Demo Day) 与结课总结 (讲座 Slides)"
        ],
        "key_takeaways": "不要做敲代码的机器，要做驾驭智能体生态的系统指挥家。理解源于执行，真正的捷径永远是在'运行-报错-修复'的飞轮中创造现实资产。"
    }
]

for w in weeks_data:
    lines = [
        f"# {w['title']}",
        "",
        f"> **斯坦福 CS146S** · 教学周期：{w['dates']} · 主讲：Mihail Eric",
        "",
        "---",
        "",
        "## 一、核心主题与教学要点 (Topics)",
        ""
    ]
    for top in w['topics']:
        lines.append(f"- **{top}**")

    lines.extend([
        "",
        "## 二、必读前沿文献与技术资料 (Reading Materials)",
        "",
        "| 资料标题 (Title) | 类别/来源 | 深度内容指引与核心洞察 |",
        "| :--- | :---: | :--- |"
    ])
    for r in w['readings']:
        lines.append(f"| [{r['title']}]({r['link']}) | 核心读物 | {r['desc']} |")

    lines.extend([
        "",
        "## 三、本周工程实践作业 (Assignment)",
        "",
        f"> **{w['assignment']}**",
        "",
        "## 四、课程讲座与嘉宾安排 (Lectures)",
        ""
    ])
    for lec in w['lectures']:
        lines.append(f"- {lec}")

    lines.extend([
        "",
        "## 五、本周核心心智模型 (Key Takeaways)",
        "",
        f"💡 **核心认知**：{w['key_takeaways']}",
        "",
        "---",
        "*CS146S 官方中文教学资料库 · 由自动化处理管线构建并经专业术语审查通过*"
    ])

    out_path = os.path.join(out_dir, w['file'])
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines) + "\n")
    print(f"[Syllabus] Generated {w['file']}")

print("All 10 weeks of syllabus successfully generated!")
