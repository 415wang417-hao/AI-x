import os
import re
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
translated_dir = os.path.join(base_dir, 'translated')
glossary_file = os.path.join(base_dir, 'glossary.json')
site_dir = os.path.join(base_dir, 'site')
os.makedirs(site_dir, exist_ok=True)
os.makedirs(os.path.join(site_dir, 'assets'), exist_ok=True)

def simple_md_to_html(md_text):
    # Escape HTML tags inside text
    lines = md_text.splitlines()
    html_out = []
    in_code_block = False
    in_table = False
    code_lang = ""
    table_lines = []

    for line in lines:
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lang = line.strip()[3:].strip()
                html_out.append(f'<pre><code class="language-{code_lang}">')
            else:
                in_code_block = False
                html_out.append('</code></pre>')
            continue

        if in_code_block:
            escaped = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html_out.append(escaped)
            continue

        # Tables
        if line.strip().startswith('|') and line.strip().endswith('|'):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line.strip())
            continue
        elif in_table:
            in_table = False
            # Render table
            html_out.append('<div class="table-wrapper"><table>')
            for idx, tl in enumerate(table_lines):
                cells = [c.strip() for c in tl.split('|')[1:-1]]
                if idx == 0:
                    html_out.append('<thead><tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr></thead><tbody>')
                elif idx == 1 and all(set(c).issubset({':', '-'}) for c in cells):
                    continue
                else:
                    html_out.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
            html_out.append('</tbody></table></div>')

        # Headings
        if line.startswith('# '):
            html_out.append(f'<h1>{line[2:].strip()}</h1>')
        elif line.startswith('## '):
            html_out.append(f'<h2>{line[3:].strip()}</h2>')
        elif line.startswith('### '):
            html_out.append(f'<h3>{line[4:].strip()}</h3>')
        elif line.startswith('#### '):
            html_out.append(f'<h4>{line[5:].strip()}</h4>')
        elif line.startswith('> '):
            html_out.append(f'<blockquote>{line[2:].strip()}</blockquote>')
        elif line.strip().startswith('- '):
            html_out.append(f'<li>{line.strip()[2:].strip()}</li>')
        elif re.match(r'^\d+\.\s+', line.strip()):
            m = re.match(r'^\d+\.\s+(.*)', line.strip())
            html_out.append(f'<li><strong>{m.group(1)}</strong></li>')
        elif line.strip() == '---':
            html_out.append('<hr/>')
        elif line.strip():
            # Paragraph
            # Bold & links & backticks
            p = line.strip()
            p = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p)
            p = re.sub(r'`(.*?)`', r'<code>\1</code>', p)
            p = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" target="_blank">\1</a>', p)
            html_out.append(f'<p>{p}</p>')

    if in_table and table_lines:
        html_out.append('<div class="table-wrapper"><table>')
        for idx, tl in enumerate(table_lines):
            cells = [c.strip() for c in tl.split('|')[1:-1]]
            if idx == 0:
                html_out.append('<thead><tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr></thead><tbody>')
            elif idx == 1 and all(set(c).issubset({':', '-'}) for c in cells):
                continue
            else:
                html_out.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
        html_out.append('</tbody></table></div>')

    return "\n".join(html_out)

