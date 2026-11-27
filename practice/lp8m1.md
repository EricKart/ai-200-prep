# Practice: LP8 · M1 Manage application secrets with Azure Key Vault

> 25 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp8m1.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-8/manage-app-secrets-key-vault)

## 1. `lp8m1-001`

A RAG API's managed identity needs to read an Azure OpenAI key from Key Vault at runtime, and nothing else. Which role should it get?

- **A.** Key Vault Reader
- **B.** Key Vault Contributor
- **C.** Key Vault Secrets Officer
- **D.** Key Vault Secrets User

<details><summary>💡 Hint</summary>

Read secret values and nothing else: the narrowest data-plane secrets role.

</details>

<details><summary>✅ Answer</summary>

**D.** Key Vault Secrets User

- A: Reader sees metadata but not secret values.
- B: Contributor is control plane only and can't read secrets.
- C: Officer can create and delete secrets, more than needed.
- D: Correct. Read-only access to secret values for application identities.

Least privilege: apps read with Secrets User; pipelines manage with Secrets Officer.

📘 Source: [Store and organize secrets, keys, and certificates](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/2-store-organize-secrets)

</details>

## 2. `lp8m1-002`

What is the maximum size of a Key Vault secret value?

- **A.** 1 MB
- **B.** 25 KB
- **C.** 256 KB
- **D.** 4 KB

<details><summary>💡 Hint</summary>

Key Vault secrets have a fixed size limit in kilobytes.

</details>

<details><summary>✅ Answer</summary>

**B.** 25 KB

- A: Learn gives a smaller limit.
- B: Correct. Secrets store strings up to 25 KB.
- C: 256 KB is the Service Bus Standard message limit.
- D: Learn gives a larger limit.

Secrets are opaque strings up to 25 KB with an optional content_type.

📘 Source: [Store and organize secrets, keys, and certificates](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/2-store-organize-secrets)

</details>

## 3. `lp8m1-003`

Compliance requires that encryption keys be protected by FIPS 140-3 Level 3 hardware security modules. Which tier do you need?

- **A.** Standard
- **B.** Free
- **C.** Premium
- **D.** Basic

<details><summary>💡 Hint</summary>

FIPS 140-3 Level 3 means hardware security modules.

</details>

<details><summary>✅ Answer</summary>

**C.** Premium

- A: Standard uses software protection validated to FIPS 140 Level 1.
- B: Learn describes Standard and Premium only.
- C: Correct. Premium protects keys in FIPS 140-3 Level 3 HSMs.
- D: Learn describes Standard and Premium only.

Choose Premium when regulations mandate HSM-protected keys.

📘 Source: [Store and organize secrets, keys, and certificates](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/2-store-organize-secrets)

</details>

## 4. `lp8m1-004`

A pipeline must encrypt training data and sign model artifacts without the key material ever leaving the vault. Which object type should you use?

- **A.** Secrets
- **B.** Keys
- **C.** Certificates
- **D.** Tags

<details><summary>💡 Hint</summary>

Encrypting and signing inside the vault uses one object type.

</details>

<details><summary>✅ Answer</summary>

**B.** Keys

- A: Secrets return their value to the caller.
- B: Correct. Keys perform cryptographic operations server-side.
- C: Certificates manage X.509 lifecycles; the need here is raw crypto operations.
- D: Tags are metadata, not credentials.

Secrets for strings, keys for cryptography, certificates for TLS.

📘 Source: [Store and organize secrets, keys, and certificates](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/2-store-organize-secrets)

</details>

## 5. `lp8m1-005`

For each statement, select Yes if the statement is true. Otherwise, select No. A production vault is created with default settings.

| Statement | Yes / No |
|---|---|
| Soft delete can be turned off later to save storage. | ☐ |
| The soft-delete retention period can be shortened after creation. | ☐ |
| Purge protection is enabled automatically. | ☐ |
| A deleted secret can be recovered within the retention period. | ☐ |

<details><summary>💡 Hint</summary>

