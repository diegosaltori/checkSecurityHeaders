import requests
import time
import threading
import logging
import os
from datetime import datetime

def setup_logger(script_name):
    """Sets up a logger that writes to a file in the 'logs' directory
    with a timestamped filename, using UTF-8 encoding.
    """
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_filename = os.path.join(log_dir, f"{script_name}_{timestamp}.log")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # Specifies UTF-8 encoding when creating the FileHandler
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def test_endpoint(logger, url, token, num_requests, delay):
    """
    Sends multiple requests to the specified API endpoint with a delay and checks rate limit headers.
    Logs the results using the provided logger.

    Args:
        logger (logging.Logger): The logger object.
        url (str): The API endpoint URL.
        token (str): The Bearer token for authentication.
        num_requests (int): The number of requests to send.
        delay (float): The delay in seconds between each request.
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }

    logger.info(f"--- Starting Sequential Test for {url} ---")
    success_count = 0
    error_count = 0

    for i in range(num_requests):
        try:
            start_time = time.time()
            response = requests.get(url, headers=headers)
            end_time = time.time()
            duration = end_time - start_time

            log_message = f"Request {i+1}: Status Code: {response.status_code}, Duration: {duration:.4f} seconds"
            print(log_message)
            logger.info(log_message)

            if 200 <= response.status_code < 300:
                limit = response.headers.get('X-RateLimit-Limit')
                remaining = response.headers.get('X-RateLimit-Remaining')
                reset = response.headers.get('X-RateLimit-Reset')  # Optional: Time until reset

                if limit and remaining:
                    limit_info = f"  ➜ X-RateLimit-Limit: {limit}"
                    remaining_info = f"  ➜ X-RateLimit-Remaining: {remaining}"
                    print(limit_info)
                    logger.info(limit_info)
                    print(remaining_info)
                    logger.info(remaining_info)
                    if int(remaining) <= 0:
                        rate_limit_exceeded = "⚠️ Rate limit possibly exceeded!"
                        print(rate_limit_exceeded)
                        logger.warning(rate_limit_exceeded)
                        if reset:
                            retry_info = f"  ➜ Retry after {reset} seconds (approximate)."
                            print(retry_info)
                            logger.warning(retry_info)
                        else:
                            retry_info = "  ➜ Check API documentation for retry information."
                            print(retry_info)
                            logger.warning(retry_info)
                else:
                    header_not_found = "  ➜ Rate limit headers not found in the response."
                    print(header_not_found)
                    logger.info(header_not_found)
                success_count += 1
            else:
                error_message = f"Request {i+1} failed: {response.text}"
                print(error_message)
                logger.error(error_message)
                error_count += 1

            print("-" * 40)
            logger.info("-" * 40)

        except requests.exceptions.RequestException as e:
            error_message = f"Request {i+1} error: {e}"
            print(error_message)
            logger.error(error_message)
            print("-" * 40)
            logger.info("-" * 40)
            error_count += 1

        time.sleep(delay)

    logger.info(f"--- Sequential Test Results for {url} ---")
    logger.info(f"Total Requests: {num_requests}")
    logger.info(f"Successful Requests: {success_count}")
    logger.info(f"Failed Requests: {error_count}")
    print("\n--- Test Results ---")
    print(f"Total Requests: {num_requests}")
    print(f"Successful Requests: {success_count}")
    print(f"Failed Requests: {error_count}")

def test_endpoint_concurrent(logger, url, token, num_requests, num_threads, delay_between_threads):
    """
    Sends multiple concurrent requests to the specified API endpoint and checks rate limit headers.
    Logs the results using the provided logger.

    Args:
        logger (logging.Logger): The logger object.
        url (str): The API endpoint URL.
        token (str): The Bearer token for authentication.
        num_requests (int): The total number of requests to send.
        num_threads (int): The number of concurrent threads to use.
        delay_between_threads (float): Delay in seconds before starting the next thread batch.
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }
    requests_per_thread = num_requests // num_threads
    remaining_requests = num_requests % num_threads
    threads = []
    results = []
    logger.info(f"--- Starting Concurrent Test for {url} with {num_threads} threads ---")

    def send_requests(thread_id, requests_to_send):
        thread_results = []
        for i in range(requests_to_send):
            try:
                start_time = time.time()
                response = requests.get(url, headers=headers)
                end_time = time.time()
                duration = end_time - start_time

                log_message = f"Thread {thread_id}, Request {i+1}: Status Code: {response.status_code}, Duration: {duration:.4f} seconds"
                thread_results.append(log_message)

                if 200 <= response.status_code < 300:
                    limit = response.headers.get('X-RateLimit-Limit')
                    remaining = response.headers.get('X-RateLimit-Remaining')
                    reset = response.headers.get('X-RateLimit-Reset')

                    if limit and remaining:
                        thread_results.append(f"  ➜ X-RateLimit-Limit: {limit}")
                        thread_results.append(f"  ➜ X-RateLimit-Remaining: {remaining}")
                        if int(remaining) <= 0:
                            thread_results.append("⚠️ Rate limit possibly exceeded!")
                            if reset:
                                thread_results.append(f"  ➜ Retry after {reset} seconds (approximate).")
                            else:
                                thread_results.append("  ➜ Check API documentation for retry information.")
                    else:
                        thread_results.append("  ➜ Rate limit headers not found in the response.")
                else:
                    thread_results.append(f"Thread {thread_id}, Request {i+1} failed: {response.text}")
            except requests.exceptions.RequestException as e:
                thread_results.append(f"Thread {thread_id}, Request {i+1} error: {e}")
            thread_results.append("-" * 40)
            # No delay between requests within a thread for this concurrent test
        results.extend(thread_results)

    for i in range(num_threads):
        requests_for_this_thread = requests_per_thread + (1 if i < remaining_requests else 0)
        thread = threading.Thread(target=send_requests, args=(i + 1, requests_for_this_thread))
        threads.append(thread)
        thread.start()
        time.sleep(delay_between_threads) # Introduce delay between starting threads

    for thread in threads:
        thread.join()

    logger.info(f"--- Concurrent Test Results for {url} ---")
    for result in results:
        print(result)
        logger.info(result)

if __name__ == "__main__":
    script_name = os.path.basename(__file__).split('.')[0]  # Get script name without extension
    logger = setup_logger(script_name)

    api_url = "API_URL"
    bearer_token = "YOUR_BEARER_TOKEN" # Replace with your actual token

    # --- Sequential Test ---
    print("--- Starting Sequential Test ---")
    logger.info("--- Starting Sequential Test ---")
    num_sequential_requests = 10
    delay_between_requests = 0.5  # Time in seconds between requests
    test_endpoint(logger, api_url, bearer_token, num_sequential_requests, delay_between_requests)

    print("\n" * 2)
    logger.info("\n" * 2)

    # --- Concurrent Test ---
    print("--- Starting Concurrent Test ---")
    logger.info("--- Starting Concurrent Test ---")
    total_concurrent_requests = 20
    num_concurrent_threads = 5
    delay_between_thread_start = 0.2 # Time in seconds between the start of each thread
    test_endpoint_concurrent(logger, api_url, bearer_token, total_concurrent_requests, num_concurrent_threads, delay_between_thread_start)
    