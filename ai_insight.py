# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - AI Insight Module (Fast & Smart)
Analyze practical applications, real-world use cases, and extract quick start commands in English.
"""

import re
import urllib.request

def fetch_repo_readme(full_name):
    """Fast fetch of README with 2-second timeout"""
    url = f"https://raw.githubusercontent.com/{full_name}/main/README.md"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GitHub-Daily-Radar"})
        with urllib.request.urlopen(req, timeout=2) as resp:
            if resp.status == 200:
                return resp.read().decode("utf-8", errors="ignore")[:3000]
    except Exception:
        pass
    return ""

def extract_quick_start(full_name, readme_text):
    """Extract fast installation command or fallback to clean clone command"""
    if readme_text:
        patterns = [
            r"(pip install [a-zA-Z0-9_\-\.]+)",
            r"(npm install [a-zA-Z0-9_\-\./@]+)",
            r"(docker run [^\n]{5,50})",
            r"(cargo install [a-zA-Z0-9_\-\.]+)"
        ]
        for p in patterns:
            match = re.search(p, readme_text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
    return f"git clone https://github.com/{full_name}.git"

def generate_ai_insight(repo_item, fetch_online=False):
    """Analyze high-value practical use cases in English"""
    full_name = repo_item["full_name"]
    topics = repo_item.get("topics", [])
    
    readme = fetch_repo_readme(full_name) if fetch_online else ""
    quick_start = extract_quick_start(full_name, readme)

    text_corpus = f"{full_name} {' '.join(topics)} {repo_item.get('description', '')}".lower()
    
    if any(k in text_corpus for k in ["agent", "agency", "hermes", "autonomous"]):
        use_case = "Build Autonomous AI Agents & Multi-Agent Workflows"
    elif any(k in text_corpus for k in ["vtuber", "live2d", "voice", "waifu", "kalidokit"]):
        use_case = "Create Virtual Companions, VTubers & Voice-Driven Characters"
    elif any(k in text_corpus for k in ["cli", "terminal", "tool", "graph", "developer-tools"]):
        use_case = "Developer Productivity, AST Code Intelligence & Terminal Tools"
    elif any(k in text_corpus for k in ["llm", "rag", "vlm", "ollama", "tts"]):
        use_case = "Deploy Large Language Models, RAG Pipelines & Audio Vision Systems"
    else:
        use_case = "Open-Source AI Tooling & Workflow Automation"

    return {
        "use_case": use_case,
        "quick_start": quick_start
    }

def enrich_repos_with_insights(categories_data):
    """Enrich all repositories with AI insights"""
    for cat in categories_data:
        for idx, r in enumerate(cat["repos"]):
            fetch_online = (idx < 2)
            r["ai_insight"] = generate_ai_insight(r, fetch_online=fetch_online)
    return categories_data
