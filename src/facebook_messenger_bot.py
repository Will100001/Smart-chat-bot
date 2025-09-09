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
    
    def get_conversations(self) -> List[Dict]:
        """Get list of available conversations"""
        try:
            if not self.is_logged_in:
                self.logger.error("Not logged in")
                return []
                
            # Look for conversation list
            conversation_selectors = [
                '[data-testid="conversation-list"]',
                '.conversation-list',
                '[role="grid"]',
                '.thread-list'
            ]
            
            conversations = []
            
            for selector in conversation_selectors:
                try:
                    conv_list = self.driver.find_element(By.CSS_SELECTOR, selector)
                    conv_items = conv_list.find_elements(By.CSS_SELECTOR, '[role="gridcell"], .conversation-item')
                    
                    for item in conv_items[:10]:  # Limit to first 10
                        try:
                            name_element = item.find_element(By.CSS_SELECTOR, 'span, strong, .name')
                            name = name_element.text.strip()
                            
                            if name:
                                conversations.append({
                                    'name': name,
                                    'element': item
                                })
                        except NoSuchElementException:
                            continue
                            
                    if conversations:
                        break
                        
                except NoSuchElementException:
                    continue
                    
            self.logger.info(f"Found {len(conversations)} conversations")
            return conversations
            
        except Exception as e:
            self.logger.error(f"Error getting conversations: {e}")
            return []
    
    def open_conversation(self, conversation_name: str) -> bool:
        """Open a specific conversation"""
        try:
            conversations = self.get_conversations()
            
            for conv in conversations:
                if conversation_name.lower() in conv['name'].lower():
                    conv['element'].click()
                    time.sleep(2)
                    self.current_chat = conversation_name
                    self.logger.info(f"Opened conversation with {conversation_name}")
                    return True
                    
            self.logger.error(f"Conversation '{conversation_name}' not found")
            return False
            
        except Exception as e:
            self.logger.error(f"Error opening conversation: {e}")
            return False
    
    def get_messages(self) -> List:
        """Get messages from current conversation"""
        try:
            if not self.current_chat:
                self.logger.error("No conversation is currently open")
                return []
                
            # Look for message container
            message_selectors = [
                '[data-testid="message-container"]',
                '.message-list',
                '[role="log"]',
                '.conversation-messages'
            ]
            
            message_elements = []
            
            for selector in message_selectors:
                try:
                    container = self.driver.find_element(By.CSS_SELECTOR, selector)
                    messages = container.find_elements(By.CSS_SELECTOR, '[data-testid*="message"], .message')
                    
                    if messages:
                        message_elements = messages
                        break
                        
                except NoSuchElementException:
                    continue
            
            # If no specific message container found, look for general message patterns
            if not message_elements:
                message_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                    'div[role="gridcell"] > div, .message-item, [data-scope="messages_table"] div')
            
            self.logger.debug(f"Found {len(message_elements)} message elements")
            return message_elements
            
        except Exception as e:
            self.logger.error(f"Error getting messages: {e}")
            return []
    
    def send_message(self, text: str) -> bool:
        """Send a message in the current conversation"""
        try:
            if not self.current_chat:
                self.logger.error("No conversation is currently open")
                return False
                
            # Look for message input field
            input_selectors = [
                '[data-testid="message-input"]',
                '[contenteditable="true"]',
                '.message-input',
                'div[role="textbox"]',
                '[aria-label*="message"]'
            ]
            
            input_field = None
            for selector in input_selectors:
                try:
                    input_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
                    
            if not input_field:
                self.logger.error("Could not find message input field")
                return False
                
            # Clear and type message
            input_field.click()
            input_field.clear()
            input_field.send_keys(text)
            
            # Send message (Enter key)
            input_field.send_keys(Keys.RETURN)
            
            self.logger.info(f"Sent message: {text}")
            time.sleep(1)  # Brief pause after sending
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return False
    
    def monitor_messages(self, conversation_name: str = None, duration: int = None) -> None:
        """Monitor messages and send auto-replies"""
        try:
            if conversation_name and not self.open_conversation(conversation_name):
                return
                
            self.logger.info(f"Starting message monitoring for {self.current_chat or 'current conversation'}")
            
            start_time = time.time()
            check_interval = self.config.get('facebook.message_check_interval', 5)
            
            while True:
                # Check if duration limit reached
                if duration and (time.time() - start_time) > duration:
                    self.logger.info("Monitoring duration reached")
                    break
                    
                try:
                    # Get new messages
                    message_elements = self.get_messages()
                    
                    if message_elements:
                        # Process messages for auto-replies
                        new_messages = self.message_handler.process_messages(message_elements)
                        
                        # Send auto-replies
                        for msg_data in new_messages:
                            self.logger.info(f"Auto-replying to {msg_data['sender']}: {msg_data['reply']}")
                            
                            # Add human-like delay
                            time.sleep(msg_data['delay'])
                            
                            # Send reply
                            if self.send_message(msg_data['reply']):
                                self.logger.info("Auto-reply sent successfully")
                            else:
                                self.logger.error("Failed to send auto-reply")
                    
                except Exception as e:
                    self.logger.error(f"Error during message monitoring: {e}")
                
                # Wait before next check
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Message monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"Error in message monitoring: {e}")
    
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