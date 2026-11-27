# Practice: LP8 · M2 Manage application settings with Azure App Configuration

> 26 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp8m2.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-8/manage-app-settings-app-config)

## 1. `lp8m2-001`

An app's managed identity only needs to read settings and feature flags from App Configuration. Which role should it get?

- **A.** Key Vault Secrets User on a vault
- **B.** App Configuration Data Owner
- **C.** App Configuration Data Reader
- **D.** Contributor on the resource group

<details><summary>💡 Hint</summary>

Reading settings and flags only: the read-only data role.

</details>

<details><summary>✅ Answer</summary>

**C.** App Configuration Data Reader

- A: That's for Key Vault secrets.
- B: Data Owner is for operators and pipelines that change settings.
- C: Correct. Read-only access to key-values, feature flags and Key Vault references.
- D: Contributor manages the resource, not least-privilege data reads.

Readers for apps, Owners for operators.

📘 Source: [Connect to App Configuration from application code](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/2-connect-app-configuration)

</details>

## 2. `lp8m2-002`

What is the endpoint format for an App Configuration store named docpipe-config?

- **A.** `https://docpipe-config.azconfig.io`
- **B.** `https://docpipe-config.config.azure.com`
- **C.** `https://docpipe-config.vault.azure.net`
- **D.** `https://docpipe-config.azurewebsites.net`

<details><summary>💡 Hint</summary>

App Configuration endpoints use their own domain.

</details>

<details><summary>✅ Answer</summary>

**A.** `https://docpipe-config.azconfig.io`

- A: Correct. Stores use `https://<store-name>.azconfig.io`.
- B: That isn't the App Configuration domain.
- C: That's a Key Vault URL.
- D: That's App Service.

Pass the endpoint and a credential to load().

📘 Source: [Connect to App Configuration from application code](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/2-connect-app-configuration)

</details>

## 3. `lp8m2-003`

For each statement, select Yes if the statement is true. Otherwise, select No. An app calls `load(endpoint=…, credential=DefaultAzureCredential())` with no selectors.

| Statement | Yes / No |
|---|---|
| It loads keys labelled Production as well as unlabelled keys. | ☐ |
| Keys are case-insensitive, so openai:endpoint matches OpenAI:Endpoint. | ☐ |
| A key plus its value can be up to 10 KB. | ☐ |
| The returned object can be used like a Python dictionary. | ☐ |

<details><summary>💡 Hint</summary>

No selector means null-label keys only. Keys are case-sensitive. There's a size limit.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| It loads keys labelled Production as well as unlabelled keys. | No | Without a selector, only null-label keys load. |
| Keys are case-insensitive, so openai:endpoint matches OpenAI:Endpoint. | No | Keys are case-sensitive. |
| A key plus its value can be up to 10 KB. | Yes | That's the combined size limit. |
| The returned object can be used like a Python dictionary. | Yes | load() returns a dictionary-like Mapping. |

Use SettingSelector to choose keys and labels.

📘 Source: [Connect to App Configuration from application code](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/2-connect-app-configuration)

</details>

## 4. `lp8m2-004`

Several apps share one store, and this app's keys all start with DocPipeline:. The code should use short names like OpenAI:Endpoint. What should you use?

- **A.** A separate App Configuration store for each key
- **B.** A `label_filter` set to the value `DocPipeline`
- **C.** Tags named `DocPipeline` on every one of the keys
- **D.** `key_filter` `DocPipeline:*` plus `trim_prefixes`

<details><summary>💡 Hint</summary>

Filter on the app's prefix, then remove it from the names the code sees.

</details>

<details><summary>✅ Answer</summary>

**D.** `key_filter` `DocPipeline:*` plus `trim_prefixes`

- A: A store per key isn't how prefixes are handled.
- B: Labels are variants, not key prefixes.
- C: Tags don't shorten key names.
- D: Correct. Filter by prefix, then trim it for cleaner names.

key_filter narrows what loads; trim_prefixes simplifies names.

📘 Source: [Connect to App Configuration from application code](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/2-connect-app-configuration)

</details>

## 5. `lp8m2-005`

An operator updates three model settings and wants running apps to pick up all three together, not one at a time. What's the pattern?

- **A.** Add a label called Refresh to the three keys
- **B.** Set refresh_interval to 0 so every key refreshes instantly
- **C.** Restart each app instance after every single change
- **D.** Change the settings, then the Sentinel key

