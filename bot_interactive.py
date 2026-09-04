# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Interactive 2-Way Telegram Bot
Bot tra cứu thông minh, tương tác 2 chiều và quét dữ liệu theo yêu cầu.
"""

import os
import sys
import time
import json
import requests
from datetime import datetime

# Đảm bảo UTF-8 trên Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def load_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_archive_repos():
    """Đọc dữ liệu từ cache radar gần nhất"""
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
        print(f"[!] Lỗi gửi tin nhắn bot: {e}")

def handle_command(bot_token, chat_id, text):
    text = text.strip()
    cmd = text.split()[0].lower()
    args = text[len(cmd):].strip()

    if cmd in ["/start", "/help"]:
        help_text = (
            "🤖 <b>CHÀO MỪNG ĐẾN VỚI GITHUB DAILY RADAR BOT!</b>\n\n"
            "Tôi có thể giúp bạn tra cứu các dự án mã nguồn mở và cập nhật công nghệ mới:\n\n"
            "🔍 <b>/find &lt;từ_khóa&gt;</b> : Tra cứu repo trong kho (VD: <code>/find voice</code>, <code>/find agent</code>)\n"
            "⚡ <b>/scan</b> : Kích hoạt quét radar ngay lập tức\n"
            "🏆 <b>/top</b> : Xem top 5 dự án nhiều sao nhất trong kho\n"
            "📊 <b>/stats</b> : Thống kê kho dữ liệu hiện tại\n"
            "❓ <b>/help</b> : Xem lại hướng dẫn này"
        )
        send_msg(bot_token, chat_id, help_text)

    elif cmd == "/find":
        if not args:
            send_msg(bot_token, chat_id, "⚠️ Vui lòng nhập từ khóa cần tìm! Ví dụ: <code>/find agent</code> hoặc <code>/find vtuber</code>")
            return
            
        repos = load_archive_repos()
        query = args.lower()
        matched = []
        for r in repos:
            searchable = f"{r.get('full_name', '')} {r.get('description', '')} {' '.join(r.get('topics', []))}".lower()
            if query in searchable:
                matched.append(r)
                
        if not matched:
            send_msg(bot_token, chat_id, f"🔍 Không tìm thấy dự án nào chứa từ khóa <b>'{args}'</b> trong kho dữ liệu.")
            return

        lines = [f"🎯 <b>Tìm thấy {len(matched)} dự án phù hợp với '{args}':</b>\n"]
        for r in matched[:5]:
            stars = f"{r.get('stargazers_count', 0):,}"
            desc = r.get('description', 'Không có mô tả')
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
            send_msg(bot_token, chat_id, "⚠️ Kho dữ liệu đang trống, hãy gõ <code>/scan</code> để quét ngay.")
            return
            
        # Sắp xếp theo stars giảm dần
        sorted_repos = sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)[:5]
        lines = ["🏆 <b>TOP 5 DỰ ÁN ĐỈNH CAO NHẤT TRONG KHO:</b>\n"]
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
            "📊 <b>THỐNG KÊ KHO DỮ LIỆU GITHUB RADAR:</b>",
            f"• Tổng số dự án đã lưu: <b>{total} repos</b>",
            f"• File Excel lưu trữ: <code>reports/github_radar_archive.xlsx</code>",
            f"• Tình trạng: 🟢 Đang hoạt động bình thường"
        ]
        send_msg(bot_token, chat_id, "\n".join(lines))

    elif cmd == "/scan":
        send_msg(bot_token, chat_id, "🚀 <b>Đang kích hoạt quét radar mới nhất từ GitHub...</b>\nVui lòng đợi khoảng 10 giây!")
        try:
            from main import run_radar
            run_radar()
        except Exception as e:
            send_msg(bot_token, chat_id, f"❌ Lỗi khi quét: {e}")
    else:
        send_msg(bot_token, chat_id, "❓ Lệnh không hợp lệ. Gõ <code>/help</code> để xem danh sách lệnh.")

def run_interactive_bot():
    config = load_config()
    telegram_cfg = config.get("telegram", {})
    bot_token = telegram_cfg.get("bot_token")
    if not bot_token:
        print("[!] Không tìm thấy Bot Token trong config.json.")
        return

    print("=" * 60)
    print("🤖 GITHUB RADAR INTERACTIVE BOT ĐANG CHẠY (LONG-POLLING)...")
    print("   Nhắn tin /start, /find, /top, /stats cho bot trên Telegram!")
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
                        print(f"[*] Nhận lệnh từ Chat ID {chat_id}: {text}")
                        handle_command(bot_token, chat_id, text)
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n[+] Đã dừng Bot.")
            break
        except Exception as e:
            print(f"[!] Lỗi kết nối Telegram polling: {e}")
            time.sleep(3)

if __name__ == "__main__":
    run_interactive_bot()