class SiteBuilder:
    def __init__(self):
        self.catalog = []

    def load_materials(self):
        # 1. Syllabus
        syl_dir = os.path.join(translated_dir, 'syllabus')
        for fname in sorted(os.listdir(syl_dir)):
            if fname.endswith('.md'):
                fp = os.path.join(syl_dir, fname)
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else fname
                self.catalog.append({
                    "id": "syl_" + fname.replace('.md', ''),
                    "category": "教学大纲 (Syllabus)",
                    "category_order": 1,
                    "title": title,
                    "filename": fname,
                    "content": content,
                    "html": simple_md_to_html(content)
                })

        # 2. Playbook
        pb_file = os.path.join(translated_dir, 'playbook', 'vibe_coding_playbook_zh.md')
        if os.path.exists(pb_file):
            with open(pb_file, 'r', encoding='utf-8') as f:
                content = f.read()
            self.catalog.append({
                "id": "playbook_vibe_coding",
                "category": "实战指南 (Playbook)",
                "category_order": 2,
                "title": "Elite 20: Vibe Coding 终极生存指南 (8周架构蓝图)",
                "filename": "vibe_coding_playbook_zh.md",
                "content": content,
                "html": simple_md_to_html(content)
            })

        # 3. Papers
        paper_dir = os.path.join(translated_dir, 'papers')
        for fname in sorted(os.listdir(paper_dir)):
            if fname.endswith('.md'):
                fp = os.path.join(paper_dir, fname)
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else fname
                self.catalog.append({
                    "id": "paper_" + fname.replace('.md', ''),
                    "category": "深度技术报告 (Research Papers)",
                    "category_order": 3,
                    "title": title,
                    "filename": fname,
                    "content": content,
                    "html": simple_md_to_html(content)
                })

        # 4. Articles
        art_dir = os.path.join(translated_dir, 'articles')
        for fname in sorted(os.listdir(art_dir)):
            if fname.endswith('.md'):
                fp = os.path.join(art_dir, fname)
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else fname
                self.catalog.append({
                    "id": "art_" + fname.replace('.md', ''),
                    "category": "核心精读文献 (31 Articles)",
                    "category_order": 4,
                    "title": title,
                    "filename": fname,
                    "content": content,
                    "html": simple_md_to_html(content)
                })

        # 5. Glossary
        if os.path.exists(glossary_file):
            with open(glossary_file, 'r', encoding='utf-8') as f:
                terms = json.load(f)
            # Make a glossary view
            gl_lines = ["# Stanford CS146S / Vibe Coding 规范双语术语表 (66 Terms)", ""]
            gl_lines.append("| 序号 | 英文术语 | 规范中文译法 | 领域类别 | 概念定义说明 | 禁用生硬译法 |")
            gl_lines.append("| :---: | :--- | :--- | :--- | :--- | :--- |")
            for idx, t in enumerate(terms, 1):
                forb = '、'.join(t.get('forbidden', [])) if t.get('forbidden') else '-'
                gl_lines.append(f"| {idx} | **{t['term']}** | `{t['translation']}` | {t['category']} | {t['description']} | {forb} |")
            gl_md = "\n".join(gl_lines)
            self.catalog.append({
                "id": "glossary_terms",
                "category": "术语规范 (Glossary)",
                "category_order": 5,
                "title": "规范双语术语表 (66 Terms 强制对齐)",
                "filename": "glossary.json",
                "content": gl_md,
                "html": simple_md_to_html(gl_md)
            })

    def build_html(self):
        catalog_json = json.dumps([{
            "id": item["id"],
            "category": item["category"],
            "category_order": item["category_order"],
            "title": item["title"],
            "filename": item["filename"],
            "html": item["html"]
        } for item in self.catalog], ensure_ascii=False)

        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CS146S: The Modern Software Developer (Stanford Vibe Coding) 全量中文课程知识库</title>
  <style>
    :root {{
      --stanford-red: #8C1515;
      --stanford-dark: #5A0000;
      --stanford-gold: #D2C295;
      --bg-color: #F8F9FA;
      --card-bg: #FFFFFF;
      --text-main: #212529;
      --text-muted: #6C757D;
      --border-color: #E9ECEF;
      --code-bg: #F1F3F5;
      --sidebar-width: 320px;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
      background: var(--bg-color);
      color: var(--text-main);
      display: flex;
      height: 100vh;
      overflow: hidden;
    }}
    /* Sidebar */
    .sidebar {{
      width: var(--sidebar-width);
      background: #FFFFFF;
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }}
    .sidebar-header {{
      background: var(--stanford-red);
      color: #FFFFFF;
      padding: 20px 18px;
    }}
    .sidebar-header h1 {{ font-size: 1.15rem; font-weight: 700; letter-spacing: -0.3px; }}
    .sidebar-header p {{ font-size: 0.8rem; opacity: 0.88; margin-top: 4px; }}
    .search-box {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-color);
      background: #FAFAFA;
    }}
    .search-input {{
      width: 100%;
      padding: 8px 12px;
      border: 1px solid #CED4DA;
      border-radius: 6px;
      font-size: 0.85rem;
      outline: none;
    }}
    .search-input:focus {{ border-color: var(--stanford-red); }}
    .nav-list {{
      flex: 1;
      overflow-y: auto;
      padding: 10px 0;
    }}
    .category-title {{
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-muted);
      padding: 10px 18px 4px;
      letter-spacing: 0.5px;
    }}
    .nav-item {{
      display: block;
      padding: 8px 18px;
      font-size: 0.85rem;
      color: #495057;
      text-decoration: none;
      cursor: pointer;
      line-height: 1.4;
      border-left: 3px solid transparent;
      transition: all 0.15s ease;
    }}
    .nav-item:hover {{ background: #F1F3F5; color: var(--stanford-red); }}
    .nav-item.active {{
      background: #FFF5F5;
      color: var(--stanford-red);
      font-weight: 600;
      border-left-color: var(--stanford-red);
    }}
    /* Main Content */
    .main {{
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      background: #FFFFFF;
    }}
    .top-bar {{
      height: 56px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 28px;
      background: #FFFFFF;
    }}
    .breadcrumbs {{ font-size: 0.85rem; color: var(--text-muted); }}
    .content-area {{
      flex: 1;
      overflow-y: auto;
      padding: 36px 48px;
      line-height: 1.75;
    }}
    .content-wrapper {{ max-width: 900px; margin: 0 auto; }}
    .content-wrapper h1 {{ font-size: 1.85rem; margin-bottom: 16px; color: #111; line-height: 1.3; border-bottom: 2px solid var(--stanford-red); padding-bottom: 12px; }}
    .content-wrapper h2 {{ font-size: 1.4rem; margin: 28px 0 14px; color: #222; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }}
    .content-wrapper h3 {{ font-size: 1.15rem; margin: 20px 0 10px; color: #333; }}
    .content-wrapper p {{ margin-bottom: 14px; font-size: 0.95rem; }}
    .content-wrapper blockquote {{
      border-left: 4px solid var(--stanford-red);
      background: #FDF7F7;
      padding: 12px 18px;
      margin: 16px 0;
      color: #444;
      border-radius: 0 6px 6px 0;
    }}
    .content-wrapper li {{ margin-left: 24px; margin-bottom: 6px; font-size: 0.95rem; }}
    .content-wrapper code {{
      background: var(--code-bg);
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.88em;
      font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
      color: #C7254E;
    }}
    .content-wrapper pre {{
      background: #1E1E1E;
      color: #D4D4D4;
      padding: 16px 20px;
      border-radius: 8px;
      overflow-x: auto;
      margin: 18px 0;
    }}
    .content-wrapper pre code {{ background: none; color: inherit; padding: 0; }}
    .table-wrapper {{ overflow-x: auto; margin: 20px 0; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; }}
    th, td {{ border: 1px solid var(--border-color); padding: 10px 14px; text-align: left; }}
    th {{ background: #F8F9FA; font-weight: 600; }}
    tr:nth-child(even) {{ background: #FAFAFA; }}
    hr {{ border: none; border-top: 1px solid var(--border-color); margin: 28px 0; }}
    .stats-badge {{
      display: inline-block;
      padding: 4px 10px;
      background: #E8F5E9;
      color: #2E7D32;
      border-radius: 12px;
      font-size: 0.75rem;
      font-weight: 600;
    }}
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="sidebar-header">
      <h1>CS146S Vibe Coding</h1>
      <p>Stanford Fall 2025 · 全量中文知识库</p>
    </div>
    <div class="search-box">
      <input type="text" id="searchInput" class="search-input" placeholder="输入关键词检索课程文献、大纲与术语...">
    </div>
    <div class="nav-list" id="navList"></div>
  </div>
  <div class="main">
    <div class="top-bar">
      <div class="breadcrumbs" id="breadcrumbs">首页</div>
      <div>
        <span class="stats-badge">100% 审计合规 · 46 篇全量就绪</span>
      </div>
    </div>
    <div class="content-area">
      <div class="content-wrapper" id="contentView"></div>
    </div>
  </div>

  <script>
    const catalog = {catalog_json};
    let currentId = catalog[0] ? catalog[0].id : '';

    function renderNav(filter = '') {{
      const navList = document.getElementById('navList');
      navList.innerHTML = '';
      
      const categories = {{}};
      catalog.forEach(item => {{
        if (filter) {{
          const q = filter.toLowerCase();
          const matchTitle = item.title.toLowerCase().includes(q);
          const matchCat = item.category.toLowerCase().includes(q);
          if (!matchTitle && !matchCat) return;
        }}
        if (!categories[item.category]) categories[item.category] = [];
        categories[item.category].push(item);
      }});

      for (const [catName, items] of Object.entries(categories)) {{
        const catHeader = document.createElement('div');
        catHeader.className = 'category-title';
        catHeader.textContent = catName;
        navList.appendChild(catHeader);

        items.forEach(item => {{
          const a = document.createElement('a');
          a.className = 'nav-item' + (item.id === currentId ? ' active' : '');
          a.textContent = item.title;
          a.title = item.title;
          a.onclick = () => selectItem(item.id);
          navList.appendChild(a);
        }});
      }}
    }}

    function selectItem(id) {{
      currentId = id;
      const item = catalog.find(x => x.id === id);
      if (!item) return;

      document.getElementById('breadcrumbs').textContent = item.category + ' / ' + item.title;
      document.getElementById('contentView').innerHTML = item.html;
      
      // Update active nav class
      document.querySelectorAll('.nav-item').forEach(el => {{
        el.classList.toggle('active', el.textContent === item.title);
      }});

      document.querySelector('.content-area').scrollTop = 0;
    }}

    document.getElementById('searchInput').addEventListener('input', (e) => {{
      renderNav(e.target.value.trim());
    }});

    // Init
    renderNav();
    if (catalog.length > 0) selectItem(catalog[0].id);
  </script>
</body>
</html>
"""
        out_html = os.path.join(site_dir, 'index.html')
        with open(out_html, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"[SiteBuilder] Built standalone static site with {len(self.catalog)} documents at: {out_html}")
        return out_html

if __name__ == '__main__':
    builder = SiteBuilder()
    builder.load_materials()
    builder.build_html()
