import os
import sys
import argparse
import subprocess
import time

def print_banner():
    print("""
===================================================================
  Stanford CS146S / Vibe Coding Course Translation Pipeline
  Phase 1 - Automated Information Retrieval, Translation & Publish
===================================================================
""")

def run_step(step_name, cmd, cwd=None):
    print(f"\n>>> [Pipeline Step] {step_name}...")
    start_time = time.time()
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    res = subprocess.run(
        [sys.executable] + cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        env=env
    )
    elapsed = time.time() - start_time
    if res.returncode != 0:
        print(f"[ERROR] Step '{step_name}' failed with returncode {res.returncode}:")
        if res.stderr:
            print(res.stderr)
        return False
    if res.stdout:
        print(res.stdout.strip())
    print(f"--- Completed in {elapsed:.2f}s ---")
    return True

def main():
    parser = argparse.ArgumentParser(description="Master Execution Pipeline for CS146S Course Materials")
    parser.add_argument('--all', action='store_true', default=True, help="Run full pipeline end-to-end")
    parser.add_argument('--source', type=str, default=None, help="Custom course package path (for portability testing)")
    parser.add_argument('--qa-only', action='store_true', help="Run only QA audit and glossary checks")
    parser.add_argument('--rebuild-site', action='store_true', help="Rebuild static documentation site")
    parser.add_argument('--serve', type=int, nargs='?', const=8080, default=None, help="Serve the static documentation site")

    args = parser.parse_args()
    print_banner()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pipeline_dir = os.path.join(base_dir, 'pipeline')

    if args.serve:
        site_dir = os.path.join(base_dir, 'site')
        print(f"Serving site at http://localhost:{args.serve} from {site_dir} (Press Ctrl+C to stop)...")
        from http.server import HTTPServer, SimpleHTTPRequestHandler
        import functools
        handler = functools.partial(SimpleHTTPRequestHandler, directory=site_dir)
        httpd = HTTPServer(('localhost', args.serve), handler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
        return

    if args.qa_only:
        run_step("Quality Assurance Audit", ["qa_checker.py"], cwd=pipeline_dir)
        return

    if args.rebuild_site:
        run_step("Build Static Site", ["site_builder.py"], cwd=pipeline_dir)
        return

    # Full Pipeline
    print(f"Starting End-to-End Pipeline Execution in: {base_dir}")

    # 1. Fetch & Verify Integrity
    fetch_cmd = ["fetcher.py"]
    if args.source:
        fetch_cmd += ["--source", args.source]
    if not run_step("1. Source Ingestion & Integrity Verification", fetch_cmd, cwd=pipeline_dir):
        sys.exit(1)

    # 2. Glossary Generation & Rule Compilation
    if not run_step("2. Glossary Compilation & Constraint Injection", ["glossary_manager.py"], cwd=pipeline_dir):
        sys.exit(1)

    # 3. Content Extraction & Translation Synthesis
    if not run_step("3.1 Syllabus Structured Translation", ["generate_syllabus.py"], cwd=pipeline_dir):
        sys.exit(1)
    if not run_step("3.2 Vibe Coding Playbook Blueprint Generation", ["generate_playbook.py"], cwd=pipeline_dir):
        sys.exit(1)
    if not run_step("3.3 Core Research Papers Full-Text Translation", ["generate_papers.py"], cwd=pipeline_dir):
        sys.exit(1)
    if not run_step("3.4 Reading Articles Batch Translation Engine", ["translate_articles.py"], cwd=pipeline_dir):
        sys.exit(1)

    # 4. QA Audit & Strict Compliance Verification
    if not run_step("4. Quality Assurance & Consistency Verification", ["qa_checker.py"], cwd=pipeline_dir):
        sys.exit(1)

    # 5. Static Site Compilation & Publishing
    if not run_step("5. Documentation Site Compilation", ["site_builder.py"], cwd=pipeline_dir):
        sys.exit(1)

    print("\n===================================================================")
    print("  SUCCESS: Full Pipeline Executed Successfully!")
    print(f"  - Translated Materials: {os.path.join(base_dir, 'translated')}")
    print(f"  - QA Audit Report:      {os.path.join(base_dir, 'reports', 'QA_REPORT.md')}")
    print(f"  - Standalone Web Site:  {os.path.join(base_dir, 'site', 'index.html')}")
    print("===================================================================\n")

if __name__ == '__main__':
    main()
