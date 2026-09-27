import os
import re
import json
from bs4 import BeautifulSoup
import pymupdf
from typing import Dict, Any, List

class ContentExtractor:
    def __init__(self, raw_source_dir: str = None, output_dir: str = None):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.raw_dir = raw_source_dir or os.path.join(base, 'raw_sources', 'CS146S_offline')
        self.materials_dir = os.path.join(base, 'materials')
        self.out_dir = output_dir or os.path.join(base, 'intermediate')
        os.makedirs(self.out_dir, exist_ok=True)

    def extract_html_article(self, html_path: str) -> Dict[str, Any]:
        with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove unwanted elements
        for tag in soup(['script', 'style', 'nav', 'footer', 'iframe', 'noscript', 'svg']):
            tag.decompose()

        # Extract title
        title = "Untitled"
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        elif soup.find('h1'):
            title = soup.find('h1').get_text().strip()

        # Find main article container if possible
        main = soup.find('article') or soup.find('main') or soup.find('div', class_=re.compile(r'content|post|article|main', re.I)) or soup.body
        if not main:
            main = soup

        # Convert to clean markdown-like structure
        content_lines = []
        for elem in main.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'pre', 'ul', 'ol', 'blockquote', 'table']):
            tag = elem.name
            text = elem.get_text().strip()
            if not text:
                continue

            if tag == 'h1':
                content_lines.append(f"\n# {text}\n")
            elif tag == 'h2':
                content_lines.append(f"\n## {text}\n")
            elif tag == 'h3':
                content_lines.append(f"\n### {text}\n")
            elif tag == 'h4':
                content_lines.append(f"\n#### {text}\n")
            elif tag == 'p':
                content_lines.append(f"\n{text}\n")
            elif tag == 'blockquote':
                quoted = "\n".join(f"> {line}" for line in text.splitlines())
                content_lines.append(f"\n{quoted}\n")
            elif tag == 'pre':
                code = elem.get_text()
                content_lines.append(f"\n`\n{code}\n`\n")
            elif tag in ['ul', 'ol']:
                items = []
                for li in elem.find_all('li', recursive=False):
                    li_text = li.get_text().strip()
                    if li_text:
                        items.append(f"- {li_text}")
                if items:
                    content_lines.append("\n" + "\n".join(items) + "\n")
            elif tag == 'table':
                # Basic table text
                rows = []
                for tr in elem.find_all('tr'):
                    cells = [td.get_text().strip().replace('\n', ' ') for td in tr.find_all(['td', 'th'])]
                    if cells:
                        rows.append("| " + " | ".join(cells) + " |")
                if rows:
                    content_lines.append("\n" + "\n".join(rows) + "\n")

        markdown_text = "\n".join(content_lines).strip()
        # Clean excessive newlines
        markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text)

        return {
            "title": title,
            "filename": os.path.basename(html_path),
            "char_count": len(markdown_text),
            "markdown": markdown_text
        }

    def extract_pdf_document(self, pdf_path: str) -> Dict[str, Any]:
        doc = pymupdf.open(pdf_path)
        pages_data = []
        full_text_list = []
        for idx in range(len(doc)):
            page = doc[idx]
            p_text = page.get_text('text').strip()
            pages_data.append({
                "page_num": idx + 1,
                "text": p_text,
                "images": len(page.get_images())
            })
            if p_text:
                full_text_list.append(f"### [第 {idx + 1} 页 / Page {idx + 1}]\n\n{p_text}")

        full_content = "\n\n---\n\n".join(full_text_list)
        return {
            "filename": os.path.basename(pdf_path),
            "page_count": len(doc),
            "char_count": len(full_content),
            "content": full_content,
            "pages": pages_data
        }

    def extract_course_index(self, index_path: str = None) -> Dict[str, Any]:
        ip = index_path or os.path.join(self.raw_dir, 'index.html')
        with open(ip, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')
        
        # Course Metadata
        title_el = soup.find('h1')
        title = title_el.get_text().strip() if title_el else "CS146S: The Modern Software Developer"

        # Overview / Logistics
        logistics = {}
        for card in soup.select('.info-card, .logistics-item, .card, div'):
            h4 = card.find(['h4', 'strong', 'h3'])
            if h4 and card.find('p'):
                key = h4.get_text().strip()
                val = card.find('p').get_text().strip()
                if key and val and len(key) < 30:
                    logistics[key] = val

        return {
            "title": title,
            "raw_html_len": len(html),
            "logistics": logistics
        }

    def chunk_text(self, text: str, max_chunk_size: int = 4000) -> List[Dict[str, Any]]:
        # Split by markdown headers if possible
        sections = re.split(r'(?=\n#{1,3}\s+)', text)
        chunks = []
        curr_chunk = ""
        curr_idx = 1

        for sec in sections:
            if not sec.strip():
                continue
            if len(curr_chunk) + len(sec) < max_chunk_size:
                curr_chunk += "\n" + sec
            else:
                if curr_chunk.strip():
                    chunks.append({
                        "chunk_id": curr_idx,
                        "text": curr_chunk.strip(),
                        "char_len": len(curr_chunk.strip())
                    })
                    curr_idx += 1
                curr_chunk = sec

        if curr_chunk.strip():
            chunks.append({
                "chunk_id": curr_idx,
                "text": curr_chunk.strip(),
                "char_len": len(curr_chunk.strip())
            })
        return chunks

if __name__ == '__main__':
    extractor = ContentExtractor()
    idx_res = extractor.extract_course_index()
    print("Course Index Extracted:", idx_res['title'])
