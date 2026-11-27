"""Imported first by run_demo.py and run_query.py.

Checks that the virtual environment is active. In a new terminal it usually isn't,
and Python would otherwise fail with "ModuleNotFoundError: No module named 'requests'".
"""
import sys


# ---- Runs the moment a lab script starts: is the virtual environment active? ----
# Without it, Python can't find the Azure packages and you'd get a confusing
# "ModuleNotFoundError: No module named 'azure'". This prints the fix instead.
try:
    import azure.monitor.opentelemetry  # noqa: F401
    import requests  # noqa: F401
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
