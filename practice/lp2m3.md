# Practice: LP2 · M3 Scale containers in Azure Container Apps

> 24 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp2m3.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-2/scale-containers-azure-container-apps)

## 1. `lp2m3-001`

A gRPC service keeps long-lived connections open, and the team wants it to scale with load and drop to zero overnight. Which rule type fits best?

- **A.** CPU scale rule
- **B.** Memory scale rule
- **C.** HTTP scale rule
- **D.** TCP scale rule

<details><summary>💡 Hint</summary>

Long-lived connections aren't counted well as requests. Which rule counts open connections?

</details>

<details><summary>✅ Answer</summary>

**D.** TCP scale rule

- A: CPU rules can't scale to zero.
- B: Memory rules can't scale to zero.
- C: HTTP rules suit short request-response cycles; Learn prefers TCP for gRPC.
- D: Correct. TCP rules suit WebSockets, gRPC and long-lived connections, and support scale to zero.

TCP scaling counts concurrent connections and supports scale to zero.

📘 Source: [Configure scale rules](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/2-configure-scale-rules)

</details>

## 2. `lp2m3-002`

What is the default HTTP concurrency threshold per replica in Azure Container Apps?

- **A.** 1 request
- **B.** 100 requests
- **C.** 50 requests
- **D.** 10 requests

<details><summary>💡 Hint</summary>

The default HTTP concurrency threshold is a small round number.

</details>

<details><summary>✅ Answer</summary>

**D.** 10 requests

- A: Learn gives a higher default.
- B: 100 appears in Learn's combined-rule YAML, not as the default.
- C: 50 is the custom value in Learn's example command.
- D: Correct. The default HTTP concurrency threshold is 10 requests per replica.

The default is 10 concurrent requests per replica; adjust it to the app's capacity.

📘 Source: [Configure scale rules](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/2-configure-scale-rules)

</details>

## 3. `lp2m3-003`

A background processor has ingress disabled, no minimum replicas and no custom scale rule. After the first idle period it never starts again. Why?

- **A.** It scaled to zero and has no trigger to activate it
- **B.** CPU rules polled every 30 seconds can't see a stopped app
- **C.** The 300-second cool-down repeats until a revision is deployed
- **D.** Jobs can't use HTTP rules, so the app was converted to a job

<details><summary>💡 Hint</summary>

Nothing can wake an app with no ingress, no minimum and no event rule.

</details>

<details><summary>✅ Answer</summary>

**A.** It scaled to zero and has no trigger to activate it

- A: Correct. With ingress disabled and no minimum or rule, the app scales to zero and can't restart.
- B: There's no CPU rule configured in this scenario.
- C: The cool-down applies once before scaling to zero.
- D: The app isn't a job; the problem is the missing trigger.

Set a minimum of one replica or add an event-driven rule that can wake the app.

📘 Source: [Configure scale rules](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/2-configure-scale-rules)

</details>

## 4. `lp2m3-004`

For each statement, select Yes if the statement is true. Otherwise, select No. An app has `minReplicas: 0`, a CPU rule at 70% and no other rules.

| Statement | Yes / No |
|---|---|
| The app can scale to zero when CPU usage is low. | ☐ |
| The platform checks the CPU rule every 30 seconds. | ☐ |
| Adding an HTTP rule as well would let the app scale to zero. | ☐ |

<details><summary>💡 Hint</summary>

CPU and memory need a running replica to measure. Think about what happens at zero.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The app can scale to zero when CPU usage is low. | No | CPU rules need a running replica to measure utilization, so they keep at least one. |
| The platform checks the CPU rule every 30 seconds. | Yes | Custom scalers such as CPU and memory are polled every 30 seconds. |
| Adding an HTTP rule as well would let the app scale to zero. | Yes | Combine resource rules with HTTP or event rules for scale to zero. |

CPU and memory rules always keep at least one replica; pair them with HTTP or event rules to reach zero.

📘 Source: [Configure scale rules](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/2-configure-scale-rules)

</details>

## 5. `lp2m3-005`

For each statement, select Yes if the statement is true. Otherwise, select No. An app scales from 1 replica under a sudden sustained load spike, with a maximum of 30.

| Statement | Yes / No |
|---|---|
| The platform waits 300 seconds before starting to scale up. | ☐ |
| Scale-up proceeds in steps such as 1, 4, 8, 16, then the maximum. | ☐ |
| When load ends, replicas are removed one at a time over five minutes. | ☐ |
| With an HTTP rule and a CPU rule, either one exceeding its threshold scales the app out. | ☐ |

