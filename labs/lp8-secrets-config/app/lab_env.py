"""Small helpers shared by every lab script.

need("NAME") reads an environment variable. If it's missing, it prints how to
set it in bash/zsh/Git Bash AND in PowerShell, then stops the script.
"""
import os
import sys


# ---- Runs the moment a lab script starts: is the virtual environment active? ----
# Without it, Python can't find the Azure packages and you'd get a confusing
# "ModuleNotFoundError: No module named 'azure'". This prints the fix instead.
try:
    import azure.identity  # noqa: F401
except ImportError:
    print("\n[!] The lab's Python packages are not available in this terminal.")
    print("    You are probably in a NEW terminal where the virtual environment is not active.")
    print("    From the lab folder, activate it, then run the script again:")
    print("      Mac / Linux / Cloud Shell (Bash):  source .venv/bin/activate")
    print("      Git Bash on Windows:               source .venv/Scripts/activate")
    print("      PowerShell on Windows:             .\\.venv\\Scripts\\Activate.ps1")
    print("      Cloud Shell (PowerShell):          ./.venv/bin/Activate.ps1")
    print("    Or paste the guide's 'New terminal' block, which does all of this.")
    print("    No .venv folder at all? Do Step 2 of the guide first.")
    sys.exit(1)

HOW_TO = {
    "KEY_VAULT_URL": "https://<your-vault-name>.vault.azure.net/",
    "AZURE_APPCONFIG_ENDPOINT": "https://<your-store-name>.azconfig.io",
    "STORAGE_ACCOUNT": "<your-storage-account-name>",
}


def need(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if value:
        return value
    example = HOW_TO.get(name, "<value>")
    print(f"\n[!] Environment variable {name} is not set in this terminal.\n")
    print("    bash / zsh / Git Bash / Cloud Shell (Bash):")
    print(f'      export {name}="{example}"\n')
    print("    PowerShell / Cloud Shell (PowerShell):")
    print(f'      $env:{name} = "{example}"\n')
    print("    Tip: the guide's 'New terminal' block sets all of them for you.")
    sys.exit(1)


def explain_auth_error(err: Exception) -> None:
    """Print a friendly hint for the two errors students hit most."""
    text = str(err)
    if "Forbidden" in text or "403" in text or "ForbiddenByRbac" in text:
        print("\n[!] 403 Forbidden: you signed in fine, but your account has no data-plane role yet.")
        print("    New role assignments can take 1-5 minutes to start working. Wait a minute and run again.")
    elif "DefaultAzureCredential failed" in text or "CredentialUnavailable" in text:
        print("\n[!] No sign-in found. Run:  az login   (then run this script again)")
