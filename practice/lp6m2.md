# Practice: LP6 · M2 Implement event messaging with Azure Managed Redis

> 23 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp6m2.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-6/implement-event-messaging-azure-managed-redis)

## 1. `lp6m2-001`

Which command subscribes to every channel that starts with ai: ?

- **A.** SUBSCRIBE ai:*
- **B.** PUBLISH ai:*
- **C.** XREADGROUP ai:*
- **D.** PSUBSCRIBE ai:*

<details><summary>💡 Hint</summary>

Pattern subscriptions have their own command, which starts with P.

</details>

<details><summary>✅ Answer</summary>

**D.** PSUBSCRIBE ai:*

- A: SUBSCRIBE takes exact channel names.
- B: PUBLISH sends a message.
- C: XREADGROUP reads Streams.
- D: Correct. PSUBSCRIBE subscribes with pattern matching.

SUBSCRIBE for named channels, PSUBSCRIBE for patterns.

📘 Source: [Publish and subscribe to events with Redis pub/sub](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/2-redis-pub-sub)

</details>

## 2. `lp6m2-002`

When a new embedding model is deployed, every running API instance must clear its cached embeddings immediately. Which Redis feature fits?

- **A.** A hash with one field per API instance
- **B.** Pub/sub: publish an invalidation message
- **C.** An atomic counter that instances poll
- **D.** A Stream with a consumer group of API instances

<details><summary>💡 Hint</summary>

Every instance must hear the same signal right away.

</details>

<details><summary>✅ Answer</summary>

**B.** Pub/sub: publish an invalidation message

- A: A hash doesn't notify anyone.
- B: Correct. Every active subscriber receives the broadcast at once.
- C: Polling adds delay; pub/sub pushes immediately.
- D: A consumer group gives each message to just one instance.

Broadcasting cache invalidation is a core pub/sub use case.

📘 Source: [Publish and subscribe to events with Redis pub/sub](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/2-redis-pub-sub)

</details>

## 3. `lp6m2-003`

For each statement, select Yes if the statement is true. Otherwise, select No. A sentiment analyzer subscribes to `conversations:new` and restarts for 30 seconds during a deployment.

| Statement | Yes / No |
|---|---|
| Messages published during those 30 seconds are delivered when it reconnects. | ☐ |
| The publisher is told the message wasn't received. | ☐ |
| Other subscribers that stayed connected receive those messages. | ☐ |

<details><summary>💡 Hint</summary>

Pub/sub only reaches subscribers that are connected at that moment.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Messages published during those 30 seconds are delivered when it reconnects. | No | Pub/sub has no persistence; offline subscribers miss messages. |
| The publisher is told the message wasn't received. | No | Pub/sub is fire-and-forget; publishers don't know who received messages. |
| Other subscribers that stayed connected receive those messages. | Yes | Redis delivers to all active subscribers. |

At-most-once, no persistence, fire-and-forget.

📘 Source: [Publish and subscribe to events with Redis pub/sub](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/2-redis-pub-sub)

</details>

## 4. `lp6m2-004`

A subscriber processes model-prediction events more slowly than they're published, and its memory keeps growing. Which pub/sub limitation is this?

- **A.** Channel naming rules
- **B.** Pattern subscriptions
- **C.** No backpressure handling
- **D.** At-most-once delivery

<details><summary>💡 Hint</summary>

Redis keeps sending even when a subscriber can't keep up.

</details>

<details><summary>✅ Answer</summary>

**C.** No backpressure handling

- A: Channel names don't affect delivery rate.
- B: Patterns don't cause this.
- C: Correct. Redis keeps delivering even if subscribers can't keep up.
- D: At-most-once is about missed messages, not slow consumers.

Without backpressure, slow subscribers can run into memory issues or message loss.

📘 Source: [Publish and subscribe to events with Redis pub/sub](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/2-redis-pub-sub)

</details>

## 5. `lp6m2-005`

A billing service must charge for every completed AI request, even if the billing service is briefly offline. Should it consume events through Redis pub/sub?

- **A.** Yes, if the channel name includes the user id
- **B.** Yes, if it uses PSUBSCRIBE instead of SUBSCRIBE
- **C.** Yes: Redis stores pub/sub messages until they're acknowledged
- **D.** No: pub/sub has no durability, so offline periods lose events

<details><summary>💡 Hint</summary>

Billing can't miss events. Does pub/sub keep messages for offline consumers?

</details>

<details><summary>✅ Answer</summary>

**D.** No: pub/sub has no durability, so offline periods lose events

