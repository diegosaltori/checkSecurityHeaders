import textwrap
import requests
import logging
import sys
import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from halo import Halo

def setup_logger():
    logging.basicConfig(
        filename="security_headers_log.txt",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def remove_emojis(text):
    # Lista de emojis a serem removidos
    emojis_to_remove = [
        "\U0001f50d",  # 🔍 (lupa)
        "\u26a0\ufe0f",  # ⚠️ (alerta)
        "\u2705"  # ✅ (check verde)
    ]
    
    for emoji in emojis_to_remove:
        text = text.replace(emoji, "")  # Remove cada emoji da string
    
    return text

def print_banner():
    print("""
    ======================================
       Security Headers Checked V2.0.1.1
       Developed by Diego Garcia Saltori
    ======================================
    """)

def choose_browser():
    print("Choose a browser: (1) Chrome | (2) Firefox | (3) Edge")
    choice = input("Enter 1, 2, or 3: ").strip()
    
    print()  # Adiciona uma linha para evitar que os logs fiquem grudados na entrada do usuário
    
    if choice == "2":
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service)
    elif choice == "3":
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service)
    else:
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service)


def get_url():
    print("Enter the website URL (without https:// is fine) or press ESC to exit:")

    url = ""
    while True:
        key_event = keyboard.read_event()

        if key_event.event_type == keyboard.KEY_DOWN:
            if key_event.name == "esc":
                print("\nExiting...")
                sys.exit()  # Encerra o script imediatamente
            elif key_event.name == "enter":
                print()  # Adiciona uma nova linha antes de continuar
                break
            elif len(key_event.name) == 1:  # Evita capturar teclas como Shift, Ctrl, etc.
                url += key_event.name
                print("\r" + " " * len(url), end="\r", flush=True)  # Limpa a linha antes de reimprimir
                print(url, end="", flush=True)

    url = url.strip()

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
            
            print("🔹 If login is required, complete it manually and press ENTER in the terminal when done.")

            input("Press ENTER to continue once you have completed the login (if required)...")
           
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
            logging.info(remove_emojis(log_output))

            for header in security_headers:
                if header in headers:
                    wrapped_value = textwrap.fill(headers[header], width=80)
                    result = f"✅ {header}:\n{wrapped_value}\n{'-'*40}"
                else:
                    result = f"⚠️ {header} not found!\n{'-'*40}"
                print(result)
                logging.info(remove_emojis(result))

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
