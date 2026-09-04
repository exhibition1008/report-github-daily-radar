# -*- coding: utf-8 -*-
"""
GitHub Daily Radar - Audio Podcast Module
Tạo kịch bản radio sinh động và sinh file âm thanh đọc bản tin công nghệ.
"""

import os
from datetime import datetime
from gtts import gTTS

def create_podcast_script(categories_data):
    """
    Tạo kịch bản bản tin radio tự nhiên, hào hứng bằng tiếng Việt.
    """
    today_str = datetime.now().strftime("%d tháng %m")
    total_repos = sum(cat["count"] for cat in categories_data)
    
    script_lines = []
    script_lines.append(f"Chào bạn! Đây là bản tin radio công nghệ GitHub Daily Radar ngày {today_str}.")
    script_lines.append(f"Hôm nay, cộng đồng mã nguồn mở thế giới có tổng cộng {total_repos} dự án nổi bật vừa được cập nhật.")
    
    for cat in categories_data:
        if not cat["repos"]:
            continue
        cat_clean_name = cat["name"].split(")")[-1].strip() if ")" in cat["name"] else cat["name"]
        cat_clean_name = cat_clean_name.replace("🤖", "").replace("✨", "").replace("🛠️", "").replace("🔥", "").strip()
        
        script_lines.append(f"Ở mục {cat_clean_name}:")
        top_items = cat["repos"][:2]
        for idx, r in enumerate(top_items, 1):
            name = r["name"]
            stars = r["stars_formatted"]
            desc = r["description"]
            # Rút gọn mô tả
            if len(desc) > 90:
                desc = desc[:87] + "..."
            script_lines.append(f"Dự án số {idx} là {name}, đạt {stars} lượt yêu thích. Với mô tả: {desc}.")
            
    script_lines.append("Toàn bộ thông tin chi tiết và file Excel đã được gửi vào tin nhắn của bạn. Chúc bạn một ngày lập trình đầy cảm hứng!")
    return " ".join(script_lines)

def generate_audio_podcast(categories_data, output_path=None):
    """
    Sinh file MP3 từ kịch bản radio.
    """
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "reports", "daily_podcast.mp3")
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print("[*] Đang tạo kịch bản radio công nghệ...")
    script_text = create_podcast_script(categories_data)
    
    print("[*] Đang tổng hợp giọng đọc AI (Text-to-Speech)...")
    try:
        tts = gTTS(text=script_text, lang="vi", slow=False)
        tts.save(output_path)
        print(f"[+] Đã tạo file Audio Podcast thành công: {output_path}")
        return output_path
    except Exception as e:
        print(f"[!] Lỗi khi sinh âm thanh podcast: {e}")
        return None
