#!/usr/bin/env python3
"""
Setup script for Smart Chat Bot Facebook automation.

This script installs necessary dependencies and browsers.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False


def main():
    """Main setup function."""
    print("🤖 Smart Chat Bot - Facebook Automation Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("⚠️  Please install dependencies manually: pip install -r requirements.txt")
    
    # Install Playwright browsers
    print("\n🌐 Installing browser dependencies...")
    if not run_command("python -m playwright install chromium", "Installing Chromium browser"):
        print("⚠️  Browser installation failed. You may need to:")
        print("   1. Check your internet connection")
        print("   2. Try running: python -m playwright install")
        print("   3. Or use system browser installation")
    
    # Create config directory if it doesn't exist
    config_dir = Path("config")
    if not config_dir.exists():
        config_dir.mkdir()
        print("✅ Created config directory")
    
    # Check if .env file exists
    env_file = config_dir / ".env"
    env_example = config_dir / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        print("\n📝 Configuration setup:")
        print(f"   Please copy {env_example} to {env_file}")
        print("   and fill in your Facebook credentials")
    
    print("\n🎉 Setup completed!")
    print("\n📖 Next steps:")
    print("   1. Configure your credentials in config/.env")
    print("   2. Run: python main.py")
    print("   3. See docs/SETUP.md for detailed instructions")


if __name__ == "__main__":
    main()