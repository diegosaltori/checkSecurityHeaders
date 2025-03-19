# Security Headers Verification with Selenium and Requests  

This script allows checking whether a web application has the main **recommended security headers**, performing a manual login via **Selenium** and reusing the authenticated cookies to access the page via **Requests**.  

## 📌 Features  
- **Opens the browser with Selenium** for the user to log in manually.  
- **Retrieves session cookies** after a successful login.  
- **Uses the cookies in Requests** to access an authenticated page.  
- **Checks the main security headers** in the page response.  
- **Displays the headers found and those that are missing.**  

## 🔧 Requirements  
Before running the script, make sure you have the necessary dependencies installed:  

```bash
pip install selenium requests
```  

You also need to have **ChromeDriver** installed and available in your system’s PATH. If you need to download it, visit:  
- [ChromeDriver Download](https://sites.google.com/chromium.org/driver/)  

## 🚀 How to Use  
1. **Edit the script** and replace `url` with the application URL where you want to log in.  
2. **Run the script:**  
   ```bash
   python secHeaders.py
   ```  
3. **The browser will open automatically.**  
4. **Log in manually. (If login is not required, proceed to the next step.)**  
5. **Return to the terminal and press ENTER** once authenticated.  
6. The script will close the browser, reuse the cookies, and check for security headers.  

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

## 🛠 Possible Improvements  
- Add logs or export results to a file.  
- Support for other browsers (Firefox, Edge).  
- Option to test multiple URLs automatically.  

---  
Built to assist in the security auditing of web applications! 🔒  
