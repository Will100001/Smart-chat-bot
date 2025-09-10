#!/usr/bin/env python3
"""
Basic usage example for Facebook Messenger Bot
This script demonstrates how to set up and use the bot for automated replies
"""
import os
import sys
import time
from dotenv import load_dotenv

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__ if '__file__' in globals() else '.')), '..', 'src'))

from facebook_messenger_bot import FacebookMessengerBot

def main():
    """Main function demonstrating basic bot usage"""
    
    # Load environment variables
    load_dotenv()
    
    print("🤖 Facebook Messenger Bot - Basic Usage Example")
    print("=" * 50)
    
    # Check if credentials are set
    email = os.getenv('FACEBOOK_EMAIL')
    password = os.getenv('FACEBOOK_PASSWORD')
    
    if not email or not password:
        print("❌ Facebook credentials not found!")
        print("\nPlease set the following environment variables:")
        print("  FACEBOOK_EMAIL=your_facebook_email")
        print("  FACEBOOK_PASSWORD=your_facebook_password")
        print("\nYou can create a .env file in the project root with these variables.")
        return
    
    # Create bot instance
    print("🚀 Initializing Facebook Messenger Bot...")
    bot = FacebookMessengerBot(headless=False)  # Set to True for headless mode
    
    try:
        # Start browser
        print("📱 Starting browser...")
        if not bot.start_browser():
            print("❌ Failed to start browser")
            return
        
        print("✅ Browser started successfully")
        
        # Login to Facebook
        print("🔐 Logging in to Facebook Messenger...")
        if not bot.login_to_facebook():
            print("❌ Login failed")
            print("💡 Tips:")
            print("  - Check your credentials")
            print("  - Handle 2FA/captcha manually if needed")
            print("  - Make sure your Facebook account is not locked")
            return
        
        print("✅ Successfully logged in!")
        print("💡 Example complete - bot is ready to use!")
        print("ℹ️  Note: Full functionality requires implementing conversation management methods")
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("🧹 Cleaning up...")
        bot.close()
        print("✅ Bot shutdown complete")

if __name__ == "__main__":
    main()