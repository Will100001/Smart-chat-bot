"""
Example script to test the webhook-based Chrome browser controller.
This script demonstrates how to send requests to the webhook server.
"""
import requests
import json
import time
from typing import Dict, Any

class WebhookTester:
    """Utility class for testing webhook endpoints."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:5000", token: str = "dev-token-change-me"):
        """
        Initialize the webhook tester.
        
        Args:
            base_url: Base URL of the webhook server.
            token: Authentication token.
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    
    def send_request(self, endpoint: str, method: str = 'POST', data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Send a request to the webhook server.
        
        Args:
            endpoint: API endpoint to call.
            method: HTTP method (GET, POST).
            data: Request payload.
            
        Returns:
            Response data as dictionary.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers)
            else:
                response = requests.post(url, headers=self.headers, json=data)
            
            print(f"🔗 {method} {url}")
            print(f"📊 Status: {response.status_code}")
            
            try:
                result = response.json()
                print(f"📝 Response: {json.dumps(result, indent=2)}")
                return result
            except json.JSONDecodeError:
                print(f"📝 Response: {response.text}")
                return {"error": "Invalid JSON response", "text": response.text}
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {str(e)}")
            return {"error": "Request failed", "details": str(e)}
    
    def test_health_check(self):
        """Test the health check endpoint."""
        print("\n🏥 Testing health check...")
        return self.send_request('/health', 'GET')
    
    def test_start_browser(self):
        """Test starting the browser."""
        print("\n🚀 Testing browser start...")
        return self.send_request('/browser/start')
    
    def test_stop_browser(self):
        """Test stopping the browser."""
        print("\n🛑 Testing browser stop...")
        return self.send_request('/browser/stop')
    
    def test_open_url(self, url: str):
        """Test opening a URL."""
        print(f"\n🌐 Testing open URL: {url}")
        return self.send_request('/browser/open_url', data={'url': url})
    
    def test_click_element(self, selector: str, selector_type: str = 'css'):
        """Test clicking an element."""
        print(f"\n👆 Testing click element: {selector}")
        return self.send_request('/browser/click_element', data={
            'selector': selector,
            'selector_type': selector_type
        })
    
    def test_fill_form(self, selector: str, text: str, selector_type: str = 'css'):
        """Test filling a form field."""
        print(f"\n✏️ Testing fill form: {selector}")
        return self.send_request('/browser/fill_form', data={
            'selector': selector,
            'text': text,
            'selector_type': selector_type
        })
    
    def test_page_info(self):
        """Test getting page information."""
        print("\n📄 Testing page info...")
        return self.send_request('/browser/page_info', 'GET')
    
    def test_multiple_actions(self):
        """Test executing multiple actions."""
        print("\n🔄 Testing multiple actions...")
        actions = [
            {
                "action": "open_url",
                "url": "https://httpbin.org/forms/post"
            },
            {
                "action": "wait",
                "seconds": 2
            },
            {
                "action": "fill_form_field",
                "selector": "input[name='custname']",
                "text": "Test User",
                "selector_type": "css"
            },
            {
                "action": "fill_form_field",
                "selector": "input[name='custtel']",
                "text": "123-456-7890",
                "selector_type": "css"
            }
        ]
        return self.send_request('/browser/execute_actions', data={'actions': actions})

def run_basic_tests():
    """Run basic functionality tests."""
    print("🧪 Starting Webhook Browser Controller Tests")
    print("=" * 50)
    
    tester = WebhookTester()
    
    # Test health check
    tester.test_health_check()
    
    # Test browser lifecycle
    tester.test_start_browser()
    time.sleep(2)  # Give browser time to start
    
    # Test basic navigation
    tester.test_open_url("https://httpbin.org/")
    time.sleep(2)
    
    # Test page info
    tester.test_page_info()
    
    # Test form interaction
    tester.test_open_url("https://httpbin.org/forms/post")
    time.sleep(2)
    
    tester.test_fill_form("input[name='custname']", "Test User")
    time.sleep(1)
    
    tester.test_fill_form("input[name='custtel']", "123-456-7890")
    time.sleep(1)
    
    # Test multiple actions
    tester.test_multiple_actions()
    
    # Clean up
    time.sleep(2)
    tester.test_stop_browser()
    
    print("\n✅ Test run completed!")

def run_advanced_tests():
    """Run advanced functionality tests."""
    print("🔬 Starting Advanced Tests")
    print("=" * 30)
    
    tester = WebhookTester()
    
    # Start browser
    tester.test_start_browser()
    time.sleep(2)
    
    # Test Google search
    print("\n🔍 Testing Google Search...")
    tester.test_open_url("https://www.google.com")
    time.sleep(3)
    
    # Accept cookies if present (common on Google)
    tester.test_click_element("button[id='L2AGLb']", "css")  # Google cookie accept button
    time.sleep(1)
    
    # Search for something
    tester.test_fill_form("input[name='q']", "Selenium WebDriver", "name")
    time.sleep(1)
    
    # Submit search (press Enter key is simulated by clicking search button)
    tester.test_click_element("input[name='btnK']", "name")
    time.sleep(3)
    
    # Get page info
    tester.test_page_info()
    
    # Clean up
    tester.test_stop_browser()
    
    print("\n✅ Advanced test run completed!")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'advanced':
        run_advanced_tests()
    else:
        run_basic_tests()
        
        print("\n💡 To run advanced tests, use:")
        print("python examples/test_webhook.py advanced")