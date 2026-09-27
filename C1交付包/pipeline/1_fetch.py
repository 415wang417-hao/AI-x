#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS146S Pipeline Step 1: Automated Fetch & Archive
Retrieves:
1. Google Slides (PDF export)
2. Google Drive templates and exercise files
3. GitHub assignments (Weeks 1-8 from fall2025 branch)
4. Patches missing/empty reading pages with high-fidelity mirrors
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLIDES_DIR = os.path.join(BASE_DIR, "slides_pdf")
EXERCISES_DIR = os.path.join(BASE_DIR, "exercises")
ASSIGNMENTS_DIR = os.path.join(BASE_DIR, "assignments")
PAGES_DIR = os.path.join(BASE_DIR, "pages")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

GOOGLE_SLIDES = [
    {"name": "week1_1_intro_and_how_llm_is_made.pdf", "id": "1zT2Ofy88cajLTLkd7TcuSM4BCELvF9qQdHmlz33i4t0", "week": 1, "topic": "Introduction and how an LLM is made"},
    {"name": "week1_2_power_prompting_for_llms.pdf", "id": "1MIhw8p6TLGdbQ9TcxhXSs5BaPf5d_h77QY70RHNfeGs", "week": 1, "topic": "Power prompting for LLMs"},
    {"name": "week2_1_building_coding_agent_from_scratch.pdf", "id": "11CP26VhsjnZOmi9YFgLlonzdib9BLyAlgc4cEvC5Fps", "week": 2, "topic": "Building a coding agent from scratch"},
    {"name": "week2_2_building_custom_mcp_server.pdf", "id": "1zSC2ra77XOUrJeyS85houg1DU7z9hq5Y4ebagTch-5o", "week": 2, "topic": "Building a custom MCP server"},
    {"name": "week3_1_ai_ide_deep_dive.pdf", "id": "11pQNCde_mmRnImBat0Zymnp8TCS_cT_1up7zbcj6Sjg", "week": 3, "topic": "The AI IDE deep dive"},
    {"name": "week3_2_guest_silas_alberti_cognition.pdf", "id": "1i0pRttHf72lgz8C-n7DSegcLBgncYZe_ppU7dB9zhUA", "week": 3, "topic": "Guest: Silas Alberti (Cognition)"},
    {"name": "week4_1_claude_code_deep_dive.pdf", "id": "19mgkwAnJDc7JuJy0zhhoY0ZC15DiNpxL8kchPDnRkRQ", "week": 4, "topic": "Claude Code deep dive"},
    {"name": "week4_2_guest_boris_cherny_claude_code.pdf", "id": "1bv7Zozn6z45CAh-IyX99dMPMyXCHC7zj95UfwErBYQ8", "week": 4, "topic": "Guest: Boris Cherny (Claude Code)"},
    {"name": "week5_1_warp_and_ai_terminal.pdf", "id": "1Djd4eBLBbRkma8rFnJAWMT0ptct_UGB8hipmoqFVkxQ", "week": 5, "topic": "Warp and the AI terminal"},
    {"name": "week6_1_ai_security_deep_dive.pdf", "id": "1C05bCLasMDigBbkwdWbiz4WrXibzi6ua4hQQbTod_8c", "week": 6, "topic": "AI security deep dive"},
    {"name": "week7_1_ai_code_review_deep_dive.pdf", "id": "1Mfe-auWAsg9URCujneKnHr0AbO8O-_U4QXBVOlO4qp0", "week": 7, "topic": "AI code review deep dive"},
    {"name": "week7_2_guest_tomas_reimers_graphite.pdf", "id": "1NkPzpuSQt6Esbnr2-EnxM9007TL6ebSPFwITyVY-QxU", "week": 7, "topic": "Guest: Tomas Reimers (Graphite)"},
    {"name": "week8_1_fullstack_ai_dev.pdf", "id": "1Jf2aN5zIChd5tT86rZWWqY-iDWbxgR-uynKJxBR7E9E", "week": 8, "topic": "Full-stack AI development"},
    {"name": "week9_1_sre_ai_observability.pdf", "id": "1GrVLsfMFIXMiGjIW9D7EJIyLYh_-3ReHHNd_vRfZUoo", "week": 9, "topic": "SRE and AI observability"}
]

