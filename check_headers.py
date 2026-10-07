import textwrap
import requests
import sys
from halo import Halo
from models.functions import Functions, logging
from models.clean_pycache import clean_pycache

def analyze_csp(csp):
    """Return practical warnings for common CSP omissions and weak values."""
    directives = {}
    for part in csp.split(';'):
        tokens = part.strip().split()
        if tokens:
            directives[tokens[0].lower()] = tokens[1:]

    warnings = []
    if not directives:
        return ["CSP header is empty or could not be parsed."]

    if "default-src" not in directives:
        warnings.append("default-src is missing; add a restrictive fallback policy.")
    if "object-src" not in directives:
        warnings.append("object-src is missing; consider object-src 'none'.")
    if "frame-ancestors" not in directives:
        warnings.append("frame-ancestors is missing; consider restricting who can embed this site.")

    for name, values in directives.items():
        if "*" in values:
            warnings.append(f"{name} allows '*'.")
        if "'unsafe-inline'" in values:
            warnings.append(f"{name} allows 'unsafe-inline'.")
        if "'unsafe-eval'" in values:
            warnings.append(f"{name} allows 'unsafe-eval'.")

    return warnings

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

                csp = headers.get("Content-Security-Policy")
                if csp:
                    warnings = analyze_csp(csp)
                    if warnings:
                        report = "⚠️ CSP review (review manually):\n" + "\n".join(f"- {warning}" for warning in warnings)
                    else:
                        report = "✅ CSP review: no common issues detected."
                    print(report)
                    logging.info(Functions.remove_emojis(report))
                elif headers.get("Content-Security-Policy-Report-Only"):
                    report = "⚠️ CSP is present only in report-only mode; violations are reported but not blocked."
                    print(report)
                    logging.warning(Functions.remove_emojis(report))

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
