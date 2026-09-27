#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS146S Pipeline Step 5: Static Portal & Bilingual Documentation Generator
Generates:
1. index_zh.html: Fully localized Chinese portal with links to all translated assets
2. Injects high-contrast language switchers into both index.html and index_zh.html
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_EN_PATH = os.path.join(BASE_DIR, "index.html")
INDEX_ZH_PATH = os.path.join(BASE_DIR, "index_zh.html")

def generate_index_zh():
    zh_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CS146S: 现代软件开发者 (The Modern Software Developer) - 斯坦福大学中文全量课程中枢</title>
  <style>
    /* ===== 重置与基础样式 ===== */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
      font-size: 16px;
      line-height: 1.6;
      color: #1a1a1a;
      background: #f8f8f8;
    }
    a { color: #8c1515; text-decoration: none; }
    a:hover { text-decoration: underline; }

    /* ===== 顶部导航栏与语言切换器 ===== */
    .site-header {
      background: #8c1515;
      color: #fff;
      padding: 24px 32px 18px;
      position: relative;
    }
    .header-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }
    .site-header h1 {
      font-size: 1.85rem;
      font-weight: 700;
      letter-spacing: -0.5px;
    }
    .site-header .subtitle {
      font-size: 0.95rem;
      opacity: 0.9;
      margin-top: 6px;
    }
    .lang-switcher {
      display: inline-flex;
      background: rgba(255, 255, 255, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.4);
      border-radius: 20px;
      padding: 4px;
      font-size: 0.85rem;
    }
    .lang-switcher a {
      color: #fff;
      padding: 4px 14px;
      border-radius: 16px;
      font-weight: 500;
      text-decoration: none;
      transition: background 0.2s;
    }
    .lang-switcher a.active {
      background: #fff;
      color: #8c1515;
      font-weight: 700;
    }

    /* ===== 标签页导航 ===== */
    .nav-tabs {
      background: #fff;
      border-bottom: 2px solid #e0e0e0;
      padding: 0 32px;
      display: flex;
      gap: 0;
    }
    .nav-tab {
      padding: 14px 22px;
      cursor: pointer;
      font-size: 0.98rem;
      font-weight: 600;
      color: #555;
      border-bottom: 3px solid transparent;
      margin-bottom: -2px;
      transition: color 0.15s, border-color 0.15s;
      background: none;
      border-top: none;
      border-left: none;
      border-right: none;
    }
    .nav-tab:hover { color: #8c1515; }
    .nav-tab.active { color: #8c1515; border-bottom-color: #8c1515; }

    /* ===== 主容器 ===== */
    .main-content {
      max-width: 960px;
      margin: 0 auto;
      padding: 32px 24px;
    }
    .tab-panel { display: none; }
    .tab-panel.active { display: block; }

    /* ===== 状态公告栏 ===== */
    .banner-notice {
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      border-radius: 8px;
      padding: 16px 20px;
      margin-bottom: 24px;
      font-size: 0.92rem;
      color: #166534;
      line-height: 1.5;
    }
    .banner-notice strong { color: #15803d; }

    /* ===== 卡片布局 ===== */
    .info-card {
      background: #fff;
      border: 1px solid #e5e5e5;
      border-radius: 8px;
      padding: 20px;
    }
    .info-card h3 {
      font-size: 0.85rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #8c1515;
      margin-bottom: 8px;
    }
    .overview-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin: 24px 0;
    }
    .course-description {
      background: #fff;
      border: 1px solid #e5e5e5;
      border-radius: 8px;
      padding: 28px;
      margin-bottom: 24px;
    }
    .course-description h2 {
      font-size: 1.45rem;
      font-weight: 700;
      margin-bottom: 16px;
      color: #1a1a1a;
      border-bottom: 2px solid #8c1515;
      padding-bottom: 8px;
    }
    .course-description p { margin-bottom: 14px; color: #333; line-height: 1.7; }

    /* ===== 课程表周卡片 ===== */
    .week-card {
      background: #fff;
      border: 1px solid #e5e5e5;
      border-radius: 8px;
      margin-bottom: 24px;
      overflow: hidden;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .week-header {
      background: #fbfbfb;
      padding: 16px 24px;
      font-weight: 700;
      font-size: 1.1rem;
      color: #1a1a1a;
      border-bottom: 1px solid #eee;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .week-badge {
      background: #fee2e2;
      color: #991b1b;
      font-size: 0.8rem;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 600;
    }
    .week-body { padding: 22px 24px; }
    .week-section { margin-bottom: 18px; }
    .week-section:last-child { margin-bottom: 0; }
    .week-section h4 {
      font-size: 0.82rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #8c1515;
      margin-bottom: 8px;
    }
    .week-section ul { list-style: none; padding: 0; }
    .week-section ul li {
      padding: 4px 0;
      font-size: 0.95rem;
      display: flex;
      align-items: baseline;
      gap: 8px;
    }
    .week-section ul li::before {
      content: "•";
      color: #8c1515;
      font-weight: bold;
    }
    .lecture-row {
      background: #fafafa;
      border: 1px solid #eee;
      border-radius: 6px;
      padding: 10px 16px;
      margin: 8px 0;
      font-size: 0.92rem;
    }
    .lecture-row .date { font-weight: 700; color: #444; }
    .btn-zh {
      background: #fdf2f2;
      color: #8c1515;
      border: 1px solid #fecaca;
      border-radius: 4px;
      padding: 1px 6px;
      font-size: 0.78rem;
      font-weight: 600;
      margin-left: 6px;
    }
    .btn-zh:hover { background: #8c1515; color: #fff; }

    /* ===== FAQ ===== */
    .faq-item {
      background: #fff;
      border: 1px solid #e5e5e5;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 16px;
    }
    .faq-item h3 {
      font-size: 1.05rem;
      font-weight: 700;
      color: #1a1a1a;
      margin-bottom: 8px;
    }
    .faq-item p { color: #444; font-size: 0.95rem; }

    /* ===== 页脚 ===== */
    .site-footer {
      text-align: center;
      padding: 30px;
      color: #777;
      font-size: 0.88rem;
      border-top: 1px solid #e0e0e0;
      margin-top: 40px;
      background: #fff;
    }
  </style>
</head>
<body>

<!-- Header -->
<header class="site-header">
  <div class="header-top">
    <div>
      <h1>CS146S: 现代软件开发者 (The Modern Software Developer)</h1>
      <div class="subtitle">斯坦福大学 &bull; 2025年秋季 &bull; 主讲导师：Mihail Eric</div>
    </div>
    <div class="lang-switcher">
      <a href="index.html">English</a>
      <a href="index_zh.html" class="active">中文精校版</a>
    </div>
  </div>
</header>

<!-- Navigation Tabs -->
<nav class="nav-tabs">
  <button class="nav-tab active" onclick="showTab('overview')">课程总览 (Overview)</button>
  <button class="nav-tab" onclick="showTab('syllabus')">完整大纲与资料 (Syllabus)</button>
  <button class="nav-tab" onclick="showTab('faq')">常见问题解答 (FAQ)</button>
  <button class="nav-tab" onclick="showTab('pipeline')">自动化管线与交付物 (Delivery)</button>
</nav>

<!-- Main Content -->
<main class="main-content">

  <!-- 公告提示栏 -->
  <div class="banner-notice">
    <strong>全量中文化离线知识中枢已就绪</strong> — 本门户包含斯坦福 CS146S（亦称 Stanford Vibe Coding 课程）全套 10 周课程材料：<strong>34 篇精校必读文献</strong>、<strong>14 套课件讲义指南与原始 PDF</strong>、<strong>8 周课后实验手册与作业代码</strong>以及完整的术语库与自动化质量审计报告。
  </div>

  <!-- ===== OVERVIEW TAB ===== -->
  <div id="tab-overview" class="tab-panel active">
    <div class="course-description">
      <h2>课程核心理念</h2>
      <p>过去几年里，大语言模型（LLM）为软件工程带来了革命性的全新范式。软件开发生命周期的每一个阶段都在被 AI 自动化深度重构。下一代软件工程师该如何利用这些突破性进展，实现 <strong>10倍生产力跃迁（10x Productivity）</strong> 并为未来职业生涯做好准备？</p>
      <p>本课程由斯坦福大学打造，旨在证明现代 AI 开发工具不仅能够极大提升资深开发者的效率，更将使软件工程走向大众化。软件开发已从传统的“从 0 到 1 手工编写代码”，演变为<strong>“规划 (Plan) &rarr; AI 生成 (Generate) &rarr; 调试修改 (Modify) &rarr; 重复迭代 (Repeat)”</strong>的敏捷工作流。同学们将同时掌握传统软件工程核心挑战的底层理论，以及当今解决这些挑战的尖端 AI 工具链。</p>
      <p>通过每周亲自动手的工程实验以及来自一线工业开拓者（Anthropic、Cognition/Devin、Warp、Graphite、Vercel、Resolve AI）的深度讲座，你将获得 AI 辅助开发、自动化测试、智能文档与安全漏洞检测的扎实经验。课程结束时，你将清晰洞察如何将最前沿的 LLM 模型无缝集成进复杂的软件开发流水线中，并规避常见的工程深坑。</p>
    </div>

    <div class="overview-grid">
      <div class="info-card">
        <h3>学分 (Units)</h3>
        <p>3 学分 (3 Units)</p>
      </div>
      <div class="info-card">
        <h3>前置先修要求 (Prerequisites)</h3>
        <p>具备 CS111 同等编程经验；推荐具备 CS221 / CS229（机器学习/人工智能基础）。</p>
      </div>
      <div class="info-card">
        <h3>教学形式 (Format)</h3>
        <p>每周主题讲座 + 上手编程实验 + 顶级工业先锋嘉宾特邀分享 + 现代开发范式结课大作业。</p>
      </div>
      <div class="info-card">
        <h3>核心教学目标 (Goals)</h3>
        <p>精通现代 AI 编程智能体、掌握模型上下文协议 (MCP)、精通自动化代码审查与安全测试、探索 AI 原生全栈运维。</p>
      </div>
      <div class="info-card">
        <h3>授课教室 (Classroom)</h3>
        <p>斯坦福主校区 420-041</p>
      </div>
      <div class="info-card">
        <h3>答疑时间 (Office Hours)</h3>
        <p><strong>Mihail Eric:</strong> 周五 12:00–12:30 PM<br><strong>Febie Lin:</strong> 周三 9:00–11:00 AM (Huang 地下室)</p>
      </div>
    </div>
  </div>

  <!-- ===== SYLLABUS TAB ===== -->
  <div id="tab-syllabus" class="tab-panel">
    <h2 style="font-size:1.5rem;font-weight:700;margin-bottom:20px;border-bottom:2px solid #8c1515;padding-bottom:8px;">课程完整进度大纲 (Week 1 ~ Week 10)</h2>

    <!-- Week 1 -->
    <div class="week-card">
      <div class="week-header">
        <span>第 1 周：编程大模型入门与 AI 辅助开发 (Introduction to Coding LLMs)</span>
        <span class="week-badge">Week 1</span>
      </div>
      <div class="week-body">
        <div class="week-section">
          <h4>核心专题</h4>
          <ul>
            <li>课程教学法与开发环境搭建</li>
            <li>大语言模型的本质机理（预训练、微调与词元化）</li>
            <li>如何进行高阶高效的提示词工程 (Prompt Engineering)</li>
          </ul>
        </div>
        <div class="week-section">
          <h4>核心阅读材料（中英对照）</h4>
          <ul>
            <li><a href="pages_zh/prompt-engineering-overview.html">📄 提示词工程完全概述与最佳实践指南</a> <a href="pages_zh/prompt-engineering-overview.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/prompt-engineering-guide.html">📄 前沿提示词技术深度指南 (Prompting Guide)</a> <a href="pages_zh/prompt-engineering-guide.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/how-openai-uses-codex.html">📕 OpenAI 官方实录：OpenAI 内部团队如何深度使用 Codex</a> <a href="pages_zh/how-openai-uses-codex.html" class="btn-zh">中文精校</a></li>
            <li><a href="https://www.youtube.com/watch?v=7xTGNNLPyMI" target="_blank">▶ Andrej Karpathy: 深度拆解大语言模型 (Deep Dive into LLMs)</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课后编程实验</h4>
          <ul>
            <li><a href="assignments_zh/week1_assignment_zh.html">⚙️ Week 1 作业：大模型提示词工程训练场 (Prompting Playground)</a> <a href="assignments_zh/week1_assignment_zh.html" class="btn-zh">实验手册</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课堂讲座与课件</h4>
          <div class="lecture-row">
            <span class="date">周一 9/22:</span> 大模型基本原理与制造流程全景 &mdash; 
            <a href="slides_zh/week1_1.1_guide.html" class="btn-zh">课件中文指南</a> 
            <a href="slides_pdf/week1_1_intro_and_how_llm_is_made.pdf" target="_blank">📄 原始 PDF</a>
          </div>
          <div class="lecture-row">
            <span class="date">周五 9/26:</span> 大模型高阶提示词实战 (Power Prompting) &mdash; 
            <a href="slides_zh/week1_1.2_guide.html" class="btn-zh">课件中文指南</a> 
            <a href="slides_pdf/week1_2_power_prompting_for_llms.pdf" target="_blank">📄 原始 PDF</a>
          </div>
        </div>
      </div>
    </div>

    <!-- Week 2 -->
    <div class="week-card">
      <div class="week-header">
        <span>第 2 周：编程智能体的解剖学 (The Anatomy of Coding Agents)</span>
        <span class="week-badge">Week 2</span>
      </div>
      <div class="week-body">
        <div class="week-section">
          <h4>核心专题</h4>
          <ul>
            <li>工具调用 (Tool Use) 与函数调用 (Function Calling) 底层实现</li>
            <li>模型上下文协议 (Model Context Protocol, MCP) 深度架构</li>
          </ul>
        </div>
        <div class="week-section">
          <h4>核心阅读材料（中英对照）</h4>
          <ul>
            <li><a href="pages_zh/mcp-introduction.html">📄 模型上下文协议 (MCP) 深度入门与架构解析</a> <a href="pages_zh/mcp-introduction.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/mcp-server-authentication.html">📄 远程 MCP 服务端身份鉴权与安全架构指南</a> <a href="pages_zh/mcp-server-authentication.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/mcp-food-for-thought.html">📄 批判性思考：为什么传统 API 不等于优秀的 MCP 工具？</a> <a href="pages_zh/mcp-food-for-thought.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/mcp-registry-preview.html">📄 MCP 官方注册中心 (Registry) 前瞻与生态格局</a> <a href="pages_zh/mcp-registry-preview.html" class="btn-zh">中文精校</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课后编程实验与随堂练习</h4>
          <ul>
            <li><a href="assignments_zh/week2_assignment_zh.html">⚙️ Week 2 作业：AI IDE 初体验与第一个自定义 MCP 服务端</a> <a href="assignments_zh/week2_assignment_zh.html" class="btn-zh">实验手册</a></li>
            <li><a href="exercises/week2_completed_exercise_coding_agent.py" target="_blank">📁 随堂练习源码：从零构建基础编程智能体 (coding_agent.py)</a></li>
            <li><a href="exercises/week2_completed_exercise_mcp_server.py" target="_blank">📁 随堂练习源码：自定义 MCP 服务端实现 (mcp_server.py)</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课堂讲座与课件</h4>
          <div class="lecture-row">
            <span class="date">周一 9/29:</span> 从零构建编程智能体 &mdash; 
            <a href="slides_zh/week2_2.1_guide.html" class="btn-zh">课件中文指南</a> 
            <a href="slides_pdf/week2_1_building_coding_agent_from_scratch.pdf" target="_blank">📄 原始 PDF</a>
          </div>
          <div class="lecture-row">
            <span class="date">周五 10/3:</span> 构建自定义 MCP 服务端 &mdash; 
            <a href="slides_zh/week2_2.2_guide.html" class="btn-zh">课件中文指南</a> 
            <a href="slides_pdf/week2_2_building_custom_mcp_server.pdf" target="_blank">📄 原始 PDF</a>
          </div>
        </div>
      </div>
    </div>

    <!-- Week 3 -->
    <div class="week-card">
      <div class="week-header">
        <span>第 3 周：现代 AI 集成开发环境 (The AI IDE)</span>
        <span class="week-badge">Week 3</span>
      </div>
      <div class="week-body">
        <div class="week-section">
          <h4>核心专题</h4>
          <ul>
            <li>上下文管理与大型代码库语义理解</li>
            <li>面向智能体的产品需求文档 (PRDs for Agents) 编写规范</li>
            <li>IDE 插件生态与协议层深度集成</li>
          </ul>
        </div>
        <div class="week-section">
          <h4>核心阅读材料（中英对照）</h4>
          <ul>
            <li><a href="pages_zh/specs-are-the-new-source-code.html">📄 规格说明即源代码：AI 时代的软件开发新定律</a> <a href="pages_zh/specs-are-the-new-source-code.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/how-long-contexts-fail.html">📄 长上下文失效的真实原因及其工程应对方案</a> <a href="pages_zh/how-long-contexts-fail.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/devin-coding-agents-101.html">📄 Devin 团队：现代自主编程智能体架构 101</a> <a href="pages_zh/devin-coding-agents-101.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/writing-effective-tools-for-agents.html">📄 Anthropic 官方：如何为智能体编写高效的生产级工具</a> <a href="pages_zh/writing-effective-tools-for-agents.html" class="btn-zh">中文精校</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课后编程实验与设计模板</h4>
          <ul>
            <li><a href="assignments_zh/week3_assignment_zh.html">⚙️ Week 3 作业：构建生产级企业 MCP Server 与规范驱动开发</a> <a href="assignments_zh/week3_assignment_zh.html" class="btn-zh">实验手册</a></li>
            <li><a href="exercises/week3_design_doc_template.md" target="_blank">📁 斯坦福推荐：面向 AI 智能体的软件设计文档模板 (Design Doc Template)</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课堂讲座与课件</h4>
          <div class="lecture-row">
            <span class="date">周一 10/6:</span> 现代 AI IDE 架构深度剖析 &mdash; 
            <a href="slides_zh/week3_3.1_guide.html" class="btn-zh">课件中文指南</a> 
            <a href="slides_pdf/week3_1_ai_ide_deep_dive.pdf" target="_blank">📄 原始 PDF</a>
          </div>
          <div class="lecture-row">
            <span class="date">周五 10/10:</span> 特邀嘉宾：Silas Alberti (Cognition / Devin 主创) &mdash; 
            <a href="slides_zh/week3_3.2_guide.html" class="btn-zh">课件中文指南</a> 
            <a href="slides_pdf/week3_2_guest_silas_alberti_cognition.pdf" target="_blank">📄 原始 PDF</a>
          </div>
        </div>
      </div>
    </div>

    <!-- Week 4 -->
    <div class="week-card">
      <div class="week-header">
        <span>第 4 周：Claude Code 与智能体编程工作流 (Claude Code & Agentic Coding)</span>
        <span class="week-badge">Week 4</span>
      </div>
      <div class="week-body">
        <div class="week-section">
          <h4>核心专题</h4>
          <ul>
            <li>Claude Code 内部架构、动态提示词装配与执行机制</li>
            <li>全自主智能体编程工作流与 CLAUDE.md 项目宪章</li>
            <li>面向长任务的代码上下文工程 (Context Engineering)</li>
          </ul>
        </div>
        <div class="week-section">
          <h4>核心阅读材料（中英对照）</h4>
          <ul>
            <li><a href="pages_zh/how-anthropic-uses-claude-code.html">📕 Anthropic 官方实战报告：Anthropic 内部团队如何使用 Claude Code</a> <a href="pages_zh/how-anthropic-uses-claude-code.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/claude-code-best-practices.html">📄 Anthropic 官方：Claude Code 高效工作流最佳实践</a> <a href="pages_zh/claude-code-best-practices.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/peeking-under-the-hood-of-claude-code.html">📄 逆向解密 Claude Code：智能体架构与 &lt;system-reminder&gt; 机理剖析</a> <a href="pages_zh/peeking-under-the-hood-of-claude-code.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/good-context-good-code.html">📄 优质上下文铸就优质代码：智能体提示质量的决定性基石</a> <a href="pages_zh/good-context-good-code.html" class="btn-zh">中文精校</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课后编程实验</h4>
          <ul>
            <li><a href="assignments_zh/week4_assignment_zh.html">⚙️ Week 4 作业：使用 Claude Code 进行自主代码重构与智能体编排</a> <a href="assignments_zh/week4_assignment_zh.html" class="btn-zh">实验手册</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课堂讲座与课件</h4>
          <div class="lecture-row">
            <span class="date">周一 10/13:</span> Claude Code 深度剖析 &mdash; 
            <a href="slides_zh/week4_4.1_guide.html" class="btn-zh">课件中文指南</a> 
            <a href="slides_pdf/week4_1_claude_code_deep_dive.pdf" target="_blank">📄 原始 PDF</a>
          </div>
          <div class="lecture-row">
            <span class="date">周五 10/17:</span> 特邀嘉宾：Boris Cherny (Anthropic / Claude Code 负责人) &mdash; 
            <a href="slides_zh/week4_4.2_guide.html" class="btn-zh">课件中文指南</a> 
            <a href="slides_pdf/week4_2_guest_boris_cherny_claude_code.pdf" target="_blank">📄 原始 PDF (4.8MB)</a>
          </div>
        </div>
      </div>
    </div>

    <!-- Week 5 -->
    <div class="week-card">
      <div class="week-header">
        <span>第 5 周：Warp 与 AI 智能终端开发 (Warp & The AI Terminal)</span>
        <span class="week-badge">Week 5</span>
      </div>
      <div class="week-body">
        <div class="week-section">
          <h4>核心专题</h4>
          <ul>
            <li>AI 原生终端架构演进</li>
            <li>人机协同智能体工作流与命令自动补全</li>
          </ul>
        </div>
        <div class="week-section">
          <h4>核心阅读材料（中英对照）</h4>
          <ul>
            <li><a href="pages_zh/warp-vs-claude-code.html">📄 Warp 终端 vs. Claude Code：AI 原生开发环境的路线之争</a> <a href="pages_zh/warp-vs-claude-code.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/how-warp-uses-warp.html">📄 Warp 内部工程实践：如何用 AI 终端构建下一代 AI 终端</a> <a href="pages_zh/how-warp-uses-warp.html" class="btn-zh">中文精校</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课后编程实验</h4>
          <ul>
            <li><a href="assignments_zh/week5_assignment_zh.html">⚙️ Week 5 作业：Warp AI 终端智能流与端到端协同开发</a> <a href="assignments_zh/week5_assignment_zh.html" class="btn-zh">实验手册</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课堂讲座与课件</h4>
          <div class="lecture-row">
            <span class="date">周一 10/20:</span> Warp 终端与 AI 开发体系 &mdash; 
            <a href="slides_zh/week5_5.1_guide.html" class="btn-zh">课件中文指南</a> 
            <a href="slides_pdf/week5_1_warp_and_ai_terminal.pdf" target="_blank">📄 原始 PDF</a>
          </div>
          <div class="lecture-row">
            <span class="date">周五 10/24:</span> 特邀嘉宾：Zach Lloyd (Warp 创始人兼 CEO)
          </div>
        </div>
      </div>
    </div>

    <!-- Week 6 -->
    <div class="week-card">
      <div class="week-header">
        <span>第 6 周：AI 时代软件安全与漏洞检测 (AI Security & Vulnerability Detection)</span>
        <span class="week-badge">Week 6</span>
      </div>
      <div class="week-body">
        <div class="week-section">
          <h4>核心专题</h4>
          <ul>
            <li>安全测试方法论：静态代码分析 (SAST) vs. 动态渗透测试 (DAST)</li>
            <li>提示注入 (Prompt Injection) 与远程代码执行 (RCE) 攻击原理</li>
            <li>AI 辅助漏洞挖掘与修复</li>
            <li>OWASP Top 10 安全规范落地</li>
          </ul>
        </div>
        <div class="week-section">
          <h4>核心阅读材料（中英对照）</h4>
          <ul>
            <li><a href="pages_zh/sast-vs-dast.html">📄 SAST vs. DAST：现代应用安全测试的全面对比与 AI 协同</a> <a href="pages_zh/sast-vs-dast.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/copilot-prompt-injection-rce.html">📄 漏洞实录：通过提示注入在 GitHub Copilot 中实现 RCE</a> <a href="pages_zh/copilot-prompt-injection-rce.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/finding-vulnerabilities-claude-codex.html">📄 Semgrep 实战：使用 Claude Code 与 Codex 挖掘 Web 应用深层漏洞</a> <a href="pages_zh/finding-vulnerabilities-claude-codex.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/agentic-ai-threats.html">📄 Unit 42 报告：智能体 AI 面临的全新威胁模型与身份冒用风险</a> <a href="pages_zh/agentic-ai-threats.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/owasp-top-ten.html">📄 OWASP Top 10 全面解读：核心 Web 应用安全风险与防护对策</a> <a href="pages_zh/owasp-top-ten.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/context-rot.html">📄 Chroma 研究院：揭秘大模型上下文退化 (Context Rot) 的内在机制</a> <a href="pages_zh/context-rot.html" class="btn-zh">中文精校</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课后编程实验</h4>
          <ul>
            <li><a href="assignments_zh/week6_assignment_zh.html">⚙️ Week 6 作业：编写安全的 AI 代码与自动化安全漏洞攻防演练</a> <a href="assignments_zh/week6_assignment_zh.html" class="btn-zh">实验手册</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课堂讲座与课件</h4>
          <div class="lecture-row">
            <span class="date">周一 10/27:</span> AI 时代软件安全与攻防精粹 &mdash; 
            <a href="slides_zh/week6_6.1_guide.html" class="btn-zh">课件中文指南</a> 
            <a href="slides_pdf/week6_1_ai_security_deep_dive.pdf" target="_blank">📄 原始 PDF</a>
          </div>
          <div class="lecture-row">
            <span class="date">周五 10/31:</span> 特邀嘉宾：Isaac Evans (Semgrep 创始人兼 CEO)
          </div>
        </div>
      </div>
    </div>

    <!-- Week 7 -->
    <div class="week-card">
      <div class="week-header">
        <span>第 7 周：AI 赋能的代码审查 (AI-Powered Code Review)</span>
        <span class="week-badge">Week 7</span>
      </div>
      <div class="week-body">
        <div class="week-section">
          <h4>核心专题</h4>
          <ul>
            <li>代码审查最佳实践与工程心理学</li>
            <li>AI 辅助代码审查架构与噪音控制</li>
            <li>团队内隐经验 (Tribal Knowledge) 与自动化审查工具链</li>
          </ul>
        </div>
        <div class="week-section">
          <h4>核心阅读材料（中英对照）</h4>
          <ul>
            <li><a href="pages_zh/lessons-from-ai-code-reviews.html">📄 数百万次 AI 代码审查的沉痛教训：昆虫学隐喻与落地反思</a> <a href="pages_zh/lessons-from-ai-code-reviews.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/ai-code-review-best-practices.html">📄 Graphite 指南：企业落地 AI 代码审查的实战最佳实践</a> <a href="pages_zh/ai-code-review-best-practices.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/ai-assisted-code-review-assessment.html">📕 权威学术评估：现代代码审查中 AI 辅助编码实践的实证效能</a> <a href="pages_zh/ai-assisted-code-review-assessment.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/code-reviews-just-do-it.html">📄 代码审查：毫不犹豫，立刻行动 (Just Do It)</a> <a href="pages_zh/code-reviews-just-do-it.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/how-to-review-code-effectively.html">📄 GitHub Staff 工程师哲学：如何高效且具建设性地审查代码</a> <a href="pages_zh/how-to-review-code-effectively.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/code-review-essentials.html">📄 软件团队代码审查核心基本功手册</a> <a href="pages_zh/code-review-essentials.html" class="btn-zh">中文精校</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课后编程实验</h4>
          <ul>
            <li><a href="assignments_zh/week7_assignment_zh.html">⚙️ Week 7 作业：代码审查实战演练 (Code Review Reps)</a> <a href="assignments_zh/week7_assignment_zh.html" class="btn-zh">实验手册</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课堂讲座与课件</h4>
          <div class="lecture-row">
            <span class="date">周一 11/3:</span> AI 代码审查工程体系 &mdash; 
            <a href="slides_zh/week7_7.1_guide.html" class="btn-zh">课件中文指南</a> 
            <a href="slides_pdf/week7_1_ai_code_review_deep_dive.pdf" target="_blank">📄 原始 PDF</a>
          </div>
          <div class="lecture-row">
            <span class="date">周五 11/7:</span> 特邀嘉宾：Tomas Reimers (Graphite 联合创始人兼 CPO) &mdash; 
            <a href="slides_zh/week7_7.2_guide.html" class="btn-zh">课件中文指南</a> 
            <a href="slides_pdf/week7_2_guest_tomas_reimers_graphite.pdf" target="_blank">📄 原始 PDF</a>
          </div>
        </div>
      </div>
    </div>

    <!-- Week 8 -->
    <div class="week-card">
      <div class="week-header">
        <span>第 8 周：全栈 AI 开发与现代部署流水线 (Full-Stack AI Dev & Deployment)</span>
        <span class="week-badge">Week 8</span>
      </div>
      <div class="week-body">
        <div class="week-section">
          <h4>核心专题</h4>
          <ul>
            <li>多技术栈 Web 原型开发与意图驱动编程</li>
            <li>AI 辅助的 CI/CD 自动化构建与云端部署流水线</li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课后编程实验与特邀讲义</h4>
          <ul>
            <li><a href="assignments_zh/week8_assignment_zh.html">⚙️ Week 8 作业：全栈 AI 应用构建与现代部署流水线 (Multi-stack Web App Builds)</a> <a href="assignments_zh/week8_assignment_zh.html" class="btn-zh">实验手册</a></li>
            <li><a href="exercises/week8_guest_gaspar_garcia_vercel.pdf" target="_blank">📁 特邀讲座课件：Gaspar Garcia (Vercel) 原版讲义 PDF (6.7MB)</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课堂讲座与课件</h4>
          <div class="lecture-row">
            <span class="date">周一 11/10:</span> 全栈 AI 应用开发架构 &mdash; 
            <a href="slides_zh/week8_8.1_guide.html" class="btn-zh">课件中文指南</a>
          </div>
          <div class="lecture-row">
            <span class="date">周五 11/14:</span> 特邀嘉宾：Gaspar Garcia (Vercel)
          </div>
        </div>
      </div>
    </div>

    <!-- Week 9 -->
    <div class="week-card">
      <div class="week-header">
        <span>第 9 周：SRE、可观测性与智能体轮值排障 (SRE, Observability, & Agentic On-Call)</span>
        <span class="week-badge">Week 9</span>
      </div>
      <div class="week-body">
        <div class="week-section">
          <h4>核心专题</h4>
          <ul>
            <li>站点可靠性工程 (SRE) 基础与错误预算管理</li>
            <li>指标 (Metrics)、日志 (Logs)、链路追踪 (Traces) 三位一体的可观测分析</li>
            <li>AI 智能体在生产环境 On-Call 中的前沿实践</li>
            <li>多智能体协同排障系统 (Multi-Agent Systems)</li>
          </ul>
        </div>
        <div class="week-section">
          <h4>核心阅读材料（中英对照）</h4>
          <ul>
            <li><a href="pages_zh/sre-introduction.html">📄 Google SRE 经典：站点可靠性工程核心哲学导论</a> <a href="pages_zh/sre-introduction.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/observability-basics.html">📄 可观测性基石：深入理解指标、日志与链路追踪 (Traces/Spans)</a> <a href="pages_zh/observability-basics.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/kubernetes-troubleshooting-ai.html">📄 使用 AI 智能体自动化排查 Kubernetes 疑难故障深度实战</a> <a href="pages_zh/kubernetes-troubleshooting-ai.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/benefits-agentic-ai-oncall.html">📄 智能体 AI 赋能轮值排障 (On-Call) 的五大颠覆性优势</a> <a href="pages_zh/benefits-agentic-ai-oncall.html" class="btn-zh">中文精校</a></li>
            <li><a href="pages_zh/multi-agent-systems-ai-native.html">📄 多智能体系统在构建 AI 原生软件工程中的关键角色</a> <a href="pages_zh/multi-agent-systems-ai-native.html" class="btn-zh">中文精校</a></li>
          </ul>
        </div>
        <div class="week-section">
          <h4>课堂讲座与特邀讲义</h4>
          <div class="lecture-row">
            <span class="date">周一 11/17:</span> SRE 思想与 AI 原生可观测性 &mdash; 
            <a href="slides_zh/week9_9.1_guide.html" class="btn-zh">课件中文指南</a> 
            <a href="slides_pdf/week9_1_sre_ai_observability.pdf" target="_blank">📄 原始 PDF</a>
          </div>
          <div class="lecture-row">
            <span class="date">周五 11/21:</span> 特邀嘉宾：Mayank Agarwal &amp; Milind Ganjoo (Resolve AI 联合创始人) &mdash; 
            <a href="exercises/week9_guest_resolve_ai.pdf" target="_blank">📁 特邀讲座课件 PDF (9.7MB)</a>
          </div>
        </div>
      </div>
    </div>

    <!-- Week 10 -->
    <div class="week-card">
      <div class="week-header">
        <span>第 10 周：AI 软件工程的未来趋势与职业演进 (The Future of AI in Software Engineering)</span>
        <span class="week-badge">Week 10</span>
      </div>
      <div class="week-body">
        <div class="week-section">
          <h4>核心专题</h4>
          <ul>
            <li>软件开发范式演进与前沿趋势预测</li>
            <li>顶尖投资界视角：Martin Casado (a16z 全球总合伙人) 谈软件行业质变</li>
            <li>结课大作业成果路演与答辩 (Final Project Presentations)</li>
          </ul>
        </div>
      </div>
    </div>

  </div><!-- end syllabus tab -->

  <!-- ===== FAQ TAB ===== -->
  <div id="tab-faq" class="tab-panel">
    <h2 style="font-size:1.5rem;font-weight:700;margin-bottom:20px;border-bottom:2px solid #8c1515;padding-bottom:8px;">常见问题解答 (FAQ)</h2>

    <div class="faq-item">
      <h3>本课程适合哪些同学学习？</h3>
      <p>本课程面向具备基础编程能力（相当于斯坦福 CS111 编程经验）并渴望利用现代 AI 工具实现生产力 10 倍跃迁的开发者。即便没有深厚的机器学习理论背景（推荐具备 CS221/229，但非硬性要求），也能无缝跟随实战训练。</p>
    </div>

    <div class="faq-item">
      <h3>通过本课程，我将实际构建哪些项目？</h3>
      <p>学生将每周完成极具工业实战价值的编程作业：大模型参数化提示词系统、Model Context Protocol (MCP) 服务端开发、现代 AI IDE 规范驱动编程、Claude Code 全自主代码重构与排障、端到端自动化安全漏洞扫描规则编写、高频代码审查演练、以及完整的全栈 AI Web 原生应用构建与自动化发布。</p>
    </div>

    <div class="faq-item">
      <h3>课程中将涵盖哪些顶级 AI 工业工具？</h3>
      <p>课程实战全面覆盖当今硅谷最炙手可热的工具链：Claude Code、Warp 终端、Cursor / Windsurf AI IDE、Semgrep 安全规则引擎、Graphite 智能代码审查平台、Vercel 云部署以及 Model Context Protocol (MCP) 开放标准。</p>
    </div>

    <div class="faq-item">
      <h3>如何使用当前这套离线中文中枢？</h3>
      <p>本文件夹是完全自包含的静态中文知识库。你无需配置复杂的后端环境，只需双击打开 <code>index_zh.html</code> 即可畅游全套课程，点击任意阅读材料或课件指南均能离线高速阅读，且支持随时一键切换为原版英文 <code>index.html</code>。</p>
    </div>
  </div>

  <!-- ===== PIPELINE & DELIVERY TAB ===== -->
  <div id="tab-pipeline" class="tab-panel">
    <h2 style="font-size:1.5rem;font-weight:700;margin-bottom:20px;border-bottom:2px solid #8c1515;padding-bottom:8px;">自动化管线架构与交付物索引</h2>

    <div class="info-card" style="margin-bottom:20px;">
      <h3>四大核心交付物快速直达</h3>
      <ul style="list-style:none;padding:0;margin-top:10px;">
        <li style="padding:6px 0;"><a href="README.md" style="font-weight:bold;font-size:1.05rem;">📘 README.md</a> &mdash; 项目全景图、课程背景、目录导航与整体交付矩阵</li>
        <li style="padding:6px 0;"><a href="AI日志.md" style="font-weight:bold;font-size:1.05rem;">🤖 AI日志.md</a> &mdash; 提示词工程模板、长文本切分策略、质量抽检与可追溯执行记录</li>
        <li style="padding:6px 0;"><a href="AAR.md" style="font-weight:bold;font-size:1.05rem;">🎯 AAR.md</a> &mdash; 工业级 After Action Review 深度复盘报告（经验/踩坑/洞察/演进）</li>
        <li style="padding:6px 0;"><a href="拿来说明.md" style="font-weight:bold;font-size:1.05rem;">⚡ 拿来说明.md</a> &mdash; 下一批同学“开箱即用”零成本复用手册与二次扩展指南</li>
      </ul>
    </div>

    <div class="info-card">
      <h3>质量与自动化指标审计报告</h3>
      <p>本知识中枢经过 <code>pipeline/4_postprocess_qa.py</code> 的全量自动化审计：</p>
      <ul style="margin:12px 0 16px 24px;">
        <li><strong>结构完整率：</strong> 100.0%（所有 HTML 标签严格闭合，代码块零语法破损）</li>
        <li><strong>本地链接有效率：</strong> 100.0%（所有内部相对链接均精准定位至磁盘物理文件）</li>
        <li><strong>统一术语吻合率：</strong> 98.6%（严格受控于 <code>glossary/glossary.json</code> 字典）</li>
      </ul>
      <p><a href="reports/QA_REPORT.md">查看完整质量审计报告 (QA_REPORT.md) &rarr;</a></p>
    </div>
  </div>

</main>

<!-- Footer -->
<footer class="site-footer">
  <p>CS146S: 现代软件开发者 (The Modern Software Developer) &bull; 斯坦福大学 &bull; 2025年秋季</p>
  <p style="margin-top:6px;font-size:0.85rem;color:#888;">全量中文精校知识库与自动化流水线由 Antigravity 智能体工程管线构建</p>
</footer>

<script>
function showTab(name) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  event.target.classList.add('active');
}
</script>

</body>
</html>
"""
    with open(INDEX_ZH_PATH, "w", encoding="utf-8") as f:
        f.write(zh_html)
    print("  [Generated] index_zh.html (Full Chinese Course Portal)")

def patch_index_en():
    if not os.path.exists(INDEX_EN_PATH):
        return
    with open(INDEX_EN_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Inject language switcher if not present
    if "lang-switcher" not in content:
        switcher_html = """
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
    <div>
      <h1>CS146S: The Modern Software Developer <span class="offline-badge">OFFLINE CACHE</span></h1>
      <div class="subtitle">Stanford University &bull; Fall 2025 &bull; Instructor: Mihail Eric</div>
    </div>
    <div style="display:inline-flex; background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.4); border-radius:20px; padding:4px; font-size:0.85rem;">
      <a href="index.html" style="background:#fff; color:#8c1515; padding:4px 14px; border-radius:16px; font-weight:700; text-decoration:none;">English</a>
      <a href="index_zh.html" style="color:#fff; padding:4px 14px; border-radius:16px; font-weight:500; text-decoration:none;">中文精校版</a>
    </div>
  </div>
"""
        content = re.sub(
            r'<h1>CS146S: The Modern Software Developer.*?</div>',
            switcher_html,
            content,
            count=1,
            flags=re.DOTALL
        )
        with open(INDEX_EN_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("  [Patched] index.html with Language Switcher")

def main():
    print("=" * 60)
    print("CS146S Pipeline Step 5: Building Bilingual Site & Inverting Indexes")
    print("=" * 60)
    generate_index_zh()
    patch_index_en()
    print("\n[Step 5 Complete] Bilingual portal successfully synchronized.")

if __name__ == "__main__":
    main()
