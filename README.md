<h1 align="center">Checking Security</h1>

# 🔄 Check Security Headers

This script allows checking whether a web application has the main **recommended security headers**, performing a manual login via **Selenium** and reusing the authenticated cookies to access the page via **Requests**.  

## 📌 Features  
- **Opens the browser with Selenium** for the user to log in manually.  
- **Retrieves session cookies** after a successful login.  
- **Uses the cookies in Requests** to access an authenticated page.  
- **Checks the main security headers** in the page response.  
- **Displays the headers found and those that are missing.**  
- **Spinner indicators** for better user experience during processing.  
- **Option to rerun the test (`yes`) or exit (`no`)** after completion.  
- **User inputs the URL**, which is automatically formatted to ensure it starts with `https://`.  

## 🔧 Requirements  
Before running the script, make sure you have the necessary dependencies installed:  

```bash
pip install selenium requests webdriver-manager halo keyboard
```  

> The script uses `webdriver-manager` to automatically handle the installation of **ChromeDriver**, **GeckoDriver**, and **EdgeDriver**. This means you don’t need to install them manually. However, if you already have them installed, the script will still work without issues.

Aqui está a versão atualizada do seu README com a informação sobre a escolha do navegador:  

## 🚀 How to Use  
1. **Run the script:**  
   ```bash
   python check_headers.py
   ```  
2. **Enter the URL of the web application** when prompted. The script will automatically add `https://` if missing.  
3. **Choose a browser:** You will be prompted to select **Chrome**, **Firefox**, or **Edge**.  
4. **The selected browser will open automatically.**  
5. **Log in manually. (If login is not required, proceed to the next step.)**  
6. **Return to the terminal and press ENTER** once authenticated.  
7. The script will close the browser, reuse the cookies, and check for security headers.  
8. After completion, you will be asked:  
   - Enter `yes` to run the test again.  
   - Enter `no` to exit the script.  



## 🔍 Security Headers Checked  
The script verifies the presence of the following security headers:  

- `Strict-Transport-Security`  
- `Content-Security-Policy`  
- `X-Frame-Options`  
- `X-XSS-Protection`  
- `X-Content-Type-Options`  
- `Referrer-Policy`  
- `Permissions-Policy`  

For each header:  
✅ If found, the value will be displayed in a formatted way.  
⚠️ If missing, a warning message will be shown.  

## 📝 Example Output  
### Terminal Output  
```plaintext
🔍 Checking security headers for: https://example.com

✅ Strict-Transport-Security:
max-age=31536000; includeSubDomains
----------------------------------------
✅ Content-Security-Policy:
default-src 'self'; script-src 'self' https://trusted.com
----------------------------------------
⚠️ X-Frame-Options not found!
----------------------------------------
⚠️ X-XSS-Protection not found!
----------------------------------------
```  

### Log File (`log_headers_YYYY-MM-DD-HH-MM-SS.txt`)  
```plaintext
2025-03-19 12:00:00 - INFO - Checking security headers for: https://example.com
2025-03-19 12:00:01 - INFO - Strict-Transport-Security:
max-age=31536000; includeSubDomains
----------------------------------------
2025-03-19 12:00:01 - INFO - Content-Security-Policy:
default-src 'self'; script-src 'self' https://trusted.com
----------------------------------------
2025-03-19 12:00:01 - WARNING - X-Frame-Options not found!
----------------------------------------
2025-03-19 12:00:01 - WARNING - X-XSS-Protection not found!
----------------------------------------
```  

---  
Built to assist in the security auditing of web applications! 🔒  

---

# 🔄 Check Rate Limit

This script allows testing the **rate limits** of a web API or website by sending multiple requests and monitoring the response headers. It supports **manual login via Selenium**, retrieving authenticated session cookies, and reusing them in **Requests** for testing.  

## 📌 Features  
- **Opens the browser with Selenium** for manual login if required.  
- **Retrieves session cookies** after a successful login.  
- **Uses the cookies in Requests** to send multiple authenticated requests.  
- **Checks rate limit headers** like `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset`.  
- **Handles rate limit restrictions** by detecting `Retry-After` headers.  
- **Spinner indicators** for better user experience during processing.  
- **Allows re-running the test (`yes`) or exiting (`no`)** after completion.  
- **User inputs the URL and number of requests**, ensuring valid values.  

## 🔧 Requirements  
Before running the script, install the necessary dependencies:  

```bash
pip install selenium requests webdriver-manager halo keyboard
```  

> The script automatically installs **ChromeDriver**, **GeckoDriver**, and **EdgeDriver** using `webdriver-manager`. If you already have them installed, it will still work.  

## 🚀 How to Use  
1. **Run the script:**  
   ```bash
   python check_rate_limit.py
   ```  
