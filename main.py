# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Main Entry Point (Ultimate Edition)
Run discovery scan, calculate velocity, extract AI insights, export HTML/Excel/Markdown, synthesize Audio Podcast, and notify Telegram/Google Sheets.
"""

import os
import sys
import json
import argparse
import webbrowser
from datetime import datetime

# UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from fetcher import fetch_all_categories
from formatter import process_radar_data
from velocity_tracker import track_and_enrich_velocity
from ai_insight import enrich_repos_with_insights
from reporter import generate_markdown, generate_html
from excel_exporter import append_or_update_excel
from telegram_notifier import send_telegram_radar
from sheets_sync import sync_to_google_sheets
from audio_podcast import generate_audio_podcast

def load_config(config_path):
    if not os.path.exists(config_path):
        print(f"[!] Config file not found at {config_path}")
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_radar():
    parser = argparse.ArgumentParser(description="GitHub Daily Radar - Discover Trending Open-Source Projects")
    parser.add_argument("--no-open", action="store_true", help="Do not open browser automatically after generation")
    parser.add_argument("--token", type=str, default=None, help="GitHub Personal Access Token (optional, raises rate limit)")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
    reports_dir = os.path.join(base_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    print("=" * 60)
    print("       🚀 STARTING GITHUB DAILY RADAR (ULTIMATE EDITION)      ")
    print("=" * 60)

    config = load_config(config_path)
    
    # 1. Fetch data from GitHub
    raw_data = fetch_all_categories(config, github_token=args.token)
    
    # 2. Process and structure data
    print("\n[*] Structuring repository data...")
    processed_data = process_radar_data(raw_data)

    # 3. Calculate Star Velocity Tracker 🔥
    print("\n[*] 📈 Analyzing Star Velocity & Growth Delta...")
    processed_data = track_and_enrich_velocity(processed_data)

    # 4. Extract AI Deep Insights & Quick Start 🧠
    print("\n[*] 🧠 Extracting AI Insights & Quick-Start Commands...")
    processed_data = enrich_repos_with_insights(processed_data)
    
    # 5. Export Markdown & HTML reports (and root index.html for GitHub Pages)
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

    # 6. Generate Audio Podcast 🎙️
    audio_path = None
    if settings.get("generate_podcast", True):
        print("\n[*] 🎙️ Synthesizing Tech Morning Audio Podcast...")
        audio_path = generate_audio_podcast(processed_data, audio_file)

    # 7. Send Telegram Notification & Voice Note 📱
    print("\n[*] 📱 Checking Telegram notification configuration...")
    send_telegram_radar(processed_data, config.get("telegram", {}), audio_file_path=audio_path)

    # 8. Save and update cumulative Excel Archive 📊
    if settings.get("export_excel", True):
        print("\n[*] 📊 Syncing to Excel Archive database...")
        append_or_update_excel(processed_data, excel_file)

    # 9. Sync to Google Sheets Online ☁️
    print("\n[*] ☁️ Checking Google Sheets sync...")
    sync_to_google_sheets(processed_data, config.get("google_sheets", {}))
        
    print("\n" + "=" * 60)
    print("✅ RADAR PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"   📄 Markdown: {md_file}")
    print(f"   🌐 HTML Dashboard: {html_file}")
    print(f"   📊 Excel Archive: {excel_file}")
    if audio_path:
        print(f"   🎙️ Audio Podcast: {audio_path}")
    print(f"   🌐 GitHub Pages: index.html")
    print("=" * 60)

    # 10. Open Dashboard in browser
    if not args.no_open and settings.get("auto_open_browser", False):
        print("\n[+] Opening Web Dashboard in your browser...")
        webbrowser.open(f"file:///{os.path.abspath(html_file)}")

if __name__ == "__main__":
    run_radar()