<details><summary>💡 Hint</summary>

Scale-up doesn't wait; scale-down does. Any rule can trigger a scale-out.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The platform waits 300 seconds before starting to scale up. | No | The scale-up stabilization window is zero seconds. |
| Scale-up proceeds in steps such as 1, 4, 8, 16, then the maximum. | Yes | Scale-up doubles in steps until it reaches the maximum. |
| When load ends, replicas are removed one at a time over five minutes. | No | After the 300-second window, all replicas that need to shut down are removed at once. |
| With an HTTP rule and a CPU rule, either one exceeding its threshold scales the app out. | Yes | With multiple rules, the app scales out when any rule's threshold is met. |

Scale up immediately in doubling steps; scale down after 300 seconds, all at once; any rule can trigger scale out.

📘 Source: [Configure scale rules](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/2-configure-scale-rules)

</details>

## 6. `lp2m3-006`

A Service Bus scale rule has messageCount set to 5, and 50 messages are waiting in the queue. How many replicas does the scaler request?

- **A.** 50
- **B.** 250
- **C.** 5
- **D.** 10

<details><summary>💡 Hint</summary>

The Service Bus scaler divides the waiting messages by the threshold.

</details>

<details><summary>✅ Answer</summary>

**D.** 10

- A: That's one replica per message.
- B: The scaler divides, it doesn't multiply.
- C: That would be one replica per 10 messages.
- D: Correct. 50 ÷ 5 = 10 replicas.

The Service Bus scaler divides the active message count by messageCount.

📘 Source: [Implement event-driven scaling with KEDA](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/3-event-driven-scaling-keda)

</details>

## 7. `lp2m3-007`

A document-extraction worker scales with a Service Bus KEDA rule. Its CPU sits at 90% while the queue is empty, and the team asks whether CPU affects the replica count. Which value does the Service Bus scaler use?

- **A.** The CPU utilization of each replica
- **B.** The number of open AMQP connections
- **C.** The namespace's total size in bytes
- **D.** The queue's active message count

<details><summary>💡 Hint</summary>

An event-driven scaler watches the event source, not the replicas.

</details>

<details><summary>✅ Answer</summary>

**D.** The queue's active message count

- A: CPU is a separate rule type. The Service Bus scaler looks at the queue.
- B: Connections aren't the scaling signal. Queued messages are.
- C: Storage size doesn't indicate how much work is waiting.
- D: Correct. The Service Bus scaler uses the active message count divided by messageCount.

The Service Bus scaler divides the active message count by messageCount to calculate the desired replica count. It's independent of CPU.

📘 Source: [Implement event-driven scaling with KEDA](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/3-event-driven-scaling-keda)

</details>

## 8. `lp2m3-008`

An Event Hub has 32 partitions, and the processing app's scale rule allows up to 100 replicas. What should you expect?

- **A.** Each replica reads every partition, so 100 replicas triple throughput
- **B.** The scaler is rejected because maxReplicas exceeds 32
- **C.** Up to 100 replicas share the load evenly across partitions
- **D.** Replicas beyond 32 add no extra processing benefit

<details><summary>💡 Hint</summary>

Each partition can be read by one consumer in a group at a time.

</details>

<details><summary>✅ Answer</summary>

**D.** Replicas beyond 32 add no extra processing benefit

- A: Within a consumer group, a partition has one active reader.
- B: Learn says it provides no benefit; it doesn't say the rule is rejected.
- C: Each partition can be read by one consumer at a time within a consumer group.
- D: Correct. You can't benefit from more replicas than partitions.

Partition count caps effective parallelism for Event Hubs (and Kafka).

📘 Source: [Implement event-driven scaling with KEDA](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/3-event-driven-scaling-keda)

</details>

## 9. `lp2m3-009`

A simple thumbnail queue needs no sessions, dead-letter queues or scheduled messages, and cost matters. Which scaler and threshold should you use?

- **A.** Azure Service Bus scaler with messageCount
- **B.** Azure Storage Queue scaler with queueLength
- **C.** A CPU scale rule with a 70% threshold
- **D.** Azure Event Hubs scaler with unprocessedEventThreshold

<details><summary>💡 Hint</summary>

