"""Part 1 - Read secrets from Key Vault with the Python SDK.

What this shows (LP8 Module 1, units 2 and 3):
  1. SecretClient + DefaultAzureCredential (no password or key in code)
  2. get_secret()  -> the value and its metadata (version, content type, tags)
  3. list_properties_of_secrets()  -> names and metadata only, never values
  4. Error handling: a missing secret raises ResourceNotFoundError
"""
import lab_env  # noqa: F401  first import: stops with a clear message if the venv isn't active
from azure.core.exceptions import HttpResponseError, ResourceNotFoundError, ServiceRequestError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from lab_env import explain_auth_error, need

vault_url = need("KEY_VAULT_URL")

# DefaultAzureCredential tries several sign-in methods in order.
# On your laptop it ends up using your `az login` account (AzureCliCredential).
# On Azure (App Service, Container Apps, AKS...) it would use a managed identity.
credential = DefaultAzureCredential()
client = SecretClient(vault_url=vault_url, credential=credential)

print(f"Vault: {vault_url}\n")

# ---- 1. Get one secret -------------------------------------------------------
print("== 1. get_secret('openai-api-key') ==")
try:
    secret = client.get_secret("openai-api-key")
except HttpResponseError as e:
    explain_auth_error(e)
    raise SystemExit(1)

masked = secret.value[:6] + "..." if secret.value else ""
print(f"  value (masked) : {masked}")        # never print real secrets in real apps
print(f"  version        : {secret.properties.version}")
print(f"  created_on     : {secret.properties.created_on}")
print(f"  content_type   : {secret.properties.content_type}")
print(f"  tags           : {secret.properties.tags}")

# ---- 2. List every secret WITHOUT reading values ----------------------------
print("\n== 2. list_properties_of_secrets()  (metadata only) ==")
required = ["openai-api-key", "cosmosdb-connection-string", "storage-connection-string"]
found = []
for prop in client.list_properties_of_secrets():
    found.append(prop.name)
    print(f"  {prop.name:<28} enabled={prop.enabled}  content_type={prop.content_type}  tags={prop.tags}")

missing = [name for name in required if name not in found]
print(f"\n  Startup check -> missing secrets: {missing or 'none, all good'}")


# ---- 3. Error handling --------------------------------------------------------
def get_secret_safely(client, secret_name):
    try:
        return client.get_secret(secret_name).value
    except ResourceNotFoundError:
        # Secret doesn't exist -> configuration error. Retrying won't help.
        print(f"  ResourceNotFoundError: '{secret_name}' is not in this vault. Check the name.")
    except HttpResponseError as e:
        # 401/403 (no role) or a server-side problem.
        print(f"  HttpResponseError {e.status_code}: {e.message}")
    except ServiceRequestError:
        # Network problem (DNS, timeout). Might work if you retry.
        print("  ServiceRequestError: network problem reaching Key Vault.")
    return None


print("\n== 3. Ask for a secret that does not exist ==")
get_secret_safely(client, "this-secret-does-not-exist")
print("\nDone. Part 1 complete.")
