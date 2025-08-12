# Webhook-based Chrome Browser Controller

This document provides detailed instructions for setting up and using the webhook-based Chrome browser controller feature in the Smart-chat-bot repository.

## 🎯 Overview

This feature enables remote control of a Google Chrome browser through HTTP webhook requests. It uses Selenium WebDriver for browser automation and Flask for the HTTP server, allowing you to:

- Open URLs programmatically
- Click buttons and elements on web pages
- Fill out forms automatically
- Execute complex sequences of browser actions
- Get page information and status

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9 or higher**
2. **Google Chrome browser** (latest version recommended)
3. **ChromeDriver** - Download from [ChromeDriver](https://chromedriver.chromium.org/) or use your package manager:
   ```bash
   # On macOS with Homebrew
   brew install chromedriver
   
   # On Ubuntu/Debian
   sudo apt-get install chromium-chromedriver
   
   # On Windows with Chocolatey
   choco install chromedriver
   ```

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/Will100001/Smart-chat-bot.git
   cd Smart-chat-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env file with your preferred settings
   ```

4. **Start the webhook server**:
   ```bash
   python main.py
   ```

The server will start on `http://127.0.0.1:5000` by default.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Server configuration
WEBHOOK_HOST=127.0.0.1
WEBHOOK_PORT=5000
FLASK_DEBUG=False

# Security - IMPORTANT: Change this in production!
WEBHOOK_SECRET_TOKEN=your-secure-secret-token-here

# Chrome configuration
CHROME_HEADLESS=False                    # Set to True for headless mode
CHROME_WINDOW_SIZE=1920,1080            # Browser window size
PAGE_LOAD_TIMEOUT=30                     # Page load timeout in seconds
IMPLICIT_WAIT_TIMEOUT=10                 # Element wait timeout in seconds

# Logging
LOG_LEVEL=INFO                           # DEBUG, INFO, WARNING, ERROR
LOG_FILE=webhook_browser.log             # Log file path
```

### Security Configuration

**⚠️ Important**: Always set a secure `WEBHOOK_SECRET_TOKEN` in production environments. This token must be included in all webhook requests for authentication.

## 📡 API Endpoints

### Authentication

All endpoints (except `/health`) require authentication using the secret token. Include the token in the request:

**Option 1: Authorization Header**
```bash
Authorization: Bearer your-secret-token
```

**Option 2: Request Body**
```json
{
  "token": "your-secret-token",
  "other": "parameters"
}
```

### Available Endpoints

#### Health Check
```http
GET /health
```
Returns server status and browser state.

#### Browser Control

**Start Browser**
```http
POST /browser/start
Content-Type: application/json
Authorization: Bearer your-token

{}
```

**Stop Browser**
```http
POST /browser/stop
Content-Type: application/json
Authorization: Bearer your-token

{}
```

**Open URL**
```http
POST /browser/open_url
Content-Type: application/json
Authorization: Bearer your-token

{
  "url": "https://example.com"
}
```

**Click Element**
```http
POST /browser/click_element
Content-Type: application/json
Authorization: Bearer your-token

{
  "selector": "#submit-button",
  "selector_type": "css"
}
```

**Fill Form Field**
```http
POST /browser/fill_form
Content-Type: application/json
Authorization: Bearer your-token

{
  "selector": "input[name='username']",
  "text": "user@example.com",
  "selector_type": "css",
  "clear_first": true
}
```

**Get Page Information**
```http
GET /browser/page_info
Authorization: Bearer your-token
```

**Execute Multiple Actions**
```http
POST /browser/execute_actions
Content-Type: application/json
Authorization: Bearer your-token

{
  "actions": [
    {
      "action": "open_url",
      "url": "https://example.com/login"
    },
    {
      "action": "fill_form_field",
      "selector": "#username",
      "text": "user@example.com"
    },
    {
      "action": "fill_form_field",
      "selector": "#password",
      "text": "password123"
    },
    {
      "action": "click_element",
      "selector": "#login-button"
    }
  ]
}
```

### Selector Types

The following selector types are supported:

- `css` - CSS selectors (default)
- `xpath` - XPath expressions
- `id` - Element ID
- `name` - Element name attribute
- `class` - Element class name
- `tag` - HTML tag name

## 🧪 Testing

### Using the Test Script

Run the included test script to verify functionality:

```bash
# Basic tests
python examples/test_webhook.py

# Advanced tests (includes Google search example)
python examples/test_webhook.py advanced
```

### Manual Testing with curl

**Health Check:**
```bash
curl http://127.0.0.1:5000/health
```

**Start Browser:**
```bash
curl -X POST http://127.0.0.1:5000/browser/start \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dev-token-change-me" \
  -d '{}'
```

**Open URL:**
```bash
curl -X POST http://127.0.0.1:5000/browser/open_url \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dev-token-change-me" \
  -d '{"url": "https://httpbin.org/"}'
```

## 🔐 Security Best Practices

1. **Token Security**: Use a strong, randomly generated secret token
2. **Network Security**: Run on localhost or use HTTPS in production
3. **Input Validation**: All inputs are validated and sanitized
4. **Resource Management**: Always stop the browser when done
5. **Logging**: Monitor logs for unauthorized access attempts

## 🛠️ Advanced Usage

### Multiple Action Sequences

Execute complex workflows by chaining actions:

```json
{
  "actions": [
    {
      "action": "open_url",
      "url": "https://example.com/form"
    },
    {
      "action": "wait",
      "seconds": 2
    },
    {
      "action": "fill_form_field",
      "selector": "#name",
      "text": "John Doe"
    },
    {
      "action": "fill_form_field",
      "selector": "#email",
      "text": "john@example.com"
    },
    {
      "action": "click_element",
      "selector": "#submit",
      "fail_on_error": true
    }
  ]
}
```

### Error Handling

All endpoints return structured JSON responses:

**Success Response:**
```json
{
  "success": true,
  "message": "Action completed successfully",
  "additional_data": "..."
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error category",
  "details": "Detailed error message"
}
```

### Custom Chrome Options

Modify `src/browser_controller.py` to add custom Chrome options:

```python
# Add to BrowserController.start_browser() method
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_experimental_option('prefs', {
    'profile.default_content_setting_values.notifications': 2
})
```

## 🔧 Troubleshooting

### Common Issues

**1. ChromeDriver not found**
```
WebDriverException: 'chromedriver' executable needs to be in PATH
```
**Solution**: Install ChromeDriver and ensure it's in your PATH, or set `CHROME_DRIVER_PATH` in your `.env` file.

**2. Port already in use**
```
OSError: [Errno 48] Address already in use
```
**Solution**: Change the port in your `.env` file or stop other services using port 5000.

**3. Element not found**
```
TimeoutException: Element not found or not clickable
```
**Solution**: Verify the selector is correct and the element is visible. Try increasing wait timeouts.

**4. Unauthorized errors**
```
{"success": false, "error": "Unauthorized"}
```
**Solution**: Ensure you're sending the correct authentication token.

### Debug Mode

Enable debug mode for detailed logging:

```bash
# In .env file
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
```

### Log Analysis

Check the log file for detailed information:

```bash
tail -f webhook_browser.log
```

## 🌐 Cross-Platform Support

This implementation has been tested on:

- **Windows 10/11** with Chrome
- **macOS** (Intel and Apple Silicon) with Chrome
- **Linux** (Ubuntu, Debian, CentOS) with Chrome/Chromium

### Platform-Specific Notes

**Windows:**
- Use forward slashes in paths or escape backslashes
- ChromeDriver should be in PATH or specify full path

**macOS:**
- Install ChromeDriver via Homebrew for easy updates
- May need to allow ChromeDriver in Security & Privacy settings

**Linux:**
- Use package manager to install chromium-chromedriver
- Ensure display server is available (use Xvfb for headless servers)

## 📚 Integration Examples

### Python Integration

```python
import requests

class BrowserClient:
    def __init__(self, base_url="http://127.0.0.1:5000", token="your-token"):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    
    def automate_login(self, username, password):
        # Start browser
        requests.post(f"{self.base_url}/browser/start", headers=self.headers)
        
        # Navigate and login
        actions = [
            {"action": "open_url", "url": "https://example.com/login"},
            {"action": "fill_form_field", "selector": "#username", "text": username},
            {"action": "fill_form_field", "selector": "#password", "text": password},
            {"action": "click_element", "selector": "#login-btn"}
        ]
        
        response = requests.post(
            f"{self.base_url}/browser/execute_actions",
            headers=self.headers,
            json={"actions": actions}
        )
        
        return response.json()
```

### Node.js Integration

```javascript
const axios = require('axios');

class BrowserClient {
    constructor(baseUrl = 'http://127.0.0.1:5000', token = 'your-token') {
        this.baseUrl = baseUrl;
        this.headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
    }
    
    async automateForm(formData) {
        // Start browser
        await axios.post(`${this.baseUrl}/browser/start`, {}, { headers: this.headers });
        
        // Fill form
        const actions = [
            { action: 'open_url', url: 'https://example.com/form' },
            ...Object.entries(formData).map(([selector, value]) => ({
                action: 'fill_form_field',
                selector,
                text: value
            })),
            { action: 'click_element', selector: '#submit' }
        ];
        
        const response = await axios.post(
            `${this.baseUrl}/browser/execute_actions`,
            { actions },
            { headers: this.headers }
        );
        
        return response.data;
    }
}
```

## 🤝 Contributing

To contribute to this feature:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section above
2. Review existing issues in the GitHub repository
3. Create a new issue with detailed information about your problem

---

**Happy Automating! 🤖✨**