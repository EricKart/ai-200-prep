"""Part 6 - Event-driven cache invalidation with Event Grid.

Key Vault -> Event Grid -> Storage queue "kv-events" -> this script.

When a new version of ANY secret is created, Key Vault emits a
Microsoft.KeyVault.SecretNewVersionCreated event. Event Grid drops it in the queue.
This script reads the queue, removes that secret from its cache, and the next read
fetches the fresh value. A long TTL (1 hour) stays as a safety net in case an event is lost.

Leave this running. In terminal 2, run `az keyvault secret set ...` and watch.
Stop with Ctrl+C.
"""
import lab_env  # noqa: F401  first import: stops with a clear message if the venv isn't active
import base64
import json
import time
from datetime import datetime

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.queue import QueueClient

from lab_env import need

kv = SecretClient(vault_url=need("KEY_VAULT_URL"), credential=DefaultAzureCredential())

# The app gets its OWN storage credential from Key Vault too (no keys in code).
queue = QueueClient.from_connection_string(kv.get_secret("storage-connection-string").value, "kv-events")

cache = {}           # name -> (value, version, loaded_at)
TTL = 3600           # fallback refresh, 1 hour


def log(msg):
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


def get(name):
    hit = cache.get(name)
    if hit and time.monotonic() - hit[2] < TTL:
        return hit
    s = kv.get_secret(name)
    cache[name] = (s.value, s.properties.version, time.monotonic())
    log(f"  cache MISS -> fetched '{name}' from Key Vault, version {s.properties.version[:8]}..")
    return cache[name]


def decode(msg):
    raw = msg.content
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return json.loads(base64.b64decode(raw))   # Event Grid writes Base64 text to queues


get("openai-api-key")
log("Listening for Key Vault events on queue 'kv-events'. Ctrl+C to stop.")
log("Now run in terminal 2:  az keyvault secret set --vault-name <vault> --name openai-api-key --value sk-demo-NEW")
try:
    while True:
        for msg in queue.receive_messages(messages_per_page=16, visibility_timeout=30):
            event = decode(msg)
            etype = event.get("eventType", "?")
            name = event.get("data", {}).get("ObjectName", "?")
            version = event.get("data", {}).get("Version", "")
            log(f"EVENT {etype}  secret={name}  version={version[:8]}..")
            if etype.endswith("SecretNewVersionCreated") and name in cache:
                cache.pop(name)
                log(f"  invalidated '{name}' in the cache")
            queue.delete_message(msg)
        value, version, _ = get("openai-api-key")       # what a request would read right now
        log(f"request reads openai-api-key -> version {version[:8]}..  value starts '{value[:10]}'")
        time.sleep(5)
except KeyboardInterrupt:
    print("\nStopped. Part 6 complete.")