No sessions, no dead-lettering, and cost matters. Which queue service is simpler?

</details>

<details><summary>✅ Answer</summary>

**B.** Azure Storage Queue scaler with queueLength

- A: Service Bus suits workloads that need advanced features or higher throughput.
- B: Correct. Storage Queue is the simpler, lower-cost option for basic queues; queueLength is its threshold.
- C: A CPU rule can't scale to zero and doesn't track the queue.
- D: Event Hubs is for partitioned, high-throughput streams.

Use Storage Queue scaling for straightforward queue processing; Service Bus for sessions, DLQs, scheduled messages or higher throughput.

📘 Source: [Implement event-driven scaling with KEDA](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/3-event-driven-scaling-keda)

</details>

## 10. `lp2m3-010`

A Service Bus processor's queue depth keeps growing faster than replicas are added, and the team stores the namespace connection string as a secret. Which two changes follow Learn's best practices? (Select two.)

- **A.** Switch the rule to a memory scale rule
- **B.** Lower the messageCount threshold
- **C.** Use a user-assigned managed identity with Azure Service Bus Data Receiver
- **D.** Raise messageCount so each replica processes more messages at once

<details><summary>💡 Hint</summary>

Grow replicas sooner, and stop storing a connection string.

</details>

<details><summary>✅ Answer</summary>

**B.** Lower the messageCount threshold  
**C.** Use a user-assigned managed identity with Azure Service Bus Data Receiver

- A: Memory rules don't track the backlog and can't scale to zero.
- B: Correct. If depth grows faster than replicas scale, lower the threshold.
- C: Correct. Prefer managed identity over stored connection strings in production.
- D: messageCount is target queue depth per replica, not processing concurrency; raising it slows scaling.

Tune messageCount from measured capacity and queue delay, and authenticate scalers with managed identity.

📘 Source: [Implement event-driven scaling with KEDA](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/3-event-driven-scaling-keda)

</details>

## 11. `lp2m3-011`

A Kafka scale rule has lagThreshold set to 100, and the consumer group's lag across all partitions is 500 messages. The topic has 10 partitions. How many replicas does the scaler target?

- **A.** 5
- **B.** 50
- **C.** 10, one per partition
- **D.** 100

<details><summary>💡 Hint</summary>

Divide the total lag by the lag that one replica is expected to handle.

</details>

<details><summary>✅ Answer</summary>

**A.** 5

- A: Correct. 500 messages of lag divided by a lagThreshold of 100 gives 5 replicas.
- B: That would be the lag divided by the partition count, which isn't how the scaler works.
- C: The partition count caps useful parallelism, but the calculation divides lag by the threshold.
- D: 100 is the threshold itself, not the desired replica count.

lagThreshold sets the lag that triggers scaling. With lagThreshold 100 and 500 messages of lag, the scaler targets 5 replicas (up to the partition count).

📘 Source: [Apply KEDA scalers for custom workloads](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/4-keda-scalers-custom-workloads)

</details>

## 12. `lp2m3-012`

Match each KEDA ScaledObject field to its Container Apps equivalent.

Choices: **--scale-rule-type** · **--scale-rule-metadata** · **--scale-rule-auth** · **--max-replicas**

- triggers[].type
- triggers[].metadata
- TriggerAuthentication
- maxReplicaCount

<details><summary>💡 Hint</summary>

Container Apps has CLI flags that map to KEDA ScaledObject fields one to one.

</details>

<details><summary>✅ Answer</summary>

- triggers[].type → **--scale-rule-type**. The scaler type becomes --scale-rule-type.
- triggers[].metadata → **--scale-rule-metadata**. Metadata becomes key-value pairs for --scale-rule-metadata.
- TriggerAuthentication → **--scale-rule-auth**. Credentials become Container Apps secrets referenced in --scale-rule-auth.
- maxReplicaCount → **--max-replicas**. Scale limits map to --min-replicas and --max-replicas.

Container Apps doesn't support the full TriggerAuthentication resource; reference secrets directly in the rule.

📘 Source: [Apply KEDA scalers for custom workloads](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/4-keda-scalers-custom-workloads)

</details>

## 13. `lp2m3-013`

From 8 AM to 6 PM on weekdays, an API needs at least five replicas ready, and it must still react to unexpected spikes and scale to zero at night. What should you configure?

