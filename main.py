#!/usr/bin/env python3
"""
Facebook Auto-Login Example Script

This script demonstrates how to use the Facebook automation functionality
to create Chrome profiles and automatically log in to Facebook.

Usage:
    python main.py

Make sure to set up your environment variables first:
    export FACEBOOK_EMAIL="your_email@example.com"
    export FACEBOOK_PASSWORD="your_password"

Or create a .env file based on config/.env.example
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from facebook_automation import ChromeProfileManager, FacebookAutoLogin, load_credentials_from_env


def main():
    """Main execution function."""
    print("🤖 Smart Chat Bot - Facebook Auto-Login")
    print("=" * 50)
    
    # Load environment variables from .env file if it exists
    env_file = Path("config/.env")
    if env_file.exists():
        load_dotenv(env_file)
        print("✅ Loaded configuration from config/.env")
    else:
        print("ℹ️  No .env file found, using system environment variables")
    
    try:
        # Load credentials
        print("\n📋 Loading Facebook credentials...")
        email, password = load_credentials_from_env()
        print(f"✅ Email: {email[:3]}***@{email.split('@')[1] if '@' in email else 'hidden'}")
        
        # Initialize profile manager
        print("\n🔧 Initializing Chrome Profile Manager...")
        profile_manager = ChromeProfileManager("chrome_profiles")
        
        # List existing profiles
        existing_profiles = profile_manager.list_profiles()
        if existing_profiles:
            print(f"📁 Found existing profiles: {', '.join(existing_profiles)}")
        else:
            print("📁 No existing profiles found")
        
        # Initialize Facebook auto-login
        print("\n🌐 Initializing Facebook Auto-Login...")
        fb_login = FacebookAutoLogin(profile_manager)
        
        # Prompt for profile name
        profile_name = input("\n📝 Enter Chrome profile name (default: 'facebook_bot'): ").strip()
        if not profile_name:
            profile_name = "facebook_bot"
        
        print(f"\n🚀 Starting Facebook login with profile: '{profile_name}'")
        print("🔄 This may take a few moments...")
        
        # Attempt login
        result = fb_login.login_to_facebook(email, password, profile_name)
        
        # Display results
        print("\n" + "=" * 50)
        print("📊 LOGIN RESULT")
        print("=" * 50)
        print(f"Status: {'✅ SUCCESS' if result['success'] else '❌ FAILED'}")
        print(f"Message: {result['message']}")
        print(f"Profile: {result['profile_used']}")
        print(f"Current URL: {result['current_url']}")
        
        if result['success']:
            print("\n🎉 Login successful!")
            
            # Ask if user wants to keep session alive
            keep_alive = input("\n❓ Keep browser session alive? (y/N): ").strip().lower()
            if keep_alive in ['y', 'yes']:
                duration = input("⏱️  Duration in minutes (default: 5): ").strip()
                try:
                    duration = int(duration) if duration else 5
                    print(f"\n⏳ Keeping session alive for {duration} minutes...")
                    print("   Press Ctrl+C to stop early")
                    fb_login.keep_session_alive(duration)
                except ValueError:
                    print("⚠️  Invalid duration, using 5 minutes")
                    fb_login.keep_session_alive(5)
                except KeyboardInterrupt:
                    print("\n⏹️  Session stopped by user")
            
        else:
            print(f"\n❌ Login failed: {result['message']}")
            
            # Provide troubleshooting tips
            print("\n🔧 Troubleshooting Tips:")
            print("   • Check your Facebook email and password")
            print("   • Ensure you don't have 2FA enabled (or handle it manually)")
            print("   • Try logging in manually first to resolve any account issues")
            print("   • Check your internet connection")
        
        # Clean up
        print("\n🧹 Cleaning up...")
        fb_login.close_browser()
        print("✅ Browser closed successfully")
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\n🔧 Setup Instructions:")
        print("   1. Copy config/.env.example to config/.env")
        print("   2. Edit config/.env with your Facebook credentials")
        print("   3. Or set environment variables:")
        print("      export FACEBOOK_EMAIL='your_email@example.com'")
        print("      export FACEBOOK_PASSWORD='your_password'")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Process interrupted by user")
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        print("   Check the logs for more details")
    
    finally:
        print("\n👋 Thank you for using Smart Chat Bot!")


if __name__ == "__main__":
    main()