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
pip install selenium selenium-wire requests webdriver-manager halo keyboard
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

### Log File (`log_headers_YYYY-MM-DD-HH-MM-SS.log`)  
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

## License
This project is licensed under the MIT License.

---  
Built to assist in the security auditing of web applications! 🔒
Developed by **Diego Garcia Saltori**