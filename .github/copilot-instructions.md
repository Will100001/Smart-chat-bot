# Smart Facebook Messenger Chatbot

Smart Facebook Messenger Chatbot is a Python-based browser automation tool that interacts with Facebook Messenger to provide automated responses. The bot uses Selenium WebDriver with stealth features to monitor conversations and send intelligent auto-replies based on configurable keywords.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Environment Setup and Dependencies
- Python 3.9+ is required. Current environment has Python 3.12.3 which is compatible.
- Install dependencies: `python3 -m pip install -r requirements.txt` -- takes 10 seconds. NEVER CANCEL.
- Chrome browser is required and available at `/usr/bin/google-chrome` with version 140.0.7339.80.

### Project Structure and Installation
- Main source code is in `src/` directory with modules: `config.py`, `facebook_messenger_bot.py`, `message_handler.py`
- Example scripts are in `examples/` directory: `basic_usage.py`, `config_demo.py`
- Dependencies are specified in `requirements.txt` with 8 packages including selenium, undetected-chromedriver, etc.
- Run validation: `python3 validate_installation.py` -- takes 1 second, validates all components. NEVER CANCEL.

### Configuration and Credentials
- Copy `.env.example` to `.env` and set Facebook credentials:
  ```bash
  cp .env.example .env
  # Edit .env with your Facebook email and password
  ```
- Configuration is managed through YAML files or environment variables
- Default keywords include: hello, help, thanks, bye with customizable responses
- Set `HEADLESS=true` environment variable for headless browser operation

### Running the Bot
- Basic usage: `python3 examples/basic_usage.py` -- requires Facebook credentials in .env
- Configuration demo: `python3 examples/config_demo.py` -- takes 0.06 seconds, shows config features. NEVER CANCEL.
- Advanced usage with custom config files and keyword management available

### Key Dependencies and Timing
- **Dependency installation**: 10 seconds for fresh install, instant if already installed
- **Validation script**: 1 second for full validation suite (8 tests, 100% success rate)
- **Configuration demo**: 0.06 seconds to demonstrate all config features
- **Basic example**: 0.24 seconds startup (credential validation phase)

## Validation

### Installation Validation
- Always run `python3 validate_installation.py` to verify setup
- Tests Python version, dependencies, imports, configuration, message handler, bot initialization, examples, and Chrome availability
- Should achieve 100% success rate with all 8 tests passing
- NEVER CANCEL validation - it completes in 1 second

### Browser Functionality
- Browser startup may fail in CI environments due to ChromeDriver download restrictions
- For local development, undetected-chromedriver provides stealth automation features
- Fallback to regular ChromeDriver when undetected version fails
- Supports both headless and windowed modes

### Testing Scenarios
- **Configuration Management**: Run `python3 examples/config_demo.py` to test keyword management, config loading/saving
- **Basic Bot Setup**: Run `python3 examples/basic_usage.py` with credentials to test login and initialization
- **Module Integration**: Validation script tests all import paths and class initialization
- **Message Processing**: Built-in tests verify keyword matching and reply generation

## Common Tasks

### Repository Structure
```
Smart-chat-bot/
├── src/
│   ├── __init__.py               # Package initialization
│   ├── config.py                 # Configuration management (3.8KB)
│   ├── facebook_messenger_bot.py # Main bot class (18.3KB)
│   └── message_handler.py        # Message processing (8.8KB)
├── examples/
│   ├── basic_usage.py           # Simple bot usage (3.6KB)
│   ├── advanced_usage.py        # Advanced features (6.4KB)
│   └── config_demo.py           # Configuration showcase (2.9KB)
├── requirements.txt             # Dependencies (159 bytes)
├── setup.py                     # Package installation (1.6KB)
├── validate_installation.py    # Installation validator (8.2KB)
├── .env.example                 # Environment template (341 bytes)
└── README.md                    # Documentation (7.9KB)
```

### Key Python Dependencies
```
selenium>=4.15.0                 # Browser automation
webdriver-manager>=4.0.1         # Chrome driver management  
python-dotenv>=1.0.0             # Environment variables
pyyaml>=6.0.1                    # Configuration files
beautifulsoup4>=4.12.0           # HTML parsing
requests>=2.31.0                 # HTTP client
lxml>=4.9.0                      # XML/HTML processing
undetected-chromedriver>=3.5.0   # Stealth automation
```

### Example Configuration Output
Default auto-reply keywords from `config_demo.py`:
- 'hello' -> 2 responses: "Hi there! How can I help you today?", "Hello! What can I do for you?"
- 'help' -> 2 responses: "I'm here to assist you...", "How can I help you?"
- 'thanks' -> 3 responses: "You're welcome!", "Happy to help!", "No problem at all!"
- 'bye' -> 3 responses: "Goodbye! Have a great day!", "See you later!", "Take care!"

### Browser Compatibility Notes
- Chrome browser is available and working at `/usr/bin/google-chrome`
- ChromeDriver download may fail in CI/restricted environments (network connectivity required)
- Bot gracefully handles ChromeDriver failures and provides informative error messages
- Supports proxy and custom browser profiles through Bitbrowser integration

### Environment Limitations
- Facebook credentials are required for actual bot operation (not provided in examples)
- Browser automation requires network access for initial ChromeDriver setup
- Stealth features may not work in all environments but fallback options available
- 2FA and captcha handling must be done manually during login process