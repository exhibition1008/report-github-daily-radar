# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Telegram Notifier Module
Gửi thông báo tóm tắt các dự án hot qua Telegram Bot.
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime

def send_telegram_radar(categories_data, telegram_config):
    """
    Gửi tin nhắn tóm tắt các dự án nổi bật qua Telegram Bot.
    """
    if not telegram_config or not telegram_config.get("enabled", False):
        print("[*] Telegram thông báo đang TẮT (Bạn có thể bật trong config.json).")
        return False
        
    bot_token = telegram_config.get("bot_token", "").strip()
    chat_id = telegram_config.get("chat_id", "").strip()
    
    if not bot_token or not chat_id or bot_token == "YOUR_BOT_TOKEN_HERE":
        print("[!] Chưa cấu hình Telegram Bot Token hoặc Chat ID trong config.json.")
        print("    -> Hướng dẫn: Nhắn @BotFather để tạo bot lấy token, và nhắn @userinfobot để lấy Chat ID.")
        return False
        
    today = datetime.now().strftime("%d/%m/%Y")
    total_repos = sum(cat["count"] for cat in categories_data)
    
    # Xây dựng nội dung tin nhắn Telegram dạng HTML
    lines = []
    lines.append(f"📡 <b>GITHUB DAILY RADAR</b> (<code>{today}</code>)")
    lines.append(f"<i>Tổng hợp {total_repos} dự án hot nhất hôm nay:</i>\n")
    
    for cat in categories_data:
        if not cat["repos"]:
            continue
        lines.append(f"<b>{cat['name']}</b>:")
        # Lấy top 3 dự án tiêu biểu cho mỗi mục để tránh tin nhắn quá dài
        top_items = cat["repos"][:3]
        for r in top_items:
            # Rút gọn mô tả nếu quá dài
            desc = r["description"]
            if len(desc) > 80:
                desc = desc[:77] + "..."
            # Escape HTML cơ bản
            desc = desc.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            full_name = r["full_name"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            
            lines.append(f"• <a href=\"{r['url']}\"><b>{full_name}</b></a> (⭐ {r['stars_formatted']})")
            lines.append(f"  <i>{desc}</i>")
        lines.append("")
        
    lines.append(f"📊 <i>Đã tự động tổng hợp &amp; cập nhật vào file Excel!</i>")
    message_text = "\n".join(lines)
    
    # Gửi qua Telegram Bot API
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(api_url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                print(f"[+] Đã gửi thông báo thành công đến Telegram (Chat ID: {chat_id})!")
                return True
    except Exception as e:
        print(f"[!] Lỗi khi gửi tin nhắn Telegram: {e}")
        return False
