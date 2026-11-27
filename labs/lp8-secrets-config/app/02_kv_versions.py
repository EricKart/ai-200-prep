"""Part 2 - Versions, expiry dates, disabling an old version.

What this shows (LP8 Module 1, unit 4):
  1. set_secret() with the SAME name creates a NEW version (nothing is overwritten)
  2. get_secret(name) returns the latest version; get_secret(name, version=...) returns an exact one
  3. list_properties_of_secret_versions() shows the rotation history
  4. expires_on is informational: an expired secret can STILL be read
  5. update_secret_properties(enabled=False) blocks an old version completely
"""
import lab_env  # noqa: F401  first import: stops with a clear message if the venv isn't active
from datetime import datetime, timedelta, timezone

from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from lab_env import explain_auth_error, need

client = SecretClient(vault_url=need("KEY_VAULT_URL"), credential=DefaultAzureCredential())
NAME = "cosmosdb-connection-string"

# ---- 1. Create a new version ------------------------------------------------
print(f"== 1. Store a new value for '{NAME}' (simulates rotating a credential) ==")
try:
    old = client.get_secret(NAME)
except HttpResponseError as e:
    explain_auth_error(e)
    raise SystemExit(1)

new_value = "AccountEndpoint=https://demo.documents.azure.com:443/;AccountKey=demo-key-v2;"
expires = datetime.now(timezone.utc) + timedelta(days=90)          # 90-day rotation policy
new = client.set_secret(
    NAME,
    new_value,
    content_type="text/plain",
    expires_on=expires,
    tags={"environment": "dev", "rotation-policy": "90-days"},
)
print(f"  old version : {old.properties.version}")
print(f"  new version : {new.properties.version}   expires_on={new.properties.expires_on:%Y-%m-%d}")

# ---- 2. Latest vs exact version ---------------------------------------------
print("\n== 2. get_secret() with and without a version ==")
latest = client.get_secret(NAME)
exact = client.get_secret(NAME, version=old.properties.version)
print(f"  get_secret(name)                 -> version {latest.properties.version[:8]}..  ends with '{latest.value[-12:]}'")
print(f"  get_secret(name, version=<old>)  -> version {exact.properties.version[:8]}..  ends with '{exact.value[-12:]}'")

# ---- 3. Rotation history ----------------------------------------------------
print("\n== 3. list_properties_of_secret_versions() ==")
for v in sorted(client.list_properties_of_secret_versions(NAME), key=lambda p: p.created_on):
    print(f"  {v.version}  created={v.created_on:%H:%M:%S}  enabled={v.enabled}  expires={v.expires_on}")

# ---- 4. Expiry is only a label ----------------------------------------------
print("\n== 4. An EXPIRED secret can still be read ==")
past = datetime.now(timezone.utc) - timedelta(days=1)
client.set_secret("expired-demo", "still-readable", expires_on=past)
print(f"  get_secret('expired-demo').value = '{client.get_secret('expired-demo').value}'  <- expiry did not block it")

# ---- 5. Disable the old version ---------------------------------------------
print("\n== 5. Disable the OLD version so nobody can keep using it ==")
client.update_secret_properties(NAME, version=old.properties.version, enabled=False)
try:
    client.get_secret(NAME, version=old.properties.version)
    print("  (unexpected) old version is still readable")
except HttpResponseError as e:
    print(f"  Reading the disabled version now fails: HTTP {e.status_code} ({e.error.code if e.error else ''})")
print(f"  Reading the latest still works: ends with '{client.get_secret(NAME).value[-12:]}'")
print("\nDone. Part 2 complete.")
