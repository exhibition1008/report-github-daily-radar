# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Reporter Module
Xuất báo cáo dưới dạng Markdown và giao diện Web HTML trực quan, hiện đại.
"""

import os
from datetime import datetime

def generate_markdown(categories_data, output_path):
    """
    Tạo báo cáo dạng Markdown.
    """
    today = datetime.now().strftime("%d/%m/%Y")
    lines = []
    lines.append(f"# 📡 GitHub Daily Radar ({today})")
    lines.append("> Tự động tổng hợp các dự án mã nguồn mở hot & thú vị nhất trên GitHub.\n")
    
    total_repos = sum(cat["count"] for cat in categories_data)
    lines.append(f"**Tổng số dự án hôm nay:** {total_repos} dự án\n---\n")
    
    for cat in categories_data:
        lines.append(f"## {cat['name']} ({cat['count']})")
        if not cat["repos"]:
            lines.append("_Chưa có dự án mới nào đạt tiêu chuẩn lọc hôm nay._\n")
            continue
            
        for r in cat["repos"]:
            tags_str = " ".join([f"`#{t}`" for t in r["topics"]])
            lines.append(f"### 🌟 [{r['full_name']}]({r['url']})")
            lines.append(f"- **Mô tả:** {r['description']}")
            lines.append(f"- **Ngôn ngữ:** {r['language']} | ⭐ **Stars:** {r['stars_formatted']} | 🍴 **Forks:** {r['forks_formatted']}")
            if tags_str:
                lines.append(f"- **Thẻ:** {tags_str}")
            lines.append("")
        lines.append("---\n")
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[+] Đã xuất Markdown: {output_path}")

def generate_html(categories_data, output_path):
    """
    Tạo báo cáo giao diện Web Dashboard (Sci-Fi / Modern Dark Mode).
    """
    today = datetime.now().strftime("%d/%m/%Y %H:%M")
    total_repos = sum(cat["count"] for cat in categories_data)
    
    header_tabs = []
    for cat in categories_data:
        cid = cat['id']
        cname = cat['name']
        ccount = cat['count']
        header_tabs.append(f'<button class="tab-btn" onclick="filterTab(\'{cid}\')">{cname} ({ccount})</button>')
    tabs_html = "\n".join(header_tabs)

    sections_html = []
    for cat in categories_data:
        cards_html = []
        for r in cat["repos"]:
            avatar_html = f'<img src="{r["owner_avatar"]}" class="avatar" alt="avatar" onerror="this.style.display=\'none\'">' if r["owner_avatar"] else ''
            topics_html = "".join([f'<span class="topic-pill">#{t}</span>' for t in r["topics"]])
            kw = f"{r['name']} {r['description']} {' '.join(r['topics'])}".lower().replace('"', '')
            
            card = f'''<div class="card" data-keywords="{kw}">
    <div class="card-header">
        {avatar_html}
        <div>
            <a href="{r['url']}" target="_blank" class="repo-title">{r['full_name']}</a>
        </div>
    </div>
    <div class="repo-desc">{r['description']}</div>
    <div class="topics">{topics_html}</div>
    <div class="card-footer">
        <div class="meta-stats">
            <div class="stat-item stat-star">⭐ {r['stars_formatted']}</div>
            <div class="stat-item">🍴 {r['forks_formatted']}</div>
            <div class="lang-badge">
                <span class="lang-dot" style="background: {r['lang_color']}"></span>
                <span>{r['language']}</span>
            </div>
        </div>
        <a href="{r['url']}" target="_blank" class="btn-view">Xem Repo ↗</a>
    </div>
</div>'''
            cards_html.append(card)
            
        cards_content = "\n".join(cards_html) if cards_html else '<p style="color:#94a3b8;">Không có dự án nào hôm nay.</p>'
        
        sec = f'''<section class="category-section" id="sec-{cat['id']}" data-category="{cat['id']}">
    <div class="category-title">
        <span>{cat['name']}</span>
        <span class="category-count">{cat['count']} dự án</span>
    </div>
    <div class="grid">
        {cards_content}
    </div>
</section>'''
        sections_html.append(sec)

    all_sections = "\n".join(sections_html)

    html_content = f'''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Daily Radar - {today}</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-main: #0b0f19;
            --bg-card: rgba(23, 32, 54, 0.7);
            --border-card: rgba(99, 140, 255, 0.15);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-cyan: #00f2fe;
            --accent-blue: #4facfe;
            --accent-purple: #9d4edd;
            --accent-gold: #fbbf24;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: var(--bg-main);
            color: var(--text-primary);
            font-family: 'Plus Jakarta Sans', sans-serif;
            min-height: 100vh;
            padding: 2.5rem 1.5rem;
            background-image: radial-gradient(circle at 50% 0%, rgba(79, 172, 254, 0.12) 0%, transparent 60%);
        }}
        .container {{ max-width: 1240px; margin: 0 auto; }}
        header {{ text-align: center; margin-bottom: 2.5rem; }}
        .badge-header {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(0, 242, 254, 0.1);
            color: var(--accent-cyan);
            border: 1px solid rgba(0, 242, 254, 0.3);
            padding: 6px 16px;
            border-radius: 99px;
            font-size: 0.85rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }}
        h1 {{
            font-size: 2.6rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 30%, var(--accent-cyan) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        .subtitle {{ color: var(--text-secondary); font-size: 1.05rem; }}
        .controls {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2.5rem;
            background: rgba(18, 24, 40, 0.85);
            padding: 14px 20px;
            border-radius: 16px;
            border: 1px solid var(--border-card);
            backdrop-filter: blur(12px);
        }}
        .tabs {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .tab-btn {{
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-secondary);
            padding: 8px 16px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        .tab-btn:hover {{ color: var(--text-primary); background: rgba(255, 255, 255, 0.05); }}
        .tab-btn.active {{
            background: linear-gradient(135deg, rgba(79, 172, 254, 0.2), rgba(0, 242, 254, 0.2));
            color: var(--accent-cyan);
            border-color: rgba(0, 242, 254, 0.4);
        }}
        .search-box {{
            display: flex;
            align-items: center;
            background: rgba(10, 15, 29, 0.8);
            border: 1px solid var(--border-card);
            border-radius: 10px;
            padding: 8px 14px;
            width: 280px;
        }}
        .search-box input {{
            background: transparent;
            border: none;
            outline: none;
            color: var(--text-primary);
            width: 100%;
            font-size: 0.9rem;
        }}
        .category-section {{ margin-bottom: 3.5rem; }}
        .category-title {{
            font-size: 1.45rem;
            font-weight: 700;
            margin-bottom: 1.2rem;
            display: flex;
            align-items: center;
            gap: 12px;
            color: #ffffff;
        }}
        .category-count {{
            font-size: 0.8rem;
            background: rgba(255, 255, 255, 0.1);
            color: var(--text-secondary);
            padding: 3px 10px;
            border-radius: 99px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 22px;
        }}
        .card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 16px;
            padding: 1.3rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.25s ease;
            backdrop-filter: blur(12px);
        }}
        .card:hover {{
            transform: translateY(-4px);
            border-color: rgba(0, 242, 254, 0.4);
            box-shadow: 0 12px 30px rgba(0, 242, 254, 0.08);
        }}
        .card-header {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 0.8rem;
        }}
        .avatar {{
            width: 40px;
            height: 40px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .repo-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #ffffff;
            text-decoration: none;
            transition: color 0.2s;
            word-break: break-all;
        }}
        .repo-title:hover {{ color: var(--accent-cyan); }}
        .repo-desc {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            line-height: 1.55;
            margin-bottom: 1.1rem;
            flex-grow: 1;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .topics {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 1.1rem;
        }}
        .topic-pill {{
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-secondary);
            font-size: 0.75rem;
            padding: 3px 8px;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            font-family: 'JetBrains Mono', monospace;
        }}
        .card-footer {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            padding-top: 0.9rem;
            font-size: 0.85rem;
        }}
        .meta-stats {{ display: flex; align-items: center; gap: 14px; }}
        .stat-item {{
            display: flex;
            align-items: center;
            gap: 4px;
            color: var(--text-secondary);
            font-weight: 600;
        }}
        .stat-star {{ color: var(--accent-gold); }}
        .lang-badge {{
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--text-secondary);
        }}
        .lang-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }}
        .btn-view {{
            background: linear-gradient(135deg, rgba(79, 172, 254, 0.15), rgba(0, 242, 254, 0.15));
            color: var(--accent-cyan);
            border: 1px solid rgba(0, 242, 254, 0.3);
            padding: 6px 14px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.82rem;
            transition: all 0.2s;
        }}
        .btn-view:hover {{
            background: var(--accent-cyan);
            color: #0b0f19;
            box-shadow: 0 0 14px rgba(0, 242, 254, 0.4);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="badge-header">⚡ Live Discovery System</div>
            <h1>GitHub Daily Radar</h1>
            <p class="subtitle">Tổng hợp {total_repos} dự án công nghệ & AI mã nguồn mở nổi bật nhất • {today}</p>
        </header>
        
        <div class="controls">
            <div class="tabs">
                <button class="tab-btn active" onclick="filterTab('all')">Tất cả ({total_repos})</button>
                {tabs_html}
            </div>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 Tìm kiếm theo tên / tag..." oninput="searchCards()">
            </div>
        </div>

        {all_sections}
    </div>
    <script>
        function filterTab(catId) {{
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            document.querySelectorAll('.category-section').forEach(sec => {{
                if (catId === 'all' || sec.getAttribute('data-category') === catId) {{
                    sec.style.display = 'block';
                }} else {{
                    sec.style.display = 'none';
                }}
            }});
        }}
        
        function searchCards() {{
            const query = document.getElementById('searchInput').value.toLowerCase();
            document.querySelectorAll('.card').forEach(card => {{
                const keywords = card.getAttribute('data-keywords') || '';
                if (keywords.includes(query)) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}
    </script>
</body>
</html>'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] Đã xuất HTML Dashboard: {output_path}")
