"""Part 10 - Dynamic refresh with a sentinel key (no restart).

Leave this running. In terminal 2, change a setting, then change the "Sentinel"
key. Within ~10 seconds this script prints the new values.

What this shows (LP8 Module 2, units 2, 3 and 4):
  - refresh_on=[WatchKey("Sentinel")] -> the provider watches ONE key
  - refresh_interval=10 -> refresh() contacts the store at most every 10 s
  - Changing other keys alone does nothing; changing the Sentinel reloads EVERYTHING together
  - feature_flag_refresh_enabled=True -> flags refresh on their own (no sentinel needed)
  - secret_refresh_interval=60 -> Key Vault secrets are re-read every 60 s
  - refresh() must be called by YOUR code (here: once per loop)

Why no trim_prefixes here? Tested Nov 2026 with azure-appconfiguration-provider 2.5.1:
when trim_prefixes is used, the periodic secret refresh writes the new secret under the
UNTRIMMED key ("DocPipeline:OpenAI:ApiKey"), so config["OpenAI:ApiKey"] keeps the old value.
Using full key names avoids that.
Stop with Ctrl+C.
"""
import lab_env  # noqa: F401  first import: stops with a clear message if the venv isn't active
import time
from datetime import datetime

from azure.appconfiguration.provider import SettingSelector, WatchKey, load
from azure.identity import DefaultAzureCredential
from featuremanagement import FeatureManager

from lab_env import need

credential = DefaultAzureCredential()
config = load(
    endpoint=need("AZURE_APPCONFIG_ENDPOINT"),
    credential=credential,
    keyvault_credential=credential,
    selects=[SettingSelector(key_filter="DocPipeline:*", label_filter="\0")],
    refresh_on=[WatchKey("Sentinel")],
    refresh_interval=10,
    feature_flag_enabled=True,
    feature_flag_refresh_enabled=True,
    secret_refresh_interval=60,
)
feature_manager = FeatureManager(config)


def snapshot():
    return (config["DocPipeline:Pipeline:BatchSize"], config["DocPipeline:Pipeline:RetryCount"],
            feature_manager.is_enabled("UseNewEmbeddingsModel"), config["DocPipeline:OpenAI:ApiKey"][:12])


print("Watching. BatchSize / RetryCount refresh via Sentinel; flags refresh by themselves; secret every 60 s.")
last = None
try:
    while True:
        try:
            config.refresh()                  # cheap: returns at once if 10 s haven't passed
        except Exception as e:  # noqa: BLE001 - a network blip must not kill the app
            print(f"  (refresh failed: {type(e).__name__}; keeping the last known values)")
        now = snapshot()
        tag = "  <-- CHANGED" if last and now != last else ""
        print(f"[{datetime.now():%H:%M:%S}] BatchSize={now[0]:<4} RetryCount={now[1]:<3} "
              f"UseNewEmbeddingsModel={str(now[2]):<5} ApiKey={now[3]}...{tag}", flush=True)
        last = now
        time.sleep(5)
except KeyboardInterrupt:
    print("\nStopped. Part 10 complete.")
