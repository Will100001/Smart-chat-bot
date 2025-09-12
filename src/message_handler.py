"""
Message handler for processing and responding to Facebook Messenger messages
"""
import random
import time
import re
from typing import List, Dict, Tuple, Optional
import logging

class MessageHandler:
    """Handles message processing and auto-reply logic"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.processed_messages = set()  # Track processed messages to avoid duplicates
        
    def extract_message_text(self, message_element) -> str:
        """Extract text content from a message element"""
        try:
            # Try different selectors for message text
            text_selectors = [
                '[data-testid="message_text"]',
                '.x1y1aw1k',  # Common messenger text class
                '.x193iq5w',  # Another text class
                'span[dir="auto"]',
                '.message-text'
            ]
            
            for selector in text_selectors:
                text_elements = message_element.find_elements('css selector', selector)
                if text_elements:
                    return text_elements[0].text.strip()
                    
            # Fallback to element text
            return message_element.text.strip()
            
        except Exception as e:
            self.logger.error(f"Error extracting message text: {e}")
            return ""
    
    def extract_sender_name(self, message_element) -> str:
        """Extract sender name from message element"""
        try:
            # Try different selectors for sender name
            name_selectors = [
                '[data-testid="sender_name"]',
                '.x1iyjqo2',  # Common sender name class
                '.author-name',
                'strong'
            ]
            
            for selector in name_selectors:
                name_elements = message_element.find_elements('css selector', selector)
                if name_elements:
                    return name_elements[0].text.strip()
                    
            return "Unknown"
            
        except Exception as e:
            self.logger.error(f"Error extracting sender name: {e}")
            return "Unknown"
    
    def is_own_message(self, message_element) -> bool:
        """Check if message is sent by the bot (own message)"""
        try:
            # Look for indicators that this is our own message
            own_message_indicators = [
                'data-testid="outgoing_message"',
                '.message-out',
                '.sent-message',
                'div[data-scope="messages_table"] div[role="gridcell"]:last-child'
            ]
            
            for indicator in own_message_indicators:
                if message_element.find_elements('css selector', indicator):
                    return True
                    
            # Check parent elements
            parent = message_element.find_element('xpath', '..')
            parent_class = parent.get_attribute('class') or ''
            
            if 'outgoing' in parent_class.lower() or 'sent' in parent_class.lower():
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking message ownership: {e}")
            return False
    
    def generate_message_id(self, message_element, text: str, sender: str) -> str:
        """Generate a unique ID for message to avoid processing duplicates"""
        try:
            # Try to get actual message ID from element
            msg_id = message_element.get_attribute('data-message-id')
            if msg_id:
                return msg_id
                
            # Fallback: create hash from content and position
            element_id = message_element.get_attribute('id') or ''
            timestamp = str(int(time.time() * 1000))  # Current timestamp
            content_hash = str(hash(f"{sender}:{text}:{element_id}"))
            
            return f"{content_hash}_{timestamp}"
            
        except Exception as e:
            self.logger.error(f"Error generating message ID: {e}")
            return str(hash(f"{sender}:{text}:{time.time()}"))
    
    def should_reply_to_message(self, text: str, sender: str) -> bool:
        """Determine if bot should reply to this message"""
        if not text.strip():
            return False
            
        # Don't reply to our own messages
        if sender.lower() == "you" or sender.lower() == "me":
            return False
            
        # Check if auto-replies are enabled
        if not self.config.get('auto_replies.enabled', True):
            return False
            
        return True
    
    def find_keyword_matches(self, text: str) -> List[str]:
        """Find matching keywords in message text"""
        text_lower = text.lower()
        keywords = self.config.get_auto_reply_keywords()
        matches = []
        
        for keyword in keywords.keys():
            # Use word boundaries to match whole words
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, text_lower):
                matches.append(keyword)
                
        return matches
    
    def generate_auto_reply(self, text: str, sender: str) -> Optional[str]:
        """Generate auto-reply based on message content"""
        try:
            keywords = self.find_keyword_matches(text)
            
            if keywords:
                # Use the first matching keyword
                keyword = keywords[0]
                keyword_responses = self.config.get_auto_reply_keywords().get(keyword, [])
                
                if keyword_responses:
                    response = random.choice(keyword_responses)
                    self.logger.info(f"Generated auto-reply for keyword '{keyword}': {response}")
                    return response
            
            # Use default reply if no keywords match
            default_replies = self.config.get('auto_replies.default_reply', [])
            if default_replies:
                response = random.choice(default_replies)
                self.logger.info(f"Generated default auto-reply: {response}")
                return response
                
            return None
            
        except Exception as e:
            self.logger.error(f"Error generating auto-reply: {e}")
            return None
    
    def get_reply_delay(self) -> float:
        """Get random delay before sending reply to seem more human"""
        delay_range = self.config.get('auto_replies.delay_range', [1, 3])
        return random.uniform(delay_range[0], delay_range[1])
    
    def process_messages(self, message_elements: List) -> List[Dict]:
        """Process a list of message elements and return new messages with replies"""
        new_messages = []
        
        for element in message_elements:
            try:
                # Skip if this is our own message
                if self.is_own_message(element):
                    continue
                    
                text = self.extract_message_text(element)
                sender = self.extract_sender_name(element)
                message_id = self.generate_message_id(element, text, sender)
                
                # Skip if already processed
                if message_id in self.processed_messages:
                    continue
                    
                # Mark as processed
                self.processed_messages.add(message_id)
                
                # Check if we should reply
                if not self.should_reply_to_message(text, sender):
                    continue
                    
                # Generate reply
                reply = self.generate_auto_reply(text, sender)
                
                if reply:
                    message_data = {
                        'id': message_id,
                        'sender': sender,
                        'text': text,
                        'reply': reply,
                        'delay': self.get_reply_delay(),
                        'element': element
                    }
                    new_messages.append(message_data)
                    
                    self.logger.info(f"New message from {sender}: {text[:50]}{'...' if len(text) > 50 else ''}")
                    
            except Exception as e:
                self.logger.error(f"Error processing message element: {e}")
                continue
                
        return new_messages
    
    def clear_processed_messages(self):
        """Clear the processed messages cache"""
        self.processed_messages.clear()
        self.logger.info("Cleared processed messages cache")