Soft delete is on and can't be turned off. Purge protection is optional.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Soft delete can be turned off later to save storage. | No | Soft delete is on by default and can't be disabled. |
| The soft-delete retention period can be shortened after creation. | No | Retention is set at creation and can't be changed. |
| Purge protection is enabled automatically. | No | Purge protection is optional; consider enabling it on production vaults. |
| A deleted secret can be recovered within the retention period. | Yes | Soft-deleted objects are recoverable during retention. |

Soft delete (7–90 days, default 90) plus optional purge protection.

📘 Source: [Store and organize secrets, keys, and certificates](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/2-store-organize-secrets)

</details>

## 6. `lp8m1-006`

A vault was accidentally deleted and then recovered from soft delete. Apps now get authorization errors, and rotation events stopped. Why?

- **A.** Recovered vaults start with purge protection disabled
- **B.** Secrets are given new names after a vault recovery
- **C.** Recovery restores keys but leaves the secrets out
- **D.** Role assignments and Event Grid subscriptions aren't restored

<details><summary>💡 Hint</summary>

Recovering a vault doesn't bring back everything that pointed at it.

</details>

<details><summary>✅ Answer</summary>

**D.** Role assignments and Event Grid subscriptions aren't restored

- A: Purge protection isn't the cause of these errors.
- B: Names don't change.
- C: Recovery restores the vault's objects.
- D: Correct. They're deleted with the vault and must be recreated manually.

After recovering a vault, recreate its role assignments and Event Grid subscriptions.

📘 Source: [Store and organize secrets, keys, and certificates](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/2-store-organize-secrets)

</details>

## 7. `lp8m1-007`

A platform engineer has Key Vault Contributor on a vault and can create and update it, but gets authorization errors when reading a secret value. Why?

- **A.** The vault must be on the Premium tier for users to read secrets
- **B.** Contributor is a control-plane role with no data-plane access
- **C.** Secrets are readable by managed identities, not by user accounts
- **D.** Contributor can read secrets only after soft delete is turned off

<details><summary>💡 Hint</summary>

Azure separates managing a resource from using the data inside it.

</details>

<details><summary>✅ Answer</summary>

**B.** Contributor is a control-plane role with no data-plane access

- A: Tier controls key protection. It doesn't decide who can read secrets.
- B: Correct. Managing the vault resource and reading its secrets are separate permissions.
- C: Users and pipelines can read secrets with the right data-plane role.
- D: Soft delete can't be turned off, and it isn't related to read access.

Key Vault Contributor is a control-plane role: it manages the vault resource but doesn't grant data-plane operations such as reading secrets. Use data-plane roles such as Key Vault Secrets User or Secrets Officer.

📘 Source: [Store and organize secrets, keys, and certificates](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/2-store-organize-secrets)

</details>

## 8. `lp8m1-008`

A monitoring tool must check which secrets exist in a vault and read their properties, such as expiry dates, but must never see secret values. Which role fits?

- **A.** Key Vault Secrets Officer
- **B.** Key Vault Secrets User
- **C.** Key Vault Reader
- **D.** Key Vault Administrator

<details><summary>💡 Hint</summary>

You want names and properties, but no values.

</details>

<details><summary>✅ Answer</summary>

**C.** Key Vault Reader

- A: Secrets Officer can create, update and delete secrets, which is far more than needed.
- B: Secrets User can read secret values, which this tool must not do.
- C: Correct. It grants read access to vault metadata, such as secret names and properties, without revealing values.
- D: Administrator grants all data-plane operations on keys, secrets and certificates.

Key Vault Reader reads vault metadata (names, properties) without values. Secrets User reads values; Secrets Officer manages secrets; Administrator has all data-plane operations; Contributor is control-plane only.

📘 Source: [Store and organize secrets, keys, and certificates](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/2-store-organize-secrets)

</details>

## 9. `lp8m1-009`

A CI/CD pipeline creates, updates and deletes secrets as part of credential rotation. Which built-in role should its identity get?

- **A.** Key Vault Contributor
- **B.** Key Vault Reader
- **C.** Key Vault Secrets User
- **D.** Key Vault Secrets Officer

<details><summary>💡 Hint</summary>

The pipeline manages the lifecycle of secrets, not the vault itself.

