"""
Browser controller module for Selenium-based Chrome automation.
Handles all browser interactions and actions.
"""
import logging
import time
from typing import Dict, Any, Optional, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    WebDriverException,
    ElementNotInteractableException
)
from .config import Config

logger = logging.getLogger(__name__)

class BrowserController:
    """Manages Chrome browser automation using Selenium."""
    
    def __init__(self):
        """Initialize the browser controller."""
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        
    def start_browser(self) -> Dict[str, Any]:
        """
        Start the Chrome browser with configured options.
        
        Returns:
            Dict containing success status and message.
        """
        try:
            # Configure Chrome options
            chrome_options = Options()
            
            if Config.CHROME_HEADLESS:
                chrome_options.add_argument('--headless')
            
            # Security and stability options for server environments
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')
            chrome_options.add_argument('--disable-javascript')
            chrome_options.add_argument('--no-first-run')
            chrome_options.add_argument('--disable-default-apps')
            chrome_options.add_argument('--disable-background-timer-throttling')
            chrome_options.add_argument('--disable-backgrounding-occluded-windows')
            chrome_options.add_argument('--disable-renderer-backgrounding')
            
            # Additional stability options
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Window size
            window_size = Config.CHROME_WINDOW_SIZE
            chrome_options.add_argument(f'--window-size={window_size}')
            
            # Initialize WebDriver
            service = None
            if Config.CHROME_DRIVER_PATH:
                service = Service(Config.CHROME_DRIVER_PATH)
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Configure timeouts
            self.driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
            self.driver.implicitly_wait(Config.IMPLICIT_WAIT_TIMEOUT)
            
            # Initialize WebDriverWait
            self.wait = WebDriverWait(self.driver, Config.IMPLICIT_WAIT_TIMEOUT)
            
            logger.info("Chrome browser started successfully")
            return {
                "success": True,
                "message": "Browser started successfully",
                "session_id": self.driver.session_id
            }
            
        except WebDriverException as e:
            logger.error(f"Failed to start browser: {str(e)}")
            return {
                "success": False,
                "error": "Failed to start browser",
                "details": str(e)
            }
    
    def stop_browser(self) -> Dict[str, Any]:
        """
        Stop the Chrome browser and clean up resources.
        
        Returns:
            Dict containing success status and message.
        """
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.wait = None
                logger.info("Browser stopped successfully")
                return {
                    "success": True,
                    "message": "Browser stopped successfully"
                }
            else:
                return {
                    "success": True,
                    "message": "Browser was not running"
                }
        except Exception as e:
            logger.error(f"Error stopping browser: {str(e)}")
            return {
                "success": False,
                "error": "Failed to stop browser",
                "details": str(e)
            }
    
    def open_url(self, url: str) -> Dict[str, Any]:
        """
        Navigate to a specified URL.
        
        Args:
            url: The URL to navigate to.
            
        Returns:
            Dict containing success status and current URL.
        """
        if not self.driver:
            return {
                "success": False,
                "error": "Browser not started"
            }
        
        try:
            logger.info(f"Navigating to URL: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(2)
            
            current_url = self.driver.current_url
            title = self.driver.title
            
            logger.info(f"Successfully loaded page: {title}")
            return {
                "success": True,
                "message": f"Successfully navigated to {url}",
                "current_url": current_url,
                "page_title": title
            }
            
        except TimeoutException:
            logger.error(f"Timeout loading URL: {url}")
            return {
                "success": False,
                "error": "Page load timeout",
                "url": url
            }
        except Exception as e:
            logger.error(f"Error loading URL {url}: {str(e)}")
            return {
                "success": False,
                "error": "Failed to load URL",
                "details": str(e)
            }
    
    def click_element(self, selector: str, selector_type: str = "css") -> Dict[str, Any]:
        """
        Click an element identified by a selector.
        
        Args:
            selector: The selector string to find the element.
            selector_type: Type of selector ('css', 'xpath', 'id', 'class', 'tag').
            
        Returns:
            Dict containing success status and message.
        """
        if not self.driver:
            return {
                "success": False,
                "error": "Browser not started"
            }
        
        try:
            # Map selector types to Selenium By methods
            by_mapping = {
                "css": By.CSS_SELECTOR,
                "xpath": By.XPATH,
                "id": By.ID,
                "class": By.CLASS_NAME,
                "tag": By.TAG_NAME,
                "name": By.NAME
            }
            
            if selector_type not in by_mapping:
                return {
                    "success": False,
                    "error": f"Invalid selector type: {selector_type}"
                }
            
            by_method = by_mapping[selector_type]
            
            # Wait for element to be clickable
            element = self.wait.until(
                EC.element_to_be_clickable((by_method, selector))
            )
            
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Brief pause after scrolling
            
            # Click the element
            element.click()
            
            logger.info(f"Successfully clicked element: {selector}")
            return {
                "success": True,
                "message": f"Successfully clicked element with {selector_type} selector: {selector}"
            }
            
        except TimeoutException:
            logger.error(f"Element not found or not clickable: {selector}")
            return {
                "success": False,
                "error": "Element not found or not clickable",
                "selector": selector,
                "selector_type": selector_type
            }
        except ElementNotInteractableException:
            logger.error(f"Element not interactable: {selector}")
            return {
                "success": False,
                "error": "Element not interactable",
                "selector": selector
            }
        except Exception as e:
            logger.error(f"Error clicking element {selector}: {str(e)}")
            return {
                "success": False,
                "error": "Failed to click element",
                "details": str(e)
            }
    
    def fill_form_field(self, selector: str, text: str, selector_type: str = "css", clear_first: bool = True) -> Dict[str, Any]:
        """
        Fill a form field with text.
        
        Args:
            selector: The selector string to find the input element.
            text: The text to enter into the field.
            selector_type: Type of selector ('css', 'xpath', 'id', 'class', 'tag').
            clear_first: Whether to clear the field before entering text.
            
        Returns:
            Dict containing success status and message.
        """
        if not self.driver:
            return {
                "success": False,
                "error": "Browser not started"
            }
        
        try:
            by_mapping = {
                "css": By.CSS_SELECTOR,
                "xpath": By.XPATH,
                "id": By.ID,
                "class": By.CLASS_NAME,
                "tag": By.TAG_NAME,
                "name": By.NAME
            }
            
            if selector_type not in by_mapping:
                return {
                    "success": False,
                    "error": f"Invalid selector type: {selector_type}"
                }
            
            by_method = by_mapping[selector_type]
            
            # Wait for element to be present and visible
            element = self.wait.until(
                EC.visibility_of_element_located((by_method, selector))
            )
            
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            # Clear field if requested
            if clear_first:
                element.clear()
            
            # Enter text
            element.send_keys(text)
            
            logger.info(f"Successfully filled field: {selector}")
            return {
                "success": True,
                "message": f"Successfully filled field with {selector_type} selector: {selector}",
                "text_length": len(text)
            }
            
        except TimeoutException:
            logger.error(f"Form field not found: {selector}")
            return {
                "success": False,
                "error": "Form field not found",
                "selector": selector,
                "selector_type": selector_type
            }
        except Exception as e:
            logger.error(f"Error filling form field {selector}: {str(e)}")
            return {
                "success": False,
                "error": "Failed to fill form field",
                "details": str(e)
            }
    
    def get_page_info(self) -> Dict[str, Any]:
        """
        Get current page information.
        
        Returns:
            Dict containing page title, URL, and other metadata.
        """
        if not self.driver:
            return {
                "success": False,
                "error": "Browser not started"
            }
        
        try:
            return {
                "success": True,
                "url": self.driver.current_url,
                "title": self.driver.title,
                "window_size": self.driver.get_window_size(),
                "session_id": self.driver.session_id
            }
        except Exception as e:
            logger.error(f"Error getting page info: {str(e)}")
            return {
                "success": False,
                "error": "Failed to get page info",
                "details": str(e)
            }
    
    def execute_multiple_actions(self, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute multiple browser actions in sequence.
        
        Args:
            actions: List of action dictionaries.
            
        Returns:
            Dict containing results of all actions.
        """
        results = []
        
        for i, action in enumerate(actions):
            action_type = action.get('action')
            
            if action_type == 'open_url':
                result = self.open_url(action.get('url', ''))
            elif action_type == 'click_element':
                result = self.click_element(
                    action.get('selector', ''),
                    action.get('selector_type', 'css')
                )
            elif action_type == 'fill_form_field':
                result = self.fill_form_field(
                    action.get('selector', ''),
                    action.get('text', ''),
                    action.get('selector_type', 'css'),
                    action.get('clear_first', True)
                )
            elif action_type == 'wait':
                time.sleep(action.get('seconds', 1))
                result = {"success": True, "message": f"Waited {action.get('seconds', 1)} seconds"}
            else:
                result = {
                    "success": False,
                    "error": f"Unknown action type: {action_type}"
                }
            
            results.append({
                "action_index": i,
                "action_type": action_type,
                "result": result
            })
            
            # Stop execution if an action fails and fail_on_error is True
            if not result.get('success') and action.get('fail_on_error', False):
                break
        
        # Calculate overall success
        success_count = sum(1 for r in results if r['result'].get('success'))
        total_count = len(results)
        
        return {
            "success": success_count == total_count,
            "total_actions": total_count,
            "successful_actions": success_count,
            "failed_actions": total_count - success_count,
            "results": results
        }