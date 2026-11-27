# LP9 cheat sheet: Observe and troubleshoot apps on Azure

> Skill area 4 · one page to review before the exam · full lessons in [content/lessons](../lessons/) · practise at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-9)

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

### M1: Instrument an app with OpenTelemetry

- CONSUMER spans are Requests; INTERNAL spans are Dependencies.
- traceparent's 2nd field is the trace ID; 3rd is the parent span ID.
- Connection string set in code overrides the environment variable.
- Same service.name for every service = one node on the Application Map.
- Default span kind is INTERNAL.
- Caught exceptions aren't recorded unless you record them.
- Sampling: env vars beat code. Connection string: code beats env vars.
- Logs go to the traces table, not requests.
- Join requests and dependencies on operation_Id.
- Custom attributes live in customDimensions; cast with toint()/tostring().

Lesson: [lp9m1](../lessons/lp9m1.md) · Practice: [lp9m1](../../practice/lp9m1.md)

### M2: Analyze app telemetry with logs and metrics

- has is faster than contains on large tables.
- take isn't sorted; top is.
- Workspace scope uses AppRequests, not requests.
- count() under sampling undercounts; use sum(itemCount).
- Joined duplicate columns get a 1 suffix.
- Dashboard tiles aren't real-time.
- Access to the dashboard alone isn't enough; viewers need access to the data too.
- Multi-select dropdowns need the in operator.
- Every parameter change re-runs dependent queries.
- Severity 0 is the most urgent.
- Up to five action groups per alert rule.
- Smart detection complements, not replaces, SLA alerts.

Lesson: [lp9m2](../lessons/lp9m2.md) · Practice: [lp9m2](../../practice/lp9m2.md)


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
