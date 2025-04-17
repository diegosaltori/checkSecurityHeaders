import textwrap
import requests
import sys
from halo import Halo
from models.functions import Functions, logging
from models.clean_pycache import clean_pycache

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
            response = session.get(url, allow_redirects=True)
            spinner.stop()
            
            security_headers = [                
                "X-XSS-Protection",
                "X-Frame-Options",
                "X-Content-Type-Options",
                "Strict-Transport-Security",
                "Content-Security-Policy",
                "Referrer-Policy",
                "Permissions-Policy",
                "Cross-Origin-Embedder-Policy",
                "Cross-Origin-Resource-Policy",
                "Cross-Origin-Opener-Policy"
            ]

            urls_checked = response.history + [response]

            for i, resp in enumerate(urls_checked):
                log_output = f"\n🔍 Checking security headers for: {resp.url} (Redirect {i})\n"
                print(log_output)
                logging.info(Functions.remove_emojis(log_output))

                headers = resp.headers
                for header in security_headers:
                    if header in headers:
                        wrapped_value = textwrap.fill(headers[header], width=80)
                        result = f"✅ {header}:\n{wrapped_value}\n{'-'*40}"
                    else:
                        result = f"⚠️ {header} not found!\n{'-'*40}"
                    print(result)
                    logging.info(Functions.remove_emojis(result))

            print(f"\n🌐 Effective URL: {response.url}")
            logging.info(f"Effective URL: {response.url}")
            clean_pycache()

        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            logging.error(error_msg)


if __name__ == "__main__":
    Functions.setup_logger_headers()
    Functions.banner_header()
    check_security_headers()