<details><summary>💡 Hint</summary>

Change the settings, then touch one key that tells apps to reload.

</details>

<details><summary>✅ Answer</summary>

**D.** Change the settings, then the Sentinel key

- A: Labels don't trigger refresh.
- B: The provider still needs refresh() calls and a watched key; per-key instant refresh isn't the pattern.
- C: Restarts aren't needed with dynamic refresh.
- D: Correct. A sentinel change triggers a reload of the whole configuration for consistency.

Sentinel key + refresh_on + refresh(): changes take effect together.

📘 Source: [Connect to App Configuration from application code](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/2-connect-app-configuration)

</details>

## 6. `lp8m2-006`

Dynamic refresh is configured with refresh_interval=60, but the app never sees updated values. The code only calls load() at startup. What's missing?

- **A.** Calls to config.refresh() in the app
- **B.** The App Configuration Data Owner role
- **C.** A second load() call every 60 seconds
- **D.** A label_filter set to the null label

<details><summary>💡 Hint</summary>

Refresh doesn't happen by itself. The app must ask for it.

</details>

<details><summary>✅ Answer</summary>

**A.** Calls to config.refresh() in the app

- A: Correct. The provider's refresh() must be called explicitly.
- B: Reading doesn't need Data Owner.
- C: Reloading by hand isn't the provider's refresh mechanism.
- D: Labels aren't the issue.

refresh() checks the watch keys if the interval has elapsed; otherwise it returns immediately.

📘 Source: [Connect to App Configuration from application code](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/2-connect-app-configuration)

</details>

## 7. `lp8m2-007`

A setting Pipeline:Stages holds a JSON array, but the app receives it as a plain string and has to parse it by hand. What should you set on the key-value?

- **A.** Content type application/json
- **B.** A key name ending in .json
- **C.** A label named json
- **D.** A tag type=json

<details><summary>💡 Hint</summary>

One optional property tells the provider how to interpret the value.

</details>

<details><summary>✅ Answer</summary>

**A.** Content type application/json

- A: Correct. The provider then parses the value as a JSON object.
- B: The key's name doesn't tell the provider how to parse the value.
- C: Labels create variants of a key. They don't change how the value is parsed.
- D: Tags are metadata for filtering. They don't affect parsing.

Each setting has a key, value, optional label, optional content type and tags. Setting content type to application/json tells the provider to parse the value as a JSON object.

📘 Source: [Connect to App Configuration from application code](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/2-connect-app-configuration)

</details>

## 8. `lp8m2-008`

An app connects to App Configuration with a connection string stored in an environment variable. Security wants no connection strings at all. What should the app use?

- **A.** Its managed identity with the App Configuration Data Reader role
- **B.** The store's access key in local.settings.json
- **C.** Anonymous access with an IP allow list
- **D.** A connection string stored in Key Vault instead

<details><summary>💡 Hint</summary>

Remove the secret entirely by authenticating as the app itself.

</details>

<details><summary>✅ Answer</summary>

**A.** Its managed identity with the App Configuration Data Reader role

- A: Correct. A managed identity removes the connection string and its rotation burden.
- B: That's another shared secret, not an identity.
- C: App Configuration isn't meant for anonymous access, and IPs aren't identities.
- D: That still uses a connection string that grants full access to the store.

Managed identities remove connection strings from configuration. The app identity needs App Configuration Data Reader to read key-values, feature flags and Key Vault references.

📘 Source: [Connect to App Configuration from application code](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/2-connect-app-configuration)

</details>

## 9. `lp8m2-009`

A new document classification stage starts producing wrong labels in production. What lets operators turn it off in seconds without redeploying?

- **A.** A new label on the Pipeline:BatchSize key
- **B.** A feature flag used as a kill switch
- **C.** A Key Vault reference for the stage
- **D.** A code rollback through the pipeline

<details><summary>💡 Hint</summary>

Turning something off in seconds without a deployment.

</details>

<details><summary>✅ Answer</summary>

**B.** A feature flag used as a kill switch

- A: Labels vary values per environment, not stage on/off.
- B: Correct. Disable the flag and the pipeline skips the stage.
- C: Key Vault references point to secrets.
- D: Rollbacks take minutes or hours.

