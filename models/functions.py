import sys
import os
from datetime import datetime
from halo import Halo
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Function to choose a browser for login
def choose_browser():
    """Allows the user to choose a browser for login."""
    print("Choose a browser: (1) Chrome | (2) Firefox | (3) Edge")
    choice = input("Enter 1, 2, or 3: ").strip()
    
    if choice == "2":
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service)
    elif choice == "3":
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service)
    else:
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service)

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
    def setup_logger_headers():
        """Sets up the logger for security header verification, creating a log file with a timestamp."""
        log_filename = os.path.join(Functions.LOG_DIR, f"log_headers_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
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
