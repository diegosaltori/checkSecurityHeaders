from selenium import webdriver
import textwrap
import requests

# Configure WebDriver (using Chrome)
driver = webdriver.Chrome()  # Make sure chromedriver is in the PATH

# Application URL
url = "https://example.com"

try:
    # Open the browser for the user to log in manually
    driver.get(url)

    print("🔹 Log in manually and press ENTER in the terminal when you are ready.")
    input("Press ENTER to continue after logging in...")

    # Retrieve cookies from Selenium to pass to requests
    cookies = driver.get_cookies()

    # Close the browser after capturing the cookies
    driver.quit()

    # Create a session with Selenium cookies
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Access the authenticated page and get the headers
    response = session.get("https://example.com")  # Replace with the post-login URL
    headers = response.headers

    # List of recommended security headers
    security_headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-XSS-Protection",
        "X-Content-Type-Options",
        "Referrer-Policy",
        "Permissions-Policy"
    ]

    print(f"\n🔍 Checking security headers for: {response.url}\n")

    for header in security_headers:
        if header in headers:
            # Automatically wrap long values
            wrapped_value = textwrap.fill(headers[header], width=80)
            print(f"✅ {header}:\n{wrapped_value}\n{'-'*40}")
        else:
            print(f"⚠️ {header} not found!\n{'-'*40}")

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()  # Ensure the browser closes in case of an error
