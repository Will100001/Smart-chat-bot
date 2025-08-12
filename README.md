    # Smart-chat-bot
    # 🤖 Emotional AI Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)

Bot percakapan cerdas dengan kemampuan:
- Memahami emosi pengguna 💖
- Memiliki memori berbasis nama 🧠
- Biodata dan kepribadian yang bisa dikustomisasi 🎭
- Bisa belajar dari interaksi 📚
- **NEW: Webhook-based Chrome browser automation** 🌐

## ⭐ New Feature: Webhook Browser Controller

This repository now includes a powerful webhook-based Chrome browser automation system that allows you to:

- 🌐 Control Chrome browser remotely via HTTP webhooks
- 🔗 Open URLs programmatically
- 👆 Click buttons and elements on web pages
- ✏️ Fill out forms automatically
- 🔄 Execute complex automation sequences
- 🔐 Secure token-based authentication

**Quick Start for Browser Automation:**
```bash
# Install dependencies
pip install -r requirements.txt

# Start the webhook server
python main.py

# Test with the example script
python examples/test_webhook.py
```

📖 **[Read the complete Browser Automation Documentation →](README_WEBHOOK.md)**

## 🚀 Cara Memulai

### Prasyarat
- Python 3.9+
- [ChromeDriver](https://chromedriver.chromium.org/) (untuk WhatsApp Web dan Browser Automation)
- Akun [OpenAI API](https://platform.openai.com/) (untuk chatbot features)

### Instalasi
1. Clone repositori:
```bash
git clone https://github.com/Will100001/Smart-chat-bot.git
cd Smart-chat-bot
