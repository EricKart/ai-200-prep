"""Part 7 - Load settings from App Configuration.

What this shows (LP8 Module 2, units 2 and 3):
  1. load() with no selector -> only keys with the NULL label (no label) are loaded
  2. SettingSelector(key_filter="DocPipeline:*") -> only this app's keys, not "OtherApp:*"
  3. trim_prefixes -> "DocPipeline:Pipeline:BatchSize" becomes "Pipeline:BatchSize"
  4. Label stacking -> defaults (null label) first, then the environment's label on top

Run it again with a different environment:
  bash/zsh:    APP_ENVIRONMENT=Production python 07_ac_load.py
  PowerShell:  $env:APP_ENVIRONMENT="Production"; python 07_ac_load.py
"""
import lab_env  # noqa: F401  first import: stops with a clear message if the venv isn't active
import os

from azure.appconfiguration.provider import SettingSelector, load
from azure.identity import DefaultAzureCredential

from lab_env import explain_auth_error, need

endpoint = need("AZURE_APPCONFIG_ENDPOINT")
credential = DefaultAzureCredential()
environment = os.environ.get("APP_ENVIRONMENT", "Development")


def show(title, config):
    print(f"\n== {title} ==")
    for key in sorted(config.keys()):
        value = config[key]
        if key.endswith("ApiKey"):            # a resolved Key Vault secret: never print it in full
            value = value[:6] + "... (from Key Vault, see Part 9)"
        print(f"  {key:<40} = {value}")


# keyvault_credential is only needed once the store holds a Key Vault reference (Part 9).
# Passing it from the start means this script works before AND after Part 9.


try:
    # 1. Everything with the null label (this is also what load() does with no selects at all)
    plain = load(endpoint=endpoint, credential=credential, keyvault_credential=credential,
                 selects=[SettingSelector(key_filter="*", label_filter="\0")],
                 startup_timeout=20)
except Exception as e:  # noqa: BLE001
    explain_auth_error(e)
    raise

show("1. load() -> every key with NO label (whole shared store)", plain)

# 2. Only this application's keys
mine = load(endpoint=endpoint, credential=credential, keyvault_credential=credential,
            selects=[SettingSelector(key_filter="DocPipeline:*", label_filter="\0")],
            startup_timeout=20)
show("2. key_filter='DocPipeline:*'  (OtherApp:* and Sentinel are gone)", mine)

# 3 + 4. Trim the prefix and stack labels: defaults first, environment overrides last
selects = [
    SettingSelector(key_filter="DocPipeline:*", label_filter="\0"),          # defaults
    SettingSelector(key_filter="DocPipeline:*", label_filter=environment),   # overrides (last wins)
]
config = load(endpoint=endpoint, credential=credential, keyvault_credential=credential, selects=selects,
              trim_prefixes=["DocPipeline:"], startup_timeout=20)
show(f"3+4. trim_prefixes + label stacking for APP_ENVIRONMENT={environment}", config)

print(f"\nThe code always asks for config['Pipeline:BatchSize'] -> {config['Pipeline:BatchSize']}")
print("Same code, different label, different value. No if/else on the environment.")
print("config.get('Pipeline:Missing', 'fallback') ->", config.get("Pipeline:Missing", "fallback"))
print("\nDone. Part 7 complete.")