- **A.** A cron scaler alone with desiredReplicas set to the maximum
- **B.** A cron scaler with desiredReplicas 5, plus an HTTP scale rule
- **C.** minReplicas 5 with no rules, so capacity stays available
- **D.** A Prometheus scaler that queries the time of day

<details><summary>💡 Hint</summary>

Combine a schedule with a reactive rule. Container Apps uses the highest replica count among active scalers.

</details>

<details><summary>✅ Answer</summary>

**B.** A cron scaler with desiredReplicas 5, plus an HTTP scale rule

- A: Cron alone can't react to unexpected spikes and wastes capacity.
- B: Correct. Cron sets baseline capacity in the window; HTTP handles spikes; the highest count wins and it can reach zero at night.
- C: A fixed minimum of 5 never scales to zero at night.
- D: Prometheus scales on metric values, not scheduled windows.

Combine scheduled (cron) and reactive (HTTP or event) scaling; Container Apps uses the highest replica count among active scalers.

📘 Source: [Apply KEDA scalers for custom workloads](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/4-keda-scalers-custom-workloads)

</details>

## 14. `lp2m3-014`

Workers pull tasks from Redis, and sometimes a worker crashes after taking a task but before finishing it. Which scaler accounts for this in-progress work?

- **A.** Cron scaler, so capacity is fixed during the busy window
- **B.** Redis Streams scaler, which tracks pending entries for a consumer group
- **C.** Redis Lists scaler, because LLEN counts in-progress items
- **D.** Kafka scaler, using lagThreshold on the Redis list

<details><summary>💡 Hint</summary>

Some work was taken by a worker that then crashed. Which Redis structure remembers work that was handed out but not finished?

</details>

<details><summary>✅ Answer</summary>

**B.** Redis Streams scaler, which tracks pending entries for a consumer group

- A: Cron doesn't look at the work at all.
- B: Correct. Streams scaling tracks delivered-but-unacknowledged entries, so it handles failures better.
- C: LLEN counts queued items; it doesn't track work already taken.
- D: The Kafka scaler reads Kafka consumer lag, not Redis.

Redis Streams scalers consider work in progress (pending entries), not just queued work.

📘 Source: [Apply KEDA scalers for custom workloads](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/4-keda-scalers-custom-workloads)

</details>

## 15. `lp2m3-015`

An inference API's real load is best described by an application metric, pending tokens per second, which it already exposes to a Prometheus server. HTTP concurrency doesn't reflect the actual work. Which scaler fits?

- **A.** A CPU scale rule at 50%
- **B.** A cron scaler with a fixed replica count
- **C.** The Prometheus scaler with a PromQL query and a threshold
- **D.** An HTTP scale rule with a lower concurrency threshold

<details><summary>💡 Hint</summary>

When standard signals don't describe the work, scale on the custom metric you already collect.

</details>

<details><summary>✅ Answer</summary>

**C.** The Prometheus scaler with a PromQL query and a threshold

- A: CPU is only an indirect signal, and the team already has a direct metric.
- B: A schedule doesn't react to the metric at all.
- C: Correct. Prometheus scaling uses application-specific metrics, and the scaler divides the query result by the threshold.
- D: Changing the threshold still scales on concurrency, which you said doesn't reflect the work.

Prometheus scaling triggers on custom metrics such as business metrics or SLO indicators. Its metadata includes serverAddress, metricName, query (PromQL) and threshold; desired replicas = query value ÷ threshold.

📘 Source: [Apply KEDA scalers for custom workloads](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/4-keda-scalers-custom-workloads)

</details>

## 16. `lp2m3-016`

A team must choose a scaler for an Azure Storage Queue. A community-maintained scaler and the Azure-native one can both read the queue. Which does Learn recommend, and why?

- **A.** Either one, because every KEDA scaler has the same support level
- **B.** The community scaler, because open-source scalers get updates faster
- **C.** The Azure-native scaler, which Microsoft maintains with first-party support
- **D.** An external scaler, because it runs as a separate component

<details><summary>💡 Hint</summary>

Scalers are grouped by who maintains them.

</details>

<details><summary>✅ Answer</summary>

**C.** The Azure-native scaler, which Microsoft maintains with first-party support

- A: Scalers are categorized by maintainer, and their support differs.
- B: Learn doesn't make that claim. It notes that community scalers can vary in documentation and support.
- C: Correct. Start with Azure-native scalers for Azure resources; community scalers can have varying documentation and support.
- D: External scalers need a separately deployed component, which adds work and isn't needed here.

