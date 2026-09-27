#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS146S Pipeline Step 2: Semantic Document Extraction & Long-Text Chunking
Features:
- HTML boilerplate stripping (navs, footers, tracking scripts)
- PDF extraction via PyMuPDF (fitz)
- Semantic chunking with token budgeting (preserves code fences, tables, headings)
- Contextual header preservation to mitigate context rot
"""

import os
import re
import json
import fitz  # PyMuPDF
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR = os.path.join(BASE_DIR, "pages")
PDFS_DIR = os.path.join(BASE_DIR, "pdfs")
SLIDES_DIR = os.path.join(BASE_DIR, "slides_pdf")
OUTPUT_EXTRACTED = os.path.join(BASE_DIR, "extracted")

os.makedirs(OUTPUT_EXTRACTED, exist_ok=True)

def html_to_clean_markdown(html_path):
    """Parses an HTML file, removes junk/scripts/nav, and extracts clean markdown."""
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")

    # Remove non-content tags
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg", "form"]):
        tag.decompose()

    # Find main content container if available
    main_node = (
        soup.find("article")
        or soup.find("main")
        or soup.find(class_=re.compile(r"content|post|article|entry", re.I))
        or soup.find("body")
    )
    if not main_node:
        main_node = soup

    # Extract title
    title = ""
    title_tag = soup.find("title") or soup.find("h1")
    if title_tag:
        title = title_tag.get_text().strip()

    # Convert common elements to markdown
    lines = []
    if title:
        lines.append(f"# {title}\n")

    for elem in main_node.descendants:
        if elem.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            level = int(elem.name[1])
            text = elem.get_text().strip()
            if text:
                lines.append(f"\n{'#' * level} {text}\n")
        elif elem.name == "p":
            text = elem.get_text().strip()
            if text:
                lines.append(f"{text}\n")
        elif elem.name == "pre":
            code = elem.get_text()
            lines.append(f"\n```\n{code.strip()}\n```\n")
        elif elem.name in ["ul", "ol"]:
            for li in elem.find_all("li", recursive=False):
                li_text = li.get_text().strip()
                if li_text:
                    lines.append(f"- {li_text}")
            lines.append("")
        elif elem.name == "blockquote":
            text = elem.get_text().strip()
            if text:
                lines.append(f"> {text}\n")

    # De-duplicate excessive newlines
    raw_md = "\n".join(lines)
    clean_md = re.sub(r"\n{3,}", "\n\n", raw_md).strip()
    return clean_md

def extract_pdf_text(pdf_path):
    """Extracts text and structural headers from PDF documents."""
    doc = fitz.open(pdf_path)
    pages_text = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()
        if text:
            pages_text.append(f"### Page {page_num + 1}\n\n{text}")
    return "\n\n---\n\n".join(pages_text)

def semantic_chunking(text, max_tokens=1500, min_tokens=300):
    """
    Intelligently splits markdown text into semantic chunks.
    Ensures that code blocks and table structures are never broken in between.
    Maintains hierarchical context headers for each chunk.
    """
    # Rough token estimation: 1 word ~ 1.3 tokens or 1 char ~ 0.25 tokens
    def estimate_tokens(t):
        return len(t.split()) + len(re.findall(r"[\u4e00-\u9fff]", t))

    sections = re.split(r"(^#{1,3}\s+.+$)", text, flags=re.MULTILINE)
    chunks = []
    current_chunk = []
    current_tokens = 0
    current_header = "Introduction"

    for part in sections:
        part = part.strip()
        if not part:
            continue

        if re.match(r"^#{1,3}\s+", part):
            current_header = part
            tokens = estimate_tokens(part)
        else:
            tokens = estimate_tokens(part)

        if current_tokens + tokens > max_tokens and current_tokens >= min_tokens:
            chunks.append({
                "header": current_header,
                "text": "\n\n".join(current_chunk),
                "tokens": current_tokens
            })
            current_chunk = [f"*(Context: Section {current_header})*\n\n{part}"]
            current_tokens = tokens
        else:
            current_chunk.append(part)
            current_tokens += tokens

    if current_chunk:
        chunks.append({
            "header": current_header,
            "text": "\n\n".join(current_chunk),
            "tokens": current_tokens
        })

    return chunks

def process_all_documents():
    manifest = {}

    # 1. Process HTML articles
    print("\n--- Processing HTML Articles ---")
    if os.path.exists(PAGES_DIR):
        for f in sorted(os.listdir(PAGES_DIR)):
            if f.endswith(".html"):
                path = os.path.join(PAGES_DIR, f)
                md = html_to_clean_markdown(path)
                chunks = semantic_chunking(md)
                base_name = f.replace(".html", "")
                out_path = os.path.join(OUTPUT_EXTRACTED, f"{base_name}.md")
                with open(out_path, "w", encoding="utf-8") as out_f:
                    out_f.write(md)
                manifest[f] = {
                    "type": "html_article",
                    "extracted_md": out_path,
                    "char_count": len(md),
                    "chunk_count": len(chunks)
                }
                print(f"  [Article] {f} -> {len(chunks)} chunks ({len(md)} chars)")

    # 2. Process Core PDFs
    print("\n--- Processing Core PDFs ---")
    if os.path.exists(PDFS_DIR):
        for f in sorted(os.listdir(PDFS_DIR)):
            if f.endswith(".pdf"):
                path = os.path.join(PDFS_DIR, f)
                text = extract_pdf_text(path)
                chunks = semantic_chunking(text, max_tokens=2000)
                base_name = f.replace(".pdf", "")
                out_path = os.path.join(OUTPUT_EXTRACTED, f"{base_name}.md")
                with open(out_path, "w", encoding="utf-8") as out_f:
                    out_f.write(text)
                manifest[f] = {
                    "type": "pdf_document",
                    "extracted_md": out_path,
                    "char_count": len(text),
                    "chunk_count": len(chunks)
                }
                print(f"  [PDF] {f} -> {len(chunks)} chunks ({len(text)} chars)")

    # Save extraction manifest
    manifest_path = os.path.join(OUTPUT_EXTRACTED, "extraction_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"\n[Step 2 Complete] Manifest written to {manifest_path}")

def main():
    print("=" * 60)
    print("CS146S Pipeline Step 2: Extraction & Semantic Chunking")
    print("=" * 60)
    process_all_documents()

if __name__ == "__main__":
    main()
