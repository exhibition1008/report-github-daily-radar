# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Fetcher Module
Thu thập các repository thịnh hành theo chủ đề từ GitHub API có cache và delay an toàn.
"""

import os
import time
import json
import urllib.request
import urllib.parse

def get_cache_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "cache_radar.json")

def load_cache():
    cache_path = get_cache_path()
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_cache(data):
    cache_path = get_cache_path()
    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def fetch_category_repos(category_config, settings, github_token=None):
    """
    Lấy danh sách các repo hot theo danh mục.
    """
    base_query = category_config["query"]
    min_stars = category_config.get("min_stars", 10)
    limit = category_config.get("limit", 6)
    
    full_query = f"{base_query} stars:>={min_stars}"
    
    params = {
        "q": full_query,
        "sort": settings.get("sort_by", "stars"),
        "order": settings.get("order", "desc"),
        "per_page": limit
    }
    
    url = f"https://api.github.com/search/repositories?{urllib.parse.urlencode(params)}"
    
    headers = {
        "User-Agent": "GitHub-Daily-Radar/1.0",
        "Accept": "application/vnd.github.v3+json"
    }
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"
        
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                items = data.get("items", [])
                return items
    except Exception as e:
        print(f"[!] Lỗi khi gọi GitHub API ('{category_config['name']}'): {e}")
        return None

def fetch_all_categories(config, github_token=None):
    """
    Lấy dữ liệu cho tất cả các danh mục được cấu hình, có fallback cache thông minh.
    """
    results = {}
    cache = load_cache()
    categories = config.get("categories", [])
    settings = config.get("settings", {})
    
    for i, cat in enumerate(categories):
        print(f"[*] Đang quét danh mục ({i+1}/{len(categories)}): {cat['name']}...")
        repos = fetch_category_repos(cat, settings, github_token)
        
        # Nếu gặp lỗi / rate limit, lấy từ cache nếu có
        if repos is None:
            if cat["id"] in cache:
                print(f"    -> Dùng dữ liệu cache gần nhất cho danh mục này.")
                repos = cache[cat["id"]].get("repos", [])
            else:
                repos = []
        else:
            # Lưu vào cache
            cache[cat["id"]] = {
                "category_info": cat,
                "repos": repos
            }
            
        results[cat["id"]] = {
            "category_info": cat,
            "repos": repos
        }
        print(f"    -> Tìm thấy {len(repos)} dự án nổi bật.")
        time.sleep(1.2) # Tránh rate limit của GitHub
        
    save_cache(cache)
    return results