Feature flags decouple feature lifecycle from deployment.

📘 Source: [Organize settings with labels and feature flags](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/3-organize-labels-feature-flags)

</details>

## 10. `lp8m2-010`

Defaults are stored with no label and production overrides with the Production label. In which order should the SettingSelectors be passed?

- **A.** Production alone, with no defaults
- **B.** Production first, then null label
- **C.** Null label first, then Production
- **D.** The null label alone, with a Production tag

<details><summary>💡 Hint</summary>

Later selectors override earlier ones, so defaults go first.

</details>

<details><summary>✅ Answer</summary>

**C.** Null label first, then Production

- A: Keys without overrides would be missing.
- B: Defaults would then override production values.
- C: Correct. Later selectors override earlier ones, so overrides go last.
- D: Tags don't select labels.

Stack defaults, then environment-specific overrides.

📘 Source: [Organize settings with labels and feature flags](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/3-organize-labels-feature-flags)

</details>

## 11. `lp8m2-011`

For each statement, select Yes if the statement is true. Otherwise, select No. An app loads settings with `feature_flag_enabled=True` and `feature_flag_refresh_enabled=True`.

| Statement | Yes / No |
|---|---|
| Changing a feature flag also triggers a refresh of regular settings. | ☐ |
| FeatureManager comes with the provider package, with no extra install. | ☐ |
| is_enabled("UseNewEmbeddingsModel") returns a boolean for the flag's state. | ☐ |

<details><summary>💡 Hint</summary>

Flag refresh and setting refresh are separate. FeatureManager is a separate package.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Changing a feature flag also triggers a refresh of regular settings. | No | The two refreshes are independent. |
| FeatureManager comes with the provider package, with no extra install. | No | Install featuremanagement separately. |
| is_enabled("UseNewEmbeddingsModel") returns a boolean for the flag's state. | Yes | FeatureManager evaluates flags at runtime. |

Flags and settings refresh independently when refresh() is called.

📘 Source: [Organize settings with labels and feature flags](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/3-organize-labels-feature-flags)

</details>

## 12. `lp8m2-012`

How does App Configuration store feature flags internally?

- **A.** In a separate store that FeatureManager alone reads
- **B.** Keys prefixed .appconfig.featureflag/
- **C.** As labels named Enabled and Disabled on keys
- **D.** As Key Vault secrets with a FeatureFlag tag

<details><summary>💡 Hint</summary>

Feature flags are stored as ordinary key-values under a reserved prefix.

</details>

<details><summary>✅ Answer</summary>

**B.** Keys prefixed .appconfig.featureflag/

- A: Flags live in the same store.
- B: Correct. The libraries hide these details behind simple flag names.
- C: Labels are environment variants, not flag states.
- D: Flags aren't Key Vault secrets.

Prefix .appconfig.featureflag/ with content type application/vnd.microsoft.appconfig.ff+json.

📘 Source: [Organize settings with labels and feature flags](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/3-organize-labels-feature-flags)

</details>

## 13. `lp8m2-013`

Which two scenarios does Learn list as feature flag patterns for AI apps? (Select two.)

- **A.** Progressive rollout of a new embeddings model
- **B.** Rotating a Cosmos DB connection string
- **C.** Storing the Azure OpenAI API key
- **D.** Staged activation of pipeline stages

<details><summary>💡 Hint</summary>

Learn lists a set of flag patterns for AI apps. Two of these match it.

</details>

<details><summary>✅ Answer</summary>

**A.** Progressive rollout of a new embeddings model  
**D.** Staged activation of pipeline stages

- A: Correct. Gate the new model's code path before full rollout.
- B: Rotation is a Key Vault concern.
- C: Secrets belong in Key Vault.
- D: Correct. Enable stages one at a time.

Rollouts, kill switches, A/B tests and staged activation.

📘 Source: [Organize settings with labels and feature flags](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/3-organize-labels-feature-flags)

</details>

## 14. `lp8m2-014`

The team wants to compare the current embedding configuration with an experimental one on live requests, sending some requests down each path. Which feature flag pattern from Learn fits?

- **A.** A sentinel key
- **B.** A/B testing configurations
- **C.** A kill switch
- **D.** Staged pipeline activation

<details><summary>💡 Hint</summary>

Two paths running side by side so that you can compare their results.