2. **Enter the website URL** when prompted. The script will automatically add `https://` if missing.  
3. **Enter the number of requests** to be sent.  
4. **Choose a browser:** Chrome, Firefox, or Edge.  
5. **The selected browser will open automatically.**  
6. **Log in manually (if required).**  
7. **Return to the terminal and press ENTER** once authenticated.  
8. The script will close the browser, reuse the cookies, and start testing the rate limits.  
9. After completion, you will be asked:  
   - Enter `yes` to run the test again.  
   - Enter `no` to exit the script.  

## 📊 Rate Limit Headers Checked  
The script retrieves and displays the following headers from the server responses:  

- `X-RateLimit-Limit` → Maximum number of requests allowed.  
- `X-RateLimit-Remaining` → Number of remaining requests before hitting the limit.  
- `X-RateLimit-Reset` → Time when the rate limit resets (in UNIX timestamp).  
- `Retry-After` → Indicates how long to wait before making another request.  

If rate limits are exceeded, the script will stop and notify the user.  

## 📝 Example Output  
### Terminal Output  
```plaintext
🔄 Testing rate limits for: https://api.github.com | Requests: 5

✅ Request 1: Status Code: 200
   ➜ X-RateLimit-Limit: 5000
   ➜ X-RateLimit-Remaining: 4999
----------------------------------------
✅ Request 2: Status Code: 200
   ➜ X-RateLimit-Limit: 5000
   ➜ X-RateLimit-Remaining: 4998
----------------------------------------
⚠️ Rate limit exceeded! Retry after 30 seconds.
```  

### Log File (`log_rate_limit_YYYY-MM-DD-HH-MM-SS.txt`)  
```plaintext
2025-03-19 12:30:00 - INFO - Testing rate limits for: https://api.github.com | Requests: 5
2025-03-19 12:30:01 - INFO - Request 1: Status Code: 200
2025-03-19 12:30:01 - INFO - X-RateLimit-Limit: 5000
2025-03-19 12:30:01 - INFO - X-RateLimit-Remaining: 4999
----------------------------------------
2025-03-19 12:30:02 - INFO - Request 2: Status Code: 200
2025-03-19 12:30:02 - INFO - X-RateLimit-Remaining: 4998
----------------------------------------
2025-03-19 12:30:05 - WARNING - Rate limit exceeded! Retry after 30 seconds.
----------------------------------------
```  

---  
Built to analyze and test the rate limits of web APIs efficiently! 🔄  

---  
# 🔄 Check IDOR Vulnerabilities

This script tests for **Insecure Direct Object References (IDOR)** vulnerabilities by attempting to access various endpoints using different user IDs and common values. The script uses session cookies to authenticate requests and logs potential vulnerabilities found.

## 📌 Features  
- **Performs authentication using session cookies.**  
- **Tests a list of common ID values** to check for IDOR issues.  
- **Checks multiple sensitive endpoints** such as `/user/`, `/account/`, `/admin/`, `/dashboard/`, etc.  
- **Logs any potential IDOR vulnerabilities detected.**  
- **Provides an option to rerun the test (`yes`) or exit (`no`).**  
- **Displays real-time processing with a loading spinner.**  

## 🔧 Requirements  
Before running the script, install the necessary dependencies:  

```bash
pip install selenium requests webdriver-manager halo keyboard
```

## 🚀 How to Use  
1. **Run the script:**  
   ```bash
   python check_idor.py
   ```  
2. **The script will prompt for a URL** where the test will be performed.  
3. **Performs login automatically** and retrieves session cookies.  
4. **Iterates through different ID values** (e.g., `1`, `2`, `9999`, `-1`, `admin`, etc.).  
5. **Tests multiple endpoints** (`/user/`, `/account/`, `/admin/`, etc.).  
6. **Logs any endpoints that return HTTP 200**, indicating a potential IDOR vulnerability.  
7. After completion, you will be asked:  
   - Enter `yes` to run the test again.  
   - Enter `no` to exit the script.  

## 📝 Example Output  
### Terminal Output  
```plaintext
🔍 Testing IDOR vulnerabilities on: https://example.com

⚠️ Potential IDOR detected at: https://example.com/user/9999 (Status: 200)
✅ No IDOR at: https://example.com/admin/guest (Status: 403)
----------------------------------------
```  

### Log File (`log_idor_YYYY-MM-DD-HH-MM-SS.txt`)  
```plaintext
2025-03-19 12:30:00 - INFO - Testing IDOR vulnerabilities on: https://example.com
2025-03-19 12:30:01 - WARNING - Potential IDOR detected at: https://example.com/user/9999 (Status: 200)
2025-03-19 12:30:02 - INFO - No IDOR at: https://example.com/admin/guest (Status: 403)
----------------------------------------
```  

---  
Built to help identify IDOR vulnerabilities in web applications! 🔍  

Developed by **Diego Garcia Saltori**