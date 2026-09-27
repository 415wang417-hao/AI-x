import os
import re
import json
from typing import Dict, Any, List
from glossary_manager import GlossaryManager

class QualityAssuranceChecker:
    def __init__(self, translated_dir: str = None, reports_dir: str = None):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.translated_dir = translated_dir or os.path.join(base, 'translated')
        self.reports_dir = reports_dir or os.path.join(base, 'reports')
        self.glossary_mgr = GlossaryManager()
        os.makedirs(self.reports_dir, exist_ok=True)

    def check_file_quality(self, filepath: str) -> Dict[str, Any]:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        issues = []
        char_count = len(content)

        # 1. Empty or nearly empty file
        if char_count < 100:
            issues.append({"type": "EMPTY_OR_TOO_SHORT", "severity": "HIGH", "detail": f"File length is only {char_count} chars"})

        # 2. Code fence completeness
        fence_count = content.count('`')
        if fence_count % 2 != 0:
            issues.append({"type": "UNCLOSED_CODE_BLOCK", "severity": "MEDIUM", "detail": f"Odd number of code fences: {fence_count}"})

        # 3. Chinese character ratio check (catching untranslated files)
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        chinese_ratio = (chinese_chars / char_count) if char_count > 0 else 0.0

        if chinese_ratio < 0.20 and char_count > 200:
            issues.append({
                "type": "LOW_CHINESE_RATIO",
                "severity": "HIGH",
                "detail": f"Chinese character ratio is {chinese_ratio:.1%}, possible untranslated English text"
            })

        # 4. Large untranslated English paragraphs (> 80 consecutive English words outside code blocks)
        non_code_text = re.sub(r'`.*?`', '', content, flags=re.DOTALL)
        english_paragraphs = re.findall(r'(?:\n\n|\r\n\r\n)([A-Za-z0-9\s,\.\(\)\"\'\:\;\?\!\-]{250,})(?:\n\n|\r\n\r\n)', non_code_text)
        if english_paragraphs:
            issues.append({
                "type": "UNTRANSLATED_PARAGRAPHS",
                "severity": "HIGH",
                "count": len(english_paragraphs),
                "sample": english_paragraphs[0][:120].strip() + "..."
            })

        # 5. Glossary and forbidden terms check
        glossary_res = self.glossary_mgr.audit_text(content)
        if glossary_res['violations']:
            for v in glossary_res['violations']:
                issues.append({
                    "type": "FORBIDDEN_TERM",
                    "severity": "HIGH",
                    "detail": f"Found forbidden term '{v['forbidden_word']}' (expected '{v['expected']}')"
                })

        return {
            "file": os.path.basename(filepath),
            "char_count": char_count,
            "chinese_chars": chinese_chars,
            "chinese_ratio": round(chinese_ratio, 3),
            "issues_count": len(issues),
            "issues": issues,
            "passed": len(issues) == 0
        }

    def run_full_audit(self) -> Dict[str, Any]:
        all_results = []
        files_scanned = 0
        passed_files = 0
        total_issues = 0

        for root, _, files in os.walk(self.translated_dir):
            for file in sorted(files):
                if file.endswith(('.md', '.html')):
                    files_scanned += 1
                    fp = os.path.join(root, file)
                    rel = os.path.relpath(fp, self.translated_dir)
                    res = self.check_file_quality(fp)
                    res['relative_path'] = rel
                    all_results.append(res)
                    if res['passed']:
                        passed_files += 1
                    total_issues += res['issues_count']

        pass_rate = (passed_files / files_scanned * 100) if files_scanned > 0 else 0.0

        summary = {
            "total_files": files_scanned,
            "passed_files": passed_files,
            "failed_files": files_scanned - passed_files,
            "pass_rate_pct": round(pass_rate, 2),
            "total_issues": total_issues,
            "status": "PASS" if total_issues == 0 and files_scanned > 0 else ("WARN" if pass_rate >= 80 else "FAIL"),
            "details": all_results
        }

        # Save JSON report
        json_path = os.path.join(self.reports_dir, 'qa_report.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        # Generate Markdown QA Report
        md_lines = [
            "# CS146S 翻译质量自动化抽检与审计报告 (QA Audit Report)",
            "",
            f"> 生成时间: 2026-09-26 | 审计引擎: QualityAssuranceChecker v1.0 | 综合状态: **{summary['status']}**",
            "",
            "## 1. 核心质量指标",
            "",
            f"- **已扫描文件总数**: {summary['total_files']} 篇",
            f"- **质量全合规文件数**: {summary['passed_files']} 篇",
            f"- **合规通过率**: {summary['pass_rate_pct']}%",
            f"- **检测出潜在问题总数**: {summary['total_issues']} 项",
            "",
            "## 2. 详细文件审查矩阵",
            "",
            "| 文件名 | 字符总数 | 中文占比 | 状态 | 检测详情 |",
            "| :--- | :---: | :---: | :---: | :--- |"
        ]

        for r in all_results:
            st = "PASS" if r['passed'] else "WARN"
            issues_desc = "; ".join(f"{iss['type']}: {iss.get('detail', '')}" for iss in r['issues']) if r['issues'] else "无缺陷，符合规范"
            md_lines.append(f"| {r['relative_path']} | {r['char_count']} | {r['chinese_ratio']:.1%} | {st} | {issues_desc} |")

        md_lines.extend([
            "",
            "---",
            "*注：质检规则涵盖：① 字符数与非空校验；② 代码块闭合完整度；③ 中文密度阈值；④ 大段英文漏译；⑤ 强制术语一致性与生硬禁用词排查。*"
        ])

        md_path = os.path.join(self.reports_dir, 'QA_REPORT.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_lines))

        print(f"[QA] Audit completed. Pass Rate: {summary['pass_rate_pct']}%. Report saved to {md_path}")
        return summary

if __name__ == '__main__':
    checker = QualityAssuranceChecker()
    checker.run_full_audit()
