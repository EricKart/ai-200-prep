# LP8 cheat sheet: Manage application secrets and configuration for AI solutions

> Skill area 4 · one page to review before the exam · full lessons in [content/lessons](../lessons/) · practise at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-8)

## Which one?

| You need… | Answer | Don't confuse with |
|---|---|---|
| App reads a secret value | Key Vault Secrets User | Key Vault Contributor can't read secrets |
| Rotate a key automatically | SecretNearExpiry (30 days) → Function → new version | Expiry doesn't block reads |
| Refresh cache after rotation | SecretNewVersionCreated event | Fixed TTL alone |
| Shared non-secret settings and flags | App Configuration (+ Key Vault references for secrets) | Secrets stored directly in App Configuration |
| Same key, different value per environment | App Configuration labels | Environment-specific key names |
| Turn a pipeline stage off in seconds | Feature flag kill switch | Code rollback |
| Trace ID in Application Insights | operation_Id | cloud_RoleName = service |
| Each service its own Application Map node | service.name (+ service.namespace) | Separate connection strings |
| Exception totals under sampling | sum(itemCount) | count() undercounts |
| Interactive investigation with filters | Workbook with parameters | Dashboards are at-a-glance |
| Alert on p95 latency per service | Log search alert | Smart detection learns baselines |

## Must remember

### M1: Manage application secrets with Azure Key Vault

- Key Vault Contributor can't read secrets.
- Soft-delete retention is fixed at creation.
- Tags are visible to anyone who can list secrets.
- Listing returns properties, never values.
- Don't retry ResourceNotFoundError; fix the configuration.
- Expired secrets are still retrievable; expiry doesn't block access.
- SecretNearExpiry fires 30 days before expiry.
- 4,000 GETs per vault per 10 seconds.
- A shared cache adds another place that holds secrets.

Lesson: [lp8m1](../lessons/lp8m1.md) · Practice: [lp8m1](../../practice/lp8m1.md)

### M2: Manage application settings with Azure App Configuration

- No selector → only null-label keys load.
- Later selectors override earlier ones.
- refresh() must be called; the provider doesn't refresh on its own.
- Load defaults first, overrides second.
- Flag changes don't trigger setting refresh, and vice versa.
- Two role assignments: Data Reader (store) and Secrets User (vault).
- secret_refresh_interval is separate from refresh_interval.
- Embedding dimensions and deployment names aren't secrets.
- Duplicating a value in both services invites drift.

Lesson: [lp8m2](../lessons/lp8m2.md) · Practice: [lp8m2](../../practice/lp8m2.md)

## Commands and syntax you'll see

```text
az appconfig kv set-keyvault --key … --secret-identifier https://…/secrets/openai-api-key
```

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
