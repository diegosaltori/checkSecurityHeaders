import requests
import sys
import jwt
from halo import Halo
from models.functions import Functions, logging

# Extensive list of common passwords for brute force testing
COMMON_PASSWORDS = [
    "password", "123456", "123456789", "qwerty", "abc123", "password1", "admin", "welcome",
    "letmein", "123123", "111111", "1234", "test", "root", "passw0rd", "superman", "654321",
    "qwerty123", "1q2w3e4r", "1qaz2wsx", "user", "admin123", "admin1", "admin1234",
    "welcome123", "p@ssw0rd", "password123", "default"
]

# Expanded list of common 2FA codes for bypass testing
COMMON_2FA_CODES = [
    "000000", "123456", "654321", "111111", "999999", "112233", "121212", "777777", "987654",
    "222222", "333333", "444444", "555555", "666666", "888888", "000111", "100100", "200200"
]

# Extended list of JWT secret keys for token manipulation testing
JWT_SECRET_KEYS = [
    "secret", "admin", "password", "jwtsecret", "mysecret", "changeme", "test", "default",
    "root", "123456", "letmein", "welcome", "qwerty", "passw0rd", "supersecret", "topsecret",
    "jwt", "auth", "securejwt", "tokensecret", "apitoken", "secure"
]



def test_authentication():
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
            spinner = Halo(text="Testing authentication vulnerabilities...", spinner="dots")
            spinner.start()

            # Brute Force Attack
            print("\n🔐 Testing Brute Force Login...")
            for password in COMMON_PASSWORDS:
                data = {"username": "admin", "password": password}
                response = session.post(f"{url}/login", data=data)
                if "invalid" not in response.text.lower():
                    print(f"⚠️ Possible weak credential: admin / {password}")
                    logging.info(f"Possible weak credential: admin / {password}")

            # 2FA Bypass
            print("\n🔐 Testing 2FA Bypass...")
            for code in COMMON_2FA_CODES:
                data = {"2fa_code": code}
                response = session.post(f"{url}/2fa", data=data)
                if "invalid" not in response.text.lower():
                    print(f"⚠️ Possible 2FA bypass with code: {code}")
                    logging.info(f"Possible 2FA bypass with code: {code}")

            # JWT Manipulation
            print("\n🔐 Testing JWT Token Manipulation...")
            token = jwt.encode({"user": "admin", "role": "user"}, "wrongsecret", algorithm="HS256")
            headers = {"Authorization": f"Bearer {token}"}
            response = session.get(f"{url}/protected", headers=headers)
            if response.status_code == 200:
                print("⚠️ Possible JWT vulnerability: Server accepted a tampered token!")
                logging.info("Possible JWT vulnerability: Server accepted a tampered token!")

            spinner.stop()

        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            logging.error(error_msg)


if __name__ == "__main__":
    Functions.setup_logger_auth()
    Functions.banner_auth()
    test_authentication()
