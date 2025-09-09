#!/usr/bin/env python3
"""
Advanced usage example for Facebook Messenger Bot
Demonstrates custom configuration and advanced features
"""
import os
import sys
import time
from dotenv import load_dotenv

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__ if '__file__' in globals() else '.')), '..', 'src'))

from facebook_messenger_bot import FacebookMessengerBot
from config import BotConfig

def setup_custom_config():
    """Create a custom configuration for the bot"""
    config = BotConfig()
    
    # Customize auto-reply keywords
    config.add_auto_reply("hello", [
        "Hello! How can I assist you today? 😊",
        "Hi there! What can I help you with?",
        "Hey! Great to hear from you!"
    ])
    
    config.add_auto_reply("help", [
        "I'm here to help! What do you need assistance with?",
        "How can I help you today?",
        "What can I do for you? 🤝"
    ])
    
    config.add_auto_reply("bye", [
        "Goodbye! Have a wonderful day! 👋",
        "See you later! Take care! 😊",
        "Bye! Feel free to message me anytime!"
    ])
    
    config.add_auto_reply("thanks", [
        "You're very welcome! 😊",
        "Happy to help! 🎉",
        "No problem at all!",
        "Anytime! Glad I could help!"
    ])
    
    # Business hours auto-replies
    config.add_auto_reply("business hours", [
        "Our business hours are 9 AM - 5 PM, Monday to Friday. 🕘",
        "We're open Monday through Friday, 9 AM to 5 PM."
    ])
    
    config.add_auto_reply("price", [
        "Please let me know what product you're interested in for pricing information! 💰",
        "I'd be happy to help with pricing. What are you looking for?"
    ])
    
    # Set custom default replies
    config.set('auto_replies.default_reply', [
        "Thanks for your message! I'll get back to you soon. 📝",
        "I received your message and will respond shortly! ⏱️",
        "Message received! Give me a moment to assist you. 🤖"
    ])
    
    # Adjust response timing
    config.set('auto_replies.delay_range', [2, 5])  # 2-5 second delay
    
    # Save the custom configuration
    config.save_config('custom_config.yaml')
    
    return config

def monitor_specific_conversations(bot):
    """Monitor specific conversations with different behaviors"""
    conversations = bot.get_conversations()
    
    if not conversations:
        print("No conversations found")
        return
    
    print("Available conversations:")
    for i, conv in enumerate(conversations, 1):
        print(f"  {i}. {conv['name']}")
    
    # Let user choose conversation to monitor
    try:
        choice = input("\nEnter conversation number to monitor (or press Enter for first): ").strip()
        
        if choice:
            idx = int(choice) - 1
            if 0 <= idx < len(conversations):
                selected_conv = conversations[idx]['name']
            else:
                print("Invalid choice, using first conversation")
                selected_conv = conversations[0]['name']
        else:
            selected_conv = conversations[0]['name']
        
        print(f"\n🔍 Monitoring conversation with: {selected_conv}")
        print("⏱️  Monitoring for 2 minutes... (Press Ctrl+C to stop)")
        
        # Monitor for 2 minutes
        bot.monitor_messages(conversation_name=selected_conv, duration=120)
        
    except (ValueError, IndexError):
        print("Invalid input, monitoring first conversation")
        bot.monitor_messages(conversation_name=conversations[0]['name'], duration=120)

def main():
    """Advanced usage example"""
    load_dotenv()
    
    print("🤖 Facebook Messenger Bot - Advanced Usage Example")
    print("=" * 55)
    
    # Check credentials
    if not os.getenv('FACEBOOK_EMAIL') or not os.getenv('FACEBOOK_PASSWORD'):
        print("❌ Facebook credentials not found! Please set FACEBOOK_EMAIL and FACEBOOK_PASSWORD")
        return
    
    print("⚙️  Setting up custom configuration...")
    config = setup_custom_config()
    print("✅ Custom configuration created (saved as custom_config.yaml)")
    
    # Create bot with custom config
    print("🚀 Initializing bot with custom configuration...")
    bot = FacebookMessengerBot(config_file='custom_config.yaml', headless=False)
    
    try:
        # Start browser
        print("📱 Starting browser...")
        if not bot.start_browser():
            print("❌ Failed to start browser")
            return
        
        # Login
        print("🔐 Logging in...")
        if not bot.login_to_facebook():
            print("❌ Login failed")
            return
        
        print("✅ Successfully logged in!")
        
        # Demonstrate different features
        print("\n📋 Available features:")
        print("1. Monitor specific conversation")
        print("2. Send custom message")
        print("3. List all conversations")
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == "1":
            monitor_specific_conversations(bot)
        elif choice == "2":
            conversations = bot.get_conversations()
            if conversations:
                print(f"Opening conversation with {conversations[0]['name']}")
                if bot.open_conversation(conversations[0]['name']):
                    message = input("Enter message to send: ")
                    if bot.send_message(message):
                        print("✅ Message sent!")
                    else:
                        print("❌ Failed to send message")
            else:
                print("No conversations available")
        elif choice == "3":
            conversations = bot.get_conversations()
            print(f"\n📋 Found {len(conversations)} conversations:")
            for conv in conversations:
                print(f"  • {conv['name']}")
        else:
            print("Invalid choice, starting default monitoring...")
            monitor_specific_conversations(bot)
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("🧹 Cleaning up...")
        bot.close()
        print("✅ Advanced example complete!")

if __name__ == "__main__":
    main()