</details>

<details><summary>✅ Answer</summary>

**D.** Key Vault Secrets Officer

- A: Contributor manages the vault resource, not the secrets inside it.
- B: Reader sees metadata only.
- C: Secrets User is read-only, so the pipeline couldn't create new versions.
- D: Correct. It grants full management of secrets for operators and pipelines that manage the secret lifecycle.

Assign Key Vault Secrets Officer to operators or CI/CD pipelines responsible for secret lifecycle; Key Vault Secrets User to apps that only read credentials.

📘 Source: [Store and organize secrets, keys, and certificates](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/2-store-organize-secrets)

</details>

## 10. `lp8m1-010`

At startup, a service must confirm that five required secrets exist without reading their values. Which method should it call?

- **A.** get_secret() for each name
- **B.** list_properties_of_secret_versions()
- **C.** list_properties_of_secrets()
- **D.** set_secret() with empty values

<details><summary>💡 Hint</summary>

One method lists secrets and their properties without returning values.

</details>

<details><summary>✅ Answer</summary>

**C.** list_properties_of_secrets()

- A: That retrieves the values themselves.
- B: That lists versions of one secret.
- C: Correct. It returns metadata such as name and enabled status, not values.
- D: Writing secrets would overwrite them.

Validate configuration early by listing secret properties.

📘 Source: [Retrieve secrets using Azure SDK client libraries](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/3-retrieve-secrets-sdk)

</details>

## 11. `lp8m1-011`

Which URL format does a SecretClient use for a vault named kv-ragpipeline-prod?

- **A.** https://kv-ragpipeline-prod.vault.azure.net/
- **B.** https://vault.azure.net/kv-ragpipeline-prod
- **C.** https://kv-ragpipeline-prod.azurewebsites.net/vault
- **D.** https://kv-ragpipeline-prod.keyvault.windows.net/

<details><summary>💡 Hint</summary>

Each vault has its own DNS name under vault.azure.net.

</details>

<details><summary>✅ Answer</summary>

**A.** https://kv-ragpipeline-prod.vault.azure.net/

- A: Correct. Vault URLs follow https://<vault-name>.vault.azure.net/.
- B: The vault name is a subdomain, not a path.
- C: That's an App Service domain.
- D: That isn't the Key Vault domain.

Find it on the vault's overview page or with az keyvault show --query properties.vaultUri.

📘 Source: [Retrieve secrets using Azure SDK client libraries](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/3-retrieve-secrets-sdk)

</details>

## 12. `lp8m1-012`

Match each exception to the right response.

Choices: **Fix the configuration; don't retry** · **Check the identity's RBAC role** · **Retry; it may be transient**

- ResourceNotFoundError for openai-api-key
- HttpResponseError: the caller isn't authorized
- ServiceRequestError: DNS timeout

<details><summary>💡 Hint</summary>

Missing secret, missing permission, or a network problem: each needs a different response.

</details>

<details><summary>✅ Answer</summary>

- ResourceNotFoundError for openai-api-key → **Fix the configuration; don't retry**. The secret name doesn't exist in the vault.
- HttpResponseError: the caller isn't authorized → **Check the identity's RBAC role**. HttpResponseError covers authentication and authorization failures.
- ServiceRequestError: DNS timeout → **Retry; it may be transient**. Network-level problems may resolve on retry.

Distinguish configuration errors from transient network failures.

📘 Source: [Retrieve secrets using Azure SDK client libraries](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/3-retrieve-secrets-sdk)

</details>

## 13. `lp8m1-013`

For each statement, select Yes if the statement is true. Otherwise, select No. A FastAPI service on Container Apps uses DefaultAzureCredential with a SecretClient.

| Statement | Yes / No |
|---|---|
| In Azure, ManagedIdentityCredential authenticates the app without stored credentials. | ☐ |
| The service should create a new SecretClient for every request. | ☐ |
| It's fine to log secret.value for debugging. | ☐ |

<details><summary>💡 Hint</summary>

