import re
import sys
import json
import logging
from seleniumwire import webdriver  # Selenium Wire para interceptar requisições
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from models.functions import Functions

def check_api_exposure():
    """Abre o navegador e intercepta requisições de API para verificar exposição de dados."""
    while True:
        url = Functions.get_url()
        
        try:
            driver = setup_browser()
            driver.get(url)
            
            print("🔹 Complete o login e navegue pela aplicação.")
            input("🔹 Quando terminar, pressione ENTER para analisar as requisições...")

            print("\n🔍 Interceptando requisições de API...")
            intercept_api_requests(driver)
        
        except Exception as e:
            logging.error(f"Erro: {e}")
        
        finally:
            driver.quit()

        user_input = input("Deseja rodar o teste novamente? (yes/no): ").strip().lower()
        if user_input != "yes":
            print("Saindo...")
            sys.exit()

def setup_browser():
    """Configura e retorna um navegador com Selenium Wire para interceptação de APIs."""
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)  # Selenium Wire

def intercept_api_requests(driver):
    """Intercepta requisições de API feitas pelo navegador e verifica se há dados sensíveis."""
    patterns = {
        "API Keys": r"(?i)(api_key|apikey|auth_token|access_token|secret|password)[=:\"'](\S+)",
        "Emails": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "JWT Tokens": r"eyJ[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+",
        "CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
        "CNPJ": r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b",
        "Cartão de Crédito": r"\b(\d{4}[- ]?){3}\d{4}\b",
        "Stack Traces": r"(Exception|Error|Traceback).*?\n",
    }
    
    if not driver.requests:
        print("⚠️ Nenhuma requisição interceptada. Verifique se há tráfego na aplicação.")

    for request in driver.requests:
        if request.response:
            try:
                content_type = request.response.headers.get('Content-Type', '')
                
                # Verifica se a resposta é JSON
                if "json" in content_type:
                    response_body = request.response.body.decode('utf-8', errors='ignore')
                    print(f"\n🌐 Interceptado: {request.url}")
                    analyze_api_response(response_body, patterns)
                
                # Verifica se há headers sensíveis
                analyze_headers(request.response.headers)
            except Exception as e:
                print(f"⚠️ Erro ao processar resposta de {request.url}: {e}")

    input("\n🛑 Pressione ENTER para encerrar o teste e fechar o navegador.")

def analyze_api_response(response, patterns):
    """Verifica se há dados sensíveis na resposta das APIs."""
    try:
        data = json.loads(response)  # Tenta carregar como JSON estruturado
        response_str = json.dumps(data, indent=2)  # Converte para string formatada
    except json.JSONDecodeError:
        response_str = response  # Se não for JSON, mantém como string
    
    for name, pattern in patterns.items():
        matches = re.findall(pattern, response_str)
        if matches:
            print(f"⚠️ Possível exposição de {name} encontrada:")
            for match in matches:
                print(f"  - {match}")
            print('-' * 40)
        else:
            print(f"✅ Nenhuma exposição de {name} detectada.")

def analyze_headers(headers):
    """Verifica headers de resposta para possíveis falhas de segurança."""
    risky_headers = {
        "Server": "Pode expor detalhes do servidor.",
        "X-Powered-By": "Pode revelar tecnologia usada.",
        "Access-Control-Allow-Origin": "CORS aberto pode permitir vazamento de dados.",
    }
    
    for header, warning in risky_headers.items():
        if header in headers:
            print(f"⚠️ Cabeçalho '{header}' encontrado: {headers[header]} -> {warning}")
    
if __name__ == "__main__":
    Functions.setup_logger_security_data_exposure()
    Functions.banner_securitydata()
    check_api_exposure()
