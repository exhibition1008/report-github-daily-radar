# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Main Entry Point
Chạy công cụ quét, xuất báo cáo Markdown/HTML/Excel, sinh file Audio Podcast, gửi Telegram và đồng bộ Google Sheets.
"""

import os
import sys
import json
import argparse
import webbrowser
from datetime import datetime

# Đảm bảo UTF-8 trên Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from fetcher import fetch_all_categories
from formatter import process_radar_data
from reporter import generate_markdown, generate_html
from excel_exporter import append_or_update_excel
from telegram_notifier import send_telegram_radar
from sheets_sync import sync_to_google_sheets
from audio_podcast import generate_audio_podcast

def load_config(config_path):
    if not os.path.exists(config_path):
        print(f"[!] Không tìm thấy file config tại {config_path}")
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_radar():
    parser = argparse.ArgumentParser(description="GitHub Daily Radar - Săn dự án hot hàng ngày")
    parser.add_argument("--no-open", action="store_true", help="Không tự động mở trình duyệt sau khi tạo báo cáo")
    parser.add_argument("--token", type=str, default=None, help="GitHub Personal Access Token (tùy chọn để tăng rate limit)")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
    reports_dir = os.path.join(base_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    print("=" * 60)
    print("       🚀 KHỞI ĐỘNG GITHUB DAILY RADAR (DISCOVERY TOOL)       ")
    print("=" * 60)

    config = load_config(config_path)
    
    # 1. Fetch dữ liệu từ GitHub
    raw_data = fetch_all_categories(config, github_token=args.token)
    
    # 2. Xử lý và format dữ liệu
    print("\n[*] Đang tổng hợp và phân loại dự án...")
    processed_data = process_radar_data(raw_data)
    
    # 3. Xuất file báo cáo Markdown & HTML
    date_str = datetime.now().strftime("%Y-%m-%d")
    md_file = os.path.join(reports_dir, f"radar_{date_str}.md")
    html_file = os.path.join(reports_dir, f"radar_{date_str}.html")
    excel_file = os.path.join(reports_dir, "github_radar_archive.xlsx")
    audio_file = os.path.join(reports_dir, f"podcast_{date_str}.mp3")
    
    settings = config.get("settings", {})
    if settings.get("export_markdown", True):
        generate_markdown(processed_data, md_file)
        
    if settings.get("export_html", True):
        generate_html(processed_data, html_file)

    # 4. Sinh file âm thanh Audio Podcast
    audio_path = None
    if settings.get("generate_podcast", True):
        print("\n[*] Đang tổng hợp bản tin Radio Audio Podcast...")
        audio_path = generate_audio_podcast(processed_data, audio_file)

    # 5. Gửi tin nhắn và file Voice qua Telegram Bot
    print("\n[*] Đang kiểm tra cấu hình Telegram...")
    send_telegram_radar(processed_data, config.get("telegram", {}), audio_file_path=audio_path)

    # 6. Lưu và cập nhật lũy tiến vào file Excel Offline
    if settings.get("export_excel", True):
        print("\n[*] Đang đồng bộ và lưu trữ vào cơ sở dữ liệu Excel (Offline)...")
        append_or_update_excel(processed_data, excel_file)

    # 7. Đồng bộ lên Google Sheets Online
    print("\n[*] Đang kiểm tra cấu hình Google Sheets Online...")
    sync_to_google_sheets(processed_data, config.get("google_sheets", {}))
        
    print("\n" + "=" * 60)
    print("✅ HOÀN THÀNH TOÀN BỘ QUY TRÌNH!")
    print(f"   📄 Markdown: {md_file}")
    print(f"   🌐 HTML Dashboard: {html_file}")
    print(f"   📊 Excel Archive: {excel_file}")
    if audio_path:
        print(f"   🎙️ Audio Podcast: {audio_path}")
    print("=" * 60)

    # 8. Tự động mở Dashboard (nếu bật)
    if not args.no_open and settings.get("auto_open_browser", False):
        print("\n[+] Đang mở Web Dashboard trên trình duyệt của bạn...")
        webbrowser.open(f"file:///{os.path.abspath(html_file)}")

if __name__ == "__main__":
    run_radar()
