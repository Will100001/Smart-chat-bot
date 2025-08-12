#!/usr/bin/env python3
"""
Setup script for Smart-chat-bot with webhook browser automation.
This script helps set up the environment and dependencies.
"""
import os
import sys
import subprocess
import platform

def run_command(cmd, description=""):
    """Run a command and handle errors."""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor} is compatible!")
    return True

def check_chrome():
    """Check if Chrome/Chromium is installed."""
    chrome_commands = ['google-chrome --version', 'chromium-browser --version', 'chromium --version']
    
    for cmd in chrome_commands:
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print(f"✅ Found Chrome: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError:
            continue
    
    print("❌ Chrome/Chromium not found!")
    print("Please install Google Chrome or Chromium browser.")
    return False

def check_chromedriver():
    """Check if ChromeDriver is installed."""
    try:
        result = subprocess.run('chromedriver --version', shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Found ChromeDriver: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("❌ ChromeDriver not found!")
        print("Please install ChromeDriver:")
        
        system = platform.system().lower()
        if system == "darwin":
            print("  brew install chromedriver")
        elif system == "linux":
            print("  sudo apt-get install chromium-chromedriver")
        elif system == "windows":
            print("  choco install chromedriver")
        else:
            print("  Download from: https://chromedriver.chromium.org/")
        
        return False

def install_dependencies():
    """Install Python dependencies."""
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    if os.path.exists('.env'):
        print("✅ .env file already exists!")
        return True
    
    if os.path.exists('.env.example'):
        print("📝 Creating .env file from template...")
        try:
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                content = src.read()
                # Generate a random token
                import secrets
                import string
                token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
                content = content.replace('your-secure-secret-token-here', token)
                dst.write(content)
            print("✅ .env file created with random security token!")
            print("🔒 You can customize the settings in .env file")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ .env.example not found!")
        return False

def test_installation():
    """Test if the installation works."""
    print("🧪 Testing installation...")
    
    # Test imports
    test_code = '''
import sys
sys.path.insert(0, ".")
try:
    from src.config import Config
    from src.webhook_server import WebhookServer
    from src.browser_controller import BrowserController
    print("✅ All modules imported successfully!")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
'''
    
    result = subprocess.run([sys.executable, '-c', test_code], capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
        return True
    else:
        print(f"❌ Test failed: {result.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Smart-chat-bot Setup Script")
    print("=" * 40)
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    if not check_chrome():
        print("⚠️  Chrome not found, but continuing setup...")
    
    if not check_chromedriver():
        print("⚠️  ChromeDriver not found, but continuing setup...")
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create environment file
    if not create_env_file():
        return False
    
    # Test installation
    if not test_installation():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Customize settings in .env file if needed")
    print("2. Start the webhook server: python main.py")
    print("3. Test the system: python examples/test_webhook.py")
    print("4. Read documentation: README_WEBHOOK.md")
    print("\n💡 For browser automation, ensure Chrome/ChromeDriver are installed")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)