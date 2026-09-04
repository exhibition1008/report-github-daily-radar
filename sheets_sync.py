# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Google Sheets Sync Module
Đồng bộ và đẩy trực tiếp dữ liệu dự án lên Google Sheets qua Webhook / Apps Script.
"""

import json
import urllib.request
from datetime import datetime

def sync_to_google_sheets(categories_data, sheets_config):
    """
    Gửi dữ liệu các repository lên Google Sheets qua Apps Script Webhook.
    """
    if not sheets_config or not sheets_config.get("enabled", False):
        print("[*] Đồng bộ Google Sheets đang TẮT (Bạn có thể bật trong config.json).")
        return False
        
    webhook_url = sheets_config.get("webhook_url", "").strip()
    if not webhook_url or webhook_url == "YOUR_GOOGLE_APPS_SCRIPT_URL_HERE":
        print("[!] Chưa cấu hình URL Google Sheets Webhook trong config.json.")
        return False
        
    today_str = datetime.now().strftime("%Y-%m-%d")
    rows = []
    
    for cat in categories_data:
        cat_name = cat["name"]
        for r in cat["repos"]:
            tags_str = ", ".join(r["topics"])
            row = [
                today_str,
                cat_name,
                r["full_name"],
                r["stars"],
                r["forks"],
                r["language"],
                r["description"],
                tags_str,
                r["url"]
            ]
            rows.append(row)
            
    if not rows:
        print("[*] Không có dữ liệu mới để gửi lên Google Sheets.")
        return True
        
    payload = {
        "action": "append_rows",
        "rows": rows
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            webhook_url, 
            data=data, 
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status in [200, 302]:
                print(f"[+] Đã đồng bộ thành công {len(rows)} dự án lên Google Sheets!")
                return True
    except Exception as e:
        print(f"[!] Lỗi khi đồng bộ lên Google Sheets: {e}")
        return False
