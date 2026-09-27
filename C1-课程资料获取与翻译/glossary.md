# Stanford CS146S / Vibe Coding 课程核心双语技术术语规范表

> 本术语表共收录 **66** 项核心概念，用于驱动全套自动化翻译管线、Prompt 上下文注入约束、以及全文一致性校验。

| 序号 | 英文术语 (Source Term) | 规范中文译名 (Standard Translation) | 领域类别 (Category) | 核心概念定义与规范说明 | 禁用/生硬译名 (Forbidden) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | **Vibe Coding** | `氛围感编程 (Vibe Coding)` | AI Programming Paradigms | 基于自然语言直觉与 LLM 紧密交互、以结果为导向、宏观编排 Agent 的新型软件构建范式 | 振动编程、感觉编码、随意写代码 |
| 2 | **Scaffolding** | `脚手架机制 / 支架工程` | Agentic Architecture | 围绕大模型构建的引导约束环境、上下文边界、自动化工具链与安全防护框架 | 建筑脚手架、木架 |
| 3 | **Context Engineering** | `上下文工程` | Prompt & Context | 系统化设计、编排、压缩与更新供给大模型的全部输入信息流的工程方法 | 语境工程、背景工程 |
| 4 | **Context Rot** | `上下文衰减 / 上下文退化` | Prompt & Context | 随着长上下文窗口中无关或陈旧 token 累积，模型检索与推理能力显著下降的现象 | 语境腐烂、上下文腐败 |
| 5 | **Model Context Protocol** | `模型上下文协议 (MCP)` | Protocols & Standards | 由 Anthropic 推出的用于连接 AI 模型与本地/远程数据源及工具的开放标准协议 | 模型语境协议 |
| 6 | **MCP Server** | `MCP 服务端 / MCP 工具服务器` | Protocols & Standards | 暴露具体资源（Resources）、提示模板（Prompts）和工具函数（Tools）供客户端调用的服务实体 | - |
| 7 | **MCP Client** | `MCP 客户端` | Protocols & Standards | 发起连接、解析协议并协调宿主环境与 MCP 服务端通信的宿主应用 | - |
| 8 | **MCP Tool** | `MCP 工具` | Protocols & Standards | MCP 规范中可供模型调用的具有副作用或查询能力的外部函数 | - |
| 9 | **MCP Resource** | `MCP 资源` | Protocols & Standards | 只读式数据附件，提供文件内容、数据库记录等上下文信息 | - |
| 10 | **Coding Agent** | `编程智能体 / 编程 Agent` | Agentic Architecture | 具有自主感知代码库、规划执行多步任务、调用终端与编辑工具能力的自治 AI 程序 | 编码代理商、编程中介 |
| 11 | **Autonomous Agent** | `自主智能体 / 自主 Agent` | Agentic Architecture | 无需人类步步介入即可根据全局目标完成感知、决策、工具调用与复盘的智能体系统 | 自动中介 |
| 12 | **Agentic Workflow** | `智能体工作流 (Agentic Workflow)` | Agentic Architecture | 由反思、工具使用、多步规划和多 Agent 协同构成的迭代式 AI 运行机制 | 代理流程 |
| 13 | **Companion Agent** | `伴随式智能体 / 专属伴随代理` | Agentic Architecture | 常驻于开发者工作流中，承担任务拆解、实时 Debug、教练反馈与 AAR 引导的角色型智能体 | 同伴代理、宠物智能体 |
| 14 | **Multi-Agent System** | `多智能体系统 (MAS)` | Agentic Architecture | 多个具有特定分工与角色的 Agent 互相通信、协作完成复杂系统的架构 | 多代理系统 |
| 15 | **Prompt Engineering** | `提示词工程` | Prompt & Context | 针对大语言模型设计、优化输入指令以激发其最佳推理与生成表现的工程方法 | 线索工程、催单工程 |
| 16 | **Few-Shot Prompting** | `少样本提示` | Prompt & Context | 在提示词中提供少量示范用例引导模型泛化生成的技巧 | 几次射击提示 |
| 17 | **Chain of Thought** | `思维链 (CoT)` | Prompt & Context | 引导模型在生成最终答案前逐步输出中间推理步骤的提示策略 | 思想链条、思绪链 |
| 18 | **System Prompt** | `系统提示词 (System Prompt)` | Prompt & Context | 为大模型会话设定基础身份、规则边界、工具定义与全局行为准则的顶层输入 | 系统提示 |
| 19 | **In-Context Learning** | `上下文内学习 (ICL)` | Prompt & Context | 模型仅依据输入上下文中的提示与样例即可即时适应新任务而无需梯度更新的能力 | 语境学习 |
| 20 | **Hallucination** | `幻觉 (Hallucination)` | AI Quality & Evaluation | 模型生成看似合理但与事实不符、逻辑自相矛盾或无法被真实世界支撑的内容 | 错觉、胡说八道 |
| 21 | **Grounding** | `事实锚定 / 真实凭据对齐 (Grounding)` | AI Quality & Evaluation | 将模型输出严格绑定于确定性的外部可信数据源的机制 | 接地、磨底 |
| 22 | **Retrieval-Augmented Generation** | `检索增强生成 (RAG)` | AI Architecture | 结合信息检索与生成式大模型的架构范式，动态检索外部知识注入 Prompt 中生成回答 | - |
| 23 | **Claude Code** | `Claude Code (终端编程智能体工具)` | Tools & Ecosystem | Anthropic 官方开发并运行于命令行的智能代理开发工具 | - |
| 24 | **Cursor** | `Cursor (AI 代码编辑器)` | Tools & Ecosystem | 深度集成 LLM 与项目级上下文感知能力的现代智能 IDE | - |
| 25 | **Warp** | `Warp (现代 AI 终端)` | Tools & Ecosystem | 集成了协作、命令预测与智能 Agent 交互的原生终端工具 | - |
| 26 | **Devin** | `Devin (AI 软件工程师)` | Tools & Ecosystem | Cognition 打造的具备独立沙盒环境的全自主软件工程 Agent | - |
| 27 | **Prompt Injection** | `提示词注入 (Prompt Injection)` | Security & Reliability | 恶意用户或未经验证的外部数据越权覆盖原有指令的安全攻击手段 | 提示灌入 |
| 28 | **Remote Code Execution** | `远程代码执行 (RCE)` | Security & Reliability | 攻击者通过漏洞在受害主机上执行任意代码的高危安全漏洞 | - |
| 29 | **Static Application Security Testing** | `静态应用程序安全测试 (SAST)` | Security & Reliability | 在不运行程序的前提下，通过分析源代码发现潜在漏洞的安全检测技术 | - |
| 30 | **Dynamic Application Security Testing** | `动态应用程序安全测试 (DAST)` | Security & Reliability | 在应用程序运行状态下从外部对其进行黑盒模拟攻击以发现缺陷的测试技术 | - |
| 31 | **Software Bill of Materials** | `软件物料清单 (SBOM)` | Security & Reliability | 构建软件所使用的全部依赖库、组件及许可证元数据的完整清单 | - |
| 32 | **OWASP Top Ten** | `OWASP 十大安全漏洞风险` | Security & Reliability | 开放 Web 应用安全项目发布的前十类最严重安全威胁共识清单 | - |
| 33 | **Code Review** | `代码审查 (Code Review / CR)` | Software Engineering | 开发团队对变更源代码进行系统性人工或自动化检查以保证质量与规范的流程 | 代码复查、代码审核 |
| 34 | **Pull Request** | `合并请求 / 拉取请求 (Pull Request / PR)` | Software Engineering | 向开源仓库或项目主分支提请审查并合入代码变更的标准化协作协议 | 推拉请求 |
| 35 | **Product Requirements Document** | `产品需求文档 (PRD)` | Software Engineering | 明确产品价值、功能范围、用户交互与验收准则的核心规格文档 | - |
| 36 | **Continuous Integration** | `持续集成 (CI)` | DevOps & SRE | 频繁将代码分支合并入主干并通过自动化测试与构建进行快速验证的工程实践 | - |
| 37 | **Continuous Deployment** | `持续部署 (CD)` | DevOps & SRE | 通过自动化流水线将通过测试的代码直接安全发布到生产环境的交付模式 | - |
| 38 | **Site Reliability Engineering** | `站点可靠性工程 (SRE)` | DevOps & SRE | 用软件工程的方法解决运维与系统可靠性问题的学科与工程实践体系 | 网站可靠性工程 |
| 39 | **Observability** | `可观测性 (Observability)` | DevOps & SRE | 通过系统外部输出的度量指标、链路日志和追踪数据推断系统内部状态的能力 | 可见性、观察性 |
| 40 | **Telemetry** | `遥测数据 (Telemetry)` | DevOps & SRE | 系统自动收集并远程传输的日志、指标与链路追踪数据集合 | 远距离测量 |
| 41 | **Trace** | `链路追踪 (Trace)` | DevOps & SRE | 记录请求在分布式系统中穿梭跨越全部节点的完整生命周期流向 | 痕迹 |
| 42 | **Span** | `跨度单元 (Span)` | DevOps & SRE | 分布式追踪系统中构成单个操作或调用的不可分割的时间跨度与执行单元 | 跨径 |
| 43 | **On-Call** | `值班响应 / 线上轮值 (On-Call)` | DevOps & SRE | 工程团队轮流负责在生产环境告警发生时在规定 SLA 内接入处理的应急机制 | 随叫随到、在线候命 |
| 44 | **Incident Management** | `故障应急管理 (Incident Management)` | DevOps & SRE | 针对生产事故从告警、分流、定级、止血、排查到复盘的全生命周期规程 | 事故管理 |
| 45 | **Service Level Objective** | `服务等级目标 (SLO)` | DevOps & SRE | 团队内部设定的关于服务可用性、延迟等指标的目标阈值范围 | - |
| 46 | **Service Level Agreement** | `服务等级协议 (SLA)` | DevOps & SRE | 向外部客户承诺并具有商业赔偿惩罚效力的服务质量底线契约 | - |
| 47 | **Abstract Syntax Tree** | `抽象语法树 (AST)` | Compiler & Code Analysis | 源代码语法结构的树状抽象表现，每个节点代表一种语法构造 | - |
| 48 | **Linter** | `静态代码检查器 (Linter)` | Software Engineering | 静态分析源代码以标记编程风格错误、反模式和潜在代码缺陷的工具 | 代码棉球 |
| 49 | **After Action Review** | `行动后复盘 (AAR)` | Methodology | 在任务完成或迭代里程碑后，对目标、过程、得失与深层原因进行结构化反思并提取复利经验的复盘框架 | 行动后回顾、事后评审 |
| 50 | **Artifact** | `交付产出物 / 现实资产 (Artifact)` | Methodology | 具有独立使用价值、可运行、可复现、可交付检验的软件与知识工程实体产物 | 工件、手工艺品、人工痕迹 |
| 51 | **Human-in-the-Loop** | `人机协同闭环 (Human-in-the-Loop / HITL)` | AI Architecture | 在自动化或智能体关键决策环节保留人类审查、干预与批准通道的系统设计 | 环路中的人类 |
| 52 | **Synthetic Data** | `合成数据 (Synthetic Data)` | AI Training & Eval | 通过算法仿真或大模型生成而非从物理现实采样的训练与测试数据集 | 人造数据 |
| 53 | **Evaluation Harness** | `评测框架 / 评测工具套件 (Eval Harness)` | AI Quality & Evaluation | 自动化运行大量测试用例以系统衡量大模型或 Agent 在特定维度表现的流水线 | 评估马具 |
| 54 | **Token Window** | `Token 上下文窗口` | Prompt & Context | 模型单次推理中能一次性加载处理的最大 Token 数量上限 | 令牌窗口 |
| 55 | **Tool Calling / Function Calling** | `工具调用 / 函数调用` | Agentic Architecture | 模型解析出结构化调用参数并交由外部执行引擎运行以拓展物理世界操作能力的技术 | 工具呼叫 |
| 56 | **Sandboxing** | `沙箱隔离 (Sandboxing)` | Security & Architecture | 在隔离受限的虚拟运行环境中执行未知或由 AI 生成的代码以防止破坏宿主机系统的安全机制 | 沙盒化 |
| 57 | **Zero-Shot Learning** | `零样本学习` | Prompt & Context | 在不提供任何示范样本的前提下直接要求模型泛化理解并执行任务 | 零击学习 |
| 58 | **Fine-Tuning** | `模型微调 (Fine-Tuning)` | AI Training | 在已预训练好的基座模型权重上使用特定领域标注数据做进一步参数更新的训练过程 | 微调、细调 |
| 59 | **Guardrails** | `防护栏机制 / 安全护栏 (Guardrails)` | Security & Reliability | 在模型输入前与输出后部署的规则过滤器与合规审查层，用于阻断越狱与恶意生成 | 公路围栏 |
| 60 | **Reproducibility** | `可复现性 / 可重现性` | Engineering Excellence | 依据既定文档、脚本和配置，在异地干净环境中能够毫无差错地重新生成相同结果的能力 | - |
| 61 | **Syllabus** | `课程大纲与教学日历 (Syllabus)` | Curriculum | 涵盖教学目标、分周进度、必读文献、作业实践与评分标准的全面导学规划表 | - |
| 62 | **Semantic Chunking** | `语义感知分块 (Semantic Chunking)` | Data Processing | 根据代码函数边界、Markdown 标题或段落自然语义结构进行内容切分以避免割裂逻辑的技术 | 语意切片 |
| 63 | **Back-Translation** | `回译质检 (Back-Translation)` | AI Quality & Evaluation | 将目标语言译文重新翻译回源语言并自动计算语义对齐度以发现漏译和幻觉的校验方法 | 倒译 |
| 64 | **Zero-Cost Reuse** | `零成本复用` | Engineering Excellence | 后续学习者无需摸索配置或修补脚本，仅凭一键命令或清晰文档即可无缝接手运行成果的工程交付标准 | - |
| 65 | **Debug Loop** | `调试循环 (Debug Loop)` | AI Programming Paradigms | 在 Vibe Coding 实践中以运行、报错、喂给 AI、修复、重复为核心的学习与构建引擎 | 查错环 |
| 66 | **ILT Production Studio** | `ILT 生产工作室` | Curriculum & Methodology | 以产出物为中心、Agent 优先、占据 80% 实战时间的真实软件生产环节 | - |

---
*版本: 1.0 (全量冻结) | 校验模式: 强制一致性合规审计 (Strict Mode)*
