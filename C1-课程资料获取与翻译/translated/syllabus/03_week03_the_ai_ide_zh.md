# 第三周：AI 原生 IDE 与上下文管理 (The AI IDE & Context Engineering)

> **斯坦福 CS146S** · 教学周期：10月6日 - 10月10日 · 主讲：Mihail Eric

---

## 一、核心主题与教学要点 (Topics)

- **现代 AI IDE (Cursor、Windsurf) 架构演进：代码库全量索引、AST 抽象语法树与语义嵌入**
- **上下文工程 (Context Engineering)：如何精准组装最紧凑、信息密度最高的项目上下文**
- **上下文衰减 (Context Rot) 危机：输入 Token 激增如何导致大模型检索与推理能力雪崩**
- **面向 Agent 的产品需求文档 (PRD as Source Code)：将需求直接作为 Agent 可执行规格说明**

## 二、必读前沿文献与技术资料 (Reading Materials)

| 资料标题 (Title) | 类别/来源 | 深度内容指引与核心洞察 |
| :--- | :---: | :--- |
| [Specs Are the New Source Code (Ravi Mehta)](../articles/specs-are-the-new-source-code.html) | 核心读物 | 软件工程范式转移：高质量规格说明书正在取代代码成为第一性资产 |
| [How Long Contexts Fail (David Breunig)](../articles/how-long-contexts-fail.html) | 核心读物 | 长上下文陷阱深度剖析：注意力分散、位置偏差与弥补方案 |
| [Context Rot (Chroma Research)](../articles/context-rot.html) | 核心读物 | 前沿实验论证：随着输入上下文增长，模型关键信息检索准确率的非线性衰退规律 |
| [Good Context, Good Code (StockApp)](../articles/good-context-good-code.html) | 核心读物 | 企业实战：如何在大型复杂代码库中构建高命中率上下文组装管线 |

## 三、本周工程实践作业 (Assignment)

> **Assignment 3: Engineering Context for IDE Agents —— 为百万行级真实开源仓库编写 .cursorrules 与模块抽象层，引导 Agent 零错误完成跨文件大型重构。**

## 四、课程讲座与嘉宾安排 (Lectures)

- 周一 10/06: AI IDE 的内核架构：从文本补全到项目级代码库感知 (讲座 Slides)
- 周五 10/10: 上下文工程防线：战胜上下文衰减与 PRD 形式化驱动 (讲座 Slides)

## 五、本周核心心智模型 (Key Takeaways)

💡 **核心认知**：代码本身只是实现细节，规格说明 (Specs) 与上下文边界 (Context Boundaries) 才是 AI 原生开发者的最高指挥棒。

---
*CS146S 官方中文教学资料库 · 由自动化处理管线构建并经专业术语审查通过*
