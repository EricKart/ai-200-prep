"""Part 3 - Cache secrets so you don't call Key Vault on every request.

What this shows (LP8 Module 1, unit 5):
  1. Without a cache: 20 "requests" = 20 Key Vault calls (slow, and can hit the 429 throttle)
  2. Time-based cache (TTL): 20 requests = 1 Key Vault call
  3. After the TTL passes, the cache fetches a fresh value once
  4. Startup preloading: load every secret once when the app starts
"""
import lab_env  # noqa: F401  first import: stops with a clear message if the venv isn't active
import time

from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from lab_env import explain_auth_error, need

VAULT_URL = need("KEY_VAULT_URL")
credential = DefaultAzureCredential()
client = SecretClient(vault_url=VAULT_URL, credential=credential)


class SecretCache:
    """Same pattern as the Learn module, plus a counter so you can SEE the vault calls."""

    def __init__(self, client, cache_ttl_seconds=900):
        self._client = client
        self._cache = {}
        self._cache_ttl = cache_ttl_seconds
        self.vault_calls = 0

    def get_secret(self, secret_name):
        cached = self._cache.get(secret_name)
        now = time.monotonic()          # clock that ignores system time changes
        if cached and (now - cached["timestamp"]) < self._cache_ttl:
            return cached["value"]      # cache hit, no network call
        secret = self._client.get_secret(secret_name)   # cache miss, call Key Vault
        self.vault_calls += 1
        self._cache[secret_name] = {"value": secret.value, "timestamp": now}
        return secret.value


def handle_requests(get, n=20):
    start = time.perf_counter()
    for _ in range(n):
        get("openai-api-key")
    return (time.perf_counter() - start) * 1000


try:
    client.get_secret("openai-api-key")   # warm-up: sign-in + first connection
except HttpResponseError as e:
    explain_auth_error(e)
    raise SystemExit(1)

# ---- 1. No cache ------------------------------------------------------------
print("== 1. No cache: every request calls Key Vault ==")
ms = handle_requests(lambda name: client.get_secret(name).value)
print(f"  20 requests -> 20 vault calls, {ms:.0f} ms total ({ms / 20:.1f} ms each)")

# ---- 2. TTL cache -----------------------------------------------------------
print("\n== 2. Time-based cache (TTL = 5 seconds for the demo; use 15-60 min in real apps) ==")
cache = SecretCache(client, cache_ttl_seconds=5)
ms = handle_requests(cache.get_secret)
print(f"  20 requests -> {cache.vault_calls} vault call(s), {ms:.0f} ms total ({ms / 20:.3f} ms each)")

# ---- 3. TTL expiry ----------------------------------------------------------
print("\n== 3. Wait 6 seconds so the cached value expires ==")
time.sleep(6)
handle_requests(cache.get_secret)
print(f"  20 more requests -> total vault calls now {cache.vault_calls} (one refresh after the TTL)")


# ---- 4. Startup preloading --------------------------------------------------
class AppConfig:
    def __init__(self, client, secret_names):
        self._secrets = {name: client.get_secret(name).value for name in secret_names}

    def get(self, secret_name):
        return self._secrets.get(secret_name)


print("\n== 4. Startup preloading ==")
config = AppConfig(client, ["openai-api-key", "cosmosdb-connection-string", "storage-connection-string"])
print(f"  Loaded {len(config._secrets)} secrets at startup. Requests now read memory only.")
print(f"  config.get('openai-api-key') starts with '{config.get('openai-api-key')[:6]}...'")

print("\nKey Vault limit to remember: 4,000 GET per vault per 10 seconds -> HTTP 429 if you go over.")
print("Done. Part 3 complete.")
