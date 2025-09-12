#!/usr/bin/env python3
"""
Configuration Demo for Facebook Messenger Bot
Shows how to customize bot behavior and auto-replies
"""
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__ if '__file__' in globals() else '.')), '..', 'src'))

from config import BotConfig

def main():
    """Demonstrate configuration features"""
    
    print("🤖 Facebook Messenger Bot - Configuration Demo")
    print("=" * 50)
    
    # Create a new config
    print("📝 Creating custom configuration...")
    config = BotConfig()
    
    # Show default keywords
    print("\n🔤 Default auto-reply keywords:")
    for keyword, responses in config.get_auto_reply_keywords().items():
        print(f"  • '{keyword}' -> {len(responses)} response(s)")
        for response in responses:
            print(f"    - \"{response}\"")
    
    # Add custom keywords
    print("\n➕ Adding custom auto-replies...")
    
    config.add_auto_reply("price", [
        "Our pricing starts at $10/month 💰",
        "Let me get you a custom quote! What's your budget? 💸",
        "Check out our pricing page: example.com/pricing 📊"
    ])
    
    config.add_auto_reply("support", [
        "I'll connect you with our support team right away! 🎧",
        "Our support hours are 9 AM - 6 PM EST 🕘",
        "For urgent issues, call: 1-800-SUPPORT 📞"
    ])
    
    config.add_auto_reply("meeting", [
        "I'd be happy to schedule a meeting! 📅",
        "What time works best for you? ⏰",
        "Let me check available slots... 🗓️"
    ])
    
    # Show updated keywords
    print("\n🆕 Updated auto-reply keywords:")
    for keyword, responses in config.get_auto_reply_keywords().items():
        print(f"  • '{keyword}' -> {len(responses)} response(s)")
    
    # Demonstrate configuration access
    print("\n⚙️ Configuration settings:")
    print(f"  • Message check interval: {config.get('facebook.message_check_interval')} seconds")
    print(f"  • Response delay range: {config.get('auto_replies.delay_range')} seconds")
    print(f"  • Headless mode: {config.get('selenium.headless')}")
    print(f"  • Window size: {config.get('selenium.window_size')}")
    
    # Demonstrate saving config
    config_file = '/tmp/demo_config.yaml'
    print(f"\n💾 Saving configuration to {config_file}...")
    config.save_config(config_file)
    
    # Load and verify
    print("🔄 Loading saved configuration...")
    loaded_config = BotConfig(config_file)
    loaded_keywords = list(loaded_config.get_auto_reply_keywords().keys())
    print(f"✅ Loaded {len(loaded_keywords)} keywords: {loaded_keywords}")
    
    print("\n🎉 Configuration demo complete!")
    print("💡 You can now use this custom config with:")
    print(f"   bot = FacebookMessengerBot(config_file='{config_file}')")

if __name__ == "__main__":
    main()