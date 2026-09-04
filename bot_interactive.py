# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Interactive 2-Way Telegram Bot
Intelligent 2-way query bot, archive search engine, and on-demand radar scanner in English.
"""

import os
import sys
import time
import json
import requests
from datetime import datetime

# UTF-8 encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def load_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_archive_repos():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cache_path = os.path.join(base_dir, "cache_radar.json")
    if not os.path.exists(cache_path):
        return []
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_repos = []
            for cat_id, cat_data in data.items():
                for r in cat_data.get("repos", []):
                    r["category_name"] = cat_data.get("category_info", {}).get("name", "")
                    all_repos.append(r)
            return all_repos
    except Exception:
        return []

def send_msg(bot_token, chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[!] Error sending bot message: {e}")

def handle_command(bot_token, chat_id, text):
    text = text.strip()
    cmd = text.split()[0].lower()
    args = text[len(cmd):].strip()

    if cmd in ["/start", "/help"]:
        help_text = (
            "🤖 <b>WELCOME TO GITHUB DAILY RADAR BOT!</b>\n\n"
            "I can help you explore trending open-source projects and discover cutting-edge tools:\n\n"
            "🔍 <b>/find &lt;keyword&gt;</b> : Search repository archive (e.g. <code>/find voice</code>, <code>/find agent</code>)\n"
            "⚡ <b>/scan</b> : Trigger live radar scan immediately\n"
            "🏆 <b>/top</b> : View top 5 highest-starred repositories\n"
            "📊 <b>/stats</b> : View database & archive statistics\n"
            "❓ <b>/help</b> : Show this help message"
        )
        send_msg(bot_token, chat_id, help_text)

    elif cmd == "/find":
        if not args:
            send_msg(bot_token, chat_id, "⚠️ Please enter a keyword to search! Example: <code>/find agent</code> or <code>/find vtuber</code>")
            return
            
        repos = load_archive_repos()
        query = args.lower()
        matched = []
        for r in repos:
            searchable = f"{r.get('full_name', '')} {r.get('description', '')} {' '.join(r.get('topics', []))}".lower()
            if query in searchable:
                matched.append(r)
                
        if not matched:
            send_msg(bot_token, chat_id, f"🔍 No repositories found containing <b>'{args}'</b> in archive database.")
            return

        lines = [f"🎯 <b>Found {len(matched)} matching projects for '{args}':</b>\n"]
        for r in matched[:5]:
            stars = f"{r.get('stargazers_count', 0):,}"
            desc = r.get('description', 'No description')
            if len(desc) > 80: desc = desc[:77] + "..."
            desc = desc.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            full_name = r.get('full_name', '').replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            url = r.get('html_url', '')
            lines.append(f"• <a href=\"{url}\"><b>{full_name}</b></a> (⭐ {stars})")
            lines.append(f"  <i>{desc}</i>\n")

        send_msg(bot_token, chat_id, "\n".join(lines))

    elif cmd == "/top":
        repos = load_archive_repos()
        if not repos:
            send_msg(bot_token, chat_id, "⚠️ Archive is currently empty. Type <code>/scan</code> to populate.")
            return
            
        sorted_repos = sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)[:5]
        lines = ["🏆 <b>TOP 5 HIGHEST-STARRED REPOSITORIES:</b>\n"]
        for idx, r in enumerate(sorted_repos, 1):
            stars = f"{r.get('stargazers_count', 0):,}"
            full_name = r.get('full_name', '')
            url = r.get('html_url', '')
            lines.append(f"<b>#{idx}</b> <a href=\"{url}\"><b>{full_name}</b></a> — ⭐ <b>{stars}</b>")
            lines.append(f"   <i>{r.get('description', '')[:70]}...</i>\n")
        send_msg(bot_token, chat_id, "\n".join(lines))

    elif cmd == "/stats":
        repos = load_archive_repos()
        total = len(repos)
        lines = [
            "📊 <b>GITHUB RADAR DATABASE STATISTICS:</b>",
            f"• Total indexed repositories: <b>{total} repos</b>",
            f"• Excel database archive: <code>reports/github_radar_archive.xlsx</code>",
            f"• Status: 🟢 Fully Operational"
        ]
        send_msg(bot_token, chat_id, "\n".join(lines))

    elif cmd == "/scan":
        send_msg(bot_token, chat_id, "🚀 <b>Triggering live radar scan from GitHub...</b>\nPlease wait ~10 seconds!")
        try:
            from main import run_radar
            run_radar()
        except Exception as e:
            send_msg(bot_token, chat_id, f"❌ Scan error: {e}")
    else:
        send_msg(bot_token, chat_id, "❓ Unknown command. Type <code>/help</code> for available commands.")

def run_interactive_bot():
    config = load_config()
    telegram_cfg = config.get("telegram", {})
    bot_token = telegram_cfg.get("bot_token")
    if not bot_token:
        print("[!] No Bot Token found in config.json.")
        return

    print("=" * 60)
    print("🤖 GITHUB RADAR INTERACTIVE BOT IS RUNNING (LONG-POLLING)...")
    print("   Send /start, /find, /top, /stats to your bot on Telegram!")
    print("=" * 60)

    last_update_id = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{bot_token}/getUpdates?offset={last_update_id + 1}&timeout=30"
            resp = requests.get(url, timeout=35).json()
            if resp.get("ok"):
                for item in resp.get("result", []):
                    last_update_id = item["update_id"]
                    msg = item.get("message", {})
                    chat_id = msg.get("chat", {}).get("id")
                    text = msg.get("text", "")
                    if chat_id and text:
                        print(f"[*] Command received from Chat ID {chat_id}: {text}")
                        handle_command(bot_token, chat_id, text)
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n[+] Bot stopped.")
            break
        except Exception as e:
            print(f"[!] Telegram polling error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    run_interactive_bot()