Managed identity in Azure. Reuse the client. Never log values.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| In Azure, ManagedIdentityCredential authenticates the app without stored credentials. | Yes | Managed identity is the recommended method on Azure compute. |
| The service should create a new SecretClient for every request. | No | Create it once at startup and reuse it. |
| It's fine to log secret.value for debugging. | No | Log the name and version, not the value. |

One reusable client, managed identity, no secret values in logs.

📘 Source: [Retrieve secrets using Azure SDK client libraries](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/3-retrieve-secrets-sdk)

</details>

## 14. `lp8m1-014`

On a developer laptop, AZURE_CLIENT_ID, AZURE_TENANT_ID and AZURE_CLIENT_SECRET are set from an old test, and the developer is also signed in with az login. Which credential does DefaultAzureCredential use first?

- **A.** EnvironmentCredential (variables)
- **B.** AzureCliCredential (from az login)
- **C.** ManagedIdentityCredential (identity)
- **D.** AzurePowerShellCredential (session)

<details><summary>💡 Hint</summary>

DefaultAzureCredential tries credentials in a fixed order. Environment variables come early.

</details>

<details><summary>✅ Answer</summary>

**A.** EnvironmentCredential (variables)

- A: Correct. EnvironmentCredential is first in the chain and wins if the variables are set.
- B: Azure CLI comes later in the chain.
- C: There's no managed identity on a laptop, and it comes after Environment.
- D: PowerShell is last.

The chain tries Environment, Workload Identity, Managed Identity, then CLI, azd and PowerShell.

📘 Source: [Retrieve secrets using Azure SDK client libraries](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/3-retrieve-secrets-sdk)

</details>

## 15. `lp8m1-015`

A FastAPI app uses the async SecretClient with an async DefaultAzureCredential. During shutdown, the logs warn about unclosed sessions. What does Learn recommend?

- **A.** Ignore the warning, because Python closes sessions on exit
- **B.** Switch to the synchronous client, which never needs closing
- **C.** Close both the client and the credential, for example with async with or await close()
- **D.** Create a new client per request so that nothing stays open

<details><summary>💡 Hint</summary>

Both async objects hold network resources that need to be released.

</details>

<details><summary>✅ Answer</summary>

**C.** Close both the client and the credential, for example with async with or await close()

- A: Unclosed sessions can leak resources. Close them explicitly.
- B: Learn's guidance for async apps is to close the async client and credential.
- C: Correct. Both are async context managers that should be closed when you're done.
- D: Reusing one client is the recommendation. Per-request clients add overhead.

The async SecretClient and credential are async context managers. Use async with, or call await client.close() and await credential.close(), for example in the app's shutdown hook.

📘 Source: [Retrieve secrets using Azure SDK client libraries](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/3-retrieve-secrets-sdk)

</details>

## 16. `lp8m1-016`

How many days before a secret's expiration does the SecretNearExpiry event fire?

- **A.** 30
- **B.** 7
- **C.** 60
- **D.** 90

<details><summary>💡 Hint</summary>

Key Vault gives a warning window before a secret expires.

</details>

<details><summary>✅ Answer</summary>

**A.** 30

- A: Correct. It fires thirty days before expiration.
- B: Learn gives a longer window.
- C: Learn gives 30.
- D: 90 is a typical expiry length, not the warning window.

Combine a 90-day expiry with SecretNearExpiry for a 30-day rotation window.

📘 Source: [Handle secret versioning and rotation](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/4-handle-versioning-rotation)

</details>

## 17. `lp8m1-017`

For each statement, select Yes if the statement is true. Otherwise, select No. A secret named cosmosdb-connection-string has an expires_on date that passed yesterday.

| Statement | Yes / No |
|---|---|
| get_secret() now fails because the secret expired. | ☐ |
| Calling set_secret() with the same name overwrites the old value in place. | ☐ |
| get_secret() without a version returns the latest enabled version. | ☐ |
| Disabling an old version stops apps retrieving it, even by version ID. | ☐ |

<details><summary>💡 Hint</summary>