- A: Channel names don't add durability.
- B: Pattern subscriptions don't add durability.
- C: Pub/sub messages aren't stored or acknowledged.
- D: Correct. Use something durable (such as Streams) when messages must not be lost.

Pub/sub suits real-time notifications, not scenarios that need durability or replay.

📘 Source: [Publish and subscribe to events with Redis pub/sub](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/2-redis-pub-sub)

</details>

## 6. `lp6m2-006`

A service publishes "prediction ready" events, and the team asks how the publisher will know whether any subscriber processed each one. What does Learn say about pub/sub?

- **A.** Redis retries delivery until every subscriber confirms
- **B.** Messages are stored until a subscriber calls XACK
- **C.** It's fire-and-forget: publishers don't know whether any subscriber received the message
- **D.** PUBLISH returns an acknowledgment from each subscriber after processing

<details><summary>💡 Hint</summary>

Pub/sub trades guarantees for speed and loose coupling.

</details>

<details><summary>✅ Answer</summary>

**C.** It's fire-and-forget: publishers don't know whether any subscriber received the message

- A: Pub/sub has no retries. Messages are delivered once to connected subscribers.
- B: XACK belongs to Streams, not pub/sub.
- C: Correct. Pub/sub decouples publishers from subscribers, so there's no delivery confirmation.
- D: Subscribers don't acknowledge processing back to the publisher in pub/sub.

