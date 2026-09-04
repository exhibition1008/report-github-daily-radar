# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Formatter Module
Format, sanitize and structure repository metadata in English.
"""

from datetime import datetime

LANGUAGE_COLORS = {
    "Python": "#3572A5",
    "TypeScript": "#3178C6",
    "JavaScript": "#F1E05A",
    "Rust": "#DEA584",
    "Go": "#00ADD8",
    "C++": "#F34B7D",
    "C#": "#178600",
    "HTML": "#E34C26",
    "Jupyter Notebook": "#DA5B0B",
    "Shell": "#89E051"
}

def format_number(num):
    """Format star and fork numbers cleanly (e.g. 12.5k)"""
    if num >= 1000:
        return f"{num/1000:.1f}k"
    return str(num)

def format_repo_item(item):
    """Format single repository item into normalized structure"""
    name = item.get("name", "")
    full_name = item.get("full_name", "")
    html_url = item.get("html_url", "")
    description = item.get("description") or "No description provided by author."
    stars = item.get("stargazers_count", 0)
    forks = item.get("forks_count", 0)
    language = item.get("language") or "N/A"
    topics = item.get("topics", [])
    owner = item.get("owner", {})
    owner_login = owner.get("login", "")
    owner_avatar = owner.get("avatar_url", "")
    created_at = item.get("created_at", "")[:10]
    updated_at = item.get("updated_at", "")[:10]
    
    lang_color = LANGUAGE_COLORS.get(language, "#8b949e")
    
    return {
        "name": name,
        "full_name": full_name,
        "url": html_url,
        "description": description,
        "stars": stars,
        "stars_formatted": format_number(stars),
        "forks": forks,
        "forks_formatted": format_number(forks),
        "language": language,
        "lang_color": lang_color,
        "topics": topics[:5],
        "owner_login": owner_login,
        "owner_avatar": owner_avatar,
        "created_at": created_at,
        "updated_at": updated_at
    }

def process_radar_data(raw_results):
    """Transform raw fetch results into processed data"""
    processed = []
    for cat_id, data in raw_results.items():
        cat_info = data["category_info"]
        items = data["repos"]
        formatted_repos = [format_repo_item(item) for item in items]
        processed.append({
            "id": cat_id,
            "name": cat_info["name"],
            "repos": formatted_repos,
            "count": len(formatted_repos)
        })
    return processed