Expiry doesn't stop reads. Writing the same name creates a new version.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| get_secret() now fails because the secret expired. | No | Expiration is informational; expired secrets can still be retrieved. |
| Calling set_secret() with the same name overwrites the old value in place. | No | It creates a new version. |
| get_secret() without a version returns the latest enabled version. | Yes | The default is the latest enabled version. |
| Disabling an old version stops apps retrieving it, even by version ID. | Yes | enabled=False prevents retrieval of that version. |

Versions accumulate; expiry signals staleness but doesn't block reads.

📘 Source: [Handle secret versioning and rotation](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/4-handle-versioning-rotation)

</details>

## 18. `lp8m1-018`

Rotate a Cosmos DB key with the dual-credential approach. Put the steps in order.

- Generate a new secondary key on the service
- Regenerate the old primary key on the service
- Store the new key as a new secret version in Key Vault
- Wait until every app instance uses the new value

<details><summary>💡 Hint</summary>

Two keys: switch to the new one everywhere before regenerating the old one.

</details>

<details><summary>✅ Answer</summary>

1. Generate a new secondary key on the service
2. Store the new key as a new secret version in Key Vault
3. Wait until every app instance uses the new value
4. Regenerate the old primary key on the service

At least one valid credential exists throughout the rotation.

📘 Source: [Handle secret versioning and rotation](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/4-handle-versioning-rotation)

</details>

## 19. `lp8m1-019`

After a key rotation, some instances still use the old key and get 401s from the downstream service. What does Learn recommend in application code?

- **A.** Call get_secret() before each downstream request
- **B.** Pin the secret version in the app configuration
- **C.** Restart the app instances on a schedule
- **D.** On auth failure, refetch the secret and retry

<details><summary>💡 Hint</summary>

When the downstream service rejects the key, try the latest secret once more.

</details>

<details><summary>✅ Answer</summary>

**D.** On auth failure, refetch the secret and retry

- A: That floods Key Vault and risks throttling.
- B: Pinning prevents picking up the rotated version.
- C: Restarts don't target the failure and still leave gaps.
- D: Correct. One extra Key Vault call only when the credential is rejected.

Retry-on-auth-failure gives zero-downtime rotation without coordination.

📘 Source: [Handle secret versioning and rotation](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/4-handle-versioning-rotation)

</details>

## 20. `lp8m1-020`

You want rotation without human steps for an API key that expires every 90 days. What should you set up?

- **A.** Purge protection with a 30-day retention period
- **B.** A monthly calendar reminder for the operations team
- **C.** SecretNearExpiry → Function → new version
- **D.** A second vault that mirrors the first one's secrets

<details><summary>💡 Hint</summary>

An expiry event can start code that creates the new version.

</details>

<details><summary>✅ Answer</summary>

**C.** SecretNearExpiry → Function → new version

- A: Purge protection prevents deletion; it doesn't rotate.
- B: That's manual rotation.
- C: Correct. The handler generates the credential and stores it as a new version.
- D: Mirroring doesn't rotate anything.

Automated rotation: SecretNearExpiry → Event Grid → Function → new secret version.

📘 Source: [Handle secret versioning and rotation](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/4-handle-versioning-rotation)

</details>

## 21. `lp8m1-021`

All app instances now use the newly rotated database credential. You want to make sure nothing can keep using the previous version. What does Learn suggest?

- **A.** Purge the old version from soft delete
- **B.** Set a new tag on the secret named version=old
- **C.** Disable the previous version with update_secret_properties(enabled=False)
- **D.** Delete the whole secret and recreate it

<details><summary>💡 Hint</summary>

Old versions stay readable until you change one of their properties.

</details>

<details><summary>✅ Answer</summary>

**C.** Disable the previous version with update_secret_properties(enabled=False)

- A: Versions aren't purged individually. You disable them.
- B: Tags are metadata, so they don't stop anyone reading a version.
- C: Correct. A disabled version can't be retrieved, which enforces use of the new credential.
- D: That removes every version, including the current one, and breaks the apps.

After a successful rotation, consider disabling previous versions with update_secret_properties(..., enabled=False) so no instance can keep using the old credential. list_properties_of_secret_versions() helps audit versions.

📘 Source: [Handle secret versioning and rotation](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/4-handle-versioning-rotation)

</details>

## 22. `lp8m1-022`

