import os
import sys
import msal
import requests
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# -----------------------------
# Configuration (inputs)
# -----------------------------
TENANT_ID = os.environ["AZURE_TENANT_ID"]
CLIENT_ID = os.environ["AZURE_CLIENT_ID"]        # SPNA client ID
KEYVAULT_NAME = os.environ["KEYVAULT_NAME"]
SECRET_NAME = "membership-manager"                # name in Key Vault

# New input
TECHNICAL_OWNER_GROUP = os.environ["TECHNICAL_OWNER_GROUP"]

KEYVAULT_URL = f"https://{KEYVAULT_NAME}.vault.azure.net"
GRAPH_URL = "https://graph.microsoft.com/v1.0"

# -----------------------------
# Step 1: Authenticate to Azure (OIDC / SPN-LOGIN via Azure CLI)
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
print(f"Token = {access_token[:10]}")  # DO NOT print full token in real pipelines

# =========================================================
# NEW FUNCTION: Validate Entra ID Group
# =========================================================
def validate_entra_group(group_name: str, token: str):
    """
    Validates whether the given group exists in Microsoft Entra ID.
    Returns (group_id, display_name) if valid.
    Exits with code 1 if not found.
    """
    group_name = group_name.strip()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        f"{GRAPH_URL}/groups",
        headers=headers,
        params={"$filter": f"displayName eq '{group_name}'"}
    )

    if response.status_code != 200:
        raise Exception(
            f"Graph API error while querying group: {response.text}"
        )

    groups = response.json().get("value", [])

    if not groups:
        print(
            f"ERROR: Group '{group_name}' does not exist in Microsoft Entra ID.\n"
            "Please create the group in Entra ID first and retry onboarding."
        )
        sys.exit(1)

    group = groups[0]
    group_id = group["id"]
    display_name = group["displayName"]

    print("SUCCESS: Valid Entra ID group found.")
    print(f"Group Name : {display_name}")
    print(f"Group ID   : {group_id}")

    return group_id, display_name


# -----------------------------
# Step 4: Validate technical owner group
# -----------------------------
group_id, group_name = validate_entra_group(
    TECHNICAL_OWNER_GROUP,
    access_token
)
