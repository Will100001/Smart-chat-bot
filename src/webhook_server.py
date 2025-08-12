"""
Webhook server module for receiving and processing browser control requests.
Uses Flask to handle HTTP requests and coordinates with the browser controller.
"""
import logging
import json
from functools import wraps
from typing import Dict, Any
from flask import Flask, request, jsonify
from .config import Config
from .browser_controller import BrowserController

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class WebhookServer:
    """Webhook server for browser control automation."""
    
    def __init__(self):
        """Initialize the webhook server."""
        self.app = Flask(__name__)
        self.browser = BrowserController()
        self.setup_routes()
        
    def validate_token(self, f):
        """Decorator to validate webhook secret token."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check for Authorization header
            auth_header = request.headers.get('Authorization')
            if auth_header:
                # Format: "Bearer <token>"
                parts = auth_header.split(' ')
                if len(parts) == 2 and parts[0] == 'Bearer':
                    token = parts[1]
                else:
                    token = auth_header
            else:
                # Check for token in request body
                if request.is_json:
                    token = request.json.get('token')
                else:
                    token = request.form.get('token')
            
            if not token or token != Config.SECRET_TOKEN:
                logger.warning(f"Unauthorized webhook request from {request.remote_addr}")
                return jsonify({
                    "success": False,
                    "error": "Unauthorized",
                    "message": "Invalid or missing authentication token"
                }), 401
            
            return f(*args, **kwargs)
        return decorated_function
    
    def setup_routes(self):
        """Set up Flask routes for the webhook server."""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            return jsonify({
                "success": True,
                "message": "Webhook server is running",
                "browser_active": self.browser.driver is not None
            })
        
        @self.app.route('/browser/start', methods=['POST'])
        @self.validate_token
        def start_browser():
            """Start the Chrome browser."""
            try:
                result = self.browser.start_browser()
                status_code = 200 if result.get('success') else 500
                return jsonify(result), status_code
            except Exception as e:
                logger.error(f"Error in start_browser: {str(e)}")
                return jsonify({
                    "success": False,
                    "error": "Internal server error",
                    "details": str(e)
                }), 500
        
        @self.app.route('/browser/stop', methods=['POST'])
        @self.validate_token
        def stop_browser():
            """Stop the Chrome browser."""
            try:
                result = self.browser.stop_browser()
                return jsonify(result)
            except Exception as e:
                logger.error(f"Error in stop_browser: {str(e)}")
                return jsonify({
                    "success": False,
                    "error": "Internal server error",
                    "details": str(e)
                }), 500
        
        @self.app.route('/browser/open_url', methods=['POST'])
        @self.validate_token
        def open_url():
            """Open a URL in the browser."""
            try:
                if not request.is_json:
                    return jsonify({
                        "success": False,
                        "error": "Content-Type must be application/json"
                    }), 400
                
                data = request.get_json()
                url = data.get('url')
                
                if not url:
                    return jsonify({
                        "success": False,
                        "error": "Missing required parameter: url"
                    }), 400
                
                result = self.browser.open_url(url)
                status_code = 200 if result.get('success') else 500
                return jsonify(result), status_code
                
            except Exception as e:
                logger.error(f"Error in open_url: {str(e)}")
                return jsonify({
                    "success": False,
                    "error": "Internal server error",
                    "details": str(e)
                }), 500
        
        @self.app.route('/browser/click_element', methods=['POST'])
        @self.validate_token
        def click_element():
            """Click an element in the browser."""
            try:
                if not request.is_json:
                    return jsonify({
                        "success": False,
                        "error": "Content-Type must be application/json"
                    }), 400
                
                data = request.get_json()
                selector = data.get('selector')
                selector_type = data.get('selector_type', 'css')
                
                if not selector:
                    return jsonify({
                        "success": False,
                        "error": "Missing required parameter: selector"
                    }), 400
                
                result = self.browser.click_element(selector, selector_type)
                status_code = 200 if result.get('success') else 500
                return jsonify(result), status_code
                
            except Exception as e:
                logger.error(f"Error in click_element: {str(e)}")
                return jsonify({
                    "success": False,
                    "error": "Internal server error",
                    "details": str(e)
                }), 500
        
        @self.app.route('/browser/fill_form', methods=['POST'])
        @self.validate_token
        def fill_form():
            """Fill a form field in the browser."""
            try:
                if not request.is_json:
                    return jsonify({
                        "success": False,
                        "error": "Content-Type must be application/json"
                    }), 400
                
                data = request.get_json()
                selector = data.get('selector')
                text = data.get('text')
                selector_type = data.get('selector_type', 'css')
                clear_first = data.get('clear_first', True)
                
                if not selector:
                    return jsonify({
                        "success": False,
                        "error": "Missing required parameter: selector"
                    }), 400
                
                if text is None:
                    return jsonify({
                        "success": False,
                        "error": "Missing required parameter: text"
                    }), 400
                
                result = self.browser.fill_form_field(selector, str(text), selector_type, clear_first)
                status_code = 200 if result.get('success') else 500
                return jsonify(result), status_code
                
            except Exception as e:
                logger.error(f"Error in fill_form: {str(e)}")
                return jsonify({
                    "success": False,
                    "error": "Internal server error",
                    "details": str(e)
                }), 500
        
        @self.app.route('/browser/page_info', methods=['GET'])
        @self.validate_token
        def get_page_info():
            """Get current page information."""
            try:
                result = self.browser.get_page_info()
                status_code = 200 if result.get('success') else 500
                return jsonify(result), status_code
                
            except Exception as e:
                logger.error(f"Error in get_page_info: {str(e)}")
                return jsonify({
                    "success": False,
                    "error": "Internal server error",
                    "details": str(e)
                }), 500
        
        @self.app.route('/browser/execute_actions', methods=['POST'])
        @self.validate_token
        def execute_actions():
            """Execute multiple browser actions in sequence."""
            try:
                if not request.is_json:
                    return jsonify({
                        "success": False,
                        "error": "Content-Type must be application/json"
                    }), 400
                
                data = request.get_json()
                actions = data.get('actions')
                
                if not actions or not isinstance(actions, list):
                    return jsonify({
                        "success": False,
                        "error": "Missing or invalid parameter: actions (must be a list)"
                    }), 400
                
                result = self.browser.execute_multiple_actions(actions)
                status_code = 200 if result.get('success') else 500
                return jsonify(result), status_code
                
            except Exception as e:
                logger.error(f"Error in execute_actions: {str(e)}")
                return jsonify({
                    "success": False,
                    "error": "Internal server error",
                    "details": str(e)
                }), 500
        
        @self.app.errorhandler(404)
        def not_found(error):
            """Handle 404 errors."""
            return jsonify({
                "success": False,
                "error": "Endpoint not found",
                "message": "The requested endpoint does not exist"
            }), 404
        
        @self.app.errorhandler(405)
        def method_not_allowed(error):
            """Handle 405 errors."""
            return jsonify({
                "success": False,
                "error": "Method not allowed",
                "message": "The requested method is not allowed for this endpoint"
            }), 405
        
        @self.app.errorhandler(500)
        def internal_error(error):
            """Handle 500 errors."""
            logger.error(f"Internal server error: {str(error)}")
            return jsonify({
                "success": False,
                "error": "Internal server error",
                "message": "An unexpected error occurred"
            }), 500
    
    def run(self, host: str = None, port: int = None, debug: bool = None):
        """
        Run the webhook server.
        
        Args:
            host: Server host (defaults to config value).
            port: Server port (defaults to config value).
            debug: Debug mode (defaults to config value).
        """
        # Validate configuration
        config_errors = Config.validate_config()
        if config_errors:
            logger.warning("Configuration warnings:")
            for error in config_errors:
                logger.warning(f"  - {error}")
        
        # Use provided values or fall back to config
        host = host or Config.HOST
        port = port or Config.PORT
        debug = debug if debug is not None else Config.DEBUG
        
        logger.info(f"Starting webhook server on {host}:{port}")
        logger.info(f"Debug mode: {debug}")
        
        try:
            self.app.run(host=host, port=port, debug=debug)
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
        finally:
            # Clean up browser if it's running
            if self.browser.driver:
                self.browser.stop_browser()
                logger.info("Browser cleaned up on server shutdown")

def create_app():
    """Factory function to create Flask app for testing."""
    server = WebhookServer()
    return server.app

if __name__ == '__main__':
    # Run the server if this module is executed directly
    server = WebhookServer()
    server.run()