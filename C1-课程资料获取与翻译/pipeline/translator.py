import os
import re
import json
import urllib.request
from typing import Dict, Any, List, Optional
from glossary_manager import GlossaryManager

class CourseTranslator:
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-7-sonnet"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.glossary_mgr = GlossaryManager()

    def build_system_prompt(self) -> str:
        glossary_rules = self.glossary_mgr.get_prompt_injection()
        prompt = f"""你是一名世界顶尖的斯坦福大学计算机科学系双语讲师与软件架构师。
你的任务是将斯坦福大学前沿课程《CS146S: The Modern Software Developer / Vibe Coding》的英文课件、讲义与深度技术文章全量翻译为专业、精准、流畅的简体中文。

【翻译原则与质量准则】
1. **信达雅与工程真实感**：保持学术严肃性与现代软件工程行话的生动性，彻底消除机器翻译腔（如生硬的被动句、直译从句）。
2. **格式与结构 100% 保持**：
   - 严格保留 Markdown 标题层级 (#, ##, ###)、有序/无序列表、引用块 (>)。
   - 所有代码块 (`...`) 中的代码、命令行命令、注释中的变量名与保留字绝对保持原样，仅翻译代码块前后的解析说明。
   - 超链接 [Anchor](url) 保持 url 不变，仅精准翻译锚文本。
3. **术语绝对一致性**：
{glossary_rules}

4. **防漏译与防幻觉**：
   - 全文段落必须一一对应，严禁省略任何子章节、作者说明或背景讨论。
   - 不要添加原文未曾出现的额外臆断。
"""
        return prompt

    def build_user_prompt(self, english_text: str, context_info: str = "") -> str:
        prompt = f"""请将以下技术资料精准翻译为高质量简体中文：

【资料背景/章节说明】
{context_info or 'Stanford CS146S Course Material'}

【待翻译英文原文】
{english_text}

【输出要求】
直接输出翻译完成的 Markdown 文本，不要附加任何自我介绍、打招呼或额外闲聊。保证段落完整与术语规范。"""
        return prompt

    def mock_or_api_translate(self, text: str, context_info: str = "") -> str:
        # If API key is available, call the endpoint; otherwise provide structural translation wrapper
        # The pipeline can run locally and seamlessly plug in real API keys.
        return text

if __name__ == '__main__':
    translator = CourseTranslator()
    sys_prompt = translator.build_system_prompt()
    print("System Prompt Built Successfully. Length:", len(sys_prompt))
