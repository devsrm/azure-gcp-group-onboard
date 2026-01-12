import os
import msal
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# -----------------------------
# Configuration (inputs)
# -----------------------------
TENANT_ID = os.environ["AZURE_TENANT_ID"]
CLIENT_ID = os.environ["AZURE_CLIENT_ID"]        # SPNA client ID
KEYVAULT_NAME = os.environ["KEYVAULT_NAME"]
SECRET_NAME = "spna-client-secret"                # name in Key Vault

KEYVAULT_URL = f"https://{KEYVAULT_NAME}.vault.azure.net"

# -----------------------------
# Step 1: Authenticate to Azure (OIDC via Azure CLI)
# -----------------------------
credential = DefaultAzureCredential()

# -----------------------------
# Step 2: Read client secret from Azure Key Vault
# -----------------------------
secret_client = SecretClient(
    vault_url=KEYVAULT_URL,
    credential=credential
)

client_secret = secret_client.get_secret(SECRET_NAME).value

# -----------------------------
# Step 3: Get Microsoft Graph access token using MSAL
# -----------------------------
app = msal.ConfidentialClientApplication(
    client_id=CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_credential=client_secret,
)

token_response = app.acquire_token_for_client(
    scopes=["https://graph.microsoft.com/.default"]
)

if "access_token" not in token_response:
    raise Exception(f"Token acquisition failed: {token_response}")

access_token = token_response["access_token"]

print("Microsoft Graph access token acquired successfully.")
print(f"Token = {access_token[:10]}")
# DO NOT print the token in real pipelines