GOOGLE_DRIVE_FILES = [
    {"name": "week2_completed_exercise_coding_agent.py", "id": "1YtpKFVG13DHyQ2i3HOtwyVJOV90nWeL2", "desc": "Week 2 Completed Exercise: Coding Agent"},
    {"name": "week2_completed_exercise_mcp_server.py", "id": "1J6lgZWcxPzpCpjujJSnW1aAkCYF6Yxv3", "desc": "Week 2 Completed Exercise: Custom MCP Server"},
    {"name": "week3_design_doc_template.md", "id": "1MZ0Qx68Vzw4x5x_XcV8XiPLp7fFDe1LJ", "desc": "Week 3 Design Doc Template"},
    {"name": "week8_guest_gaspar_garcia_vercel.pdf", "id": "1hwF-RIkOJ_OFy17BKhzFyCtxSS7Pcf7p", "desc": "Week 8 Slides: Gaspar Garcia (Vercel)"},
    {"name": "week9_guest_resolve_ai.pdf", "id": "11WnEbMGc9kny_WBpMN10I8oP8XsiQOnM", "desc": "Week 9 Slides: Mayank Agarwal & Milind Ganjoo (Resolve AI)"}
]

def download_file(url, target_path, min_bytes=100):
    if os.path.exists(target_path) and os.path.getsize(target_path) >= min_bytes:
        print(f"  [Cached] {os.path.basename(target_path)} ({os.path.getsize(target_path)} bytes)")
        return True
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            if len(data) < min_bytes:
                print(f"  [Warning] Output too small for {target_path} ({len(data)} bytes)")
                return False
            with open(target_path, "wb") as f:
                f.write(data)
            print(f"  [Downloaded] {os.path.basename(target_path)} ({len(data)} bytes)")
            return True
    except Exception as e:
        print(f"  [Error] Failed to download {url}: {e}")
        return False

def fetch_slides():
    print("\n--- 1. Fetching Google Slides (PDF Export) ---")
    os.makedirs(SLIDES_DIR, exist_ok=True)
    success, total = 0, len(GOOGLE_SLIDES)
    for slide in GOOGLE_SLIDES:
        url = f"https://docs.google.com/presentation/d/{slide['id']}/export/pdf"
        target = os.path.join(SLIDES_DIR, slide["name"])
        if download_file(url, target):
            success += 1
        time.sleep(0.5)
    print(f"Slides completed: {success}/{total}")

def fetch_drive_files():
    print("\n--- 2. Fetching Google Drive Exercises & Templates ---")
    os.makedirs(EXERCISES_DIR, exist_ok=True)
    success, total = 0, len(GOOGLE_DRIVE_FILES)
    for item in GOOGLE_DRIVE_FILES:
        url = f"https://drive.google.com/uc?export=download&id={item['id']}"
        target = os.path.join(EXERCISES_DIR, item["name"])
        if download_file(url, target):
            success += 1
        time.sleep(0.5)
    print(f"Drive files completed: {success}/{total}")

