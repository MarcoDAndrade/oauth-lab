import requests
import json
from typing import Optional, Dict

class CognitoAuthenticator:
    def __init__(self, client_id, client_secret, cognito_domain, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self._access_token: Optional[str] = None
        self.cognito_domain = cognito_domain
        self.scope = scope
        self.token_url = f"https://{self.cognito_domain}/oauth2/token"

    def get_m2m_jwt_token(self):
        """
        Obtains a JWT token for machine-to-machine (M2M) authentication from Cognito.

        Returns:
            str: The JWT access token if successful, None otherwise.
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope
        }

        try:
            response = requests.post(self.token_url, headers=headers, data=data)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            token_data = response.json()
            self._access_token = token_data.get('access_token')
            return self._access_token
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining M2M JWT token: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status code: {e.response.status_code}")
                print(f"Response body: {e.response.text}")
            return None

    def get_authorized_headers(self) -> Dict[str, str]:
        """
        Returns a dictionary of headers with the Authorization bearer token.
        If the token is not yet obtained, it will try to get it.
        """
        if not self._access_token:
            self.get_m2m_jwt_token()

        if self._access_token:
            return {"Authorization": f"Bearer {self._access_token}"}
        else:
            return {}

if __name__ == '__main__':
    # Example Usage:
    # Replace with your actual Cognito details
    CLIENT_ID = "your_cognito_client_id"
    CLIENT_SECRET = "your_cognito_client_secret"
    COGNITO_DOMAIN = "your_cognito_domain.auth.us-east-1.amazoncognito.com" # e.g., your-app.auth.us-east-1.amazoncognito.com
    SCOPE = "your_api_scope/read your_api_scope/write" # e.g., "api/read api/write"

    authenticator = CognitoAuthenticator(CLIENT_ID, CLIENT_SECRET, COGNITO_DOMAIN, SCOPE)
    jwt_token = authenticator.get_m2m_jwt_token()

    if jwt_token:
        print("\nSuccessfully obtained Cognito M2M JWT Token:")
        print(f"JWT Token: {jwt_token}\n")

        # Get headers for making authorized API calls
        auth_headers = authenticator.get_authorized_headers()
        print("Authorization headers for API calls:")
        print(auth_headers)

    else:
        print("Failed to obtain Cognito M2M JWT Token.")