import textwrap
import requests
import logging
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from halo import Halo

def setup_logger():
    logging.basicConfig(
        filename="security_headers_log.txt", 
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def print_banner():
    print("""
    ======================================
       Security Headers Checked V2.0.1.1
    Developed by Diego Garcia Saltori
    ======================================
    """)

def choose_browser():
    print("Choose a browser: (1) Chrome | (2) Firefox")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "2":
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service)
    else:
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service)

def get_url():
    url = input("Enter the website URL (without https:// is fine): ").strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url

def check_security_headers():
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
        url = get_url()
        driver = choose_browser()
        
        try:
            spinner = Halo(text='Opening browser...', spinner='dots')
            spinner.start()
            driver.get(url)
            spinner.stop()
            print("🔹 Log in manually and press ENTER in the terminal when ready.")
            input("Press ENTER to continue after logging in...")
            
            spinner.text = "Retrieving cookies..."
            spinner.start()
            cookies = driver.get_cookies()
            driver.quit()
            spinner.stop()
            
            session = requests.Session()
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])

            spinner.text = "Fetching security headers..."
            spinner.start()
            response = session.get(url)  # Usando a URL digitada pelo usuário
            headers = response.headers
            spinner.stop()
            
            security_headers = [
                "Strict-Transport-Security",
                "Content-Security-Policy",
                "X-Frame-Options",
                "X-XSS-Protection",
                "X-Content-Type-Options",
                "Referrer-Policy",
                "Permissions-Policy"
            ]
            
            log_output = f"\n🔍 Checking security headers for: {response.url}\n"
            print(log_output)
            logging.info(log_output)

            for header in security_headers:
                if header in headers:
                    wrapped_value = textwrap.fill(headers[header], width=80)
                    result = f"✅ {header}:\n{wrapped_value}\n{'-'*40}"
                else:
                    result = f"⚠️ {header} not found!\n{'-'*40}"
                print(result)
                logging.info(result)

        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            logging.error(error_msg)

        finally:
            driver.quit()

if __name__ == "__main__":
    setup_logger()
    print_banner()
    check_security_headers()
