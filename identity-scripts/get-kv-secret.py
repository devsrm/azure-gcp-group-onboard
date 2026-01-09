from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

# -------- CONFIG --------
KEY_VAULT_NAME = "group-onboarding-kv"
SECRET_NAME = "group-onboarding-kv"
# ------------------------

KV_URL = f"https://{KEY_VAULT_NAME}.vault.azure.net"

def get_secret(vault_url: str, secret_name: str) -> str:
    """
    Retrieves a secret value from Azure Key Vault using RBAC.
    """
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    secret = client.get_secret(secret_name)
    return secret.value


if __name__ == "__main__":
    value = get_secret(KV_URL, SECRET_NAME)
    print(f"Value:{value}")
    print(f"Secret '{SECRET_NAME}' retrieved successfully.")
