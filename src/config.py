"""
Configuration management for Facebook Messenger Bot
"""
import os
import yaml
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

class BotConfig:
    """Configuration manager for the Facebook Messenger Bot"""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or environment variables"""
        if self.config_file and os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        
        # Default configuration with environment variable fallbacks
        return {
            'facebook': {
                'email': os.getenv('FACEBOOK_EMAIL', ''),
                'password': os.getenv('FACEBOOK_PASSWORD', ''),
                'messenger_url': 'https://www.messenger.com/',
                'login_timeout': 30,
                'message_check_interval': 5
            },
            'selenium': {
                'headless': os.getenv('HEADLESS', 'false').lower() == 'true',
                'window_size': [1920, 1080],
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'implicit_wait': 10,
                'page_load_timeout': 30,
                'bitbrowser_port': os.getenv('BITBROWSER_PORT', None)
            },
            'auto_replies': {
                'enabled': True,
                'keywords': {
                    'hello': ['Hi there! How can I help you today?', 'Hello! What can I do for you?'],
                    'help': ['I\'m here to assist you. What do you need help with?', 'How can I help you?'],
                    'thanks': ['You\'re welcome!', 'Happy to help!', 'No problem at all!'],
                    'bye': ['Goodbye! Have a great day!', 'See you later!', 'Take care!']
                },
                'default_reply': ['I received your message. Let me get back to you soon!'],
                'delay_range': [1, 3]  # Random delay between responses in seconds
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key path (e.g., 'facebook.email')"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by key path"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value
    
    def save_config(self, file_path: str = None) -> None:
        """Save current configuration to file"""
        if not file_path:
            file_path = self.config_file or 'config.yaml'
            
        with open(file_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False, indent=2)
    
    def get_auto_reply_keywords(self) -> Dict[str, List[str]]:
        """Get auto-reply keywords and responses"""
        return self.get('auto_replies.keywords', {})
    
    def add_auto_reply(self, keyword: str, responses: List[str]) -> None:
        """Add or update auto-reply for a keyword"""
        keywords = self.get_auto_reply_keywords()
        keywords[keyword.lower()] = responses
        self.set('auto_replies.keywords', keywords)