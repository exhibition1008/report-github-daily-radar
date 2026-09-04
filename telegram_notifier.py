# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Telegram Notifier Module
Gửi thông báo tóm tắt dạng văn bản và file Audio Podcast qua Telegram Bot.
"""

import os
import json
import requests
import urllib.request
from datetime import datetime

def send_telegram_radar(categories_data, telegram_config, audio_file_path=None):
    """
    Gửi tin nhắn tóm tắt và file âm thanh podcast qua Telegram Bot.
    """
    if not telegram_config or not telegram_config.get("enabled", False):
        print("[*] Telegram thông báo đang TẮT (Bạn có thể bật trong config.json).")
        return False
        
    bot_token = telegram_config.get("bot_token", "").strip()
    chat_id = telegram_config.get("chat_id", "").strip()
    
    if not bot_token or not chat_id or bot_token == "YOUR_BOT_TOKEN_HERE":
        print("[!] Chưa cấu hình Telegram Bot Token hoặc Chat ID trong config.json.")
        return False
        
    today = datetime.now().strftime("%d/%m/%Y")
    total_repos = sum(cat["count"] for cat in categories_data)
    
    # 1. Gửi tin nhắn văn bản tóm tắt
    lines = []
    lines.append(f"📡 <b>GITHUB DAILY RADAR</b> (<code>{today}</code>)")
    lines.append(f"<i>Tổng hợp {total_repos} dự án hot nhất hôm nay:</i>\n")
    
    for cat in categories_data:
        if not cat["repos"]:
            continue
        lines.append(f"<b>{cat['name']}</b>:")
        top_items = cat["repos"][:3]
        for r in top_items:
            desc = r["description"]
            if len(desc) > 80:
                desc = desc[:77] + "..."
            desc = desc.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            full_name = r["full_name"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            
            lines.append(f"• <a href=\"{r['url']}\"><b>{full_name}</b></a> (⭐ {r['stars_formatted']})")
            lines.append(f"  <i>{desc}</i>")
        lines.append("")
        
    lines.append(f"📊 <i>Đã tự động tổng hợp &amp; cập nhật vào file Excel!</i>")
    message_text = "\n".join(lines)
    
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
                print(f"[+] Đã gửi bản tin văn bản đến Telegram (Chat ID: {chat_id})!")
    except Exception as e:
        print(f"[!] Lỗi khi gửi tin nhắn Telegram: {e}")

    # 2. Gửi file Audio Podcast (nếu có)
    if audio_file_path and os.path.exists(audio_file_path):
        print("[*] Đang gửi file Audio Podcast đến Telegram...")
        voice_url = f"https://api.telegram.org/bot{bot_token}/sendVoice"
        try:
            with open(audio_file_path, "rb") as f:
                files = {"voice": f}
                data = {
                    "chat_id": chat_id,
                    "caption": f"🎙️ Bản tin Audio Podcast ({today}) - Nghe tóm tắt nhanh dự án hot!"
                }
                resp = requests.post(voice_url, data=data, files=files, timeout=30)
                if resp.status_code == 200:
                    print(f"[+] Đã gửi file Audio Podcast thành công đến Telegram!")
                else:
                    # Fallback sang sendAudio nếu sendVoice không được
                    audio_url = f"https://api.telegram.org/bot{bot_token}/sendAudio"
                    f.seek(0)
                    files = {"audio": f}
                    resp2 = requests.post(audio_url, data=data, files=files, timeout=30)
                    if resp2.status_code == 200:
                        print(f"[+] Đã gửi Audio thành công!")
        except Exception as e:
            print(f"[!] Lỗi khi gửi file âm thanh qua Telegram: {e}")

    return True