Microsoft maintains Azure-native scalers (Service Bus, Event Hubs, Storage Queue, Blob, Log Analytics, Azure Monitor). Community-maintained scalers vary in documentation and support. External scalers run as separate components.

📘 Source: [Apply KEDA scalers for custom workloads](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/4-keda-scalers-custom-workloads)

</details>

## 17. `lp2m3-017`

You allocate 0.5 CPU cores to a container. What is the minimum memory you must allocate?

- **A.** 2.0 GiB
- **B.** 4.0 GiB
- **C.** 0.5 GiB
- **D.** 1.0 GiB

<details><summary>💡 Hint</summary>

There's a fixed ratio between memory in GiB and CPU in cores.

</details>

<details><summary>✅ Answer</summary>

**D.** 1.0 GiB

- A: That's more than required.
- B: That's far more than required.
- C: Memory must be at least twice the CPU value.
- D: Correct. 2 × 0.5 = 1.0 GiB.

Memory in GiB must be at least twice the CPU in cores.

📘 Source: [Select compute resources for performance and cost](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/5-compute-resources-performance-cost)

</details>

## 18. `lp2m3-018`

An inference container needs a GPU and 12 GiB of memory. Which environment option does Learn require?

- **A.** A Consumption-only environment
- **B.** The Consumption profile in a workload profiles environment
- **C.** A Dedicated workload profile
- **D.** Two containers of 6 GiB each in the Consumption plan

<details><summary>💡 Hint</summary>

GPUs and bigger allocations aren't available in the serverless profile.

</details>

<details><summary>✅ Answer</summary>

**C.** A Dedicated workload profile

- A: Consumption maxes out at 4 cores and 8 GiB per container and has no GPU.
- B: The Consumption profile has the same limits as Consumption-only.
- C: Correct. Dedicated profiles are required for GPU workloads and allocations above 4 cores or 8 GiB.
- D: The requirement is per container, and the GPU need remains.

Dedicated workload profiles support GPU, larger allocations and consistent performance.

📘 Source: [Select compute resources for performance and cost](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/5-compute-resources-performance-cost)

</details>

## 19. `lp2m3-019`

A container app has a main inference container and a logging sidecar. The inference container needs 6 cores and 12 GiB. The app runs in a Consumption-only environment. What happens?

- **A.** It doesn't fit: Consumption allows up to 4 cores and 8 GiB per container, so it needs a Dedicated workload profile
- **B.** It fits, because the limit applies to the whole replica and the sidecar is small
- **C.** It fits once the memory is raised to 24 GiB to keep the 2:1 ratio
- **D.** It fits if you raise --max-replicas so that the load spreads

<details><summary>💡 Hint</summary>

The Consumption plan has a maximum per container. Does it apply per container or per replica?

</details>

<details><summary>✅ Answer</summary>

**A.** It doesn't fit: Consumption allows up to 4 cores and 8 GiB per container, so it needs a Dedicated workload profile

- A: Correct. The Consumption limit applies per container, and larger allocations need a Dedicated profile.
- B: The 4-core / 8-GiB limit is per container, not per replica.
- C: The ratio doesn't lift the per-container limit in Consumption.
- D: More replicas don't change the limit for one container's allocation.

In the Consumption plan, the maximum allocation per container is 4 cores and 8 GiB, applied per container (not per replica). Larger allocations or GPUs need a Dedicated workload profile.

📘 Source: [Select compute resources for performance and cost](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/5-compute-resources-performance-cost)

</details>

## 20. `lp2m3-020`

For each statement, select Yes if the statement is true. Otherwise, select No. An app uses 0.5 cores and 1.0 GiB per replica with `--max-replicas 20` in the Consumption plan.

| Statement | Yes / No |
|---|---|
| At peak, the app can use up to 10 cores of processing capacity. | ☐ |
| If a replica exceeds its CPU allocation, the platform terminates and restarts it. | ☐ |
| Running replicas that aren't processing requests are billed at the full active rate. | ☐ |
| The app could be configured with up to 1000 replicas per revision. | ☐ |

<details><summary>💡 Hint</summary>

