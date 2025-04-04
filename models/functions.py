import sys
import os
import time
from datetime import datetime
from halo import Halo
import logging
# from selenium import webdriver
from seleniumwire import webdriver  # Importa seleniumwire para capturar requisições
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

# Function to choose a browser for login
def choose_browser():
    """Allows the user to choose a browser for login."""
    print("Choose a browser: (1) Chrome | (2) Firefox | (3) Edge")
    choice = input("Enter 1, 2, or 3: ").strip()

    seleniumwire_options = {}  # Dicionário para armazenar opções do seleniumwire

    if choice == "2":  # Firefox
        options = FirefoxOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options, seleniumwire_options=seleniumwire_options)

    elif choice == "3":  # Edge
        options = EdgeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options, seleniumwire_options=seleniumwire_options)

    else:  # Chrome (padrão)
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options, seleniumwire_options=seleniumwire_options)


class Functions:
    def banner_header():
        print("""
        ======================================
              Checking Security Headers  
                   Version 1.0.1
          Developed by Diego Garcia Saltori
        ======================================
        """)
    def banner_rate():
        print("""
        ======================================
             Checking Security Rate Limit 
                   Version 1.0.1
          Developed by Diego Garcia Saltori
        ======================================
        """)
    def banner_idor():
        print("""
        ======================================
              Checking Security IDOR  
                   Version 1.0.1
          Developed by Diego Garcia Saltori
        ======================================
        """)
        
    def banner_xss():
        print("""
        ======================================
              Checking Security XSS  
                   Version 1.0.1
          Developed by Diego Garcia Saltori
        ======================================
        """)
    def banner_auth():
        print("""
        ======================================
               Checking Authentication  
                   Version 1.0.1
          Developed by Diego Garcia Saltori
        ======================================
        """)
        
    def banner_securitydata():
        print("""
        ======================================
               Checking Data Exposure  
                   Version 1.0.1
          Developed by Diego Garcia Saltori
        ======================================
        """)
    # Function to capture the website URL
    def get_url():
        """Captures the website URL from the user."""
        url = input("Enter the website URL (without https:// is fine) or press ENTER to exit: ").strip()
        
        if not url:
            print("Exiting...")
            sys.exit()

        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        return url

    # Function to capture the number of requests
    def get_max_requests():
        """Captures the number of requests from the user."""
        while True:
            try:
                max_requests = int(input("Enter the number of requests to send: ").strip())
                if max_requests > 0:
                    return max_requests
                else:
                    print("Please enter a valid positive number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
    def perform_loginsource(url):
        """Opens the selected browser, waits for user login, retrieves cookies, and captures page source."""
        driver = choose_browser()
        
        spinner = Halo(text='Opening browser...', spinner='dots')
        spinner.start()
        driver.get(url)
        spinner.stop()
        
        print("🔹 If login is required, complete it manually and press ENTER in the terminal when done.")
        input("Press ENTER to continue once you have completed the login...")

        spinner.text = "Retrieving cookies and page source..."
        spinner.start()
        cookies = driver.get_cookies()
        page_source = driver.page_source  # Captura o HTML da página
        driver.quit()
        spinner.stop()
        
        return cookies, page_source  # Retorna os cookies e o HTML da página

    # Function to perform login and retrieve cookies
    def perform_login(url):
        """Opens the selected browser, waits for user login, and retrieves cookies."""
        driver = choose_browser()
        
        spinner = Halo(text='Opening browser...', spinner='dots')
        spinner.start()
        driver.get(url)
        spinner.stop()
        
        print("🔹 If login is required, complete it manually and press ENTER in the terminal when done.")
        input("Press ENTER to continue once you have completed the login...")
        
        spinner.text = "Retrieving cookies..."
        spinner.start()
        cookies = driver.get_cookies()
        driver.quit()
        spinner.stop()
        
        return cookies
    
    def get_bearer_token(login_url):
        """Attempts to capture the Bearer token using network requests, localStorage, sessionStorage, and cookies."""
        driver = choose_browser()

        print("🔐 Opening browser for authentication...")
        driver.get(login_url)

        print("🔹 If login is required, complete it manually and press ENTER in the terminal when done.")
        input("Press ENTER to continue once you have completed the login...")

        # Aguarda carregamento
        time.sleep(3)  

        # 🔍 **1. Capturar o Token nas Requisições de Rede**
        print("🔍 Searching for Bearer token in network requests...")
        for request in driver.requests:
            if request.response and "Authorization" in request.headers:
                auth_header = request.headers["Authorization"]
                if auth_header.startswith("Bearer "):
                    bearer_token = auth_header.split("Bearer ")[1]
                    print(f"✅ Bearer token found in network requests: {bearer_token[:20]}...")
                    driver.quit()
                    return bearer_token

        # 🔍 **2. Capturar o Token no localStorage/sessionStorage**
        print("🔍 Searching for Bearer token in localStorage/sessionStorage...")
        script = """
        let token = null;
        for (let key in localStorage) {
            if (key.toLowerCase().includes('token')) {
                token = localStorage.getItem(key);
                break;
            }
        }
        if (!token) {
            for (let key in sessionStorage) {
                if (key.toLowerCase().includes('token')) {
                    token = sessionStorage.getItem(key);
                    break;
                }
            }
        }
        return token;
        """
        token_from_storage = driver.execute_script(script)
        if token_from_storage:
            print(f"✅ Bearer token found in storage: {token_from_storage[:20]}...")
            driver.quit()
            return token_from_storage

        # 🔍 **3. Capturar o Token nos Cookies**
        print("🔍 Searching for Bearer token in cookies...")
        cookies = driver.get_cookies()
        for cookie in cookies:
            if "token" in cookie["name"].lower():  # Busca qualquer cookie que tenha "token" no nome
                token_from_cookies = cookie["value"]
                print(f"✅ Bearer token found in cookies: {token_from_cookies[:20]}...")
                driver.quit()
                return token_from_cookies

        print("⚠️ No Bearer token found in network, storage, or cookies. Ensure you are logging into the correct endpoint.")
        driver.quit()
        return None

    
    # Criação da pasta de logs
    LOG_DIR = "logs"
    os.makedirs(LOG_DIR, exist_ok=True)
    

    @staticmethod
    def setup_logger_rate():
        """Sets up the logger for rate limit testing, creating a log file with a timestamp."""
        log_filename = os.path.join(Functions.LOG_DIR, f"log_rate_limit_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    @staticmethod
    def setup_logger_idor():
        """Sets up the logger for IDOR testing, creating a log file with a timestamp."""
        log_filename = os.path.join(Functions.LOG_DIR, f"log_idor_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
    @staticmethod
    def setup_logger_xss():
        """Sets up the logger for XSS testing, creating a log file with a timestamp."""
        log_filename = os.path.join(Functions.LOG_DIR, f"log_xss_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )      
        
    @staticmethod
    def setup_logger_auth():
        """Sets up the logger for Authentication testing, creating a log file with a timestamp."""
        log_filename = os.path.join(Functions.LOG_DIR, f"log_auth_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )    
    @staticmethod
    def setup_logger_headers():
        """Sets up the logger for security header verification, creating a log file with a timestamp."""
        log_filename = os.path.join(Functions.LOG_DIR, f"log_headers_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )    
    @staticmethod
    def setup_logger_security_data_exposure():
        """Sets up the logger for security data exposure verification, creating a log file with a timestamp."""
        log_filename = os.path.join(Functions.LOG_DIR, f"log_security_data_exposure_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        
    def remove_emojis(text):
        """Removes specific emojis from the given text."""
        # List of emojis to be removed
        emojis_to_remove = [
            "\U0001F50D",  # 🔍 (Magnifying glass)
            "\u26A0\ufe0f",  # ⚠️ (Warning)
            "\u2705",  # ✅ (Green check)
            "\U0001F4CA",  # 📊 (Bar chart)
            "\U0001F522",  # 🔢 (Numbers input)
            "\U000023F0",  # ⏰ (Alarm clock)
            "\U000023F3"  # ⏳ (Hourglass)
        ]
        
        for emoji in emojis_to_remove:
            text = text.replace(emoji, "")  # Remove each emoji from the string
        
        return text
