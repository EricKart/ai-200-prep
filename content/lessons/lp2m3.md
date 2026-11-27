# LP2 · M3: Scale containers in Azure Container Apps

> **Learning path 2:** Deploy and manage apps on Azure Container Apps · **Skill area 1:** Develop and deploy containerized solutions · about 87 min on Microsoft Learn  
> Study it interactively at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-2/scale-containers-azure-container-apps)

Container Apps scales on HTTP traffic, TCP connections, CPU, memory, or events through KEDA. You'll learn how each rule behaves, how queue-based scaling is calculated, which compute profile to choose, and how revision modes affect traffic and cost.

**In this lesson**

1. [Configure scale rules](#configure-scale-rules)
2. [Implement event-driven scaling with KEDA](#implement-event-driven-scaling-with-keda)
3. [Apply KEDA scalers for custom workloads](#apply-keda-scalers-for-custom-workloads)
4. [Select compute resources for performance and cost](#select-compute-resources-for-performance-and-cost)
5. [Choose and apply revision modes](#choose-and-apply-revision-modes)

## Configure scale rules

📘 Microsoft Learn: [Configure scale rules](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/2-configure-scale-rules)

Scale rules are **if-this-then-add-replicas** instructions. HTTP and TCP rules count requests or connections and can drop to zero. CPU and memory rules need at least one replica running to measure anything, so they never reach zero. Scale-up is quick (1, 4, 8, 16…); scale-down waits five minutes.

**Key facts**

- A scale definition has **limits** (min and max replicas), **rules** (triggers) and **behavior** (timing and algorithms). Container Apps is powered by **KEDA**.
- Default with ingress enabled and no custom rules: **0 to 10 replicas**. With ingress **disabled** and no minimum or custom rule, the app scales to zero and **can't restart** (no trigger).
- Billing follows replicas: zero replicas = **no compute charges**; running but idle replicas bill at a **lower idle rate**.
- **HTTP** rule: concurrent requests = requests in the past **15 seconds ÷ 15**. Default threshold **10 per replica**. Supports scale to zero. **Container Apps jobs can't use HTTP rules**.
- **TCP** rule (`--scale-rule-tcp-concurrency`): concurrent connections, same 15-second window; for **WebSockets, gRPC** and long-lived connections. Supports scale to zero.
- **CPU and memory** rules are KEDA custom scalers on average utilization; they **can't scale to zero** (need one replica to measure). Combine with HTTP or event rules for scale to zero.
- Polling: custom scalers (CPU, memory, events) every **30 seconds**; HTTP and TCP use a 15-second window.
- **Cool-down** before scaling to zero: **300 seconds**. Scale-up stabilization: **0 seconds**, in steps `**1, 4, 8, 16, 32`…**. Scale-down stabilization: **300 seconds**, and replicas are removed **all at once**.
- With multiple rules, the app scales out when **any** rule's threshold is met. Use at least one replica in production to avoid cold starts.

| Rule | Measures | Scale to zero? |
|---|---|---|
| HTTP | Concurrent requests (15 s window), default 10/replica | Yes |
| TCP | Concurrent connections (15 s window) | Yes |
| CPU / memory | Average utilization %, polled every 30 s | No, minimum 1 |
| Event-driven (KEDA) | Queue depth, lag, custom metrics, polled every 30 s | Yes |

> [!WARNING]
> **Exam traps**
>
> - Ingress disabled + no min + no rule = scaled to zero **forever**.
> - Jobs can't use HTTP scale rules.
> - Cool-down to zero is **300 s**; replicas keep billing during short quiet gaps.

## Implement event-driven scaling with KEDA

📘 Microsoft Learn: [Implement event-driven scaling with KEDA](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/3-event-driven-scaling-keda)

KEDA watches your **to-do pile** (a queue, a stream) and hires enough workers to clear it. With Service Bus, **messages ÷ messageCount = replicas**. With Event Hubs, you can't have more useful workers than **partitions**. When the pile is empty, all workers can go home (scale to zero).

**Key facts**

- KEDA monitors external sources (queue depth, partition lag, custom metrics). Custom scalers follow the KEDA **ScaledObject** pattern: scaler type, metadata, authentication. Polled every **30 seconds**.
- Microsoft-maintained Azure scalers: **Service Bus, Event Hubs, Storage Queue, Blob Storage, Log Analytics, Azure Monitor**. Community scalers cover non-Azure sources.
- Event-driven scaling **supports scale to zero**; new messages trigger scale-up.
- **Service Bus**: metadata `queueName` (or `topicName` + `subscriptionName`), `namespace`, **messageCount**. Replicas = message count ÷ messageCount (5 per replica, 50 messages → **10** replicas). Each subscription scales on its own backlog.
- **Storage Queue**: `queueName`, `accountName`, **queueLength**. Cheaper, fewer features; no sessions, dead-letter queues or scheduled messages (use Service Bus for those).
- **Event Hubs**: `consumerGroup`, **unprocessedEventThreshold** (per partition), **checkpointStrategy** (`blobMetadata` recommended). More replicas than **partitions** gives no benefit.
- Authentication: **secrets** (connection strings, referenced with `--scale-rule-auth`) or **managed identity** (user-assigned identity with roles such as **Azure Service Bus Data Receiver**). Prefer managed identity in production.
- messageCount sets the **target queue depth per replica**; it doesn't control processing concurrency. If queue depth grows faster than replicas, **lower** the threshold; if replicas idle, **raise** it.

| Scaler | Threshold parameter | Notes |
|---|---|---|
| Azure Service Bus | messageCount | Queue or topic subscription |
| Azure Storage Queue | queueLength | Simpler, cheaper, fewer features |
| Azure Event Hubs | unprocessedEventThreshold | Per partition; replicas ≤ partitions; checkpointStrategy blobMetadata |

> [!WARNING]
> **Exam traps**
>
> - 50 messages with messageCount 5 → **10 replicas**.
> - Event Hubs with 32 partitions: maxReplicas above **32** adds nothing.
> - Queue growing faster than replicas scale → **lower** messageCount.

## Apply KEDA scalers for custom workloads

📘 Microsoft Learn: [Apply KEDA scalers for custom workloads](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/4-keda-scalers-custom-workloads)

Beyond Azure services, KEDA can watch **Kafka lag**, **Redis lists and streams**, **Prometheus** metrics or simply a **clock** (cron). A cron rule pre-warms capacity for known busy hours, and HTTP or event rules cover the surprises; the highest request wins.

**Key facts**

- Container Apps supports any **ScaledObject-based** KEDA scaler: Kafka, Redis Lists, Redis Streams, Prometheus, Cron, PostgreSQL, MySQL, MongoDB, external metrics APIs.
- Maintainers: Microsoft (Azure-native), community, and **external scalers** (separate components, extra deployment steps).
- **Kafka**: `bootstrapServers`, `consumerGroup`, `topic`, **lagThreshold** (lag 500 ÷ 100 → 5 replicas). Auth via SASL/PLAIN, SASL/SCRAM or TLS with secrets. Replicas above partition count add nothing.
- **Redis Lists**: list length via **LLEN** (`address`, `listName`, `listLength`). **Redis Streams**: **pending entries** for a consumer group (delivered but not acknowledged), which handles failures better. Variants for standard, Cluster and Sentinel.
- **Cron**: `timezone`, `start`, `end`, **desiredReplicas**; inactive outside the window. Combine with other scalers; Container Apps uses the **highest replica count** among active scalers.
- **Prometheus**: `serverAddress`, `metricName`, `query` (PromQL), `threshold`; value ÷ threshold = replicas. For business metrics like active sessions.
- Converting KEDA specs: `triggers[].type` → **--scale-rule-type**; `triggers[].metadata` → **--scale-rule-metadata**; TriggerAuthentication → secrets in **--scale-rule-auth** (or `--scale-rule-identity`); minReplicaCount/maxReplicaCount → **--min-replicas/--max-replicas**.
- Container Apps doesn't support the full **TriggerAuthentication** resource; reference secrets directly. External scalers or custom intervals may not be available.

| KEDA field | Container Apps |
|---|---|
| triggers[].type | --scale-rule-type (custom type in YAML) |
| triggers[].metadata | --scale-rule-metadata |
| TriggerAuthentication | Secrets in --scale-rule-auth, or --scale-rule-identity |
| minReplicaCount / maxReplicaCount | --min-replicas / --max-replicas |

> [!WARNING]
> **Exam traps**
>
> - Redis Streams counts **pending** (unacknowledged) entries; Lists count **length**.
> - Several active scalers → the **highest** replica count wins.

## Select compute resources for performance and cost

📘 Microsoft Learn: [Select compute resources for performance and cost](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/5-compute-resources-performance-cost)

You choose a size for each container (CPU cores and GiB of memory, memory at least twice the CPU) and Container Apps multiplies it by the number of replicas. Run out of memory and the replica is **killed and restarted**; run out of CPU and it's merely **slowed down**.

**Key facts**

- CPU in cores, memory in **GiB**, per container. **Memory ≥ 2 × CPU** (0.5 cores → at least 1.0 GiB). Default **0.25 cores / 0.5 GiB**.
- Billing: **vCPU-seconds** and **GiB-seconds**. Idle replicas bill at a lower rate; zero replicas cost nothing.
- Over the **memory** limit → replica terminated and restarted. Over the **CPU** allocation → **throttled**.
- **Consumption** plan maximum: **4 cores and 8 GiB per container** (each container in an app, including sidecars, has its own allocation).
- Environment types: **Consumption-only** (serverless, shared) and **Workload profiles** (a Consumption profile plus **Dedicated** profiles with reserved VM sizes).
- Dedicated profiles: **GPU**, more than 4 cores or 8 GiB per container, consistent latency, compliance needs for dedicated infrastructure.
- Total capacity = per-replica resources × max replicas (20 × 0.5 cores = 10 cores). Max **1000 replicas per revision**.
- Larger replicas: fewer scaling events but coarser granularity. Smaller replicas: precise scaling but more scaling overhead. Start with defaults and increase only on evidence.

| Need | Choose |
|---|---|
| Variable traffic, scale to zero savings | Consumption |
| GPU inference | Dedicated workload profile |
| 6 cores in one container | Dedicated workload profile (Consumption max is 4 cores / 8 GiB) |
| Strict, consistent latency | Dedicated workload profile |

> [!WARNING]
> **Exam traps**
>
> - Memory limit → **restart**; CPU limit → **throttling**.
> - 0.75 cores needs at least **1.5 GiB**.

## Choose and apply revision modes

📘 Microsoft Learn: [Choose and apply revision modes](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/6-revision-modes-traffic-management)

Changes to the **template** (image, scale rules, environment variables) make a new revision; changes to the **app** (secrets, ingress, traffic rules) don't. Single revision mode swaps old for new automatically. Multiple revision mode lets you split traffic and use **labels**, private URLs that always hit one revision.

**Key facts**

- A revision is an **immutable snapshot**. **Revision-scope** changes (template: images, scale rules, environment variables) create a new revision. **Application-scope** changes (**secrets, ingress settings, traffic splitting rules**) don't.
- **Single revision mode** is the **default**: zero-downtime swap; the new revision must pass health checks and match the old replica count before traffic shifts, then the old one deactivates. No traffic splitting.
- **Multiple revision mode** (`--revision-mode multiple`): canary, blue-green and A/B testing. Old revisions aren't deactivated automatically.
- Inactive revisions use no resources; up to **100** are kept, oldest purged first.
- Traffic splitting: `az containerapp ingress traffic set --revision-weight order-api--v1=80 order-api--v2=20`. Weights total 100; routing is **probabilistic**. A weight on **latest** follows new deployments automatically.
- **Labels** give a unique URL that always routes to one revision, independent of traffic splitting. Rules: start with a letter, lowercase alphanumerics and dashes, no consecutive dashes, max **64** characters. Moving a label is **atomic**.
- Each active revision scales independently, so a 50/50 split can use more resources than one revision. Move through percentages quickly (10% → 50% → 100%) and deactivate old revisions promptly.

| Change | New revision? |
|---|---|
| Container image | Yes (revision scope) |
| Scale rules | Yes |
| Environment variables | Yes |
| Secrets | No (application scope) |
| Ingress settings | No |
| Traffic splitting rules | No |

> [!WARNING]
> **Exam traps**
>
> - Updating a **secret** doesn't create a new revision.
> - Labels ignore traffic weights; the main URL follows them.
> - Two revisions at 50/50 each keep their own minimum replicas.

## Check yourself

- **Practice questions:** [lp2m3 on GitHub](../../practice/lp2m3.md), or [on the site](https://aryantripathi.dev/ai-200/lp-2/scale-containers-azure-container-apps) with hints and saved progress
- **Cheat sheet:** [Learning path 2](../cheatsheets/lp2.md)
- **Microsoft Learn exercise:** [Configure autoscaling using KEDA triggers](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/7-exercise-configure-autoscaling-keda)
- **Hands-on lab:** [labs/](../../labs/README.md) has a lab for this learning path

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
