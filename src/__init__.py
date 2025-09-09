"""
Facebook Messenger Bot Package
"""

try:
    from .facebook_messenger_bot import FacebookMessengerBot
    from .config import BotConfig
    from .message_handler import MessageHandler
except ImportError:
    from facebook_messenger_bot import FacebookMessengerBot
    from config import BotConfig
    from message_handler import MessageHandler

__version__ = "1.0.0"
__author__ = "Smart Chat Bot Team"

__all__ = ["FacebookMessengerBot", "BotConfig", "MessageHandler"]