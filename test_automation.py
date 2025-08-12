#!/usr/bin/env python3
"""
Test script to verify Facebook automation functionality.

This script tests the core functionality without requiring actual Facebook credentials
or browser installation, making it safe for CI/CD and development environments.
"""

import sys
import os
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_profile_manager():
    """Test Chrome Profile Manager functionality."""
    print("🧪 Testing ChromeProfileManager...")
    
    try:
        from facebook_automation import ChromeProfileManager
        
        # Use temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            pm = ChromeProfileManager(temp_dir)
            
            # Test profile creation
            profile_path = pm.create_profile_path("test_profile")
            assert profile_path.exists(), "Profile directory should be created"
            
            # Test profile listing
            profiles = pm.list_profiles()
            assert "test_profile" in profiles, "Profile should be listed"
            
            # Test multiple profiles
            pm.create_profile_path("profile2")
            pm.create_profile_path("profile3")
            profiles = pm.list_profiles()
            assert len(profiles) == 3, "Should have 3 profiles"
            
        print("✅ ChromeProfileManager tests passed")
        return True
        
    except Exception as e:
        print(f"❌ ChromeProfileManager test failed: {e}")
        return False


def test_credential_loading():
    """Test credential loading functionality."""
    print("🧪 Testing credential loading...")
    
    try:
        from facebook_automation import load_credentials_from_env
        
        # Test with missing credentials
        # Clear any existing environment variables first
        old_email = os.environ.pop("FACEBOOK_EMAIL", None)
        old_password = os.environ.pop("FACEBOOK_PASSWORD", None)
        
        try:
            load_credentials_from_env()
            print("❌ Should have raised ValueError for missing credentials")
            return False
        except ValueError:
            print("✅ Correctly raised error for missing credentials")
        
        # Test with valid credentials
        os.environ["FACEBOOK_EMAIL"] = "test@example.com"
        os.environ["FACEBOOK_PASSWORD"] = "testpass"
        
        email, password = load_credentials_from_env()
        assert email == "test@example.com", "Email should match"
        assert password == "testpass", "Password should match"
        
        # Clean up
        if old_email:
            os.environ["FACEBOOK_EMAIL"] = old_email
        if old_password:
            os.environ["FACEBOOK_PASSWORD"] = old_password
        
        print("✅ Credential loading tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Credential loading test failed: {e}")
        return False


def test_facebook_login_class():
    """Test FacebookAutoLogin class initialization."""
    print("🧪 Testing FacebookAutoLogin class...")
    
    try:
        from facebook_automation import ChromeProfileManager, FacebookAutoLogin
        
        # Create a temporary profile manager
        with tempfile.TemporaryDirectory() as temp_dir:
            pm = ChromeProfileManager(temp_dir)
            fb_login = FacebookAutoLogin(pm)
            
            # Test basic properties
            assert fb_login.profile_manager == pm, "Profile manager should be set"
            assert fb_login.browser is None, "Browser should be None initially"
            assert fb_login.context is None, "Context should be None initially"
            assert fb_login.page is None, "Page should be None initially"
            
        print("✅ FacebookAutoLogin class tests passed")
        return True
        
    except Exception as e:
        print(f"❌ FacebookAutoLogin class test failed: {e}")
        return False


def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import playwright
        print("✅ Playwright imported successfully")
        
        from facebook_automation import ChromeProfileManager, FacebookAutoLogin, load_credentials_from_env
        print("✅ Facebook automation modules imported successfully")
        
        import dotenv
        print("✅ Python-dotenv imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False


def test_project_structure():
    """Test that project structure is correct."""
    print("🧪 Testing project structure...")
    
    try:
        # Check required files exist
        required_files = [
            "src/facebook_automation.py",
            "config/.env.example",
            "docs/SETUP.md",
            "main.py",
            "requirements.txt",
            "setup.py",
            "README.md"
        ]
        
        for file_path in required_files:
            path = Path(file_path)
            assert path.exists(), f"Required file {file_path} should exist"
        
        # Check directory structure
        assert Path("src").is_dir(), "src directory should exist"
        assert Path("config").is_dir(), "config directory should exist"
        assert Path("docs").is_dir(), "docs directory should exist"
        
        print("✅ Project structure tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Project structure test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🤖 Smart Chat Bot - Facebook Automation Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_project_structure,
        test_profile_manager,
        test_credential_loading,
        test_facebook_login_class
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Facebook automation system is ready to use.")
        print("\n📝 Next steps:")
        print("   1. Install browsers: python -m playwright install chromium")
        print("   2. Configure credentials: cp config/.env.example config/.env")
        print("   3. Run the automation: python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())