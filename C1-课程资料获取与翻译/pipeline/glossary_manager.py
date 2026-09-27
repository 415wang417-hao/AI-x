import os
import json
import re
from typing import List, Dict, Any, Tuple

DEFAULT_GLOSSARY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'glossary.json')
DEFAULT_MD_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'glossary.md')

class GlossaryManager:
    def __init__(self, glossary_path: str = None):
        self.glossary_path = glossary_path or DEFAULT_GLOSSARY_PATH
        self.terms: List[Dict[str, Any]] = self.load_glossary()

    def load_glossary(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.glossary_path):
            raise FileNotFoundError(f"Glossary file not found: {self.glossary_path}")
        with open(self.glossary_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate_markdown(self, output_path: str = None) -> str:
        out = output_path or DEFAULT_MD_PATH
        lines = [
            "# Stanford CS146S / Vibe Coding 课程核心双语技术术语规范表",
            "",
            f"> 本术语表共收录 **{len(self.terms)}** 项核心概念，用于驱动全套自动化翻译管线、Prompt 上下文注入约束、以及全文一致性校验。",
            "",
            "| 序号 | 英文术语 (Source Term) | 规范中文译名 (Standard Translation) | 领域类别 (Category) | 核心概念定义与规范说明 | 禁用/生硬译名 (Forbidden) |",
            "| :---: | :--- | :--- | :--- | :--- | :--- |"
        ]
        for idx, item in enumerate(self.terms, 1):
            term = item['term']
            trans = item['translation']
            cat = item.get('category', 'General')
            desc = item.get('description', '')
            forbidden = '、'.join(item.get('forbidden', [])) if item.get('forbidden') else '-'
            lines.append(f"| {idx} | **{term}** | `{trans}` | {cat} | {desc} | {forbidden} |")

        lines.extend([
            "",
            "---",
            "*版本: 1.0 (全量冻结) | 校验模式: 强制一致性合规审计 (Strict Mode)*"
        ])
        content = "\n".join(lines) + "\n"
        with open(out, 'w', encoding='utf-8') as f:
            f.write(content)
        return out

    def get_prompt_injection(self) -> str:
        lines = [
            "【强制术语表规范 (Glossary Constraints)】",
            "在翻译以下文本时，必须严格遵守以下关键术语的中文统一译法，严禁出现右侧的生硬禁译词汇："
        ]
        for item in self.terms:
            forb = f" (严禁使用: {'/'.join(item['forbidden'])})" if item.get('forbidden') else ""
            lines.append(f"- {item['term']} => {item['translation']}{forb}")
        return "\n".join(lines)

    def audit_text(self, text: str) -> Dict[str, Any]:
        violations = []
        matches = []
        
        # Mask out valid standard translations to avoid false positive substring matches
        sanitized_text = text
        for item in self.terms:
            trans = item['translation']
            sanitized_text = sanitized_text.replace(trans, " __STANDARD_TERM__ ")
            core_trans = trans.split('(')[0].split('/')[0].strip()
            if len(core_trans) >= 2:
                sanitized_text = sanitized_text.replace(core_trans, " __STANDARD_TERM__ ")

        for item in self.terms:
            # Check forbidden words in sanitized text
            for f_word in item.get('forbidden', []):
                if f_word in sanitized_text:
                    count = sanitized_text.count(f_word)
                    violations.append({
                        "term": item['term'],
                        "forbidden_word": f_word,
                        "expected": item['translation'],
                        "count": count
                    })
            trans_core = item['translation'].split('(')[0].split('/')[0].strip()
            if trans_core in text:
                matches.append(item['term'])

        total_checked = len(self.terms)
        violation_count = sum(v['count'] for v in violations)
        compliance_score = max(0.0, 100.0 - (violation_count * 5.0))
        return {
            "total_terms": total_checked,
            "matched_terms": len(set(matches)),
            "violations": violations,
            "violation_instances": violation_count,
            "compliance_score": compliance_score,
            "is_compliant": len(violations) == 0
        }

    def audit_directory(self, dir_path: str) -> Dict[str, Any]:
        results = {}
        total_violations = 0
        file_count = 0
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(('.md', '.html', '.txt')):
                    file_count += 1
                    fp = os.path.join(root, file)
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    audit = self.audit_text(content)
                    if audit['violations']:
                        total_violations += audit['violation_instances']
                        results[os.path.relpath(fp, dir_path)] = audit['violations']
        return {
            "files_scanned": file_count,
            "total_violations": total_violations,
            "violating_files": results,
            "overall_status": "PASS" if total_violations == 0 else "FAIL"
        }

if __name__ == '__main__':
    import sys
    gm = GlossaryManager()
    md_file = gm.generate_markdown()
    print(f"Glossary Markdown updated: {md_file}")
    if len(sys.argv) > 1 and sys.argv[1] == '--audit':
        target = sys.argv[2] if len(sys.argv) > 2 else '.'
        res = gm.audit_directory(target)
        print(json.dumps(res, indent=2, ensure_ascii=False))
