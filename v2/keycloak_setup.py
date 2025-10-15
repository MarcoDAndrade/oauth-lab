import time
from keycloak import KeycloakAdmin, KeycloakOpenID
from keycloak.exceptions import KeycloakError
import requests

# --- Configurações ---
KEYCLOAK_SERVER_URL = "http://localhost:8080/auth/"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"
REALM_NAME = "my-lab-realm"
CLIENT_ID = "my-m2m-client"

def wait_for_keycloak(url, retries=10, delay=10):
    """Espera o Keycloak ficar disponível."""
    print(f"Aguardando o Keycloak ficar disponível em {url}...")
    for i in range(retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("Keycloak está online!")
                return True
        except requests.ConnectionError:
            pass
        print(f"Tentativa {i+1}/{retries}: Keycloak não disponível. Aguardando {delay}s...")
        time.sleep(delay)
    print("Erro: O Keycloak não ficou disponível a tempo.")
    return False

def setup_keycloak():
    """
    Conecta ao Keycloak, cria um realm e um client para o fluxo M2M,
    e gera um arquivo .env com as credenciais.
    """
    if not wait_for_keycloak(KEYCLOAK_SERVER_URL):
        return

    try:
        # Conecta ao realm 'master' para tarefas administrativas
        keycloak_admin = KeycloakAdmin(
            server_url=KEYCLOAK_SERVER_URL,
            username=ADMIN_USERNAME,
            password=ADMIN_PASSWORD,
            realm_name="master",
            verify=True
        )

        # 1. Cria o Realm se não existir
        print(f"Verificando/Criando o realm '{REALM_NAME}'...")
        try:
            keycloak_admin.create_realm(
                payload={"realm": REALM_NAME, "enabled": True},
                skip_exists=True
            )
            print(f"Realm '{REALM_NAME}' criado ou já existente.")
        except KeycloakError as e:
            if e.response_code == 409: # 409 Conflict = Already exists
                print(f"Realm '{REALM_NAME}' já existe.")
            else:
                raise

        # Muda o contexto para o novo realm
        keycloak_admin.realm_name = REALM_NAME

        # 2. Cria o Client para M2M se não existir
        print(f"Verificando/Criando o client '{CLIENT_ID}'...")
        client_internal_id = keycloak_admin.get_client_id(CLIENT_ID)
        if not client_internal_id:
            keycloak_admin.create_client(
                payload={
                    "clientId": CLIENT_ID,
                    "enabled": True,
                    "protocol": "openid-connect",
                    "publicClient": False, # Confidencial
                    "serviceAccountsEnabled": True, # Habilita o fluxo client_credentials
                    "standardFlowEnabled": False, # Desabilita fluxo de login de usuário
                    "directAccessGrantsEnabled": False,
                }
            )
            print(f"Client '{CLIENT_ID}' criado.")
            client_internal_id = keycloak_admin.get_client_id(CLIENT_ID)
        else:
            print(f"Client '{CLIENT_ID}' já existe.")

        # 3. Obtém o Client Secret
        client_secret = keycloak_admin.get_client_secrets(client_internal_id)[0]['value']
        print("Client Secret obtido com sucesso.")

        # 4. Cria o arquivo .env
        with open(".env", "w") as f:
            f.write(f'KEYCLOAK_SERVER_URL="{KEYCLOAK_SERVER_URL.rstrip("/")}"\n')
            f.write(f'KEYCLOAK_REALM="{REALM_NAME}"\n')
            f.write(f'KEYCLOAK_CLIENT_ID="{CLIENT_ID}"\n')
            f.write(f'KEYCLOAK_CLIENT_SECRET="{client_secret}"\n')
        print("\nArquivo .env criado com sucesso com as seguintes configurações:")
        print(f"  - REALM: {REALM_NAME}\n  - CLIENT_ID: {CLIENT_ID}\n  - CLIENT_SECRET: {client_secret[:4]}...{client_secret[-4:]}")

    except Exception as e:
        print(f"\nOcorreu um erro durante o setup: {e}")

if __name__ == "__main__":
    setup_keycloak()