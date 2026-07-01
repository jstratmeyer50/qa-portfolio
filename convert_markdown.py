#!/usr/bin/env python3
"""
Batch converter for markdown files to styled HTML pages for QA Portfolio
"""

import os
import re
import sys
from pathlib import Path

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

def markdown_to_html(md_content):
    """Convert markdown content to HTML"""
    html = md_content
    
    # Preserve code blocks first
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"<<<CODE_BLOCK_{len(code_blocks)-1}>>>"
    
    html = re.sub(r'```[\s\S]*?```', save_code_block, html)
    
    # Headers
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    html = re.sub(r'__(.*?)__', r'<strong>\1</strong>', html)
    html = re.sub(r'_(.*?)_', r'<em>\1</em>', html)
    
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    
    # Lists
    html = re.sub(r'^\* (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # Restore code blocks
    for i, block in enumerate(code_blocks):
        html = html.replace(f"<<<CODE_BLOCK_{i}>>>", block)
    
    # Paragraphs
    html = re.sub(r'\n\n+', '</p><p>', html)
    html = '<p>' + html + '</p>'
    
    # Clean up
    html = html.replace('<p><h', '<h')
    html = html.replace('</h></p>', '</h>')
    
    return html

def create_html_page(md_file, folder_name, folder_title):
    """Create an HTML page from a markdown file"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Extract title from first H1
    title_match = re.search(r'^# (.*?)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.basename(md_file)
    
    # Extract metadata
    version = ""
    author = ""
    date = ""
    status = ""
    
    meta_patterns = {
        'version': r'\*\*Document Version:\*\*\s*([\d.]+)',
        'author': r'\*\*Author:\*\*\s*(.+?)(?:\n|$)',
        'date': r'\*\*Date:\*\*\s*(.+?)(?:\n|$)',
        'status': r'\*\*Status:\*\*\s*(.+?)(?:\n|$)',
    }
    
    for key, pattern in meta_patterns.items():
        match = re.search(pattern, md_content)
        if match:
            if key == 'version':
                version = match.group(1)
            elif key == 'author':
                author = match.group(1).strip()
            elif key == 'date':
                date = match.group(1).strip()
            elif key == 'status':
                status = match.group(1).strip()
    
    # Convert markdown content to HTML (simple conversion)
    html_content = markdown_to_html(md_content)
    
    # Generate output filename
    page_slug = slugify(title)
    output_file = md_file.parent / f"{page_slug}.html"
    
    # Generate HTML page
    html_page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | QA Portfolio</title>
  <link rel="stylesheet" href="../styles.css" />
  <style>
    .breadcrumb {{ margin-bottom: 2rem; font-size: 0.9rem; color: #8fff88; }}
    .breadcrumb a {{ color: #a8ff8f; }}
    .content-header {{ margin-bottom: 2rem; }}
    .content-header h1 {{ margin: 0 0 1rem 0; }}
    .meta-info {{ display: flex; flex-wrap: wrap; gap: 2rem; margin: 1.5rem 0; padding: 1rem; background: rgba(0, 20, 0, 0.4); border-left: 3px solid rgba(168, 255, 143, 0.5); border-radius: 3px; }}
    .meta-item {{ display: flex; flex-direction: column; gap: 0.25rem; }}
    .meta-label {{ font-size: 0.8rem; color: #8fff88; text-transform: uppercase; letter-spacing: 0.1em; }}
    .meta-value {{ color: #d8ffd5; font-weight: 600; }}
    .document-content {{ line-height: 1.8; color: #d8ffd5; }}
    .document-content h2 {{ margin: 2rem 0 1rem 0; border-bottom: 1px solid rgba(144, 255, 144, 0.2); padding-bottom: 0.5rem; }}
    .document-content h3 {{ margin: 1.5rem 0 0.75rem 0; color: #b8ff8f; }}
    .document-content p {{ margin: 1rem 0; }}
    .document-content ul, .document-content ol {{ margin: 1rem 0; padding-left: 2rem; }}
    .document-content li {{ margin: 0.5rem 0; }}
    .document-content table {{ width: 100%; margin: 1.5rem 0; border-collapse: collapse; border: 1px solid rgba(144, 255, 144, 0.3); }}
    .document-content th, .document-content td {{ padding: 0.75rem; text-align: left; border: 1px solid rgba(144, 255, 144, 0.2); }}
    .document-content th {{ background: rgba(10, 30, 10, 0.5); font-weight: 700; color: #b8ff8f; }}
    .document-content code {{ background: rgba(0, 10, 0, 0.5); padding: 0.2rem 0.4rem; border-radius: 2px; font-family: "Courier New", Courier, monospace; color: #a8ff8f; }}
    .document-content pre {{ background: rgba(0, 10, 0, 0.6); padding: 1rem; border-radius: 4px; overflow-x: auto; margin: 1.5rem 0; border-left: 3px solid rgba(168, 255, 143, 0.4); }}
    .back-link {{ display: inline-block; margin-top: 2rem; padding: 0.5rem 1rem; background: rgba(56, 255, 118, 0.1); border: 1px solid rgba(168, 255, 143, 0.4); border-radius: 3px; color: #a8ff8f; text-decoration: none; font-size: 0.9rem; transition: all 0.2s ease; }}
    .back-link:hover {{ background: rgba(56, 255, 118, 0.2); border-color: rgba(168, 255, 143, 0.8); }}
  </style>
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <div>
        <h1>Jess Stratmeyer</h1>
        <p class="lead">QA Portfolio</p>
      </div>
      <nav class="site-nav" aria-label="Primary navigation">
        <a href="../index.html">Home</a>
        <a href="../test-plans/">Test Plans</a>
        <a href="../test-cases/">Test Cases</a>
        <a href="../bug-reports/">Bug Reports</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="section container">
      <div class="breadcrumb">
        <a href="../index.html">Home</a> / <a href="../{folder_name}/">{folder_title}</a> / {title}
      </div>

      <div class="content-header">
        <h1>{title}</h1>
      </div>

      {f'<div class="meta-info">' + 
       (f'<div class="meta-item"><span class="meta-label">Version</span><span class="meta-value">{version}</span></div>' if version else '') +
       (f'<div class="meta-item"><span class="meta-label">Author</span><span class="meta-value">{author}</span></div>' if author else '') +
       (f'<div class="meta-item"><span class="meta-label">Date</span><span class="meta-value">{date}</span></div>' if date else '') +
       (f'<div class="meta-item"><span class="meta-label">Status</span><span class="meta-value">{status}</span></div>' if status else '') +
       '</div>' if (version or author or date or status) else ''}

      <div class="document-content">
        {html_content}
      </div>

      <a href="../{folder_name}/" class="back-link">← Back to {folder_title}</a>
    </section>
  </main>

  <footer style="text-align: center; padding: 2rem; color: #8fff88; font-size: 0.9rem; border-top: 1px solid rgba(144, 255, 144, 0.2); margin-top: 3rem;">
    <p>&copy; 2024 Jess Stratmeyer | QA Portfolio</p>
  </footer>
</body>
</html>'''
    
    print(f"Creating: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_page)

if __name__ == '__main__':
    # Configuration
    folders = {
        'test-plans': 'Test Plans',
        'test-cases': 'Test Cases',
        'bug-reports': 'Bug Reports',
        'checklists': 'Checklists',
        'process-docs': 'Process Docs',
        'exploratory-testing': 'Exploratory Testing',
    }
    
    portfolio_root = Path('/Users/jessestratmeyer/Desktop/code/qa-portfolio')
    
    for folder_name, folder_title in folders.items():
        folder_path = portfolio_root / folder_name
        if folder_path.exists():
            for md_file in folder_path.glob('*.md'):
                create_html_page(md_file, folder_name, folder_title)
                
    print("✓ All markdown files converted to HTML!")
