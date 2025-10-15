import os
import requests
from auth_factory import get_authenticator
from dotenv import load_dotenv
load_dotenv() # Carrega variáveis do arquivo .env para o ambiente

def test_api_call(api_url: str, headers: dict):
    """Helper function to test an API call with the provided auth headers."""
    print(f"   -> Making a test call to: {api_url}")
    try:
        response = requests.get(api_url, headers=headers, timeout=5)
        response.raise_for_status()
        print(f"   -> API call successful! Status: {response.status_code}")
        # print("   -> API Response:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"   -> API call failed: {e}")

if __name__ == "__main__":
    print("--- Client demonstrating the Authenticator Factory ---")

    # --- Test Case 1: Keycloak ---
    # The authenticator will print detailed errors if it fails to get a token.
    print("\n[1] Attempting Keycloak Authentication...")
    try:
        # Carrega a configuração do Keycloak a partir de variáveis de ambiente
        keycloak_config = {
            "server_url": os.getenv("KEYCLOAK_SERVER_URL"),
            "realm": os.getenv("KEYCLOAK_REALM"),
            "client_id": os.getenv("KEYCLOAK_CLIENT_ID"),
            "client_secret": os.getenv("KEYCLOAK_CLIENT_SECRET")
        }

        # Valida se as variáveis foram carregadas
        if not all(keycloak_config.values()):
            print("-> Erro: Variáveis de ambiente do Keycloak não encontradas.")
            print("   Execute 'python keycloak_setup.py' primeiro para gerar o arquivo .env")
            exit()
        
        # Get authenticator from the factory
        keycloak_auth = get_authenticator("keycloak", keycloak_config)
        print(f"-> Successfully created a {type(keycloak_auth).__name__} instance.")

        # Get headers (which implicitly fetches the token)
        auth_headers = keycloak_auth.get_authorized_headers()

        if auth_headers:
            print("-> Keycloak authentication successful!")
            print("   Authorization Headers:", auth_headers)
            # test_api_call("http://yourapi.com/protected/resource", auth_headers)
        else:
            print("-> Failed to get Keycloak token. Check server connection and credentials.")

    except ValueError as e:
        print(f"-> Configuration Error: {e}")

    # --- Test Case 2: Cognito ---
    print("\n[2] Attempting Cognito Authentication...")
    try:
        # Define Cognito config (replace with your actual data)
        # Você pode adicionar estas variáveis ao seu arquivo .env também
        cognito_config = {
            "cognito_domain": os.getenv("COGNITO_DOMAIN", "your_cognito_domain..."),
            "client_id": os.getenv("COGNITO_CLIENT_ID", "your_cognito_client_id"),
            "client_secret": os.getenv("COGNITO_CLIENT_SECRET", "your_cognito_client_secret"),
            "scope": os.getenv("COGNITO_SCOPE", "api/read")
        }

        cognito_auth = get_authenticator("cognito", cognito_config)
        print(f"-> Successfully created a {type(cognito_auth).__name__} instance.")
        auth_headers = cognito_auth.get_authorized_headers()

        if auth_headers:
            print("-> Cognito authentication successful!")
            print("   Authorization Headers:", auth_headers)
    except ValueError as e:
        print(f"-> Configuration Error: {e}")
