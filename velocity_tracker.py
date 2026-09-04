# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Velocity Tracker Module
Đo lường tốc độ tăng trưởng số sao (Star Velocity) của các repository theo ngày.
"""

import os
import json
from datetime import datetime

def get_velocity_cache_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "cache_velocity.json")

def load_velocity_cache():
    cache_path = get_velocity_cache_path()
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_velocity_cache(cache_data):
    cache_path = get_velocity_cache_path()
    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def track_and_enrich_velocity(categories_data):
    """
    Tính toán delta số sao so với lần quét gần nhất và gắn nhãn huy hiệu tăng trưởng.
    """
    cache = load_velocity_cache()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    for cat in categories_data:
        for r in cat["repos"]:
            full_name = r["full_name"]
            current_stars = r["stars"]
            
            repo_history = cache.get(full_name, {})
            last_recorded_stars = repo_history.get("last_stars")
            last_date = repo_history.get("last_date")
            
            if last_recorded_stars is not None and last_date != today_str:
                delta = current_stars - last_recorded_stars
                if delta > 0:
                    r["star_growth"] = delta
                    r["star_growth_formatted"] = f"+{delta:,}"
                else:
                    r["star_growth"] = 0
                    r["star_growth_formatted"] = "0"
            else:
                # Lần đầu phát hiện
                r["star_growth"] = 0
                r["star_growth_formatted"] = "Mới"

            # Gán huy hiệu tăng trưởng (Velocity Badge)
            growth = r["star_growth"]
            if growth >= 1000:
                r["velocity_badge"] = "🔥 Siêu tân tinh (+1000⭐)"
                r["velocity_class"] = "badge-supernova"
            elif growth >= 300:
                r["velocity_badge"] = "⚡ Bứt phá (+300⭐)"
                r["velocity_class"] = "badge-hot"
            elif growth > 0:
                r["velocity_badge"] = f"📈 Tăng {r['star_growth_formatted']}⭐"
                r["velocity_class"] = "badge-growing"
            else:
                r["velocity_badge"] = "✨ Nổi bật"
                r["velocity_class"] = "badge-normal"

            # Cập nhật cache
            cache[full_name] = {
                "last_stars": current_stars,
                "last_date": today_str
            }
            
    save_velocity_cache(cache)
    return categories_data