An inference API calls get_secret() on every request and starts receiving HTTP 429 during spikes. What's the main fix?

- **A.** Cache the secret in memory with a TTL
- **B.** Move the vault to the Premium tier
- **C.** Retry each 429 immediately without delay
- **D.** Create a new SecretClient per request

<details><summary>💡 Hint</summary>

Calling the vault on every request causes throttling. Keep secrets for a short while.

</details>

<details><summary>✅ Answer</summary>

**A.** Cache the secret in memory with a TTL

- A: Correct. Caching turns thousands of vault calls into a few refreshes.
- B: Tier doesn't raise these throttling limits.
- C: Retry with exponential backoff and jitter; immediate retries make it worse.
- D: New clients add overhead and don't reduce calls.

Key Vault allows up to 4,000 GETs per vault per 10 seconds.

📘 Source: [Implement caching strategies to reduce Key Vault calls](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/5-implement-caching-strategies)

</details>

## 23. `lp8m1-023`

Which Key Vault event should an app subscribe to so it can invalidate its cache as soon as a secret is rotated?

- **A.** SecretExpired (after expiry)
- **B.** SecretNearExpiry (30 days out)
- **C.** SecretNewVersionCreated
- **D.** Microsoft.Storage.BlobCreated

<details><summary>💡 Hint</summary>

A new version means rotation. Which event announces it?

</details>

<details><summary>✅ Answer</summary>

**C.** SecretNewVersionCreated

- A: That fires after expiry passes.
- B: That fires 30 days before expiry, used to trigger rotation.
- C: Correct. It fires when a new secret version is stored.
- D: That's a Blob Storage event.

Combine event-driven invalidation with a time-based fallback.

📘 Source: [Implement caching strategies to reduce Key Vault calls](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/5-implement-caching-strategies)

</details>

## 24. `lp8m1-024`

An API key rotates every week, and the team needs fresh credentials soon after rotation. Which cache setup fits Learn's guidance?

- **A.** No cache; call Key Vault on each request
- **B.** 5–15 minute TTL plus Event Grid
- **C.** A 30–60 minute TTL without events
- **D.** Startup preload refreshed every few hours

<details><summary>💡 Hint</summary>

A short TTL, with events to invalidate early.

</details>

<details><summary>✅ Answer</summary>

**B.** 5–15 minute TTL plus Event Grid

- A: Uncached reads risk throttling.
- B: Correct. High-rotation secrets need short TTLs and Event Grid.
- C: That's for monthly or quarterly rotation.
- D: That's for annual or static secrets.

Match cache lifetime to rotation frequency and revocation risk.

📘 Source: [Implement caching strategies to reduce Key Vault calls](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/5-implement-caching-strategies)

</details>

## 25. `lp8m1-025`

For each statement, select Yes if the statement is true. Otherwise, select No. A team considers caching secrets in a shared Azure Managed Redis instance for 50 replicas.

| Statement | Yes / No |
|---|---|
| It can cut Key Vault calls to one per refresh cycle regardless of replica count. | ☐ |
| It adds no new security considerations, because Redis is inside Azure. | ☐ |
| Per-process caching makes Key Vault calls independent of the number of instances. | ☐ |
| Retrying 429s should use exponential backoff with random jitter. | ☐ |

<details><summary>💡 Hint</summary>

A shared cache cuts calls but adds its own risks.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| It can cut Key Vault calls to one per refresh cycle regardless of replica count. | Yes | One process fetches; others read the shared cache. |
| It adds no new security considerations, because Redis is inside Azure. | No | Secrets now live in another place needing access control and encryption. |
| Per-process caching makes Key Vault calls independent of the number of instances. | No | Per-process calls scale linearly with instances; a shared cache makes them independent. |
| Retrying 429s should use exponential backoff with random jitter. | Yes | Jitter avoids a thundering herd. |

Shared caches reduce calls but add complexity and exposure.

📘 Source: [Implement caching strategies to reduce Key Vault calls](https://learn.microsoft.com/en-us/training/modules/manage-app-secrets-key-vault/5-implement-caching-strategies)

</details>


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
