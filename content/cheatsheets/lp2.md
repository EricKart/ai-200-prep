# LP2 cheat sheet: Deploy and manage apps on Azure Container Apps

> Skill area 1 · one page to review before the exam · full lessons in [content/lessons](../lessons/) · practise at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-2)

## Which one?

| You need… | Answer | Don't confuse with |
|---|---|---|
| Service reachable only inside the environment | --ingress internal | external = callable from outside |
| Reviewable config as the single source of truth | --yaml (other flags ignored) | az containerapp up is for quick prototypes |
| Map a stored secret to an env var | secretref:<secret-name> | Never paste the value in YAML |
| Send 10% of traffic to a new revision | Multiple revision mode + traffic weights | Single revision mode can't split |
| Testers hit one revision via its own URL | Revision label | Traffic weight on latest moves real users |
| Changes that create a new revision | Template: image, env vars, scale rules | Secrets, ingress, traffic = application scope |
| Scale on queue depth, down to zero | KEDA Service Bus/Storage Queue scaler | CPU/memory rules never reach zero |
| WebSockets or gRPC scaling | TCP scale rule | HTTP rule = request concurrency |
| GPU or more than 4 cores / 8 GiB per container | Dedicated workload profile | Consumption max 4 cores / 8 GiB |
| Run AI-generated Python safely | Dynamic sessions: built-in code interpreter | Custom container pool for native binaries |
| Backend calls the session pool API | Azure ContainerApps Session Executor role, audience https://dynamicsessions.io | Users never get the token |

## Must remember

### M1: Deploy containers to Azure Container Apps

- Internal ingress = reachable **only within the environment**.
- Separate environments per lifecycle reduce the blast radius of new revisions.
- With --yaml, every other flag on the command is **ignored**.
- Upper-case repository names cause pull failures that look like auth errors.
- **--set-env-vars** adds or updates without removing other variables.
- secretref:<secret-name> uses the secret's **name**, so the value never appears in YAML or shell history.
- Inactive revisions appear only with **--all**.
- Zero replicas can mean **scale to zero**, not necessarily a failure.

Lesson: [lp2m1](../lessons/lp2m1.md) · Practice: [lp2m1](../../practice/lp2m1.md)

### M2: Manage containers in Azure Container Apps

- Deactivate, don't delete, when investigating a bad revision.
- Inactive revisions are purged automatically above **100** (adjust with --max-inactive-revisions).
- Restart isn't a substitute for finding the root cause.
- Stop affects every revision of the app.
- Don't log raw prompts or documents; log ids and metadata.
- Compare a working revision's config with the failing one.
- Readiness failure = **no traffic**; liveness failure = **restart**.
- Slow model load → raise **initialDelaySeconds** / **failureThreshold**.
- Throttling → more **CPU**; out-of-memory restarts → more **memory**.
- Minimum replicas cut cold starts but add baseline cost.

Lesson: [lp2m2](../lessons/lp2m2.md) · Practice: [lp2m2](../../practice/lp2m2.md)

### M3: Scale containers in Azure Container Apps

- Ingress disabled + no min + no rule = scaled to zero **forever**.
- Jobs can't use HTTP scale rules.
- Cool-down to zero is **300 s**; replicas keep billing during short quiet gaps.
- 50 messages with messageCount 5 → **10 replicas**.
- Event Hubs with 32 partitions: maxReplicas above **32** adds nothing.
- Queue growing faster than replicas scale → **lower** messageCount.
- Redis Streams counts **pending** (unacknowledged) entries; Lists count **length**.
- Several active scalers → the **highest** replica count wins.
- Memory limit → **restart**; CPU limit → **throttling**.
- 0.75 cores needs at least **1.5 GiB**.
- Updating a **secret** doesn't create a new revision.
- Labels ignore traffic weights; the main URL follows them.
- Two revisions at 50/50 each keep their own minimum replicas.

Lesson: [lp2m3](../lessons/lp2m3.md) · Practice: [lp2m3](../../practice/lp2m3.md)

### M4: Run AI-generated code securely in Azure Container Apps dynamic sessions

- Both pool types give **Hyper-V isolation**; choose by runtime and protocol needs.
- Custom container pools need a **workload profiles** environment.
- SessionsPythonREPLTool uses the **same** code interpreter pool; it isn't a different security boundary.
- Egress is **pool-wide**; don't weaken a shared pool for one workload.
- Hyper-V isolation separates sessions but doesn't protect data **inside** a session from its own code.
- Never take the session identifier from the client.
- An HTTP 200 doesn't mean the Python code succeeded.
- One shared SessionsPythonREPLTool instance mixes users' files and state.
- Same identifier after expiry → possibly a **new, empty** session.
- A timeout doesn't prove the code didn't run.
- DELETE success is **204 No Content**.

Lesson: [lp2m4](../lessons/lp2m4.md) · Practice: [lp2m4](../../practice/lp2m4.md)

## Commands and syntax you'll see

```text
az containerapp env create
az containerapp up
az containerapp env show
az extension add --name containerapp --upgrade
az login
az upgrade
az containerapp create
az containerapp update --image …:v2
az containerapp create/update --yaml ./containerapp.yml
az containerapp secret set --secrets embeddings-api-key=…
az containerapp registry set --server myregistry.azurecr.io --username … --password …
az containerapp registry list
az containerapp show
az containerapp logs show
az containerapp revision list
az containerapp replica list
az containerapp update --image <registry>/<repo>@sha256:<digest>
az containerapp show --query properties.template.containers
az containerapp revision deactivate
az containerapp stop
az containerapp restart
az containerapp logs show --follow
az containerapp update --cpu <cores> --memory <size>
az containerapp ingress traffic set --revision-weight order-api--v1=80 order-api--v2=20
az containerapp sessionpool create --container-type PythonLTS …
```


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