Capacity is per-replica size times replica count. CPU limits throttle; memory limits restart.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| At peak, the app can use up to 10 cores of processing capacity. | Yes | 20 replicas × 0.5 cores = 10 cores. |
| If a replica exceeds its CPU allocation, the platform terminates and restarts it. | No | CPU over-use is throttled; exceeding memory causes termination. |
| Running replicas that aren't processing requests are billed at the full active rate. | No | Idle replicas are billed at a lower idle rate. |
| The app could be configured with up to 1000 replicas per revision. | Yes | The maximum replica count is 1000 per revision. |

Total capacity = per-replica size × replica count; memory limits restart, CPU limits throttle.

📘 Source: [Select compute resources for performance and cost](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/5-compute-resources-performance-cost)

</details>

## 21. `lp2m3-021`

Which change to a container app creates a new revision?

- **A.** Changing the ingress settings
- **B.** Changing the traffic splitting weights
- **C.** Updating a secret value
- **D.** Changing an environment variable

<details><summary>💡 Hint</summary>

Template changes create revisions. Secrets, ingress and traffic rules don't.

</details>

<details><summary>✅ Answer</summary>

**D.** Changing an environment variable

- A: Ingress settings are application scope.
- B: Traffic rules are application scope.
- C: Secrets are application scope; no new revision.
- D: Correct. Environment variables are part of the template, so they're revision scope.

Template (revision-scope) changes create revisions; secrets, ingress and traffic rules don't.

📘 Source: [Choose and apply revision modes](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/6-revision-modes-traffic-management)

</details>

## 22. `lp2m3-022`

Testers must reach the new revision through a stable URL before it receives any production traffic, without changing the current 100/0 weights. What should you use?

- **A.** A revision label on the new revision
- **B.** Single revision mode
- **C.** A traffic weight on latest
- **D.** A second container app environment

<details><summary>💡 Hint</summary>

You want a stable URL to one revision that's separate from traffic weights.

</details>

<details><summary>✅ Answer</summary>

**A.** A revision label on the new revision

- A: Correct. A label URL always routes to the labelled revision, independent of traffic splitting.
- B: Single revision mode shifts all traffic to the new revision.
- C: A weight on latest sends production traffic to the new revision.
- D: A separate environment isn't needed; labels solve this directly.

Labels give direct access to a revision for testing, separate from traffic splitting.

📘 Source: [Choose and apply revision modes](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/6-revision-modes-traffic-management)

</details>

## 23. `lp2m3-023`

Two revisions each have minReplicas 1 and an HTTP rule, and traffic is split 50/50 for a week. Costs are higher than with one revision, and neither revision scaled up at peak. What explains this?

- **A.** Labels on both revisions double the replica count for each request
- **B.** Each revision scales on its own share of traffic and keeps its own minimum
- **C.** Traffic splitting disables scale rules until the split returns to 100/0
- **D.** Inactive revisions keep consuming resources until they are purged

<details><summary>💡 Hint</summary>

With two active revisions, ask: does scaling look at the app as a whole, or at each revision separately?

</details>

<details><summary>✅ Answer</summary>

**B.** Each revision scales on its own share of traffic and keeps its own minimum

- A: Labels don't change replica counts.
- B: Correct. Each revision keeps its own minimum and sees only half the traffic, so it may not cross the threshold.
- C: Scale rules stay active during splits.
- D: Both revisions are active; inactive revisions consume no resources.

Move through traffic percentages quickly and deactivate old revisions promptly to control resources.

📘 Source: [Choose and apply revision modes](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/6-revision-modes-traffic-management)

</details>

## 24. `lp2m3-024`

You configure traffic splitting between the stable revision and a canary in multiple revision mode, with weights of 90 and 5. The command fails. Why?

- **A.** The canary needs a label before it can get weight
- **B.** The weights must total 100 percent
- **C.** A canary must start at 10 percent or more
- **D.** Traffic splitting needs single revision mode

<details><summary>💡 Hint</summary>

Add up the two weights.

</details>

<details><summary>✅ Answer</summary>

**B.** The weights must total 100 percent

- A: Labels give direct URLs for testing. They aren't needed for weights.
- B: Correct. Traffic weights across active revisions must total 100 percent.
- C: There's no minimum canary weight. The total is the problem.
- D: Single revision mode has one active revision, so it can't split traffic.

Traffic splitting distributes requests across active revisions by percentage weights that total 100 percent. Routing is probabilistic per request.

📘 Source: [Choose and apply revision modes](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/6-revision-modes-traffic-management)

</details>


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
