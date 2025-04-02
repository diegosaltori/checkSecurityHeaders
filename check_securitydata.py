import re
import sys
import json
import logging
from seleniumwire import webdriver  # Selenium Wire for intercepting requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from models.functions import Functions

def check_api_exposure():
    """Opens the browser and intercepts API requests to check for data exposure."""
    while True:
        url = Functions.get_url()
        monitored_api = input("Enter the base URL of the API you want to monitor (optional, press ENTER to skip): ").strip()
        
        try:
            driver = setup_browser()
            driver.get(url)
            
            print("🔹 Complete the login and navigate through the application.")
            input("🔹 When finished, press ENTER to analyze the requests...")

            print("\n🔍 Intercepting API requests and JS files...")
            intercept_requests(driver, monitored_api)
        
        except Exception as e:
            logging.error(f"Error: {e}")
        
        finally:
            driver.quit()

        user_input = input("Do you want to run the test again? (yes/no): ").strip().lower()
        if user_input != "yes":
            print("Exiting...")
            sys.exit()

def setup_browser():
    """Configures and returns a browser with Selenium Wire for API and JS interception."""
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def intercept_requests(driver, monitored_api):
    """Intercepts API requests and JavaScript files made by the browser."""
    patterns = {
        "API Keys": r"(?i)(api_key|apikey|auth_token|access_token|secret|password|REACT_APP_API_KEY)[=:\"'](\S+)",
        "Emails": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "JWT Tokens": r"eyJ[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+",
        "CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
        "CNPJ": r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b",
        "Credit Card": r"\b(\d{4}[- ]?){3}\d{4}\b",
    }
    
    if not driver.requests:
        print("⚠️ No requests intercepted. Check if there is traffic in the application.")
    
    for request in driver.requests:
        if request.response:
            try:
                content_type = request.response.headers.get('Content-Type', '')
                
                # Checks if the URL matches the monitored API or if no API was specified
                if not monitored_api or monitored_api in request.url:
                    print(f"\n🌐 Intercepted: {request.url}")
                    
                    # If it's JSON, check for sensitive data
                    if "json" in content_type:
                        response_body = request.response.body.decode('utf-8', errors='ignore')
                        analyze_response(response_body, patterns)
                    
                    # If it's a JS file, check for possible data exposure
                    elif request.url.endswith(".js"):
                        response_body = request.response.body.decode('utf-8', errors='ignore')
                        analyze_response(response_body, patterns)
            
            except Exception as e:
                print(f"⚠️ Error processing response from {request.url}: {e}")

def analyze_response(response, patterns):
    """Checks for sensitive data in API responses and JS files."""
    for name, pattern in patterns.items():
        matches = re.findall(pattern, response)
        if matches:
            print(f"⚠️ Possible exposure of {name} found:")
            for match in matches:
                print(f"  - {match}")
            print('-' * 40)
        else:
            print(f"✅ No exposure of {name} detected.")

if __name__ == "__main__":
    Functions.setup_logger_security_data_exposure()
    Functions.banner_securitydata()
    check_api_exposure()