</details>

<details><summary>✅ Answer</summary>

**B.** A/B testing configurations

- A: The sentinel key triggers a configuration refresh. It isn't a feature flag pattern.
- B: Correct. Flags can route different requests through different paths so that you can compare results.
- C: A kill switch turns a stage off in an emergency. It doesn't compare two paths.
- D: Staged activation turns stages on one at a time. It doesn't compare configurations.

Learn's feature flag patterns for AI apps: progressive model rollouts, kill switches, A/B testing configurations, and staged pipeline activation.

📘 Source: [Organize settings with labels and feature flags](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/3-organize-labels-feature-flags)

</details>

## 15. `lp8m2-015`

OpenAI:ApiKey is a Key Vault reference. Loading fails with an error naming the vault and secret, although other settings load fine. What's most likely missing?

- **A.** Key Vault Secrets User on that vault
- **B.** A label on the OpenAI:ApiKey key itself
- **C.** App Configuration Data Owner on the store
- **D.** The featuremanagement package installed

<details><summary>💡 Hint</summary>

The reference resolves in Key Vault, so the identity needs a role there too.

</details>

<details><summary>✅ Answer</summary>

**A.** Key Vault Secrets User on that vault

- A: Correct. Store access works, but resolving the reference needs vault access.
- B: Labels don't affect resolution permissions.
- C: Reading settings needs Data Reader, which already works.
- D: Feature management is unrelated.

The identity needs a role on App Configuration and on every referenced vault.

📘 Source: [Reference Key Vault secrets from App Configuration](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/4-reference-key-vault-secrets)

</details>

## 16. `lp8m2-016`

You create a reference with `--secret-identifier https://my-keyvault.vault.azure.net/secrets/openai-api-key` (no version). What happens when the secret rotates?

- **A.** App Configuration copies the new value into the store
- **B.** Nothing; versionless identifiers are pinned to the first version
- **C.** The reference breaks until you update it
- **D.** The app gets the new value on its next load or secret refresh

<details><summary>💡 Hint</summary>

A versionless reference follows rotation.

</details>

<details><summary>✅ Answer</summary>

**D.** The app gets the new value on its next load or secret refresh

- A: App Configuration stores only the pointer.
- B: Versionless means latest, not first.
- C: Versionless references keep working after rotation.
- D: Correct. Omitting the version resolves the latest version.

Omit the version so rotated secrets are picked up automatically.

📘 Source: [Reference Key Vault secrets from App Configuration](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/4-reference-key-vault-secrets)

</details>

## 17. `lp8m2-017`

For each statement, select Yes if the statement is true. Otherwise, select No. An app loads settings with `keyvault_credential=DefaultAzureCredential()` and `secret_refresh_interval=3600`.

| Statement | Yes / No |
|---|---|
| App Configuration stores the actual secret value for OpenAI:ApiKey. | ☐ |
| Application code needs a separate SecretClient to read OpenAI:ApiKey. | ☐ |
| Secrets can be re-resolved hourly while settings are checked more often. | ☐ |
| Secret refresh happens only when the app calls refresh(). | ☐ |

<details><summary>💡 Hint</summary>

App Configuration stores a pointer. The provider resolves it.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| App Configuration stores the actual secret value for OpenAI:ApiKey. | No | It stores only the reference URI. |
| Application code needs a separate SecretClient to read OpenAI:ApiKey. | No | The provider resolves references transparently. |
| Secrets can be re-resolved hourly while settings are checked more often. | Yes | secret_refresh_interval is independent of refresh_interval. |
| Secret refresh happens only when the app calls refresh(). | Yes | The refresh call triggers re-resolution once the interval elapses. |

One load() returns settings and resolved secrets; each has its own refresh cadence.

📘 Source: [Reference Key Vault secrets from App Configuration](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/4-reference-key-vault-secrets)

</details>

## 18. `lp8m2-018`

Production and Development must use different OpenAI API keys stored in different vaults, under the same key name OpenAI:ApiKey. How?

- **A.** Two keys named OpenAI:ApiKey:Prod and OpenAI:ApiKey:Dev in code
- **B.** Store both secret values directly in App Configuration
- **C.** Two labelled references for OpenAI:ApiKey
- **D.** Use tags to choose the vault at runtime

<details><summary>💡 Hint</summary>

