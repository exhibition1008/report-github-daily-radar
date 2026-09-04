# 📡 GitHub Daily Radar (Ultimate Edition)

Automated discovery engine that tracks, analyzes, stores, and broadcasts trending open-source GitHub repositories across **AI Agents, Sci-Fi Assistants (JARVIS), Anime/VTuber AI, Developer Tools, and Frontier LLMs**.

---

## ✨ Key Features

- 🤖 **Smart Radar Discovery:** Scrapes and filters fastest-growing repositories on GitHub.
- 📈 **Star Velocity Tracker:** Measures daily star growth rate and awards badges (`🔥 Supernova`, `⚡ Breakout`, `📈 Trending`).
- 🧠 **AI Deep Insights & Quick Start:** Extracts practical use cases and 10-second setup commands.
- 🎙️ **Daily Audio Podcast:** Synthesizes an English morning show radio digest (`.mp3`) delivered right to your headphones.
- 📱 **2-Way Interactive Telegram Bot:** Query your repository archive (`/find agent`, `/top`, `/stats`, `/scan`) on demand via `@Artifykit_bot`.
- 📊 **Cumulative Excel Database (`.xlsx`):** Automatically appends new projects and updates stars without duplicates.
- ☁️ **Google Sheets Sync:** Real-time cloud sync to your custom Google Sheet via Webhook.
- 🌐 **GitHub Pages Auto-Deploy:** Instant dark-mode web dashboard hosted free at `https://<username>.github.io/github-daily-radar`.

---

## 🚀 Quick Start

### 1. Run Manually:
```bash
python main.py
```

### 2. Run Interactive Telegram Bot:
```bash
python bot_interactive.py
```
*Send `/start`, `/find voice`, `/top`, or `/scan` to your bot on Telegram!*

### 3. Command Line Options:
- Run without opening browser:
  ```bash
  python main.py --no-open
  ```
- Use GitHub Token for higher rate limits:
  ```bash
  python main.py --token your_github_personal_token
  ```

---

## ⚙️ Configuration (`config.json`)

```json
{
  "categories": [
    {
      "id": "ai_agents_scifi",
      "name": "🤖 AI Agents & Sci-Fi Assistants (JARVIS)",
      "query": "ai-agent OR jarvis",
      "min_stars": 30,
      "limit": 6
    }
  ],
  "settings": {
    "export_html": true,
    "export_markdown": true,
    "export_excel": true,
    "generate_podcast": true
  },
  "telegram": {
    "enabled": true,
    "bot_token": "YOUR_BOT_TOKEN_HERE",
    "chat_id": "YOUR_CHAT_ID_HERE"
  },
  "google_sheets": {
    "enabled": false,
    "webhook_url": "YOUR_WEBHOOK_URL_HERE"
  }
}
```

---

## 🤖 24/7 Automation via GitHub Actions

This repository includes a pre-configured workflow in `.github/workflows/daily-radar.yml` that runs every morning at **00:00 UTC (7:00 AM VN time)**:
1. Runs the radar scan.
2. Synthesizes and broadcasts the audio podcast to Telegram.
3. Commits updated Excel and Markdown archives.
4. Automatically deploys the latest HTML dashboard to **GitHub Pages**.
