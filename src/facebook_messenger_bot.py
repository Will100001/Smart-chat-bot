"""
Facebook Messenger Browser Automation Bot
A chatbot that interacts with Facebook Messenger through browser automation
"""
import time
import logging
import random
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

try:
    from .config import BotConfig
    from .message_handler import MessageHandler
except ImportError:
    from config import BotConfig
    from message_handler import MessageHandler

class FacebookMessengerBot:
    """Facebook Messenger automation bot using Selenium"""
    
    def __init__(self, config_file: str = None, headless: bool = False):
        self.config = BotConfig(config_file)
        self.config.set('selenium.headless', headless)
        
        # Set up logging
        logging.basicConfig(
            level=getattr(logging, self.config.get('logging.level', 'INFO')),
            format=self.config.get('logging.format')
        )
        self.logger = logging.getLogger(__name__)
        
        self.driver = None
        self.wait = None
        self.message_handler = MessageHandler(self.config)
        self.is_logged_in = False
        self.current_chat = None
        
    def _setup_chrome_options(self) -> Options:
        """Configure Chrome options for the bot"""
        options = Options()
        
        # Basic options
        if self.config.get('selenium.headless'):
            options.add_argument('--headless')
            
        options.add_argument(f'--user-agent={self.config.get("selenium.user_agent")}')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Window size
        window_size = self.config.get('selenium.window_size', [1920, 1080])
        options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
        
        # Bitbrowser compatibility
        bitbrowser_port = self.config.get('selenium.bitbrowser_port')
        if bitbrowser_port:
            options.add_argument(f'--remote-debugging-port={bitbrowser_port}')
            
        # Additional stealth options
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins-discovery')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=VizDisplayCompositor')
        
        return options
    
    def start_browser(self) -> bool:
        """Initialize and start the browser"""
        try:
            self.logger.info("Starting browser...")
            
            options = self._setup_chrome_options()
            
            # Try undetected-chromedriver first for better stealth
            try:
                self.driver = uc.Chrome(options=options)
                self.logger.info("Using undetected-chromedriver")
            except Exception as e:
                self.logger.warning(f"Undetected-chromedriver failed: {e}")
                self.logger.info("Falling back to regular ChromeDriver")
                
                # Fallback to regular ChromeDriver
                service = webdriver.ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            
            # Configure timeouts
            self.driver.implicitly_wait(self.config.get('selenium.implicit_wait', 10))
            self.driver.set_page_load_timeout(self.config.get('selenium.page_load_timeout', 30))
            
            self.wait = WebDriverWait(self.driver, 10)
            
            # Execute stealth script
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("Browser started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start browser: {e}")
            return False
    
    def login_to_facebook(self) -> bool:
        """Login to Facebook Messenger"""
        try:
            email = self.config.get('facebook.email')
            password = self.config.get('facebook.password')
            
            if not email or not password:
                self.logger.error("Facebook credentials not provided in configuration")
                return False
                
            self.logger.info("Navigating to Facebook Messenger...")
            self.driver.get(self.config.get('facebook.messenger_url'))
            
            # Wait for page to load
            time.sleep(3)
            
            # Check if already logged in
            if self._is_logged_in():
                self.logger.info("Already logged in to Facebook Messenger")
                self.is_logged_in = True
                return True
            
            # Look for login elements
            self.logger.info("Attempting to login...")
            
            # Try to find email field
            email_selectors = ['#email', '[name="email"]', '[type="email"]', '#m_login_email']
            email_field = None
            
            for selector in email_selectors:
                try:
                    email_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    break
                except TimeoutException:
                    continue
                    
            if not email_field:
                self.logger.error("Could not find email field")
                return False
                
            # Enter email
            email_field.clear()
            email_field.send_keys(email)
            
            # Find password field
            password_selectors = ['#pass', '[name="pass"]', '[type="password"]', '#m_login_password']
            password_field = None
            
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
                    
            if not password_field:
                self.logger.error("Could not find password field")
                return False
                
            # Enter password
            password_field.clear()
            password_field.send_keys(password)
            
            # Find and click login button
            login_selectors = [
                '[name="login"]', 
                '[type="submit"]', 
                '#loginbutton',
                'button[data-testid="royal_login_button"]'
            ]
            
            login_button = None
            for selector in login_selectors:
                try:
                    login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
                    
            if login_button:
                login_button.click()
            else:
                # Try pressing Enter
                password_field.send_keys(Keys.RETURN)
            
            # Wait for login to complete
            self.logger.info("Waiting for login to complete...")
            time.sleep(5)
            
            # Check if login was successful
            if self._is_logged_in():
                self.logger.info("Successfully logged in to Facebook Messenger")
                self.is_logged_in = True
                return True
            else:
                self.logger.error("Login failed - check credentials or handle 2FA/captcha")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during login: {e}")
            return False
    
    def _is_logged_in(self) -> bool:
        """Check if currently logged in to Facebook Messenger"""
        try:
            # Look for indicators that we're logged in
            logged_in_indicators = [
                '[data-testid="MessengerAppShell"]',
                '.messenger-app',
                '[role="main"]',
                '.conversation-list',
                '#js_1'  # Common Facebook main container
            ]
            
            for selector in logged_in_indicators:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element:
                        return True
                except NoSuchElementException:
                    continue
                    
            # Check URL
            current_url = self.driver.current_url
            if 'messenger.com' in current_url and 'login' not in current_url:
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking login status: {e}")
            return False
    
    def close(self):
        """Close the browser and cleanup"""
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("Browser closed")
        except Exception as e:
            self.logger.error(f"Error closing browser: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()