Labels create variants of the same key name.

</details>

<details><summary>✅ Answer</summary>

**C.** Two labelled references for OpenAI:ApiKey

- A: Environment-specific key names are what labels avoid.
- B: Secrets shouldn't be stored directly in App Configuration.
- C: Correct. Labels work on references just like other keys.
- D: Tags don't select values at load time.

Label references to point to environment-specific vaults.

📘 Source: [Reference Key Vault secrets from App Configuration](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/4-reference-key-vault-secrets)

</details>

## 19. `lp8m2-019`

A configuration has 80 Key Vault references and secret_refresh_interval of 10 seconds across 30 instances. What should you consider?

- **A.** Total Key Vault requests against its limits
- **B.** Nothing; references are cached by App Configuration
- **C.** App Configuration's 10 KB value limit
- **D.** Moving the references into feature flags

<details><summary>💡 Hint</summary>

Many references, frequent refresh and many instances multiply into Key Vault calls.

</details>

<details><summary>✅ Answer</summary>

**A.** Total Key Vault requests against its limits

- A: Correct. Each resolution is a Key Vault request; choose an interval that fits limits and rotation.
- B: Each resolution generates a request to Key Vault.
- C: The pointer is small; the issue is request volume.
- D: Feature flags aren't for secrets.

Align secret refresh with your rotation schedule and Key Vault limits.

📘 Source: [Reference Key Vault secrets from App Configuration](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/4-reference-key-vault-secrets)

</details>

## 20. `lp8m2-020`

A Key Vault reference was created with --secret-identifier that ends in a version ID. The secret rotates monthly, but the app keeps loading the old value. Why?

- **A.** App Configuration caches secret values for 30 days
- **B.** The app's identity lacks App Configuration Data Owner
- **C.** The reference is pinned to that secret version
- **D.** Key Vault references refresh only when the store is restarted

<details><summary>💡 Hint</summary>

Look at the end of the secret URI.

</details>

<details><summary>✅ Answer</summary>

**C.** The reference is pinned to that secret version

- A: App Configuration stores only the pointer, not the secret value.
- B: Reading references needs Data Reader. A missing role would fail, not return old values.
- C: Correct. Including a version in the URI pins the reference; leave it out to follow rotation.
- D: Stores aren't restarted, and the provider re-resolves versionless references.

--secret-identifier accepts the full URI; appending a version pins the reference to that version. Use a versionless URI so the app gets the new value on its next load or secret refresh.

📘 Source: [Reference Key Vault secrets from App Configuration](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/4-reference-key-vault-secrets)

</details>

## 21. `lp8m2-021`

Settings load, but every Key Vault reference fails to resolve. The app identity has App Configuration Data Reader on the store. What else does it need?

- **A.** Key Vault Secrets User on the referenced vault
- **B.** Key Vault Contributor on the vault
- **C.** Nothing, because App Configuration reads the secret for the app
- **D.** App Configuration Data Owner on the store

<details><summary>💡 Hint</summary>

The secret lives in a different service from the setting.

</details>

<details><summary>✅ Answer</summary>

**A.** Key Vault Secrets User on the referenced vault

- A: Correct. References resolve in Key Vault, so the identity needs permissions on both services.
- B: Contributor is control-plane only, so it can't read secret values.
- C: App Configuration stores only the pointer. The app's identity reads the secret.
- D: Data Owner adds write access to the store. It doesn't grant access to the vault.

For Key Vault references to resolve, the application identity needs permissions on both App Configuration (Data Reader) and Key Vault (Key Vault Secrets User).

📘 Source: [Reference Key Vault secrets from App Configuration](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/4-reference-key-vault-secrets)

</details>

## 22. `lp8m2-022`

Match each setting to where Learn says it belongs.

Choices: **App Configuration value** · **App Configuration feature flag** · **Key Vault via reference**

- Embedding dimensions: 1536
- EnableBatchProcessing on/off
- Storage account access key

<details><summary>💡 Hint</summary>

Ask whether the value grants access or only changes behavior.

</details>

<details><summary>✅ Answer</summary>

- Embedding dimensions: 1536 → **App Configuration value**. Non-sensitive behavior setting.
- EnableBatchProcessing on/off → **App Configuration feature flag**. A runtime toggle.
- Storage account access key → **Key Vault via reference**. Grants access to a resource.

