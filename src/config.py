"""
Configuration module for webhook-based Chrome browser control.
Handles environment variables and security settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the webhook browser controller."""
    
    # Server configuration
    HOST = os.getenv('WEBHOOK_HOST', '127.0.0.1')
    PORT = int(os.getenv('WEBHOOK_PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Security configuration
    SECRET_TOKEN = os.getenv('WEBHOOK_SECRET_TOKEN')
    if not SECRET_TOKEN:
        print("WARNING: WEBHOOK_SECRET_TOKEN not set. Using default token for development.")
        SECRET_TOKEN = 'dev-token-change-me'
    
    # Chrome WebDriver configuration
    CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH')  # Optional, will use PATH if not set
    CHROME_HEADLESS = os.getenv('CHROME_HEADLESS', 'False').lower() == 'true'
    CHROME_WINDOW_SIZE = os.getenv('CHROME_WINDOW_SIZE', '1920,1080')
    
    # Browser timeouts (in seconds)
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', 30))
    IMPLICIT_WAIT_TIMEOUT = int(os.getenv('IMPLICIT_WAIT_TIMEOUT', 10))
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'webhook_browser.log')
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration settings."""
        errors = []
        
        if not cls.SECRET_TOKEN or cls.SECRET_TOKEN == 'dev-token-change-me':
            errors.append("WEBHOOK_SECRET_TOKEN should be set to a secure value in production")
        
        try:
            width, height = map(int, cls.CHROME_WINDOW_SIZE.split(','))
            if width <= 0 or height <= 0:
                errors.append("CHROME_WINDOW_SIZE must be positive integers")
        except ValueError:
            errors.append("CHROME_WINDOW_SIZE must be in format 'width,height'")
        
        return errors