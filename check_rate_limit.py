import time
import sys
import requests
from halo import Halo
from models.functions import Functions, logging

# Function to test the rate limit of the given URL
def check_rate_limit(url, max_requests, delay=1):
    """Tests the rate limit by sending multiple requests to the given URL."""
    session = requests.Session()
    
    cookies = Functions.perform_login(url)
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    
    print(f"\n🚀 Starting rate limit test for: {url} | Requests: {max_requests}\n")
    logging.info(f"Testing rate limit for: {url} | Requests: {max_requests}")
    
    for i in range(1, max_requests + 1):
        spinner = Halo(text=f"Sending request {i}...", spinner="dots")
        spinner.start()

        response = session.get(url)
        headers = response.headers
        spinner.stop()

        status_icon = "✅" if response.status_code == 200 else "⚠️"
        print(f"{status_icon} Request {i}: Status Code: {response.status_code}")
        logging.info(f"Request {i}: Status Code: {response.status_code}")
        
        if "X-RateLimit-Limit" in headers:
            print(f"   📊 X-RateLimit-Limit: {headers['X-RateLimit-Limit']}")
            logging.info(f"  X-RateLimit-Limit: {headers['X-RateLimit-Limit']}")
        
        if "X-RateLimit-Remaining" in headers:
            print(f"   🔢 X-RateLimit-Remaining: {headers['X-RateLimit-Remaining']}")
            logging.info(f"  X-RateLimit-Remaining: {headers['X-RateLimit-Remaining']}")
        
        if "X-RateLimit-Reset" in headers:
            print(f"   ⏰ X-RateLimit-Reset: {headers['X-RateLimit-Reset']}")
            logging.info(f"  X-RateLimit-Reset: {headers['X-RateLimit-Reset']}")
        
        if "Retry-After" in headers:
            print(f"   ⏳ Rate limit exceeded! Retry after {headers['Retry-After']} seconds.")
            logging.warning(f"Rate limit exceeded! Retry after {headers['Retry-After']} seconds.")
            break
        
        time.sleep(delay)

# Main execution loop
if __name__ == "__main__":
    Functions.setup_logger_rate()
    Functions.banner_rate()
    first_run = True

    while True:
        if not first_run:            
            user_input = input("\nDo you want to run the test again? (yes/no): ").strip().lower()            
            if user_input == "no":
                print("Exiting...")
                sys.exit()
            elif user_input != "yes":
                continue
        
        first_run = False
        url = Functions.get_url()
        max_requests = Functions.get_max_requests()
        check_rate_limit(url, max_requests)
