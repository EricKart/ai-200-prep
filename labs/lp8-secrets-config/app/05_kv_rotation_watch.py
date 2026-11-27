"""Part 5 - Zero-downtime rotation with a REAL credential (a storage account key).

Leave this running in terminal 1. In terminal 2 you rotate the storage key
(dual-credential rotation). Watch this script keep working the whole time.

How it stays up (LP8 Module 1, units 4 and 5):
  - It caches the connection string from Key Vault (TTL cache, 20 s for the demo)
  - Every 3 s it calls Azure Storage with the cached value
  - If Storage says "authentication failed", it re-reads the secret from Key Vault
    (which returns the LATEST version) and retries once: the retry-on-auth-failure pattern

Stop it with Ctrl+C.

Optional: pass a cache TTL in seconds, e.g.  python 05_kv_rotation_watch.py 600
(a long TTL makes the auth-failure + refetch path easy to see).
"""
import lab_env  # noqa: F401  first import: stops with a clear message if the venv isn't active
import sys
import time
from datetime import datetime

from azure.core.exceptions import ClientAuthenticationError, HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.queue import ExponentialRetry, QueueServiceClient

from lab_env import explain_auth_error, need

SECRET = "storage-connection-string"
TTL = int(sys.argv[1]) if len(sys.argv) > 1 else 20   # optional: python 05_kv_rotation_watch.py 600
kv = SecretClient(vault_url=need("KEY_VAULT_URL"), credential=DefaultAzureCredential())

cache = {"value": None, "version": None, "at": 0.0}


def log(msg):
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


def load_secret(reason):
    s = kv.get_secret(SECRET)
    if s.properties.version != cache["version"]:
        log(f"  Key Vault -> version {s.properties.version[:8]}.. ({reason})  <-- NEW VALUE")
    cache.update(value=s.value, version=s.properties.version, at=time.monotonic())


def get_conn():
    if cache["value"] is None or time.monotonic() - cache["at"] >= TTL:
        load_secret("cache TTL expired" if cache["value"] else "first load")
    return cache["value"]


def call_storage(conn):
    # A real, authenticated call. It fails with 403 if the key in `conn` was regenerated.
    # Short retries so the demo reacts in seconds (the SDK default waits 15 s, then longer).
    svc = QueueServiceClient.from_connection_string(
        conn, retry_policy=ExponentialRetry(initial_backoff=1, increment_base=2, retry_total=2),
        connection_timeout=10, read_timeout=10)
    return [q.name for q in svc.list_queues()]


def call_downstream(max_retries=1):
    conn = get_conn()
    for attempt in range(max_retries + 1):
        try:
            return call_storage(conn)
        except (ClientAuthenticationError, HttpResponseError) as e:
            if getattr(e, "status_code", None) not in (401, 403) or attempt == max_retries:
                raise
            log("  Storage rejected the key (403). The credential was probably rotated. Re-reading Key Vault...")
            load_secret("refetch after auth failure")
            conn = cache["value"]


try:
    get_conn()
except HttpResponseError as e:
    explain_auth_error(e)
    raise SystemExit(1)

log(f"Watching. Calling Azure Storage every 3 s. Cache TTL = {TTL} s. Press Ctrl+C to stop.")
ok = failed = 0
try:
    while True:
        try:
            queues = call_downstream()
            ok += 1
            log(f"OK   storage call #{ok:<3} using version {cache['version'][:8]}..  queues={queues}")
        except Exception as e:  # noqa: BLE001 - show any failure to the student
            failed += 1
            log(f"FAIL {type(e).__name__}: {str(e).splitlines()[0][:110]}")
        time.sleep(3)
except KeyboardInterrupt:
    print(f"\nStopped. Successful calls: {ok}, failed calls: {failed}.")
    print("Zero failed calls during the rotation = zero downtime. Part 5 complete.")
