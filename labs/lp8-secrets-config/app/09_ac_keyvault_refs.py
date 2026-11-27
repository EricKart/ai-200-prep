"""Part 9 - Key Vault references: one load() gives settings AND secrets.

What this shows (LP8 Module 2, unit 4):
  - "DocPipeline:OpenAI:ApiKey" in App Configuration holds only a POINTER (URI) to Key Vault
  - With keyvault_credential=..., the provider follows the pointer and returns the secret value
  - Without it, load() fails: the provider refuses to hand you an unresolved reference
"""
import lab_env  # noqa: F401  first import: stops with a clear message if the venv isn't active
from azure.appconfiguration.provider import SettingSelector, load
from azure.identity import DefaultAzureCredential

from lab_env import need

endpoint = need("AZURE_APPCONFIG_ENDPOINT")
credential = DefaultAzureCredential()
selects = [SettingSelector(key_filter="DocPipeline:*", label_filter="\0")]

print("== 1. load() WITHOUT keyvault_credential ==")
try:
    load(endpoint=endpoint, credential=credential, selects=selects, startup_timeout=10)
    print("  (unexpected) loaded without resolving the reference")
except Exception as e:  # noqa: BLE001
    print(f"  Fails as expected -> {type(e).__name__}: {' '.join(str(e).split())[:130]}")

print("\n== 2. load() WITH keyvault_credential (same identity for both services) ==")
config = load(
    endpoint=endpoint,
    credential=credential,            # needs App Configuration Data Reader (or Owner)
    keyvault_credential=credential,   # needs Key Vault Secrets User (or Officer)
    selects=selects,
    trim_prefixes=["DocPipeline:"],
)
print(f"  OpenAI:Endpoint      = {config['OpenAI:Endpoint']}        <- plain value from App Configuration")
print(f"  OpenAI:ApiKey        = {config['OpenAI:ApiKey'][:10]}...  <- resolved from Key Vault")
print(f"  Pipeline:BatchSize   = {config['Pipeline:BatchSize']}")
print("\nThe app code can't tell which value came from where. That's the point.")
print("Done. Part 9 complete.")
