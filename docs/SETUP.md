# Facebook Auto-Login Setup Guide

This guide will help you set up and use the Facebook auto-login functionality in the Smart Chat Bot repository.

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** - Check with `python --version`
- **Internet Connection** - Required for downloading browser dependencies
- **Facebook Account** - Valid email and password

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers (this may take a few minutes)
playwright install chromium
```

### 2. Configure Credentials

Create your configuration file:

```bash
# Copy the example configuration
cp config/.env.example config/.env

# Edit the configuration file with your credentials
nano config/.env  # or use your preferred editor
```

Edit `config/.env`:
```bash
FACEBOOK_EMAIL=your_email@example.com
FACEBOOK_PASSWORD=your_password_here
```

**⚠️ Security Note**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

### 3. Run the Application

```bash
python main.py
```

## 📖 Detailed Usage

### Basic Usage

The simplest way to use the Facebook auto-login is through the main script:

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

# Clean up
fb_login.close_browser()
```

### Advanced Configuration

You can customize various aspects of the automation:

```python
# Custom profile directory
profile_manager = ChromeProfileManager("custom_profiles")

# Multiple profiles
profiles = ["work_profile", "personal_profile", "test_profile"]
for profile in profiles:
    result = fb_login.login_to_facebook(email, password, profile)
    # Handle each result...
```

### Environment Variables

The following environment variables are supported:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FACEBOOK_EMAIL` | Your Facebook email/username | - | ✅ Yes |
| `FACEBOOK_PASSWORD` | Your Facebook password | - | ✅ Yes |
| `HEADLESS_MODE` | Run browser in headless mode | `false` | ❌ No |
| `PROFILE_DIRECTORY` | Directory for Chrome profiles | `chrome_profiles` | ❌ No |

## 🛠️ Features

### Chrome Profile Management

- **Isolated Profiles**: Each profile maintains separate cookies, cache, and session data
- **Persistent Sessions**: Profiles are saved and can be reused across sessions
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Facebook Auto-Login

- **Automatic Form Filling**: Handles email and password input automatically
- **Login Verification**: Verifies successful login by checking page elements
- **Error Detection**: Detects common error scenarios (wrong credentials, CAPTCHA, 2FA)
- **Session Management**: Option to keep browser session alive

### Error Handling

The system gracefully handles various scenarios:

- **Invalid Credentials**: Clear error messages for authentication failures
- **CAPTCHA Detection**: Alerts when manual intervention is needed
- **Two-Factor Authentication**: Detects 2FA prompts
- **Network Issues**: Proper timeout handling
- **Already Logged In**: Detects existing sessions

## 🔧 Troubleshooting

### Common Issues

#### 1. "Browser not found" Error

```bash
# Install Playwright browsers
playwright install chromium
```

#### 2. Login Fails with Correct Credentials

- **Two-Factor Authentication**: Disable 2FA temporarily or handle manually
- **Account Locked**: Log in manually first to resolve any account issues
- **Suspicious Activity**: Facebook may require verification for new devices

#### 3. CAPTCHA Appears

- **Manual Intervention**: Complete CAPTCHA manually when prompted
- **Account History**: Use an account with good standing to reduce CAPTCHA frequency

#### 4. Import Errors

```bash
# Ensure you're running from the project root
cd /path/to/Smart-chat-bot

# Check Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
```

### Debug Mode

For debugging, you can modify the browser launch options:

```python
# In facebook_automation.py, modify _launch_browser_with_profile:
browser = playwright.chromium.launch_persistent_context(
    user_data_dir=str(profile_path),
    headless=False,  # Set to True for headless mode
    slow_mo=1000,    # Add delay between actions
    devtools=True    # Open developer tools
)
```

### Logging

The application includes detailed logging. To see debug information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔒 Security Best Practices

### Credential Security

1. **Never hardcode credentials** in your scripts
2. **Use environment variables** or secure configuration files
3. **Don't commit** `.env` files to version control
4. **Use strong passwords** and enable 2FA when possible

### Browser Security

1. **Isolated Profiles**: Each automation run uses a separate profile
2. **Clean Sessions**: Regularly clear old profiles if not needed
3. **Headless Mode**: Use headless mode in production environments

### Facebook Compliance

1. **Respect Terms of Service**: Use automation responsibly
2. **Rate Limiting**: Don't make excessive login attempts
3. **Human-like Behavior**: The automation includes delays to appear natural

## 🎯 Use Cases

### Typical Scenarios

1. **Testing**: Automated testing of Facebook integrations
2. **Monitoring**: Check account status or notifications
3. **Content Management**: Automated posting or page management
4. **Research**: Data collection for analysis (within ToS limits)

### Integration Examples

```python
# Social media management
def post_to_facebook(message, profile="marketing_profile"):
    fb_login = FacebookAutoLogin(profile_manager)
    result = fb_login.login_to_facebook(email, password, profile)
    
    if result['success']:
        # Navigate to posting interface
        # Fill and submit post
        pass

# Account monitoring
def check_notifications(profile="monitor_profile"):
    fb_login = FacebookAutoLogin(profile_manager)
    result = fb_login.login_to_facebook(email, password, profile)
    
    if result['success']:
        # Check for new notifications
        # Process alerts
        pass
```

## 📚 API Reference

### ChromeProfileManager

#### Methods

- `__init__(profiles_dir: str = "chrome_profiles")`: Initialize manager
- `create_profile_path(profile_name: str) -> Path`: Create profile directory
- `list_profiles() -> list[str]`: List existing profiles

### FacebookAutoLogin

#### Methods

- `__init__(profile_manager: ChromeProfileManager)`: Initialize login handler
- `login_to_facebook(email: str, password: str, profile_name: str) -> Dict`: Perform login
- `close_browser()`: Clean up browser resources
- `keep_session_alive(duration_minutes: int)`: Keep session active

#### Return Format

The `login_to_facebook` method returns a dictionary:

```python
{
    'success': bool,        # True if login successful
    'message': str,         # Status message or error description
    'profile_used': str,    # Name of the Chrome profile used
    'current_url': str      # Current page URL after login attempt
}
```

## 🤝 Contributing

When contributing to this functionality:

1. **Follow existing code style**
2. **Add appropriate error handling**
3. **Update documentation** for new features
4. **Test on multiple platforms** when possible
5. **Respect Facebook's Terms of Service**

## 📞 Support

If you encounter issues:

1. **Check this documentation** for common solutions
2. **Review error messages** carefully
3. **Test with a simple Facebook account** first
4. **Check internet connectivity** and Facebook availability

For technical issues, please create an issue in the repository with:
- Your operating system
- Python version
- Error messages (without sensitive information)
- Steps to reproduce the problem