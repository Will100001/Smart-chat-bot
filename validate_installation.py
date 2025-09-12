#!/usr/bin/env python3
"""
Installation and validation script for Facebook Messenger Bot
Verifies that all components are properly installed and working
"""
import sys
import os
import subprocess
import traceback

def check_python_version():
    """Check if Python version is 3.9+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python 3.9+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_imports():
    """Test that all modules can be imported"""
    print("🔧 Testing imports...")
    try:
        sys.path.insert(0, 'src')
        from config import BotConfig
        from message_handler import MessageHandler
        from facebook_messenger_bot import FacebookMessengerBot
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_configuration():
    """Test configuration functionality"""
    print("⚙️ Testing configuration...")
    try:
        sys.path.insert(0, 'src')
        from config import BotConfig
        
        # Test basic config creation
        config = BotConfig()
        
        # Test keyword access
        keywords = config.get_auto_reply_keywords()
        assert isinstance(keywords, dict), "Keywords should be a dictionary"
        assert len(keywords) > 0, "Should have default keywords"
        
        # Test adding keywords
        config.add_auto_reply("test", ["test response"])
        updated_keywords = config.get_auto_reply_keywords()
        assert "test" in updated_keywords, "Should be able to add keywords"
        
        # Test config access
        interval = config.get('facebook.message_check_interval', 0)
        assert interval > 0, "Should have valid message check interval"
        
        print("✅ Configuration tests passed")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        traceback.print_exc()
        return False

def test_message_handler():
    """Test message handler functionality"""
    print("💬 Testing message handler...")
    try:
        sys.path.insert(0, 'src')
        from config import BotConfig
        from message_handler import MessageHandler
        
        config = BotConfig()
        handler = MessageHandler(config)
        
        # Test keyword matching
        matches = handler.find_keyword_matches("hello there")
        assert "hello" in matches, "Should match 'hello' keyword"
        
        # Test reply generation
        reply = handler.generate_auto_reply("hello", "test_user")
        assert reply is not None, "Should generate a reply for 'hello'"
        assert isinstance(reply, str), "Reply should be a string"
        
        print("✅ Message handler tests passed")
        return True
    except Exception as e:
        print(f"❌ Message handler test failed: {e}")
        traceback.print_exc()
        return False

def test_bot_initialization():
    """Test bot initialization (without browser)"""
    print("🤖 Testing bot initialization...")
    try:
        sys.path.insert(0, 'src')
        from facebook_messenger_bot import FacebookMessengerBot
        
        # Test basic initialization
        bot = FacebookMessengerBot()
        assert bot.config is not None, "Bot should have config"
        assert bot.message_handler is not None, "Bot should have message handler"
        
        # Test with custom config
        bot2 = FacebookMessengerBot(headless=True)
        assert bot2.config.get('selenium.headless') == True, "Should respect headless parameter"
        
        print("✅ Bot initialization tests passed")
        return True
    except Exception as e:
        print(f"❌ Bot initialization test failed: {e}")
        traceback.print_exc()
        return False

def test_examples():
    """Test that example scripts are valid"""
    print("📝 Testing example scripts...")
    try:
        # Test syntax of example files
        example_files = [
            'examples/basic_usage.py',
            'examples/advanced_usage.py',
            'examples/config_demo.py'
        ]
        
        for example_file in example_files:
            if os.path.exists(example_file):
                with open(example_file, 'r') as f:
                    code = f.read()
                    compile(code, example_file, 'exec')
                print(f"✅ {example_file} syntax valid")
            else:
                print(f"⚠️ {example_file} not found")
        
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in example: {e}")
        return False

def check_chrome_availability():
    """Check if Chrome browser is available"""
    print("🌐 Checking Chrome availability...")
    try:
        # Try to find Chrome executable
        chrome_paths = [
            '/usr/bin/google-chrome',
            '/usr/bin/chromium-browser',
            '/usr/bin/chromium',
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                print(f"✅ Found Chrome at: {path}")
                return True
        
        # Try to run chrome command
        try:
            subprocess.run(['google-chrome', '--version'], 
                         capture_output=True, check=True, timeout=5)
            print("✅ Chrome found in PATH")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        print("⚠️ Chrome not found - you'll need to install Chrome for the bot to work")
        return False
    except Exception as e:
        print(f"⚠️ Error checking Chrome: {e}")
        return False

def main():
    """Run all validation tests"""
    print("🚀 Facebook Messenger Bot - Installation Validator")
    print("=" * 55)
    
    tests = [
        ("Python Version", check_python_version),
        ("Dependencies", install_dependencies),
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("Message Handler", test_message_handler),
        ("Bot Initialization", test_bot_initialization),
        ("Example Scripts", test_examples),
        ("Chrome Browser", check_chrome_availability)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            failed += 1
    
    print(f"\n📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! Your Facebook Messenger Bot is ready to use!")
        print("\n📋 Next steps:")
        print("1. Set up your credentials in .env file")
        print("2. Run: python examples/basic_usage.py")
        print("3. Or try: python examples/config_demo.py")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please fix the issues above before using the bot.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)