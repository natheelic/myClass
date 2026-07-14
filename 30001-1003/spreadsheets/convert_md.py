import markdown
import glob
import os

html_template = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Prompt', sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            color: #f8fafc;
            background-color: #0a0a0f;
        }}
        h1, h2, h3, h4 {{ color: #3b82f6; }}
        h1 {{ border-bottom: 2px solid #3b82f6; padding-bottom: 0.5rem; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 2rem; }}
        th, td {{ border: 1px solid #334155; padding: 0.75rem; text-align: left; }}
        th {{ background-color: #1e293b; color: #fff; }}
        code {{ background-color: #1e293b; padding: 0.2rem 0.4rem; border-radius: 4px; color: #fb7185; }}
        a {{ color: #60a5fa; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .back-btn {{
            display: inline-block;
            margin-bottom: 2rem;
            padding: 0.5rem 1rem;
            background: #1e293b;
            color: #fff;
            border-radius: 8px;
            text-decoration: none;
            transition: background 0.3s;
        }}
        .back-btn:hover {{ background: #3b82f6; }}
    </style>
</head>
<body>
    <a href="index.html" class="back-btn">&larr; กลับหน้าหลัก (Back to Portal)</a>
    <div class="content">
        {content}
    </div>
</body>
</html>"""

for md_file in glob.glob("*.md"):
    with open(md_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    html_content = markdown.markdown(text, extensions=['tables', 'fenced_code'])
    
    # Extract title from first line if possible
    title = md_file.replace(".md", "")
    first_line = text.split('\n')[0]
    if first_line.startswith("# "):
        title = first_line.replace("# ", "").strip()
        
    final_html = html_template.format(title=title, content=html_content)
    
    html_file = md_file.replace(".md", ".html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"Converted {md_file} to {html_file}")
