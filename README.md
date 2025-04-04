<h1 align="center">Checking Security</h1>

## 🔧 Requirements  
Before running the scripts, it is recommended to create and activate a virtual environment:

```bash
python -m venv venv
source venv/scripts/activate  # On macOS and Linux
venv\Scripts\activate    # On Windows
```

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
Install the necessary dependencies:

```bash
pip install selenium requests webdriver-manager halo keyboard
```

> The script uses `webdriver-manager` to automatically handle the installation of **ChromeDriver**, **GeckoDriver**, and **EdgeDriver**. This means you don’t need to install them manually. However, if you already have them installed, the script will still work without issues.

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

---
# 🔄 XSS Security Testing

## Overview
The `check XSS` script is designed to automate the testing for Cross-Site Scripting (XSS) vulnerabilities in web applications. It sends various payloads to predefined endpoints and analyzes responses to detect potential security risks.

## How It Works
1. The script retrieves the target URL.
2. It performs an authentication process and sets session cookies.
3. It iterates through a list of known XSS payloads.
4. For each payload, it sends requests to multiple endpoints.
5. It checks whether the payload is reflected in the response.
6. Results are logged and displayed, indicating whether a potential XSS vulnerability was found.

## 🔧 Requirements  
Before running the script, install the necessary dependencies:  

```bash
pip install selenium requests webdriver-manager halo keyboard
```
## Usage
```sh
python check_xss.py
```
Follow the on-screen prompts to input the target URL.

## XSS Payloads Tested
The script includes a comprehensive list of common XSS payloads, including:
- Script injection (`<script>alert('XSS')</script>`)
- Event-based attacks (`<img src=x onerror=alert('XSS')>`)
- URI scheme attacks (`javascript:alert('XSS')`)
- Input field exploits (`<input type=text value='' onfocus=alert('XSS')>`)
- HTML attribute manipulation (`"><script>alert('XSS')</script>`)
- Other advanced techniques (`<math><mtext><style onload=alert('XSS')></style></mtext></math>`)

## Logging and Output
Results are displayed in the terminal with:
- `⚠️ Potential XSS detected` if the payload is reflected
- `✅ No XSS` if no vulnerability is found
All results are logged to a file for further analysis.

## Customization
- Modify the `XSS_PAYLOADS` list in `check_xss.py` to add/remove test cases.
- Change `endpoints` to test specific parts of your application.
- Adjust the logging settings in `Functions.setup_logger_xss()`.

## Disclaimer
This tool is intended for security professionals and ethical hackers to test their own applications. Unauthorized use against third-party systems is strictly prohibited.

## License
MIT License

---

# Security Headers & API Exposure Scanner

This script is designed to analyze and intercept API requests in a web application using Selenium Wire. It detects potential security vulnerabilities, including exposed API keys, sensitive user information, and insecure response headers.

## Features
- Intercepts API requests while navigating the web application.
- Detects exposed API keys, JWT tokens, email addresses, CPF, CNPJ, credit card numbers, and stack traces.
- Checks response headers for potential security risks.
- Allows deep navigation before finalizing the test.

## Requirements
- Python 3.x
- Google Chrome
- ChromeDriver (managed automatically by `webdriver_manager`)

### Dependencies
Install the required dependencies using pip:
```bash
pip install selenium selenium-wire webdriver-manager
```

## Usage
1. Run the script:
   ```bash
   python security.py
   ```
2. Enter the target URL when prompted.
3. Navigate through the application and interact with it.
4. When ready, press `ENTER` to analyze API requests.
5. Review detected vulnerabilities in the terminal.
6. Press `ENTER` to finalize and close the browser.
7. Choose whether to run the test again.

## Sensitive Data Patterns Detected
- **API Keys**
- **Emails**
- **JWT Tokens**
- **CPF (Brazilian Tax ID)**
- **CNPJ (Brazilian Company ID)**
- **Credit Card Numbers**
- **Stack Traces**

## Security Headers Checked
- `Server`
- `X-Powered-By`
- `Access-Control-Allow-Origin`

## Example Output
```
🔹 Complete the login and navigate through the application.
🔹 When finished, press ENTER to analyze requests...

🌐 Intercepted: https://example.com/api/user
⚠️ Possible exposure of Emails found:
  - user@example.com
----------------------------------------
✅ No JWT Tokens detected.

⚠️ Header 'Server' found: Apache -> May expose server details.
```

## Notes
- Ensure Chrome is installed on your machine.
- The script should be run in an environment with network access to the target application.

## License
This project is licensed under the MIT License.


Developed by **Diego Garcia Saltori**