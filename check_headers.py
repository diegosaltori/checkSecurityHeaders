import textwrap
import requests
import sys
from halo import Halo
from models.functions import Functions, logging

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
        url = Functions.get_url()
        
        try:
            session = requests.Session()
            cookies = Functions.perform_login(url)
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])

            spinner = Halo(text='Fetching security headers...', spinner='dots')
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
            logging.info(Functions.remove_emojis(log_output))

            for header in security_headers:
                if header in headers:
                    wrapped_value = textwrap.fill(headers[header], width=80)
                    result = f"✅ {header}:\n{wrapped_value}\n{'-'*40}"
                else:
                    result = f"⚠️ {header} not found!\n{'-'*40}"
                print(result)
                logging.info(Functions.remove_emojis(result))

        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            logging.error(error_msg)


if __name__ == "__main__":
    Functions.setup_logger_headers()
    Functions.banner_header()
    check_security_headers()
