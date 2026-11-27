# Lab LP8: Secrets and configuration for an AI app

> Covers all of **Learning Path 8**: Key Vault (M1) and App Configuration (M2). About 2 hours.
> **Step-by-step guide with explanations and diagrams:** open [guide.html](guide.html) in your browser (works offline).
> Part of [AI-200 Prep](../../README.md) · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200)

## What you'll do

- Create a Key Vault with RBAC, give yourself a data-plane role, and store three secrets.
- Read secrets from Python with `DefaultAzureCredential`, then work with versions, expiry and disabling old versions.
- Cache secrets and measure why it matters. Use the async client.
- Rotate a real storage key with zero downtime (dual-credential rotation).
- Invalidate the cache with Event Grid when a new secret version is created.
- Create an App Configuration store (Free tier), import settings, use labels and feature flags, add a Key Vault reference, and refresh with a sentinel key.

## Before you start

- An Azure subscription where you can create resource groups and role assignments.
- Azure CLI signed in (`az login`), Python 3.10+, and a terminal (bash, zsh, Git Bash, Cloud Shell or PowerShell).
- Put the lab folder in your home folder (`~/ai200-lp8-lab`). On macOS, some terminals can't run `az` inside `~/Downloads`.

## Cost

Official pricing, November 2026. Check the pricing pages for your region.

| Resource | Price | This lab |
|---|---|---|
| Key Vault Standard | about $0.03 per 10,000 operations, with no monthly fee | a few hundred operations |
| App Configuration **Free** tier | $0 (one free store per subscription) | The lab passes `--sku Free` on purpose: the default Standard tier bills about $1.20 a day |
| Storage account | pennies for a few KB | |
| Event Grid | first 100,000 operations per month free | |

Expect **well under ₹10 in total** if you clean up the same day.

## Run it

1. Open [guide.html](guide.html) and pick **Bash** or **PowerShell** once at the top. Every command block then matches your terminal.
2. Commands are in [cmd/bash.sh](cmd/bash.sh) and [cmd/ps.ps1](cmd/ps.ps1), split into named steps (`# @@ step-name`). Python scripts are in [app/](app/).
3. Opening a new terminal later? Use the guide's **New terminal** block. It re-activates the venv and looks up your resource names. Don't re-run the variables step, because that makes new random names.

## Clean up

Delete everything as soon as you finish:

```bash
az group delete --name rg-ai200-lp8 --yes
az keyvault purge --name <your-vault-name> --location centralindia
```

Key Vault and App Configuration keep deleted stores in soft delete, so check that nothing is left with `az keyvault list-deleted` and `az appconfig list-deleted`.

## Tested

Tested live in Central India on 26–27 Nov 2026 (bash and a fresh zsh run). Findings from testing are noted in the guide, for example
that the provider parameter is `feature_flag_enabled`, while the Learn page writes `feature_flags_enabled`.
The PowerShell blocks are a line-by-line translation and **haven't been run live yet**. Please [report](../../CONTRIBUTING.md) anything that fails.

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200)
