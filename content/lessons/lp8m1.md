# LP8 · M1: Manage application secrets with Azure Key Vault

> **Learning path 8:** Manage application secrets and configuration for AI solutions · **Skill area 4:** Secure, monitor and troubleshoot solutions · about 74 min on Microsoft Learn  
> Study it interactively at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-8/manage-app-secrets-key-vault)

Key Vault keeps your API keys, connection strings and certificates out of code. You'll learn how to store and organize secrets, read them with the SDK, rotate them, and cache them safely.

**In this lesson**

1. [Store and organize secrets, keys, and certificates](#store-and-organize-secrets-keys-and-certificates)
2. [Retrieve secrets using Azure SDK client libraries](#retrieve-secrets-using-azure-sdk-client-libraries)
3. [Handle secret versioning and rotation](#handle-secret-versioning-and-rotation)
4. [Implement caching strategies to reduce Key Vault calls](#implement-caching-strategies-to-reduce-key-vault-calls)

## Store and organize secrets, keys, and certificates

📘 Microsoft Learn: [Store and organize secrets, keys, and certificates](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/2-store-organize-secrets)

Key Vault is a **bank vault for credentials**. **Secrets** are strings (API keys, connection strings), **keys** do cryptography _inside_ the vault, **certificates** manage TLS certs. Give each app and environment its own vault, give apps the **Secrets User** role, and turn on **purge protection** in production.

**Key facts**

- Three capabilities: **secrets**, **keys**, **certificates**. Everything is encrypted at rest; access = Entra ID authentication + Azure RBAC authorization.
- Tiers: **Standard** (software, FIPS 140 Level 1) and **Premium** (**HSM-protected** keys, FIPS 140-3 Level 3; key material never leaves the HSM).
- **Secrets**: strings up to **25 KB**, treated as opaque; optional **content_type** (up to 255 chars), e.g. text/plain or application/json.
- **Keys**: crypto runs server-side; RSA 2048/3072/4096, EC P-256, P-256K, P-384, P-521, symmetric (oct). Used to encrypt data or sign model artifacts.
- **Certificates**: X.509 with private keys; issuance, renewal, revocation with CAs. Storing one creates a matching **key and secret**.
- Organize with a **vault per application and environment** (kv-ragpipeline-dev/staging/prod) to limit blast radius and simplify RBAC.
- Vault names: globally unique, **3–24** characters, alphanumerics and hyphens, start with a letter, end with a letter or digit, no consecutive hyphens.
- Tags: up to **15** per secret (names ≤512 chars, values ≤256). Anyone with list/get can read tags, so no sensitive values.
- Prefer **Azure RBAC** over legacy access policies (granular, PIM, control and data planes). Roles: **Secrets User** (read values; apps), **Secrets Officer** (manage secrets; operators, CI/CD), **Administrator** (all data-plane ops, not role assignments), **Reader** (metadata, no values). **Key Vault Contributor** is **control plane only**: no secret access.
- **Soft delete** is on by default and can't be disabled: retention **7–90 days (default 90)**, set at creation, unchangeable. **Purge protection** blocks permanent deletion during retention. A recovered vault does **not** restore its RBAC assignments or Event Grid subscriptions.

| Role | Can do | Give to |
|---|---|---|
| Key Vault Secrets User | Read secret values | App managed identities |
| Key Vault Secrets Officer | Create, update, delete, list secrets | Operators, CI/CD |
| Key Vault Administrator | All data-plane ops on keys, secrets, certs | Vault admins |
| Key Vault Reader | Read metadata only | Monitoring and discovery tools |
| Key Vault Contributor | Manage the vault resource only | Not for reading secrets |

> [!WARNING]
> **Exam traps**
>
> - Key Vault Contributor can't read secrets.
> - Soft-delete retention is fixed at creation.
> - Tags are visible to anyone who can list secrets.

## Retrieve secrets using Azure SDK client libraries

📘 Microsoft Learn: [Retrieve secrets using Azure SDK client libraries](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/3-retrieve-secrets-sdk)

Install **azure-keyvault-secrets** and **azure-identity**, create a **SecretClient** with the vault URL and **DefaultAzureCredential**, then call `get_secret()`. Handle a missing secret differently from a network blip.

**Key facts**

- `pip install azure-keyvault-secrets azure-identity`; SecretClient(vault_url, credential). URL: `https://<vault-name>.vault.azure.net/`.
- **DefaultAzureCredential** order: EnvironmentCredential → WorkloadIdentityCredential → **ManagedIdentityCredential** → AzureCliCredential → AzureDeveloperCliCredential → AzurePowerShellCredential.
- `get_secret(name)` returns **KeyVaultSecret** (value, name, properties: version, created, expires, enabled, content_type, tags). Log name and version, never the value.
- `list_properties_of_secrets()` lists metadata **without values**; use it to validate that required secrets exist at startup.
- Errors: **ResourceNotFoundError** (secret missing: configuration problem), **HttpResponseError** (auth, authorization, server errors), **ServiceRequestError** (network: may succeed on retry).
- Async: `azure.keyvault.secrets.aio` and `azure.identity.aio`; close with async with or await close(); create once at startup and reuse.

> [!WARNING]
> **Exam traps**
>
> - Listing returns properties, never values.
> - Don't retry ResourceNotFoundError; fix the configuration.

## Handle secret versioning and rotation

📘 Microsoft Learn: [Handle secret versioning and rotation](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/4-handle-versioning-rotation)

Saving a secret with the same name **adds a new version**; apps that ask for the name get the newest. Rotate by hand, automatically when Key Vault says a secret is **near expiry**, or with **two keys** so something valid always exists. Apps should refetch and retry when a key stops working.

**Key facts**

- Each `set_secret()` with the same name creates a **new version** (GUID). `get_secret(name)` returns the **latest enabled** version; pass a version for an exact one.
- `list_properties_of_secret_versions(name)` shows version history; disable old versions with `update_secret_properties(…, enabled=False)`.
- **Manual rotation**: store new version, restart or signal the app; gap until it refetches.
- **Automated rotation**: Event Grid **SecretNearExpiry** fires **30 days** before expiry (and **SecretExpired** after); a Function generates a new credential and stores a new version.
- **Dual-credential** (Storage, Cosmos DB): regenerate secondary → store it → wait for all instances → regenerate the old primary. Always one valid credential.
- App pattern: on a downstream auth failure, **refetch** the secret and **retry** once.
- **expires_on** is informational: expired secrets can still be retrieved. Typical: 90-day expiry + SecretNearExpiry (30-day warning).

| Strategy | How | Good for |
|---|---|---|
| Manual | Operator stores new version, restarts app | Long-lived third-party keys |
| Automated (Event Grid) | SecretNearExpiry → Function → new version | Removing the human step |
| Dual-credential | New secondary → store → wait → regenerate primary | Services with two active keys |

> [!WARNING]
> **Exam traps**
>
> - Expired secrets are still retrievable; expiry doesn't block access.
> - SecretNearExpiry fires 30 days before expiry.

## Implement caching strategies to reduce Key Vault calls

📘 Microsoft Learn: [Implement caching strategies to reduce Key Vault calls](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/5-implement-caching-strategies)

Don't call Key Vault on every request: keep secrets in memory for a while. The cache time depends on how often the secret rotates. To refresh immediately after a rotation, listen for **SecretNewVersionCreated**. If you see **429**s, your cache is too short or something bypasses it.

**Key facts**

- Throttling: up to **4,000 GET** transactions per vault per **10 seconds** per region; writes (CREATE, IMPORT) **300** per 10 s; subscription aggregate **5×** the per-vault limit. Over the limit → **HTTP 429**.
- **Time-based cache**: store value + timestamp; refresh after a TTL (e.g. 900 s = at most 4 fetches per hour per instance). Use `time.monotonic()`.
- **Event-driven invalidation**: **SecretNewVersionCreated** via Event Grid → invalidate → refetch on next use. Combine with a TTL as fallback.
- Scopes: **per-process** (recommended start; 10 replicas × 15-min TTL ≤ 40 calls/hour/secret), **shared distributed** (e.g. Azure Managed Redis; fewer calls, but another place holding secrets), **startup preloading** (+ periodic refresh).
- TTL guide: daily/weekly rotation → **5–15 min** + Event Grid; monthly/quarterly → **30–60 min**; annual/static → preload, refresh every few hours. For possible emergency revocation: short TTL or Event Grid.
- On 429: exponential backoff with **jitter** (`1, 2, 4, 8, 16` s); log throttling to tune caching. Bursts at deployment → stagger startups or use a shared cache.

| Rotation | Cache approach |
|---|---|
| Daily or weekly | 5–15 min TTL + SecretNewVersionCreated |
| Monthly or quarterly | 30–60 min TTL |
| Annual or static | Startup preload + refresh every few hours |

> [!WARNING]
> **Exam traps**
>
> - 4,000 GETs per vault per 10 seconds.
> - A shared cache adds another place that holds secrets.

## Check yourself

- **Practice questions:** [lp8m1 on GitHub](../../practice/lp8m1.md), or [on the site](https://aryantripathi.dev/ai-200/lp-8/manage-app-secrets-key-vault) with hints and saved progress
- **Cheat sheet:** [Learning path 8](../cheatsheets/lp8.md)
- **Microsoft Learn exercise:** [Manage secrets with Azure Key Vault](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/6-exercise-manage-secrets)
- **Hands-on lab:** [labs/](../../labs/README.md) has a lab for this learning path

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
