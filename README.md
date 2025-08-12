    # Smart-chat-bot
    # 🤖 Emotional AI Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)

Bot percakapan cerdas dengan kemampuan:
- Memahami emosi pengguna 💖
- Memiliki memori berbasis nama 🧠
- Biodata dan kepribadian yang bisa dikustomisasi 🎭
- Bisa belajar dari interaksi 📚

## 🚀 Cara Memulai

### Prasyarat
- Python 3.9+
- [ChromeDriver](https://chromedriver.chromium.org/) (untuk WhatsApp Web)
- Akun [OpenAI API](https://platform.openai.com/)

### Instalasi
1. Clone repositori:
```bash
git clone https://github.com/username/emotional-chatbot.git
cd emotional-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

3. Configure Facebook credentials:
```bash
cp config/.env.example config/.env
# Edit config/.env with your Facebook credentials
```

4. Run the Facebook auto-login:
```bash
python main.py
```

## 📖 Documentation

- **[Setup Guide](docs/SETUP.md)**: Comprehensive setup and usage instructions
- **[API Reference](docs/SETUP.md#-api-reference)**: Detailed API documentation
- **[Troubleshooting](docs/SETUP.md#-troubleshooting)**: Common issues and solutions

## 🔧 Browser Automation Usage

### Basic Example
```python
from src.facebook_automation import ChromeProfileManager, FacebookAutoLogin

# Create profile manager
profile_manager = ChromeProfileManager()

# Create Facebook login handler  
fb_login = FacebookAutoLogin(profile_manager)

# Login to Facebook
result = fb_login.login_to_facebook(
    email="your_email@example.com",
    password="your_password", 
    profile_name="my_profile"
)

print(f"Login successful: {result['success']}")
fb_login.close_browser()
```

### Environment Variables
Set these in your `config/.env` file:
```bash
FACEBOOK_EMAIL=your_email@example.com
FACEBOOK_PASSWORD=your_password_here
```

## 🛡️ Security & Compliance

- **No Hardcoded Credentials**: Uses environment variables for security
- **Isolated Profiles**: Each browser session is completely isolated
- **Terms of Service**: Please ensure compliance with Facebook's Terms of Service
- **Ethical Use**: Use automation responsibly and respect rate limits

## 🌍 Cross-Platform Support

This solution works on:
- ✅ Windows 10/11
- ✅ macOS (Intel & Apple Silicon)
- ✅ Linux (Ubuntu, Debian, etc.)

## 📁 Project Structure

```
Smart-chat-bot/
├── src/
│   └── facebook_automation.py    # Main automation module
├── config/
│   └── .env.example             # Configuration template
├── docs/
│   └── SETUP.md                 # Comprehensive documentation
├── main.py                      # Example usage script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and automation purposes. Users are responsible for:
- Complying with Facebook's Terms of Service
- Using their own legitimate accounts
- Respecting rate limits and ethical guidelines
- Ensuring proper security of their credentials
