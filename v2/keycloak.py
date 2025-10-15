import requests

class KeycloakM2M:
    def __init__(self, server_url, realm, client_id, client_secret):
        self.server_url = server_url
        self.realm = realm
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = f"{self.server_url}/realms/{self.realm}/protocol/openid-connect/token"
        self._access_token = None

    def get_access_token(self):
        """
        Obtains an M2M (Machine-to-Machine) access token from Keycloak.
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        try:
            response = requests.post(self.token_url, headers=headers, data=data)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            token_data = response.json()
            self._access_token = token_data.get("access_token")
            return self._access_token
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining Keycloak token: {e}")
            return None

    def get_authorized_headers(self):
        """
        Returns a dictionary of headers with the Authorization bearer token.
        If the token is not yet obtained, it will try to get it.
        """
        if not self._access_token:
            self.get_access_token()

        if self._access_token:
            return {"Authorization": f"Bearer {self._access_token}"}
        else:
            return {}

# Example Usage:
if __name__ == "__main__":
    # Replace with your Keycloak server details
    KEYCLOAK_SERVER_URL = "http://localhost:8080"  # e.g., "https://your-keycloak-instance.com"
    KEYCLOAK_REALM = "your-realm"
    KEYCLOAK_CLIENT_ID = "your-client-id"
    KEYCLOAK_CLIENT_SECRET = "your-client-secret"

    # Initialize the Keycloak M2M client
    keycloak_client = KeycloakM2M(
        server_url=KEYCLOAK_SERVER_URL,
        realm=KEYCLOAK_REALM,
        client_id=KEYCLOAK_CLIENT_ID,
        client_secret=KEYCLOAK_CLIENT_SECRET
    )

    # Get the access token
    token = keycloak_client.get_access_token()

    if token:
        print("Successfully obtained Keycloak M2M access token:")
        print(f"Access Token: {token}\n")

        # Get headers for making authorized API calls
        auth_headers = keycloak_client.get_authorized_headers()
        print("Authorization headers for API calls:")
        print(auth_headers)

        # Example of using the token to access a protected resource
        # protected_api_url = "http://yourapi.com/protected/resource"
        # api_response = requests.get(protected_api_url, headers=auth_headers)
        # print(api_response.json())
    else:
        print("Failed to obtain Keycloak M2M access token.")