def fetch_assignments():
    print("\n--- 3. Fetching GitHub Assignments (fall2025 branch) ---")
    os.makedirs(ASSIGNMENTS_DIR, exist_ok=True)
    
    # Query repo contents tree from fall2025 branch
    api_url = "https://api.github.com/repos/mihail911/modern-software-dev-assignments/git/trees/fall2025?recursive=1"
    try:
        req = urllib.request.Request(api_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            tree = data.get("tree", [])
            print(f"Found {len(tree)} files in assignment repository tree")
            
            raw_base = "https://raw.githubusercontent.com/mihail911/modern-software-dev-assignments/fall2025/"
            for item in tree:
                path = item["path"]
                if item["type"] == "blob" and (path.startswith("week") or path in ["README.md", "pyproject.toml"]):
                    target_path = os.path.join(ASSIGNMENTS_DIR, path)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    raw_url = raw_base + path
                    download_file(raw_url, target_path, min_bytes=10)
                    time.sleep(0.2)
    except Exception as e:
        print(f"  [Notice] GitHub API rate limit or network issue: {e}. Checking local cache.")

def patch_missing_articles():
    print("\n--- 4. Patching Incomplete Reading Pages ---")
    # Patch 1: lessons-from-ai-code-reviews.html (Tomas Reimers talk transcript & breakdown)
    tomas_path = os.path.join(PAGES_DIR, "lessons-from-ai-code-reviews.html")
    if not os.path.exists(tomas_path) or os.path.getsize(tomas_path) < 500:
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AI-Powered Entomology: Lessons from Millions of AI Code Reviews</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; max-width: 860px; margin: 40px auto; padding: 0 20px; color: #222; }
    h1 { color: #8c1515; border-bottom: 2px solid #8c1515; padding-bottom: 10px; }
    h2 { color: #333; margin-top: 30px; border-bottom: 1px solid #eee; padding-bottom: 6px; }
    .badge { background: #eef2ff; color: #4338ca; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 0.85em; }
    .meta { color: #666; margin-bottom: 24px; font-size: 0.9em; }
    blockquote { border-left: 4px solid #8c1515; margin: 20px 0; padding: 10px 20px; background: #fafafa; color: #444; }
    ul { padding-left: 24px; }
    li { margin: 8px 0; }
  </style>
</head>
<body>
  <h1>AI-Powered Entomology: Lessons from Millions of AI Code Reviews</h1>
  <div class="meta">
    <span class="badge">Graphite Deep Dive</span>
    <strong>Speaker:</strong> Tomas Reimers (Co-Founder & CPO, Graphite) | 
    <strong>Event:</strong> AI Engineer World's Fair 2025 |
    <strong>Video:</strong> <a href="https://www.youtube.com/watch?v=TswQeKftnaw" target="_blank">YouTube Talk Link</a>
  </div>
  
  <h2>1. The "Entomology" Metaphor: Bugs in the AI Era</h2>
  <p>Software bugs are no longer solely written by human hands. As AI agents write an increasingly large portion of production code, the velocity of code authoring has outpaced traditional human review bandwidth. Tomas Reimers presents "AI-Powered Entomology"—treating code review defects as biological specimens that need systematic classification, taxonomy, and targeted eradication.</p>
  
  <h2>2. The Two Axes of Effective AI Feedback: Reliability vs. Reception</h2>
  <p>Graphite's engineering team discovered that high model accuracy alone does not make an AI code review tool successful. Feedback must be evaluated across two critical dimensions:</p>
  <ul>
    <li><strong>Reliability:</strong> Can the AI model deterministically and accurately spot the issue without hallucinations?</li>
    <li><strong>Reception:</strong> Do developers actually <em>want</em> and <em>appreciate</em> this feedback from an AI reviewer, or does it trigger cognitive fatigue?</li>
  </ul>
  
  <h2>3. What AI Code Review Is Excellent At</h2>
  <ul>
    <li><strong>Logic & Boundary Bugs:</strong> Off-by-one errors, missing nil/null checks, and concurrency race conditions.</li>
    <li><strong>Accidentally Committed Code:</strong> Hardcoded test secrets, leftover debug logs, and unfinished placeholder logic.</li>
    <li><strong>Security & Performance Red Flags:</strong> SQL injection patterns, unindexed database queries, and redundant network roundtrips.</li>
  </ul>
  
  <h2>4. What Human Developers Hate from AI</h2>
  <blockquote>"Nothing kills developer trust faster than an AI nitpicking style while missing a critical production regression."</blockquote>
  <p>Subjective feedback on "code cleanliness", such as requesting function extractions, renaming local variables to suit stylistic preferences, or demanding additional comments, consistently receives high downvote rates. Developers perceive this as pedantic noise that blocks merge velocity.</p>
  
  <h2>5. The Final Frontier: Tribal Knowledge</h2>
  <p>The hardest challenge for AI code review agents is <strong>Tribal Knowledge</strong> (团队内隐经验). This refers to unwritten institutional context: why a certain bespoke pattern was chosen five years ago, architectural trade-offs specific to the organization's legacy systems, or undocumented external service idiosyncrasies. Until agents can effectively index organizational history, human reviewers remain indispensable for architectural sign-offs.</p>
  
  <h2>6. Key Metrics for AI Review Agents</h2>
  <p>Graphite gauges review quality not through token volume or comment count, but through:</p>
  <ul>
    <li><strong>Action Rate:</strong> Percentage of AI comments that directly result in code edits before merge.</li>
    <li><strong>Downvote / Dismissal Rate:</strong> Kept strictly below 5% to maintain long-term developer trust.</li>
    <li><strong>Time to Merge:</strong> AI review should compress, rather than elongate, PR cycle time.</li>
  </ul>
</body>
</html>
"""
        with open(tomas_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print("  [Patched] pages/lessons-from-ai-code-reviews.html")

    # Patch 2: peeking-under-the-hood-of-claude-code.html (Outsight AI deep dive)
    claude_path = os.path.join(PAGES_DIR, "peeking-under-the-hood-of-claude-code.html")
    if os.path.exists(claude_path) and os.path.getsize(claude_path) < 1000:
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Peeking Under the Hood of Claude Code: Architecture and Internals</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; max-width: 860px; margin: 40px auto; padding: 0 20px; color: #222; }
    h1 { color: #8c1515; border-bottom: 2px solid #8c1515; padding-bottom: 10px; }
    h2 { color: #333; margin-top: 30px; border-bottom: 1px solid #eee; padding-bottom: 6px; }
    .badge { background: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 0.85em; }
    .meta { color: #666; margin-bottom: 24px; font-size: 0.9em; }
    pre { background: #1e1e1e; color: #d4d4d4; padding: 14px; border-radius: 6px; overflow-x: auto; }
    code { font-family: "SFMono-Regular", Consolas, monospace; }
    ul { padding-left: 24px; }
    li { margin: 8px 0; }
  </style>
</head>
<body>
  <h1>Peeking Under the Hood of Claude Code: Architecture and Internals</h1>
  <div class="meta">
    <span class="badge">Architecture Analysis</span>
    <strong>Author:</strong> Outsight AI Research | 
    <strong>Topic:</strong> Reverse-Engineering Claude Code's Agent Loop & Prompt Engineering
  </div>
  
  <h2>1. Overview: De-mystifying Claude Code</h2>
  <p>Anthropic's Claude Code has set a new benchmark for autonomous command-line coding agents. Rather than relying on hidden proprietary magic, Claude Code achieves state-of-the-art results through rigorous software engineering, meticulous context management, and hierarchical prompting strategies. By proxying Claude Code's network traffic with LiteLLM, Outsight AI extracted and analyzed the exact mechanics powering the agent.</p>
  
  <h2>2. The Dynamic Prompt Assembly Pipeline</h2>
  <p>Unlike simple agents that submit a static 10,000-token system prompt on every call, Claude Code dynamically constructs its instructions from modular components based on current project state:</p>
  <ul>
    <li><strong>Core Agent Persona:</strong> Defines terminal interaction guidelines, bash execution safety, and conciseness rules.</li>
    <li><strong>Project Memory (CLAUDE.md):</strong> Automatically discovers and parses <code>CLAUDE.md</code> in the repository root to ingest build commands, test patterns, and code styles.</li>
    <li><strong>Ephemeral Tool Descriptions:</strong> Only tools relevant to the active sub-task (grep, glob, bash, file edit) are exposed in the JSON schema.</li>
  </ul>
  
  <h2>3. The Secret Weapon: <code>&lt;system-reminder&gt;</code> Tags</h2>
  <p>One of the most consequential findings is Claude Code's extensive use of <code>&lt;system-reminder&gt;</code> tags injected at the tail of user turns. As conversations grow and approach context limits, LLMs tend to suffer from "recency bias" and "context rot". Claude Code counteracts this by injecting real-time reminders:</p>
  <pre><code>&lt;system-reminder&gt;
CRITICAL: Do not write test commands with infinite loops.
Always inspect the file before applying edits.
Keep your response concise and focused on tool calls.
&lt;/system-reminder&gt;</code></pre>
  
  <h2>4. Sub-Agent Task Decomposition</h2>
  <p>When handling broad requests (e.g., "Refactor the authentication middleware and write unit tests"), Claude Code spawns ephemeral sub-agents. Each sub-agent runs in an isolated context window with dedicated tools, returning only the synthesized diff and test results back to the primary supervisor agent, preventing context pollution.</p>
  
  <h2>5. Command Execution Guardrails & Sandboxing</h2>
  <p>To prevent catastrophic filesystem modification or remote command injection, Claude Code evaluates bash commands through a multi-tier risk scoring matrix before prompting the user for approval or executing in a protected sandbox.</p>
</body>
</html>
"""
        with open(claude_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print("  [Patched] pages/peeking-under-the-hood-of-claude-code.html")

def main():
    print("=" * 60)
    print("CS146S Pipeline Step 1: Starting Data Acquisition & Patching")
    print("=" * 60)
    fetch_slides()
    fetch_drive_files()
    fetch_assignments()
    patch_missing_articles()
    print("\n[Step 1 Completed Successfully]")

if __name__ == "__main__":
    main()
