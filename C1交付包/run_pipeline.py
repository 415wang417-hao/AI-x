#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS146S Master Pipeline Orchestrator (主控流水线 CLI)
Usage:
  python run_pipeline.py --step all
  python run_pipeline.py --step fetch
  python run_pipeline.py --step extract
  python run_pipeline.py --step translate
  python run_pipeline.py --step qa
  python run_pipeline.py --step build
"""

import os
import sys
import time
import argparse
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINE_DIR = os.path.join(BASE_DIR, "pipeline")

STEPS = [
    ("fetch", "1_fetch.py", "多源数据采集与缺失补全 (GitHub / Google Slides / Drive)"),
    ("extract", "2_extract_chunk.py", "长文档语义解析与智能分块 (HTML / PDF)"),
    ("translate", "3_translate.py", "高质量机器翻译与术语库注入 (HTML / Slides / Labs)"),
    ("translate_pdfs", "translate_pdfs.py", "核心旗舰 PDF 文献深度翻译 (Codex / Claude Code / Code Review)"),
    ("qa", "4_postprocess_qa.py", "自动化质量审计与格式完整度校验 (QA Check)"),
    ("build", "5_build_site.py", "静态双语课程门户构建与索引互联 (Site Generation)")
]

def run_step(script_name, description):
    script_path = os.path.join(PIPELINE_DIR, script_name)
    if not os.path.exists(script_path):
        print(f"[Error] Script not found: {script_path}")
        return False

    print("\n" + "=" * 70)
    print(f">> 执行阶段: {description}")
    print(f">> 脚本路径: pipeline/{script_name}")
    print("=" * 70)

    start_time = time.time()
    result = subprocess.run([sys.executable, script_path], cwd=BASE_DIR)
    elapsed = time.time() - start_time

    if result.returncode == 0:
        print(f">> 阶段完成 [成功] - 耗时 {elapsed:.2f} 秒\n")
        return True
    else:
        print(f">> 阶段失败 [退出码 {result.returncode}] - 耗时 {elapsed:.2f} 秒\n")
        return False

def main():
    parser = argparse.ArgumentParser(description="CS146S 现代软件开发者 (Vibe Coding) 端到端自动化管线")
    parser.add_argument(
        "--step",
        choices=["all", "fetch", "extract", "translate", "qa", "build"],
        default="all",
        help="指定执行的管线阶段 (默认: all 执行全部阶段)"
    )
    args = parser.parse_args()

    print("\n" + "#" * 70)
    print("# CS146S: The Modern Software Developer (Stanford Vibe Coding)")
    print("# 全量信息获取、批量翻译与双语知识中枢构建流水线")
    print("#" * 70)

    total_start = time.time()

    if args.step == "all":
        for step_id, script, desc in STEPS:
            success = run_step(script, desc)
            if not success:
                print(f"[Pipeline Interrupted] 阶段 {step_id} 遇到错误，流水线终止。")
                sys.exit(1)
    else:
        for step_id, script, desc in STEPS:
            if step_id.startswith(args.step):
                success = run_step(script, desc)
                if not success:
                    sys.exit(1)

    total_elapsed = time.time() - total_start
    print("\n" + "#" * 70)
    print(f"# 全部指定阶段执行完毕！总计耗时: {total_elapsed:.2f} 秒")
    print(f"# 中文门户主页: {os.path.join(BASE_DIR, 'index_zh.html')}")
    print(f"# 英文原版主页: {os.path.join(BASE_DIR, 'index.html')}")
    print("#" * 70 + "\n")

if __name__ == "__main__":
    main()
