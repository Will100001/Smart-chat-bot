"""
Main entry point for the webhook-based Chrome browser controller.
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.webhook_server import WebhookServer

def main():
    """Main function to start the webhook server."""
    print("🚀 Starting Webhook-based Chrome Browser Controller")
    print("=" * 50)
    
    server = WebhookServer()
    server.run()

if __name__ == '__main__':
    main()