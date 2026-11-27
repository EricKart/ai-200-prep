# LP7 cheat sheet: Integrate backend services for AI solutions

> Skill area 3 · one page to review before the exam · full lessons in [content/lessons](../lessons/) · practise at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-7)

## Which one?

| You need… | Answer | Don't confuse with |
|---|---|---|
| Each request handled by one worker, absorbs bursts | Service Bus queue | Topic = fan-out copies |
| Several services react to one result | Service Bus topic + subscriptions | Queue competing consumers |
| Ordered processing per document | Service Bus sessions | Duplicate detection doesn't order |
| Long job loses its lock (default 1 min) | AutoLockRenewer / renew_message_lock | Lock max is 5 minutes |
| React to a blob upload without polling | Event Grid system topic (BlobCreated) | Custom topics are for your own events |
| Handler work takes over 30 seconds | Return 202 Accepted, process async | 400 stops retries |
| HTTP work longer than 230 seconds | Async request-reply via Service Bus trigger | functionTimeout can't beat the load balancer |
| Wait days for human approval | Durable Functions: external event + durable timer (task_any) | time.sleep in an orchestrator |
| Many responders watch one live job | Web PubSub operation group | Groups don't assign work |

## Must remember

### M1: Queue and process AI operations with Azure Service Bus

- Standard max message size: **256 KB**; Premium: **100 MB** (AMQP).
- Private endpoints and VNet integration need **Premium**.
- Correlation filters are more efficient than SQL filters for exact matches.
- Default filter is TrueFilter (accept all).
- Reusing a message_id with duplicate detection on can silently drop distinct requests.
- Claim-check works without upgrading to Premium.
- Lock default is **1 minute** (max 5); expiry causes duplicate processing.
- DLQ messages don't expire on their own.
- Deferred messages are retrieved by **sequence number** only.

Lesson: [lp7m1](../lessons/lp7m1.md) · Practice: [lp7m1](../../practice/lp7m1.md)

### M2: Develop event-driven AI workflows with Azure Event Grid

- You can't publish to a system topic.
- Events are notifications; the subscriber fetches the full resource if needed.
- Pull delivery needs a namespace topic.
- Advanced filters: AND across conditions, OR within one condition's values; max 25.
- Can't convert CloudEvents to the Event Grid schema.
- Returning 400 for a transient problem means the event is never retried.
- Without a dead-letter container, events that exhaust retries are **dropped**.
- A 30-minute TTL with 10 max attempts: TTL wins (~6 attempts).
- Data Sender role on the topic for managed identity publishing.
- A list of events goes in one HTTP request.

Lesson: [lp7m2](../lessons/lp7m2.md) · Practice: [lp7m2](../../practice/lp7m2.md)

### M3: Build serverless AI backends with Azure Functions

- 230-second HTTP limit applies regardless of host.json functionTimeout.
- Flex Consumption is Linux-only.
- Legacy Linux Consumption retires after September 2028.
- No storage connection → queue and timer triggers don't run.
- UseDevelopmentStorage=true only works locally.
- One trigger per function, always.
- maxDeliveryCount lives on the queue, not in host.json.
- Missing Key Vault Secrets User → the setting shows an error, not the secret.
- Versioned secret URIs don't follow rotation.
- Blob triggers need extra storage roles beyond Blob Data Owner.
- Never embed the master key in a client.

Lesson: [lp7m3](../lessons/lp7m3.md) · Practice: [lp7m3](../../practice/lp7m3.md)

### M4: Orchestrate durable AI workflows with Azure Durable Functions

- datetime.now() or time.sleep() in an orchestrator breaks replay.
- Activities can run more than once; make writes idempotent.
- Durable Task Scheduler is the recommended provider for new apps.
- Yield each call immediately = sequential, not fan-out.
- task_all returns results in task-list order, not completion order.
- If the event wins, cancel the timer; an event task needn't be cancelled when the timer wins.
- Events can arrive before the orchestrator waits; they're buffered.
- uuid.uuid4() inside a retried activity makes every attempt look new.
- A timer win doesn't stop an activity that's already running.

Lesson: [lp7m4](../lessons/lp7m4.md) · Practice: [lp7m4](../../practice/lp7m4.md)

### M5: Deliver real-time AI experiences with Azure Web PubSub

- SSE reconnects automatically, but resume needs server-side retained events.
- Web PubSub isn't a drop-in replacement for an existing SignalR app.
- Group publish ≠ work assignment.
- Notify only after the state change is durable.
- Expired token ≠ disconnected client.
- Never give a viewer webpubsub.sendToGroup.
- Group broadcasts use GROUP_MESSAGE, not SERVER_MESSAGE.
- Model output isn't trusted markup.
- Request the snapshot only after subscribing.
- Client dedup doesn't make backend processing exactly-once.
- Progress can be coalesced; text deltas can't be dropped silently.
- A delivery failure isn't a model failure.

Lesson: [lp7m5](../lessons/lp7m5.md) · Practice: [lp7m5](../../practice/lp7m5.md)

## Commands and syntax you'll see

```text
az eventgrid topic create … --input-schema cloudeventschemav1_0
az eventgrid topic show
func --version
func init
func new
func start
func azure functionapp fetch-app-settings
func settings encrypt
```


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
