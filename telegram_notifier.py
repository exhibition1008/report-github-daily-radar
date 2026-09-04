# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Telegram Notifier Module
Send structured text summaries and audio podcast voice notes via Telegram Bot in English.
"""

import os
import json
import requests
import urllib.request
from datetime import datetime

def send_telegram_radar(categories_data, telegram_config, audio_file_path=None):
    """
    Send daily digest and audio podcast via Telegram Bot in English.
    """
    if not telegram_config or not telegram_config.get("enabled", False):
        print("[*] Telegram notification is DISABLED (Enable in config.json).")
        return False
        
    bot_token = telegram_config.get("bot_token", "").strip()
    chat_id = telegram_config.get("chat_id", "").strip()
    
    if not bot_token or not chat_id or bot_token == "YOUR_BOT_TOKEN_HERE":
        print("[!] Telegram Bot Token or Chat ID not configured.")
        return False
        
    today = datetime.now().strftime("%B %d, %Y")
    total_repos = sum(cat["count"] for cat in categories_data)
    
    # 1. Text Summary Message
    lines = []
    lines.append(f"📡 <b>GITHUB DAILY RADAR</b> (<code>{today}</code>)")
    lines.append(f"<i>Curated digest of {total_repos} trending open-source projects today:</i>\n")
    
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
            
            velocity_badge = f" <code>{r.get('velocity_badge', '')}</code>" if r.get("velocity_badge") else ""
            lines.append(f"• <a href=\"{r['url']}\"><b>{full_name}</b></a> (⭐ {r['stars_formatted']}){velocity_badge}")
            lines.append(f"  <i>{desc}</i>")
        lines.append("")
        
    lines.append(f"📊 <i>Automatically aggregated &amp; synced to your Excel archive!</i>")
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
                print(f"[+] Sent text summary to Telegram (Chat ID: {chat_id})!")
    except Exception as e:
        print(f"[!] Error sending Telegram text message: {e}")

    # 2. Audio Podcast Voice Note
    if audio_file_path and os.path.exists(audio_file_path):
        print("[*] Uploading Audio Podcast to Telegram...")
        voice_url = f"https://api.telegram.org/bot{bot_token}/sendVoice"
        try:
            with open(audio_file_path, "rb") as f:
                files = {"voice": f}
                data = {
                    "chat_id": chat_id,
                    "caption": f"🎙️ Audio Podcast Digest ({today}) - Listen to today's trending tech!"
                }
                resp = requests.post(voice_url, data=data, files=files, timeout=30)
                if resp.status_code == 200:
                    print(f"[+] Sent Audio Podcast voice note to Telegram successfully!")
                else:
                    audio_url = f"https://api.telegram.org/bot{bot_token}/sendAudio"
                    f.seek(0)
                    files = {"audio": f}
                    resp2 = requests.post(audio_url, data=data, files=files, timeout=30)
                    if resp2.status_code == 200:
                        print(f"[+] Sent Audio file to Telegram successfully!")
        except Exception as e:
            print(f"[!] Error uploading audio to Telegram: {e}")

    return True
