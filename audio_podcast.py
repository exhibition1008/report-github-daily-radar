# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Audio Podcast Module
Generate conversational tech morning radio script and synthesize audio digest in English.
"""

import os
from datetime import datetime
from gtts import gTTS

def create_podcast_script(categories_data):
    """
    Generate natural, energetic tech morning show script in English.
    """
    today_str = datetime.now().strftime("%B %d, %Y")
    total_repos = sum(cat["count"] for cat in categories_data)
    
    script_lines = []
    script_lines.append(f"Hello! Welcome to the GitHub Daily Radar Tech Morning Digest for {today_str}.")
    script_lines.append(f"Today, the global open-source community has {total_repos} trending projects making waves.")
    
    for cat in categories_data:
        if not cat["repos"]:
            continue
        cat_clean_name = cat["name"].split(")")[-1].strip() if ")" in cat["name"] else cat["name"]
        cat_clean_name = cat_clean_name.replace("🤖", "").replace("✨", "").replace("🛠️", "").replace("🔥", "").strip()
        
        script_lines.append(f"In the category of {cat_clean_name}:")
        top_items = cat["repos"][:2]
        for idx, r in enumerate(top_items, 1):
            name = r["name"]
            stars = r["stars_formatted"]
            desc = r["description"]
            if len(desc) > 90:
                desc = desc[:87] + "..."
            script_lines.append(f"Project number {idx} is {name}, boasting {stars} stars. Featuring: {desc}.")
            
    script_lines.append("Full insights and the Excel database have been updated. Have an inspired and productive day of coding!")
    return " ".join(script_lines)

def generate_audio_podcast(categories_data, output_path=None):
    """
    Synthesize MP3 audio podcast in English.
    """
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "reports", "daily_podcast.mp3")
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print("[*] Generating English tech morning show radio script...")
    script_text = create_podcast_script(categories_data)
    
    print("[*] Synthesizing AI Voice Podcast (Text-to-Speech)...")
    try:
        tts = gTTS(text=script_text, lang="en", tld="com", slow=False)
        tts.save(output_path)
        print(f"[+] Audio Podcast generated successfully: {output_path}")
        return output_path
    except Exception as e:
        print(f"[!] Error generating audio podcast: {e}")
        return None