If the value alone grants access, it belongs in Key Vault.

📘 Source: [Decide what to store in App Configuration vs Key Vault](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/5-decide-app-config-vs-key-vault)

</details>

## 23. `lp8m2-023`

For each statement, select Yes if the statement is true. Otherwise, select No. A team reviews its configuration design.

| Statement | Yes / No |
|---|---|
| Storing the Azure OpenAI API key directly as an App Configuration value is fine because the store is encrypted. | ☐ |
| Putting batch sizes in Key Vault is a good way to secure them. | ☐ |
| Keeping a copy of a connection string in both services without a reference can cause drift. | ☐ |

<details><summary>💡 Hint</summary>

Credentials belong in Key Vault, behavior in App Configuration.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Storing the Azure OpenAI API key directly as an App Configuration value is fine because the store is encrypted. | No | Secrets miss Key Vault's per-access audit, rotation and HSM protection. |
| Putting batch sizes in Key Vault is a good way to secure them. | No | Non-sensitive values in Key Vault waste its capabilities and risk throttling. |
| Keeping a copy of a connection string in both services without a reference can cause drift. | Yes | Use a reference so there's one source of truth. |

Each service for its intended purpose, linked by references.

📘 Source: [Decide what to store in App Configuration vs Key Vault](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/5-decide-app-config-vs-key-vault)

</details>

## 24. `lp8m2-024`

Which App Configuration capability lets operators roll back the whole configuration to a known point in time?

- **A.** Key-value snapshots
- **B.** Purge protection
- **C.** Secret versioning
- **D.** Event Grid subscriptions

<details><summary>💡 Hint</summary>

One App Configuration feature captures a whole configuration at a point in time.

</details>

<details><summary>✅ Answer</summary>

**A.** Key-value snapshots

- A: Correct. Snapshots support point-in-time rollback.
- B: Purge protection is a Key Vault feature.
- C: Secret versioning is Key Vault's.
- D: Event Grid delivers events; it doesn't roll back config.

App Configuration: labels, flags, snapshots, dynamic refresh.

📘 Source: [Decide what to store in App Configuration vs Key Vault](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/5-decide-app-config-vs-key-vault)

</details>

## 25. `lp8m2-025`

Compliance requires a record of which identity read each credential and when. Why does this push the credential into Key Vault?

- **A.** App Configuration can't store strings longer than 1 KB
- **B.** Key Vault tracks each access; App Config RBAC is store-level
- **C.** Key Vault values refresh faster than App Configuration
- **D.** App Configuration doesn't support managed identities

<details><summary>💡 Hint</summary>

Which service records each read of each credential?

</details>

<details><summary>✅ Answer</summary>

**B.** Key Vault tracks each access; App Config RBAC is store-level

- A: The limit is 10 KB for key + value, and size isn't the reason.
- B: Correct. Per-object access tracking needs Key Vault.
- C: Refresh speed isn't the criterion.
- D: App Configuration supports managed identity.

Per-access audit, rotation and expiry are Key Vault strengths.

📘 Source: [Decide what to store in App Configuration vs Key Vault](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/5-decide-app-config-vs-key-vault)

</details>

## 26. `lp8m2-026`

Which value belongs in Key Vault rather than App Configuration, according to Learn's placement rule?

- **A.** The model deployment name text-embedding-ada-002
- **B.** A database connection string that contains a password
- **C.** The Azure OpenAI endpoint URL
- **D.** The pipeline's retry count

<details><summary>💡 Hint</summary>

The test is whether the value grants access to a resource.

</details>

<details><summary>✅ Answer</summary>

**B.** A database connection string that contains a password

- A: A deployment name controls behavior without granting access.
- B: Correct. Values that grant access or contain credentials are sensitive and belong in Key Vault.
- C: An endpoint URL alone doesn't grant access, so it's an App Configuration value.
- D: Retry counts control behavior, so they belong in App Configuration.

The key criterion is whether a value grants access or contains credentials. Endpoints, deployment names, dimensions, batch sizes and flags go to App Configuration; API keys and connection strings with credentials go to Key Vault.

📘 Source: [Decide what to store in App Configuration vs Key Vault](https://learn.microsoft.com/en-us/training/modules/manage-app-settings-app-config/5-decide-app-config-vs-key-vault)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