Pub/sub characteristics: at-most-once delivery, no persistence, fire-and-forget (publishers don't know if anyone received the message), and high throughput.

📘 Source: [Publish and subscribe to events with Redis pub/sub](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/2-redis-pub-sub)

</details>

## 7. `lp6m2-007`

Browser clients should see AI predictions the moment the backend publishes them to a Redis channel. Which pattern does Learn show?

- **A.** A backend subscriber that forwards each message over WebSocket connections
- **B.** Browsers poll a Stream with XRANGE every second
- **C.** Browsers connect to Redis directly and run SUBSCRIBE
- **D.** The backend writes each prediction to a cookie

<details><summary>💡 Hint</summary>

Something on the server has to hold an open connection to each browser.

</details>

<details><summary>✅ Answer</summary>

**A.** A backend subscriber that forwards each message over WebSocket connections

- A: Correct. Combining pub/sub with WebSockets pushes real-time updates to browsers.
- B: Polling adds latency and load. The pattern is to push over WebSockets.
- C: Browsers don't connect to Redis. A backend service bridges the two.
- D: Cookies travel with requests. They can't push new data to the browser.

Learn's example combines pub/sub with WebSocket connections: a backend subscriber receives channel messages and pushes them to connected browser clients.

📘 Source: [Publish and subscribe to events with Redis pub/sub](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/2-redis-pub-sub)

</details>

## 8. `lp6m2-008`

Status channels are named ml:models:resnet:status, ml:models:bert:status and so on. One monitoring service must receive the status of every model, including ones added later. Which subscription fits?

- **A.** PSUBSCRIBE ml:models:*:status
- **B.** SUBSCRIBE ml:models:resnet:status ml:models:bert:status
- **C.** SUBSCRIBE ml:models:*:status
- **D.** XREADGROUP on a stream named ml:models

<details><summary>💡 Hint</summary>

You need a wildcard, and wildcards need a particular command.

</details>

<details><summary>✅ Answer</summary>

**A.** PSUBSCRIBE ml:models:*:status

- A: Correct. A pattern subscription matches every channel with that shape, including new ones.
- B: This lists today's channels and misses models added later.
- C: SUBSCRIBE takes exact channel names. Patterns need PSUBSCRIBE.
- D: That reads a Stream, not pub/sub channels.

Channels are strings. PSUBSCRIBE subscribes with patterns such as ai:conversations:* or ml:models:*:status, so new matching channels are included.

📘 Source: [Publish and subscribe to events with Redis pub/sub](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/2-redis-pub-sub)

</details>

## 9. `lp6m2-009`

Which command marks a Stream task as completed by a consumer?

- **A.** XREADGROUP
- **B.** XADD
- **C.** XINFO
- **D.** XACK

<details><summary>💡 Hint</summary>

Streams have three commands: add, read in a group, acknowledge.

</details>

<details><summary>✅ Answer</summary>

**D.** XACK

- A: XREADGROUP reads tasks.
- B: XADD adds tasks.
- C: XINFO reports metrics.
- D: Correct. XACK acknowledges completion.

XADD → XREADGROUP → XACK.

📘 Source: [Implement task queues with Redis Streams](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/3-redis-streams)

</details>

## 10. `lp6m2-010`

An upload endpoint must return immediately while documents are analyzed later, and no document may be lost if a worker crashes. What should the endpoint do?

- **A.** Process the document inside the request
- **B.** Store the job in a string with a 60-second TTL
- **C.** XADD the job to a Stream and return a job id
- **D.** PUBLISH the job to a channel and return

<details><summary>💡 Hint</summary>

Return quickly and keep the job safe from worker crashes.

</details>

<details><summary>✅ Answer</summary>

**C.** XADD the job to a Stream and return a job id

- A: That blocks the API.
- B: An expiring string can disappear before processing.
- C: Correct. Streams keep tasks until acknowledged and let workers process at their own pace.
- D: Pub/sub would lose jobs if no worker is listening.

Streams give durable async queues for long AI operations.

📘 Source: [Implement task queues with Redis Streams](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/3-redis-streams)

</details>

## 11. `lp6m2-011`

For each statement, select Yes if the statement is true. Otherwise, select No. Workers read from a Stream with a consumer group, and one worker crashes after reading a task but before XACK.

| Statement | Yes / No |
|---|---|
| The task stays in the pending list. | ☐ |
| XPENDING can show tasks that have been pending too long. | ☐ |
| The task is deleted when the worker's connection drops. | ☐ |
| XACK was already sent automatically when the worker read the task. | ☐ |

<details><summary>💡 Hint</summary>

An unacknowledged task stays pending, and you can inspect it.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The task stays in the pending list. | Yes | Unacknowledged tasks remain pending. |
| XPENDING can show tasks that have been pending too long. | Yes | XPENDING finds stuck tasks. |
| The task is deleted when the worker's connection drops. | No | Tasks survive crashes. |
| XACK was already sent automatically when the worker read the task. | No | The worker must call XACK after processing; it crashed before that. |

Pending lists and XCLAIM make Stream processing self-healing.

📘 Source: [Implement task queues with Redis Streams](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/3-redis-streams)

</details>

## 12. `lp6m2-012`

A queue Stream processes millions of tasks a day and Redis memory keeps climbing, although every task is acknowledged. Why?

- **A.** Pending tasks are duplicated on each read
- **B.** Consumer groups disable eviction
- **C.** Acknowledged entries stay until trimmed
- **D.** XACK copies each task into a second stream

<details><summary>💡 Hint</summary>

Acknowledging doesn't delete. Trim the stream.

</details>

<details><summary>✅ Answer</summary>

**C.** Acknowledged entries stay until trimmed

- A: Reading doesn't duplicate entries.
- B: Learn doesn't say this.
- C: Correct. Tasks don't auto-expire; trim with maxlen on XADD or XTRIM.
- D: XACK doesn't copy tasks.

Plan trimming upfront: xadd(…, maxlen=10000, approximate=True) or periodic XTRIM.

📘 Source: [Implement task queues with Redis Streams](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/3-redis-streams)

</details>

## 13. `lp6m2-013`

Put the steps of a reliable Stream worker in order.

- Acknowledge it with XACK
- Create the consumer group once (ignore the error if it exists)
- Process the task
- Read new tasks with XREADGROUP

<details><summary>💡 Hint</summary>

Create the group, read, process, acknowledge.

</details>

<details><summary>✅ Answer</summary>

1. Create the consumer group once (ignore the error if it exists)
2. Read new tasks with XREADGROUP
3. Process the task
4. Acknowledge it with XACK

Unacknowledged tasks remain pending for retry.

📘 Source: [Implement task queues with Redis Streams](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/3-redis-streams)

</details>

## 14. `lp6m2-014`

A pipeline needs microsecond-level notifications that a model finished loading, and losing one notification is acceptable. Should you use a Stream?

- **A.** No: pub/sub is faster and loss is acceptable
- **B.** No: Streams can't hold more than one message
- **C.** Yes: pub/sub can't send to more than one subscriber
- **D.** Yes: Streams have lower latency than pub/sub in every case

<details><summary>💡 Hint</summary>

Does this need durability, or speed?

</details>

<details><summary>✅ Answer</summary>

**A.** No: pub/sub is faster and loss is acceptable

- A: Correct. Streams add a few milliseconds for persistence and acks; pub/sub fits low-latency, loss-tolerant notifications.
- B: Streams hold many entries.
- C: Pub/sub broadcasts to all subscribers.
- D: Streams are slightly slower than pub/sub.

Choose Streams for reliability, pub/sub for the lowest latency.

📘 Source: [Implement task queues with Redis Streams](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/3-redis-streams)

</details>

## 15. `lp6m2-015`

A new analytics service is added next month and must process every inference request already queued in a Stream, from the beginning. Which Streams benefit makes this possible?

- **A.** Streams broadcast each entry to subscribers in real time
- **B.** Streams delete entries as soon as they're read
- **C.** Streams keep history, so new services can catch up
- **D.** Streams keep entries for subscribers connected at the time

<details><summary>💡 Hint</summary>

Unlike pub/sub, a Stream remembers what was added to it.

</details>

<details><summary>✅ Answer</summary>

**C.** Streams keep history, so new services can catch up

- A: That describes pub/sub, which doesn't keep history.
- B: Entries stay in the Stream until trimmed.
- C: Correct. You can query, replay for debugging, or let new services catch up on historical data.
- D: That's pub/sub's limitation. Streams persist entries.

Streams benefits: tasks survive crashes, automatic retry via pending entries, built-in work distribution with consumer groups, processing history (replay and catch-up), and simple async patterns.

📘 Source: [Implement task queues with Redis Streams](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/3-redis-streams)

</details>

## 16. `lp6m2-016`

An inference queue Stream should keep roughly the last 10,000 entries and drop older ones as new tasks arrive, without a separate cleanup job. How can the producer do this?

- **A.** Set a 10,000-second TTL on each entry
- **B.** Call XADD with maxlen=10000 and approximate=True
- **C.** Call XACK with count=10000
- **D.** Use PUBLISH instead of XADD

<details><summary>💡 Hint</summary>

The add command itself can cap the stream's length.

</details>

<details><summary>✅ Answer</summary>

**B.** Call XADD with maxlen=10000 and approximate=True

- A: Stream entries don't get individual TTLs.
- B: Correct. XADD can trim the stream as it adds, keeping about the last 10,000 entries.
- C: XACK acknowledges entries. It doesn't trim the stream.
- D: That moves to pub/sub, which loses durability.

Acknowledged entries stay until trimmed. Cap a stream with XADD …, maxlen=N, approximate=True, or trim it separately with XTRIM.

📘 Source: [Implement task queues with Redis Streams](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/3-redis-streams)

</details>

## 17. `lp6m2-017`

Three worker instances subscribe to the same pub/sub channel for inference requests. What happens when one request is published?

- **A.** All three workers receive and process it
- **B.** Redis queues it until a worker is idle
- **C.** One worker gets it, chosen round-robin
- **D.** The first worker to acknowledge it keeps it

<details><summary>💡 Hint</summary>

Pub/sub copies each message to every subscriber.

</details>

<details><summary>✅ Answer</summary>

**A.** All three workers receive and process it

- A: Correct. Pub/sub duplicates messages to every subscriber, tripling the cost.
- B: Pub/sub doesn't queue messages.
- C: Pub/sub doesn't load-balance.
- D: Pub/sub has no acknowledgments.

Use Stream consumer groups to distribute work.

📘 Source: [Choose between broadcast and coordinated distribution](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/4-coordinate-multiple-subscribers)

</details>

## 18. `lp6m2-018`

A worker restarts and should first finish tasks it had already received but not acknowledged. Which read ID should it pass to XREADGROUP?

- **A.** *
- **B.** >
- **C.** 0
- **D.** $

<details><summary>💡 Hint</summary>

New messages use one special ID. Your own unacknowledged ones start from the beginning of your pending list.

</details>

<details><summary>✅ Answer</summary>

**C.** 0

- A: * isn't used to read pending messages.
- B: > returns only new messages never delivered to any consumer.
- C: Correct. An ID such as 0 reads this consumer's pending messages.
- D: Learn doesn't use $ for this.

> for new work; 0 to re-read your own pending tasks.

📘 Source: [Choose between broadcast and coordinated distribution](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/4-coordinate-multiple-subscribers)

</details>

## 19. `lp6m2-019`

Match each scenario to the Redis approach.

Choices: **Pub/sub broadcast** · **Stream consumer group** · **Hybrid: Stream + pub/sub**

- Feature flag changed; every service must reload its config
- Each document summary job must run on exactly one GPU worker
- Queue a large document for processing and tell dashboards it arrived

<details><summary>💡 Hint</summary>

Broadcast to everyone, or hand each job to exactly one worker.

</details>

<details><summary>✅ Answer</summary>

- Feature flag changed; every service must reload its config → **Pub/sub broadcast**. All instances need the same update.
- Each document summary job must run on exactly one GPU worker → **Stream consumer group**. Consumer groups give each message to one consumer.
- Queue a large document for processing and tell dashboards it arrived → **Hybrid: Stream + pub/sub**. Queue the work in a Stream and broadcast the notification.

Broadcast vs coordinate: choose by whether everyone or exactly one should act.

📘 Source: [Choose between broadcast and coordinated distribution](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/4-coordinate-multiple-subscribers)

</details>

## 20. `lp6m2-020`

For each statement, select Yes if the statement is true. Otherwise, select No. A Stream consumer group scales from two workers to five.

| Statement | Yes / No |
|---|---|
| The new workers start receiving tasks without code changes. | ☐ |
| Each task is now delivered to all five workers. | ☐ |
| Each worker gets a smaller share of the total workload. | ☐ |

<details><summary>💡 Hint</summary>

Consumer groups split work, and more members means smaller shares.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The new workers start receiving tasks without code changes. | Yes | New workers in the group automatically share the work. |
| Each task is now delivered to all five workers. | No | Each message goes to exactly one consumer in the group. |
| Each worker gets a smaller share of the total workload. | Yes | Work spreads across more workers. |

Consumer groups scale horizontally by simply adding consumers.

📘 Source: [Choose between broadcast and coordinated distribution](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/4-coordinate-multiple-subscribers)

</details>

## 21. `lp6m2-021`

A monitoring service should reassign tasks that have been pending for more than five minutes because their worker crashed. Which commands does it use?

- **A.** PUBLISH to announce them, then SUBSCRIBE to retry
- **B.** XADD a copy of each task, then XACK the original
- **C.** XTRIM the stream so stuck tasks are removed
- **D.** XPENDING to find them, XCLAIM to reassign

<details><summary>💡 Hint</summary>

One command lists entries nobody acknowledged. Another transfers them to a different consumer.

</details>

<details><summary>✅ Answer</summary>

**D.** XPENDING to find them, XCLAIM to reassign

- A: Pub/sub can't reassign Stream tasks.
- B: Duplicating tasks risks double processing.
- C: Trimming deletes entries rather than recovering them.
- D: Correct. XPENDING finds stuck tasks; XCLAIM moves them to a healthy worker.

XPENDING + XCLAIM keep tasks from being lost when workers crash.

📘 Source: [Choose between broadcast and coordinated distribution](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/4-coordinate-multiple-subscribers)

</details>

## 22. `lp6m2-022`

When a user finishes an AI interaction, the analytics, billing and recommendation services must each react in their own way. Losing an event for one service is acceptable. Which approach does Learn describe for notifying them?

- **A.** Publish one event to a channel that all three services subscribe to
- **B.** Add the event to one Stream read by a single consumer group of all three services
- **C.** Write the event to a Redis List that all three pop from
- **D.** Call each service's API in turn from the web request

<details><summary>💡 Hint</summary>

All three need the same event. Should it be copied or distributed?

</details>

<details><summary>✅ Answer</summary>

**A.** Publish one event to a channel that all three services subscribe to

- A: Correct. Pub/sub suits notifying heterogeneous services that each process the same event.
- B: A single consumer group gives each entry to one consumer, so only one service would get each event.
- C: Popping removes the item, so only one service would get it.
- D: That couples the request to every service. Pub/sub decouples them.

Use pub/sub when all services must react to the same event (cache invalidation, configuration updates, monitoring, notifying heterogeneous services). Use Stream consumer groups to distribute work so each task runs once.

📘 Source: [Choose between broadcast and coordinated distribution](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/4-coordinate-multiple-subscribers)

</details>

## 23. `lp6m2-023`

Three GPU workers each subscribe to the channel ai:inference:requests. Costs tripled, and results are inconsistent. What should the team change?

- **A.** Add a fourth worker to spread the load
- **B.** Have the workers use PSUBSCRIBE instead of SUBSCRIBE
- **C.** Move the requests to a Stream that the workers read through one consumer group
- **D.** Publish each request three times, once per worker

<details><summary>💡 Hint</summary>

Pub/sub duplicates messages. What distributes them instead?

</details>

<details><summary>✅ Answer</summary>

**C.** Move the requests to a Stream that the workers read through one consumer group

- A: With pub/sub, a fourth worker would also process every request.
- B: Pattern subscriptions still broadcast every message to every subscriber.
- C: Correct. Consumer groups deliver each entry to only one worker, which distributes the load.
- D: That multiplies the duplication.

Pub/sub broadcasts, so every worker processes every request. Stream consumer groups give each message to exactly one consumer, enabling horizontal scaling without duplicate work.

📘 Source: [Choose between broadcast and coordinated distribution](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/4-coordinate-multiple-subscribers)

</details>


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
