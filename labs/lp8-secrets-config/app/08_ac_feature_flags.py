"""Part 8 - Feature flags with FeatureManager.

What this shows (LP8 Module 2, unit 3):
  - load(..., feature_flag_enabled=True) loads the flags
  - FeatureManager(config).is_enabled("Name") returns True/False
  - A flag is a kill switch / rollout switch you flip WITHOUT redeploying

IMPORTANT: the real parameter name is feature_flag_enabled (no "s").
The Learn page writes feature_flags_enabled=True. Python accepts that silently,
ignores it, and every flag reads as False. This script proves it.
"""
import lab_env  # noqa: F401  first import: stops with a clear message if the venv isn't active
from azure.appconfiguration.provider import SettingSelector, load
from azure.identity import DefaultAzureCredential
from featuremanagement import FeatureManager

from lab_env import need

endpoint = need("AZURE_APPCONFIG_ENDPOINT")
credential = DefaultAzureCredential()
only_mine = [SettingSelector(key_filter="DocPipeline:*", label_filter="\0")]
FLAGS = ["UseNewEmbeddingsModel", "EnableBatchProcessing", "ClassificationStage"]

# ---- The trap -----------------------------------------------------------------
wrong = load(endpoint=endpoint, credential=credential, keyvault_credential=credential, selects=only_mine,
             feature_flags_enabled=True, startup_timeout=20)          # typo-style name
fm_wrong = FeatureManager(wrong)
print("== With feature_flags_enabled=True (wrong name, silently ignored) ==")
for f in FLAGS:
    print(f"  {f:<24} -> {fm_wrong.is_enabled(f)}")

# ---- The right way ------------------------------------------------------------
config = load(endpoint=endpoint, credential=credential, keyvault_credential=credential, selects=only_mine,
              feature_flag_enabled=True, startup_timeout=20)
feature_manager = FeatureManager(config)
print("\n== With feature_flag_enabled=True (correct) ==")
for f in FLAGS:
    print(f"  {f:<24} -> {feature_manager.is_enabled(f)}")


def process(document):
    steps = ["extract text"]
    if feature_manager.is_enabled("UseNewEmbeddingsModel"):
        steps.append("embed with NEW model (text-embedding-3-large)")      # progressive rollout
    else:
        steps.append("embed with CURRENT model (text-embedding-ada-002)")
    if feature_manager.is_enabled("ClassificationStage"):                  # kill switch
        steps.append("classify")
    else:
        steps.append("SKIP classify (kill switch is off)")
    return f"{document}: " + " -> ".join(steps)


print("\n== What the pipeline does right now ==")
print(" ", process("invoice-001.pdf"))
print("\nFlip a flag in terminal 2 (see the guide), run this script again, and the output changes.")
print("Done. Part 8 complete.")
