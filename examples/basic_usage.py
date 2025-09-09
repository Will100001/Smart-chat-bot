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
        
        # Get available conversations
        print("📋 Getting available conversations...")
        conversations = bot.get_conversations()
        
        if not conversations:
            print("⚠️  No conversations found")
            print("💡 Try opening Facebook Messenger in the browser and start a conversation")
        else:
            print(f"✅ Found {len(conversations)} conversations:")
            for i, conv in enumerate(conversations, 1):
                print(f"  {i}. {conv['name']}")
        
        # Demo: Monitor messages (you can specify a conversation name)
        print("\n🔍 Starting message monitoring...")
        print("💬 The bot will now monitor for new messages and send auto-replies")
        print("🛑 Press Ctrl+C to stop monitoring")
        
        # You can specify a conversation name to monitor:
        # bot.monitor_messages(conversation_name="Friend Name", duration=60)
        
        # Or monitor the current/first conversation:
        if conversations:
            bot.monitor_messages(conversation_name=conversations[0]['name'], duration=60)
        else:
            print("⚠️  No conversations available for monitoring")
            print("Please open a conversation manually and try again")
        
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