"""
Facebook Auto-Login Module with Chrome Profile Management

This module provides functionality to:
1. Create isolated Chrome browser profiles
2. Automatically log in to Facebook using provided credentials
3. Handle basic error scenarios and verification

Requirements:
- Playwright library for browser automation
- Environment variables for secure credential storage
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, TimeoutError


class ChromeProfileManager:
    """Manages Chrome browser profiles for isolated sessions."""
    
    def __init__(self, profiles_dir: str = "chrome_profiles"):
        """
        Initialize the Chrome Profile Manager.
        
        Args:
            profiles_dir: Directory to store Chrome profiles
        """
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(exist_ok=True)
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the profile manager."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def create_profile_path(self, profile_name: str) -> Path:
        """
        Create a path for a new Chrome profile.
        
        Args:
            profile_name: Name of the profile
            
        Returns:
            Path object for the profile directory
        """
        profile_path = self.profiles_dir / profile_name
        profile_path.mkdir(exist_ok=True)
        return profile_path
    
    def list_profiles(self) -> list[str]:
        """
        List all existing Chrome profiles.
        
        Returns:
            List of profile names
        """
        if not self.profiles_dir.exists():
            return []
        
        return [
            item.name for item in self.profiles_dir.iterdir() 
            if item.is_dir()
        ]


class FacebookAutoLogin:
    """Handles automated Facebook login using Chrome profiles."""
    
    def __init__(self, profile_manager: ChromeProfileManager):
        """
        Initialize the Facebook Auto-Login handler.
        
        Args:
            profile_manager: Instance of ChromeProfileManager
        """
        self.profile_manager = profile_manager
        self.logger = profile_manager.logger
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    def _launch_browser_with_profile(self, profile_name: str) -> Browser:
        """
        Launch Chrome browser with a specific profile.
        
        Args:
            profile_name: Name of the Chrome profile to use
            
        Returns:
            Browser instance
        """
        profile_path = self.profile_manager.create_profile_path(profile_name)
        
        playwright = sync_playwright().start()
        
        # Launch Chrome with the specified profile
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=str(profile_path),
            headless=False,  # Set to True for headless operation
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        return browser
    
    def login_to_facebook(
        self, 
        email: str, 
        password: str, 
        profile_name: str = "facebook_profile"
    ) -> Dict[str, Any]:
        """
        Automatically log in to Facebook using the provided credentials.
        
        Args:
            email: Facebook email/username
            password: Facebook password
            profile_name: Name of Chrome profile to use
            
        Returns:
            Dictionary containing login result and status information
        """
        result = {
            'success': False,
            'message': '',
            'profile_used': profile_name,
            'current_url': ''
        }
        
        try:
            self.logger.info(f"Starting Facebook login with profile: {profile_name}")
            
            # Launch browser with profile
            self.context = self._launch_browser_with_profile(profile_name)
            self.page = self.context.new_page()
            
            # Navigate to Facebook login page
            self.logger.info("Navigating to Facebook login page...")
            self.page.goto("https://www.facebook.com/login", timeout=30000)
            
            # Wait for page to load
            self.page.wait_for_load_state("networkidle", timeout=15000)
            
            # Check if already logged in
            if self._is_already_logged_in():
                self.logger.info("Already logged in to Facebook")
                result['success'] = True
                result['message'] = "Already logged in"
                result['current_url'] = self.page.url
                return result
            
            # Fill in login credentials
            self.logger.info("Filling in login credentials...")
            
            # Wait for email field and fill it
            email_selector = 'input[name="email"], input[id="email"]'
            self.page.wait_for_selector(email_selector, timeout=10000)
            self.page.fill(email_selector, email)
            
            # Wait for password field and fill it
            password_selector = 'input[name="pass"], input[id="pass"]'
            self.page.wait_for_selector(password_selector, timeout=10000)
            self.page.fill(password_selector, password)
            
            # Click login button
            login_button_selector = 'button[name="login"], button[id="loginbutton"], input[type="submit"]'
            self.page.wait_for_selector(login_button_selector, timeout=10000)
            
            self.logger.info("Clicking login button...")
            self.page.click(login_button_selector)
            
            # Wait for navigation after login
            self.page.wait_for_load_state("networkidle", timeout=20000)
            
            # Verify successful login
            if self._verify_login_success():
                self.logger.info("Facebook login successful!")
                result['success'] = True
                result['message'] = "Login successful"
                result['current_url'] = self.page.url
            else:
                # Check for common error scenarios
                error_message = self._check_for_errors()
                self.logger.warning(f"Login failed: {error_message}")
                result['message'] = error_message
                result['current_url'] = self.page.url
                
        except TimeoutError as e:
            error_msg = f"Timeout during login process: {str(e)}"
            self.logger.error(error_msg)
            result['message'] = error_msg
            
        except Exception as e:
            error_msg = f"Unexpected error during login: {str(e)}"
            self.logger.error(error_msg)
            result['message'] = error_msg
        
        return result
    
    def _is_already_logged_in(self) -> bool:
        """
        Check if user is already logged in to Facebook.
        
        Returns:
            True if already logged in, False otherwise
        """
        try:
            # Check for common elements that appear when logged in
            logged_in_indicators = [
                '[data-testid="watch_feed"]',  # Watch feed
                '[aria-label="Home"]',         # Home navigation
                '[data-testid="blue_bar"]',    # Top navigation bar
                'div[role="main"]'             # Main content area
            ]
            
            for selector in logged_in_indicators:
                if self.page.query_selector(selector):
                    return True
                    
            # Check URL patterns that indicate logged in state
            current_url = self.page.url.lower()
            if any(pattern in current_url for pattern in ['/home', '/feed', '/?']):
                return True
                
            return False
            
        except Exception:
            return False
    
    def _verify_login_success(self) -> bool:
        """
        Verify that login was successful by checking for post-login elements.
        
        Returns:
            True if login was successful, False otherwise
        """
        try:
            # Wait a bit for page to load after login
            self.page.wait_for_timeout(3000)
            
            # Check for various indicators of successful login
            success_indicators = [
                '[data-testid="watch_feed"]',
                '[aria-label="Home"]',
                '[data-testid="blue_bar"]',
                'div[role="banner"]',
                '[aria-label="Facebook"]'
            ]
            
            for selector in success_indicators:
                try:
                    element = self.page.wait_for_selector(selector, timeout=5000)
                    if element:
                        return True
                except TimeoutError:
                    continue
            
            # Check URL patterns
            current_url = self.page.url.lower()
            success_urls = ['/home', '/feed', '/?']
            
            if any(pattern in current_url for pattern in success_urls):
                return True
                
            # Check if we're not on login page anymore
            if '/login' not in current_url:
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"Error verifying login success: {str(e)}")
            return False
    
    def _check_for_errors(self) -> str:
        """
        Check for common error messages on the login page.
        
        Returns:
            Error message string
        """
        try:
            # Common error selectors
            error_selectors = [
                '[data-testid="royal_login_error"]',
                '.login_error_box',
                '#error_box',
                '[role="alert"]'
            ]
            
            for selector in error_selectors:
                error_element = self.page.query_selector(selector)
                if error_element:
                    error_text = error_element.inner_text()
                    if error_text.strip():
                        return f"Facebook error: {error_text.strip()}"
            
            # Check for CAPTCHA
            if self.page.query_selector('[data-testid="captcha"]') or 'captcha' in self.page.url.lower():
                return "CAPTCHA verification required - manual intervention needed"
            
            # Check for two-factor authentication
            if self.page.query_selector('[name="approvals_code"]') or 'checkpoint' in self.page.url:
                return "Two-factor authentication required - manual intervention needed"
            
            # Check if still on login page
            if '/login' in self.page.url.lower():
                return "Still on login page - credentials may be incorrect"
            
            return "Unknown error occurred during login"
            
        except Exception as e:
            return f"Error checking for login errors: {str(e)}"
    
    def close_browser(self):
        """Close the browser and clean up resources."""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            self.logger.info("Browser closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing browser: {str(e)}")
    
    def keep_session_alive(self, duration_minutes: int = 10):
        """
        Keep the browser session alive for a specified duration.
        
        Args:
            duration_minutes: How long to keep the session alive
        """
        if not self.page:
            self.logger.warning("No active page to keep alive")
            return
        
        self.logger.info(f"Keeping session alive for {duration_minutes} minutes...")
        
        try:
            # Keep the page active
            self.page.wait_for_timeout(duration_minutes * 60 * 1000)
        except KeyboardInterrupt:
            self.logger.info("Session interrupted by user")
        except Exception as e:
            self.logger.error(f"Error keeping session alive: {str(e)}")


def load_credentials_from_env() -> tuple[str, str]:
    """
    Load Facebook credentials from environment variables.
    
    Returns:
        Tuple of (email, password)
        
    Raises:
        ValueError: If credentials are not found in environment variables
    """
    email = os.getenv('FACEBOOK_EMAIL')
    password = os.getenv('FACEBOOK_PASSWORD')
    
    if not email or not password:
        raise ValueError(
            "Facebook credentials not found in environment variables. "
            "Please set FACEBOOK_EMAIL and FACEBOOK_PASSWORD."
        )
    
    return email, password


# Example usage function
def main():
    """Example usage of the Facebook auto-login functionality."""
    try:
        # Load credentials from environment variables
        email, password = load_credentials_from_env()
        
        # Create profile manager
        profile_manager = ChromeProfileManager()
        
        # Create Facebook auto-login instance
        fb_login = FacebookAutoLogin(profile_manager)
        
        # Attempt login
        result = fb_login.login_to_facebook(email, password, "my_facebook_profile")
        
        # Print result
        print(f"Login Result: {result}")
        
        if result['success']:
            print("Login successful! Keeping session alive for 2 minutes...")
            fb_login.keep_session_alive(2)
        
        # Clean up
        fb_login.close_browser()
        
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()