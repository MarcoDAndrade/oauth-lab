from typing import Union, Dict, Any

from keycloak import KeycloakM2M
from Cognito import CognitoAuthenticator

# Define a type hint for the authenticator instances for better static analysis
Authenticator = Union[KeycloakM2M, CognitoAuthenticator]

def get_authenticator(provider: str, config: Dict[str, Any]) -> Authenticator:
    """
    Factory function to get an authenticator instance based on the provider.

    This function acts as a single entry point to create clients for different
    OAuth/OIDC providers, abstracting the instantiation logic.

    :param provider: The name of the provider (e.g., 'keycloak' or 'cognito').
                     The comparison is case-insensitive.
    :param config: A dictionary with the configuration parameters for the provider.
    :return: An instance of the appropriate authenticator class (KeycloakM2M or CognitoAuthenticator).
    :raises ValueError: If the provider is not supported or if required configuration is missing.
    """
    provider_lower = provider.lower()

    if provider_lower == 'keycloak':
        required_keys = {'server_url', 'realm', 'client_id', 'client_secret'}
        if not required_keys.issubset(config):
            missing = required_keys - set(config.keys())
            raise ValueError(f"Missing required config for Keycloak: {missing}")
        
        return KeycloakM2M(
            server_url=config['server_url'],
            realm=config['realm'],
            client_id=config['client_id'],
            client_secret=config['client_secret']
        )

    elif provider_lower == 'cognito':
        required_keys = {'client_id', 'client_secret', 'cognito_domain', 'scope'}
        if not required_keys.issubset(config):
            missing = required_keys - set(config.keys())
            raise ValueError(f"Missing required config for Cognito: {missing}")

        return CognitoAuthenticator(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            cognito_domain=config['cognito_domain'],
            scope=config['scope']
        )

    else:
        raise ValueError(f"Unsupported provider: '{provider}'. Supported providers are 'keycloak' and 'cognito'.")


if __name__ == "__main__":
    print("--- Demonstrating Authenticator Factory ---")

    # --- Example 1: Get a Keycloak Authenticator ---
    print("\n1. Testing Keycloak Authenticator:")
    try:
        keycloak_config = {
            "server_url": "http://localhost:8080",
            "realm": "your-realm",
            "client_id": "your-client-id",
            "client_secret": "your-client-secret"
        }
        keycloak_auth = get_authenticator("keycloak", keycloak_config)
        print(f"Successfully created a {type(keycloak_auth).__name__} instance.")
        
        # The following lines would make actual calls. They are commented out
        # to prevent errors when running without a live server.
        # headers = keycloak_auth.get_authorized_headers()
        # if headers:
        #     print("Keycloak authorization headers:", headers)
        # else:
        #     print("Failed to get Keycloak token.")

    except ValueError as e:
        print(f"Error: {e}")

    # --- Example 2: Get a Cognito Authenticator ---
    print("\n2. Testing Cognito Authenticator:")
    try:
        cognito_config = {
            "cognito_domain": "your_cognito_domain.auth.us-east-1.amazoncognito.com",
            "client_id": "your_cognito_client_id",
            "client_secret": "your_cognito_client_secret",
            "scope": "api/read api/write"
        }
        cognito_auth = get_authenticator("cognito", cognito_config)
        print(f"Successfully created a {type(cognito_auth).__name__} instance.")
    except ValueError as e:
        print(f"Error: {e}")