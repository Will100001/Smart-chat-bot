# 🤖 Smart Facebook Messenger Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)

An intelligent browser automation chatbot that interacts with Facebook Messenger. The bot can automatically log in, read messages, and send personalized auto-replies based on keywords and predefined rules.

## ✨ Features

- 🔐 **Automated Facebook Login** - Secure login to Facebook Messenger
- 📨 **Message Reading** - Real-time monitoring of incoming messages  
- 🤖 **Smart Auto-Replies** - Keyword-based automated responses
- ⚙️ **Customizable Rules** - Flexible configuration for different scenarios
- 🌐 **Browser Compatibility** - Works with Chrome, Bitbrowser, and other Chrome-based browsers
- 🕵️ **Stealth Mode** - Undetected browser automation to avoid detection
- 📊 **Conversation Management** - Handle multiple conversations
- ⏱️ **Human-like Timing** - Realistic response delays

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Chrome browser installed
- Facebook account credentials

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Will100001/Smart-chat-bot.git
cd Smart-chat-bot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up credentials:**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Facebook credentials
FACEBOOK_EMAIL=your_facebook_email@example.com
FACEBOOK_PASSWORD=your_facebook_password
```

4. **Run the basic example:**
```bash
python examples/basic_usage.py
```

## 📖 Usage Guide

### Basic Usage

```python
from src.facebook_messenger_bot import FacebookMessengerBot

# Create bot instance
bot = FacebookMessengerBot(headless=False)

# Start browser and login
bot.start_browser()
bot.login_to_facebook()

# Monitor messages and send auto-replies
bot.monitor_messages(conversation_name="Friend Name", duration=300)

# Cleanup
bot.close()
```

### Advanced Configuration

Create a custom configuration file:

```python
from src.config import BotConfig

config = BotConfig()

# Add custom auto-reply keywords
config.add_auto_reply("hello", [
    "Hi! How can I help you today? 😊",
    "Hello there! What's up?"
])

config.add_auto_reply("help", [
    "I'm here to assist you!",
    "What do you need help with?"
])

# Save configuration
config.save_config('my_config.yaml')

# Use with bot
bot = FacebookMessengerBot(config_file='my_config.yaml')
```

## ⚙️ Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FACEBOOK_EMAIL` | Your Facebook email | Required |
| `FACEBOOK_PASSWORD` | Your Facebook password | Required |
| `HEADLESS` | Run browser in headless mode | `false` |
| `BITBROWSER_PORT` | Port for Bitbrowser connection | None |

### Bot Configuration

The bot supports extensive configuration through YAML files or programmatically:

```yaml
facebook:
  email: "your_email@example.com"
  password: "your_password"
  messenger_url: "https://www.messenger.com/"
  login_timeout: 30
  message_check_interval: 5

selenium:
  headless: false
  window_size: [1920, 1080]
  user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  implicit_wait: 10
  page_load_timeout: 30
  bitbrowser_port: null

auto_replies:
  enabled: true
  keywords:
    hello: ["Hi there!", "Hello! How can I help?"]
    help: ["I'm here to assist you!", "What do you need?"]
    thanks: ["You're welcome!", "Happy to help!"]
    bye: ["Goodbye!", "See you later!"]
  default_reply: ["Thanks for your message!"]
  delay_range: [1, 3]
```

## 🔧 Browser Compatibility

### Chrome (Default)
The bot works out of the box with Chrome:
```python
bot = FacebookMessengerBot()  # Uses Chrome automatically
```

### Bitbrowser
For Bitbrowser compatibility:
```python
# Set Bitbrowser port in environment or config
os.environ['BITBROWSER_PORT'] = '9222'
bot = FacebookMessengerBot()
```

### Custom Browser Path
```python
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = "/path/to/your/browser"
# Pass options to bot if needed
```

## 🛡️ Security & Best Practices

### 1. Credentials Security
- Never commit credentials to version control
- Use environment variables or encrypted config files
- Consider using app-specific passwords

### 2. Rate Limiting
- The bot includes human-like delays between actions
- Avoid sending too many messages too quickly
- Monitor for Facebook's rate limiting

### 3. Account Safety
- Use a dedicated Facebook account for automation
- Enable 2FA but handle it manually when needed
- Be aware of Facebook's Terms of Service

### 4. Stealth Features
The bot includes several anti-detection features:
- Undetected ChromeDriver
- Human-like typing and delays
- Realistic user agent strings
- Random response timing

## 🚨 Troubleshooting

### Common Issues

**1. Login Failed**
```
❌ Login failed - check credentials or handle 2FA/captcha
```
- Verify your email and password
- Handle 2FA manually in the browser
- Check if your account is temporarily locked

**2. No Conversations Found**
```
⚠️ No conversations found
```
- Open Facebook Messenger manually first
- Start a conversation to have something to monitor
- Check if the page loaded correctly

**3. Browser Won't Start**
```
❌ Failed to start browser
```
- Ensure Chrome is installed
- Check if ChromeDriver is accessible
- Try running with `headless=False` to see what's happening

**4. Messages Not Detected**
```
Found 0 message elements
```
- Facebook may have changed their HTML structure
- Try refreshing the page manually
- Check browser console for errors

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

bot = FacebookMessengerBot()
```

## 📝 Examples

### Example 1: Customer Service Bot
```python
from src.facebook_messenger_bot import FacebookMessengerBot
from src.config import BotConfig

# Setup customer service responses
config = BotConfig()
config.add_auto_reply("business hours", [
    "We're open Monday-Friday 9AM-5PM! 🕘"
])
config.add_auto_reply("support", [
    "I'll connect you with our support team right away! 🎧"
])

bot = FacebookMessengerBot(config_file='customer_service.yaml')
bot.start_browser()
bot.login_to_facebook()
bot.monitor_messages(duration=3600)  # Monitor for 1 hour
```

### Example 2: Personal Assistant Bot
```python
config = BotConfig()
config.add_auto_reply("schedule", [
    "Let me check your calendar... 📅",
    "What would you like to schedule?"
])
config.add_auto_reply("remind", [
    "I'll set a reminder for you! ⏰"
])

bot = FacebookMessengerBot(config_file='assistant.yaml')
# ... rest of setup
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit: `git commit -am 'Add feature'`
5. Push: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and automation purposes. Users are responsible for:
- Complying with Facebook's Terms of Service
- Respecting privacy and consent of message recipients
- Using the bot responsibly and ethically

The developers are not responsible for any misuse of this software.

## 🔗 Related Projects

- [Selenium WebDriver](https://selenium-python.readthedocs.io/)
- [Undetected ChromeDriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)

---

Made with ❤️ by the Smart Chat Bot Team
