import requests
import sys
from halo import Halo
from models.functions import Functions, logging

def test_idor():
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
            # Create a session to maintain cookies and authentication
            session = requests.Session()
            cookies = Functions.perform_login(url)
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])
            
            spinner = Halo(text='Testing IDOR vulnerabilities...', spinner='dots')
            spinner.start()
            
            # List of common ID values to test for IDOR vulnerabilities
            idor_tests = ["1", "2", "9999", "-1", "admin", "test", "123", "guest", "root"]
            
            # List of common endpoints that might be vulnerable to IDOR
            idor_endpoints = [
                "/profile/", "/user/", "/account/", "/admin/", "/dashboard/", "/settings/",
                "/order/", "/purchase/", "/transaction/", "/cart/", "/invoice/", "/report/",
                "/edit/", "/delete/", "/update/", "/view/", "/info/", "/details/"
            ]
            
            # Iterate over all endpoints and test IDs
            for endpoint in idor_endpoints:
                for test_id in idor_tests:
                    test_url = f"{url}{endpoint}{test_id}"
                    response = session.get(test_url, allow_redirects=False)
                    
                    # Check response status to identify potential IDOR issues
                    if response.status_code == 200:
                        result = f"⚠️ Potential IDOR detected at: {test_url} (Status: {response.status_code})"
                    else:
                        result = f"✅ No IDOR at: {test_url} (Status: {response.status_code})"
                    
                    print(result)
                    logging.info(Functions.remove_emojis(result))
            
            spinner.stop()
            
        except Exception as e:
            # Handle errors gracefully and log them
            error_msg = f"Error: {e}"
            print(error_msg)
            logging.error(error_msg)

if __name__ == "__main__":
    # Setup logger and display banner before starting the test
    Functions.setup_logger_idor()
    Functions.banner_idor()
    test_idor()
