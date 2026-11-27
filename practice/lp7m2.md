# Practice: LP7 · M2 Develop event-driven AI workflows with Azure Event Grid

> 25 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp7m2.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-7/event-driven-workflows-event-grid)

## 1. `lp7m2-001`

New documents arrive in Blob Storage, and an embeddings pipeline currently polls the container every five minutes. What should replace the polling?

- **A.** A custom topic
- **B.** A Service Bus queue polled each minute
- **C.** A webhook that lists the container
- **D.** An Event Grid subscription to BlobCreated

<details><summary>💡 Hint</summary>

Stop asking the container whether something is new. Let the platform tell you.

</details>

<details><summary>✅ Answer</summary>

**D.** An Event Grid subscription to BlobCreated

- A: The pipeline consumes this event; Blob Storage publishes it through a system topic.
- B: That's still polling.
- C: Listing on a timer is still polling.
- D: Correct. The system topic pushes a BlobCreated event as soon as the blob appears.

Reactive data processing: subscribe to storage events instead of polling.

📘 Source: [Understand Azure Event Grid concepts and event-driven patterns for AI solutions](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/2-understand-event-grid-concepts)

</details>

## 2. `lp7m2-002`

Which statement about Event Grid system topics is true?

- **A.** You publish your application's events to them
- **B.** They support pull delivery and nothing else
- **C.** They're created automatically for Azure services
- **D.** They require you to define the event schema

<details><summary>💡 Hint</summary>

Azure services publish through topics that Event Grid creates for them.

</details>

<details><summary>✅ Answer</summary>

**C.** They're created automatically for Azure services

- A: Only the Azure service publishes to a system topic.
- B: Learn doesn't limit system topics to pull delivery.
- C: Correct. They appear when you subscribe to a supported Azure resource's events.
- D: System topic schemas are predefined by the service.

System topics: Azure services. Custom topics: your code.

📘 Source: [Understand Azure Event Grid concepts and event-driven patterns for AI solutions](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/2-understand-event-grid-concepts)

</details>

## 3. `lp7m2-003`

Match each requirement to the event handler Learn describes.

Choices: **Azure Functions** · **Azure Event Hubs** · **Service Bus queue** · **Webhook**

- Lightweight, stateless processing with automatic scaling
- Feed events into a high-throughput streaming pipeline
- Ordered or transactional processing
- Send events to a custom inference endpoint over HTTP

<details><summary>💡 Hint</summary>

Match each processing need to the handler built for it.

</details>

<details><summary>✅ Answer</summary>

- Lightweight, stateless processing with automatic scaling → **Azure Functions**. Functions suit stateless event processing.
- Feed events into a high-throughput streaming pipeline → **Azure Event Hubs**. Event Hubs ingests high-throughput streams.
- Ordered or transactional processing → **Service Bus queue**. Service Bus suits guaranteed ordering or transactions.
- Send events to a custom inference endpoint over HTTP → **Webhook**. Webhooks reach any HTTP endpoint.

Choose the handler by processing requirements.

📘 Source: [Understand Azure Event Grid concepts and event-driven patterns for AI solutions](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/2-understand-event-grid-concepts)

</details>

## 4. `lp7m2-004`

For each statement, select Yes if the statement is true. Otherwise, select No. A content moderation platform uses Event Grid.

| Statement | Yes / No |
|---|---|
| Uploads trigger Microsoft.Storage.BlobCreated events from a system topic. | ☐ |
| The classifier can publish com.contoso.ai.ContentClassified to the same system topic. | ☐ |
| Notification and analytics services can each subscribe to the custom topic independently. | ☐ |
| Each event should carry the full uploaded image. | ☐ |

<details><summary>💡 Hint</summary>

Azure events come through system topics. Your own events go to custom topics.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Uploads trigger Microsoft.Storage.BlobCreated events from a system topic. | Yes | Blob Storage publishes through a system topic. |
| The classifier can publish com.contoso.ai.ContentClassified to the same system topic. | No | You can't publish to system topics; use a custom topic. |
| Notification and analytics services can each subscribe to the custom topic independently. | Yes | Multiple subscriptions fan out events. |
| Each event should carry the full uploaded image. | No | Events are lightweight notifications; subscribers fetch the resource. |

System topics for Azure events, custom topics for your own; keep events small.

📘 Source: [Understand Azure Event Grid concepts and event-driven patterns for AI solutions](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/2-understand-event-grid-concepts)

</details>

## 5. `lp7m2-005`

A consumer can't accept incoming HTTP requests and wants to read events at its own pace. Which option fits?

- **A.** A system topic with a webhook
- **B.** Pull delivery from a namespace topic
- **C.** Push delivery to a webhook endpoint it hosts
- **D.** A custom topic with push delivery to Functions

<details><summary>💡 Hint</summary>

If the consumer can't receive HTTP, it has to go and fetch events.

</details>

<details><summary>✅ Answer</summary>

**B.** Pull delivery from a namespace topic

- A: Webhooks are push delivery.
- B: Correct. Namespace topics support pull delivery, so the consumer reads on demand.
- C: Webhooks need an HTTP endpoint that accepts requests.
- D: That's push delivery.

Push sends to an endpoint; pull lets the consumer connect and read.

📘 Source: [Understand Azure Event Grid concepts and event-driven patterns for AI solutions](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/2-understand-event-grid-concepts)

</details>

## 6. `lp7m2-006`

A team is designing a new set of AI pipeline events and must choose an event schema. They want an open, protocol-independent standard that works beyond Azure. Which schema does Learn recommend?

- **A.** Event Grid schema
- **B.** Event Hubs Avro
- **C.** Custom JSON with no required attributes
- **D.** CloudEvents v1.0

<details><summary>💡 Hint</summary>

One schema is an open standard from the Cloud Native Computing Foundation.

</details>

<details><summary>✅ Answer</summary>

**D.** CloudEvents v1.0

- A: The Event Grid schema remains for backward compatibility. It's not the recommendation for new work.
- B: Avro is a serialization format, not an Event Grid event schema.
- C: Without standard attributes, subscribers can't rely on id, source or type.
- D: Correct. CloudEvents v1.0 is an open CNCF standard and the recommended schema for new implementations.

CloudEvents v1.0 is recommended for new implementations: an open, protocol-independent CNCF standard. The Event Grid schema is kept for backward compatibility and can't represent CloudEvents extension attributes.

📘 Source: [Work with event schemas and properties](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/3-event-schemas-properties)

</details>

## 7. `lp7m2-007`

Which CloudEvents attribute should subscribers use to detect and deduplicate repeated deliveries?

- **A.** The id attribute of each event
- **B.** type attribute
- **C.** subject attribute
- **D.** source attribute

<details><summary>💡 Hint</summary>

Event Grid may deliver the same event more than once. Which attribute is unique per event?

</details>

<details><summary>✅ Answer</summary>

**A.** The id attribute of each event

- A: Correct. id uniquely identifies each event.
- B: type categorizes the event.
- C: subject is a filterable path.
- D: source identifies the originating system.

Event Grid is at-least-once, so handlers dedupe on id.

📘 Source: [Work with event schemas and properties](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/3-event-schemas-properties)

</details>

## 8. `lp7m2-008`

A subscription should receive only events from the embeddings pipeline, whose subjects look like `/pipelines/embeddings/batch-42`. Which filter fits?

- **A.** --included-event-types /pipelines/embeddings
- **B.** subjectEndsWith /embeddings
- **C.** StringContains on the id attribute
- **D.** subjectBeginsWith /pipelines/embeddings/

<details><summary>💡 Hint</summary>

The subjects share a prefix. Filter on how the subject starts.

</details>

<details><summary>✅ Answer</summary>

**D.** subjectBeginsWith /pipelines/embeddings/

- A: Event types aren't subject paths.
- B: The subject doesn't end with /embeddings.
- C: id is a unique identifier, not a routing path.
- D: Correct. A prefix filter routes events from a specific pipeline.

Set hierarchical subjects so subscribers can filter by prefix or suffix.

📘 Source: [Work with event schemas and properties](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/3-event-schemas-properties)

</details>

## 9. `lp7m2-009`

Your topic publishes CloudEvents, and a legacy handler only accepts the Event Grid schema. What happens if you set the subscription's delivery schema to the Event Grid schema?

- **A.** Event Grid converts it, dropping extension attributes
- **B.** That conversion isn't supported for CloudEvents topics
- **C.** The topic switches its input schema automatically
- **D.** Both formats arrive in one payload

<details><summary>💡 Hint</summary>

Conversion works in one direction only.

</details>

<details><summary>✅ Answer</summary>

**B.** That conversion isn't supported for CloudEvents topics

- A: Learn says this conversion isn't supported at all.
- B: Correct. CloudEvents-to-Event Grid conversion isn't supported because of extension attributes.
- C: Input schema is set on the topic and doesn't change automatically.
- D: Event Grid doesn't do this.

Event Grid schema → CloudEvents works; the reverse doesn't.

📘 Source: [Work with event schemas and properties](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/3-event-schemas-properties)

</details>

## 10. `lp7m2-010`

For each statement, select Yes if the statement is true. Otherwise, select No. A subscription has two advanced filters: `data.status StringIn [flagged, failed]` and `data.confidence NumberGreaterThan 0.9`.

| Statement | Yes / No |
|---|---|
| An event with status flagged and confidence 0.95 is delivered. | ☐ |
| An event with status failed and confidence 0.5 is delivered. | ☐ |
| An event with status failed and confidence 0.97 is delivered. | ☐ |
| A subscription can have up to 100 advanced filter conditions. | ☐ |

<details><summary>💡 Hint</summary>

Conditions combine with AND; values inside one condition combine with OR.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| An event with status flagged and confidence 0.95 is delivered. | Yes | It meets both conditions (AND between conditions). |
| An event with status failed and confidence 0.5 is delivered. | No | Both conditions must match; 0.5 fails the second. |
| An event with status failed and confidence 0.97 is delivered. | Yes | Within a condition's values, OR applies: failed matches. |
| A subscription can have up to 100 advanced filter conditions. | No | The limit is 25 conditions per subscription. |

AND between conditions, OR within each condition's values.

📘 Source: [Work with event schemas and properties](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/3-event-schemas-properties)

</details>

## 11. `lp7m2-011`

A review service should receive only InferenceCompleted events from the content-moderation pipeline. How do type and subject filters on one subscription combine?

- **A.** An event has to match both of the filters
- **B.** A subscription allows one filter type at most
- **C.** An event that matches either filter is delivered
- **D.** The subject filter replaces the type filter

<details><summary>💡 Hint</summary>

Type says what happened, and subject says where. How do two filters on one subscription combine?

</details>

<details><summary>✅ Answer</summary>

**A.** An event has to match both of the filters

- A: Correct. A subscription with both filters only receives events matching all criteria.
- B: You can combine type and subject filtering.
- C: Filters on the same subscription combine with AND.
- D: Both filters apply.

Use type filtering for what happened and subject filtering for where.

📘 Source: [Work with event schemas and properties](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/3-event-schemas-properties)

</details>

## 12. `lp7m2-012`

Only inference results with a confidence above 0.9 should reach the auto-approve handler. Confidence is a number in the event's data. Which subscription filter does this?

- **A.** Event type filter: com.contoso.ai.HighConfidence
- **B.** Subject filter: subjectEndsWith confidence-0.9
- **C.** Advanced filter: data.confidence NumberGreaterThan 0.9
- **D.** Output batching with a preferred batch size of 0.9 KB

<details><summary>💡 Hint</summary>

The value is a number inside data. Which filter type can compare numbers?

</details>

<details><summary>✅ Answer</summary>

**C.** Advanced filter: data.confidence NumberGreaterThan 0.9

- A: That only works if the publisher creates a separate event type, which it doesn't.
- B: Subject filters match text in the subject, not numbers in the data.
- C: Correct. Advanced filters compare values inside the event data.
- D: Batching groups deliveries. It doesn't filter events.

Advanced filters match on values in the event data, with operators such as NumberGreaterThan and StringIn. Type and subject filters don't evaluate numeric payload values.

📘 Source: [Work with event schemas and properties](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/3-event-schemas-properties)

</details>

## 13. `lp7m2-013`

An inference handler takes about 2 minutes per event, and Event Grid keeps retrying events that were actually processed. What should the handler do?

- **A.** Return 400 so Event Grid stops retrying
- **B.** Increase Event Grid's timeout to 5 minutes
- **C.** Return 202 Accepted at once, then process
- **D.** Return 503 after the work is finished

<details><summary>💡 Hint</summary>

Event Grid waits only a short time. Acknowledge first, then do the slow work.

</details>

<details><summary>✅ Answer</summary>

**C.** Return 202 Accepted at once, then process

- A: 400 means "don't retry" for a malformed request, not for success.
- B: The 30-second wait isn't something you raise.
- C: Correct. 202 counts as successful delivery; Event Grid waits only 30 seconds.
- D: 503 signals overload and triggers retries.

Acknowledge early with 202 when processing takes longer than 30 seconds.

📘 Source: [Configure delivery and retry policies for reliable event processing](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/4-delivery-retry-policies)

</details>

## 14. `lp7m2-014`

What is Event Grid's default maximum number of delivery attempts?

- **A.** 1,440
- **B.** 24
- **C.** 30
- **D.** 10

<details><summary>💡 Hint</summary>

Default maximum delivery attempts is a round number.

</details>

<details><summary>✅ Answer</summary>

**C.** 30

- A: 1,440 is the default event TTL in minutes.
- B: 24 isn't the default.
- C: Correct. Default max attempts is 30 (range 1–30).
- D: 10 is the Service Bus default max delivery count.

Max attempts default 30; event TTL default 1,440 minutes (24 hours).

📘 Source: [Configure delivery and retry policies for reliable event processing](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/4-delivery-retry-policies)

</details>

## 15. `lp7m2-015`

For each statement, select Yes if the statement is true. Otherwise, select No. An event subscription uses default settings and its webhook returns errors.

| Statement | Yes / No |
|---|---|
| If the webhook returns 400 Bad Request, Event Grid retries with backoff. | ☐ |
| If it returns 503, Event Grid retries following its backoff schedule. | ☐ |
| Events that exhaust retries are kept in Blob Storage automatically. | ☐ |
| The handler might receive the same event twice. | ☐ |

<details><summary>💡 Hint</summary>

Some status codes are retried and some aren't. Exhausted events aren't kept unless you enable it.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| If the webhook returns 400 Bad Request, Event Grid retries with backoff. | No | 400 isn't retried. |
| If it returns 503, Event Grid retries following its backoff schedule. | Yes | Transient errors are retried. |
| Events that exhaust retries are kept in Blob Storage automatically. | No | Dead-lettering is disabled by default; without it, events are dropped. |
| The handler might receive the same event twice. | Yes | At-least-once delivery means possible duplicates. |

Return accurate status codes, make handlers idempotent and configure dead-lettering.

📘 Source: [Configure delivery and retry policies for reliable event processing](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/4-delivery-retry-policies)

</details>

## 16. `lp7m2-016`

A real-time moderation subscription should stop retrying stale events after 30 minutes. A teammate also sets max attempts to 10. What happens?

- **A.** TTL wins first, after about six attempts
- **B.** All 10 attempts run, then it stops
- **C.** TTL is ignored once max attempts is set
- **D.** Event Grid retries every 3 minutes to fit 10 attempts

<details><summary>💡 Hint</summary>

Two limits apply. Which one runs out sooner with the default retry schedule?

</details>

<details><summary>✅ Answer</summary>

**A.** TTL wins first, after about six attempts

- A: Correct. Whichever limit comes first stops retries; only about six attempts fit in 30 minutes.
- B: The TTL expires before 10 attempts.
- C: Both limits apply.
- D: The backoff schedule doesn't stretch to fit.

Retry stops at the first of max attempts or event TTL.

📘 Source: [Configure delivery and retry policies for reliable event processing](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/4-delivery-retry-policies)

</details>

## 17. `lp7m2-017`

Dead-lettered events show lastDeliveryOutcome = NotFound for all of them since yesterday's deployment. What's the most likely issue?

- **A.** The handler endpoint URL changed
- **B.** The TTL is too long
- **C.** The inference service is overloaded
- **D.** Events are too large

<details><summary>💡 Hint</summary>

NotFound for every event after a deployment points at the destination.

</details>

<details><summary>✅ Answer</summary>

**A.** The handler endpoint URL changed

- A: Correct. Learn ties a batch of NotFound outcomes to a changed handler URL.
- B: TTL length doesn't produce NotFound.
- C: Overload shows up as TimedOut or Busy.
- D: 413 isn't a NotFound outcome.

Use deadLetterReason and lastDeliveryOutcome to diagnose systemic failures.

📘 Source: [Configure delivery and retry policies for reliable event processing](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/4-delivery-retry-policies)

</details>

## 18. `lp7m2-018`

Which response from an event handler does Event Grid treat as a successful delivery?

- **A.** 503 Service Unavailable
- **B.** 202 Accepted
- **C.** 400 Bad Request
- **D.** 413 Request Entity Too Large

<details><summary>💡 Hint</summary>

Success is in the 2xx range.

</details>

<details><summary>✅ Answer</summary>

**B.** 202 Accepted

- A: 503 tells Event Grid to retry. It isn't a success.
- B: Correct. Event Grid treats 200, 201, 202, 203 and 204 as success.
- C: 400 is a permanent error. Event Grid doesn't retry it, and it isn't a success.
- D: 413 is a permanent error, not a success.

Event Grid treats 200–204 as successful delivery. 400 and 413 are permanent errors (not retried); 503 triggers retries with backoff.

📘 Source: [Configure delivery and retry policies for reliable event processing](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/4-delivery-retry-policies)

</details>

## 19. `lp7m2-019`

You enable dead-lettering on an event subscription so that undeliverable events are kept. Where does Event Grid write them?

- **A.** To an Azure Storage queue
- **B.** To a Log Analytics table
- **C.** To a Service Bus dead-letter queue created automatically
- **D.** To an Azure Blob Storage container that already exists

<details><summary>💡 Hint</summary>

Dead-lettering is off by default, and you must point it at existing storage.

</details>

<details><summary>✅ Answer</summary>

**D.** To an Azure Blob Storage container that already exists

- A: Event Grid dead-letters to Blob Storage, not Storage queues.
- B: Logs can record delivery failures, but the events themselves go to Blob Storage.
- C: Event Grid doesn't use Service Bus for its dead-letter location.
- D: Correct. Dead-lettered events go to a Blob container you specify, which must exist beforehand.

Dead-lettering is off by default. When enabled, undeliverable events go to an Azure Blob Storage container you specify (it must exist). They carry properties such as deadLetterReason and lastDeliveryOutcome.

📘 Source: [Configure delivery and retry policies for reliable event processing](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/4-delivery-retry-policies)

</details>

## 20. `lp7m2-020`

A webhook handler returns 400 whenever its vector database is briefly unavailable, and those events are never processed. What's the right fix?

- **A.** Enable output batching on the subscription
- **B.** Raise max delivery attempts from 10 to 30
- **C.** Return 503 during the outage so that Event Grid retries
- **D.** Return 401 so that Event Grid retries in five minutes

<details><summary>💡 Hint</summary>

The handler is telling Event Grid the event is bad, when really the database is down for a moment.

</details>

<details><summary>✅ Answer</summary>

**C.** Return 503 during the outage so that Event Grid retries

- A: Batching groups events. It doesn't change how errors are retried.
- B: More attempts don't help when the status code stops retries completely.
- C: Correct. 503 triggers retries with backoff, while 400 means a permanent problem and is never retried.
- D: 401 isn't retried for webhook endpoints, so the events would still be lost.

Return accurate status codes: 400 means a permanent payload problem and isn't retried; use 503 for temporary outages so Event Grid retries with exponential backoff. Make handlers idempotent.

📘 Source: [Configure delivery and retry policies for reliable event processing](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/4-delivery-retry-policies)

</details>

## 21. `lp7m2-021`

A subscription uses output batching with up to 100 events per delivery. The handler fails on one event in a batch. How does Event Grid respond?

- **A.** It splits the batch in half and retries each half
- **B.** It retries the whole batch of 100 events
- **C.** It retries the failed event alone
- **D.** It dead-letters only the failed event

<details><summary>💡 Hint</summary>

The handler acknowledges a batch with one response.

</details>

<details><summary>✅ Answer</summary>

**B.** It retries the whole batch of 100 events

- A: Event Grid doesn't split batches on failure.
- B: Correct. Batch delivery is all or nothing, so handlers must be idempotent.
- C: Event Grid doesn't track success per event inside a batch.
- D: Without per-event acknowledgment, it can't single out one event.

Output batching is all-or-none: if any event fails, Event Grid retries the whole batch. Keep handlers idempotent and batches small enough to finish within the 30-second timeout.

📘 Source: [Configure delivery and retry policies for reliable event processing](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/4-delivery-retry-policies)

</details>

## 22. `lp7m2-022`

A Container Apps service publishes custom events with a managed identity. Which role should the identity have on the custom topic?

- **A.** Storage Blob Data Contributor
- **B.** Azure Service Bus Data Sender
- **C.** Event Grid Contributor
- **D.** Event Grid Data Sender

<details><summary>💡 Hint</summary>

Production publishers should use Entra ID, with the role that allows sending.

</details>

<details><summary>✅ Answer</summary>

**D.** Event Grid Data Sender

- A: That's for Blob Storage.
- B: That's for Service Bus.
- C: Learn names Data Sender for publishing.
- D: Correct. Grant the managed identity Event Grid Data Sender on the topic.

Entra ID with managed identity is the recommended production auth.

📘 Source: [Publish custom events from AI applications](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/5-publish-custom-events)

</details>

## 23. `lp7m2-023`

An inference result is a 3 MB JSON document. What should the InferenceCompleted event's data contain?

- **A.** A link to the stored result plus a summary
- **B.** The full 3 MB result, so nothing is fetched
- **C.** The result split across several events
- **D.** Nothing; subscribers query the model again

<details><summary>💡 Hint</summary>

Events describe what happened and where to find the details.

</details>

<details><summary>✅ Answer</summary>

**A.** A link to the stored result plus a summary

- A: Correct. Reference results, add metadata and a summary for fast decisions.
- B: Don't embed full results in events.
- C: Splitting isn't the recommended design.
- D: Subscribers shouldn't recompute results.

Events describe what happened and where to find details.

📘 Source: [Publish custom events from AI applications](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/5-publish-custom-events)

</details>

## 24. `lp7m2-024`

A CI/CD pipeline publishes a CloudEvent to a custom topic with curl. Which two settings does Learn show? (Select two.)

- **A.** A Bearer token for `https://dynamicsessions.io`
- **B.** `Content-Type: application/x-www-form-urlencoded`
- **C.** An `aeg-sas-key` header with the topic key
- **D.** `Content-Type: application/cloudevents+json; charset=utf-8`

<details><summary>💡 Hint</summary>

One setting tells Event Grid the payload format. The other authenticates the request when you don't use Entra ID.

</details>

<details><summary>✅ Answer</summary>

**C.** An `aeg-sas-key` header with the topic key  
**D.** `Content-Type: application/cloudevents+json; charset=utf-8`

- A: That audience is for dynamic sessions, not Event Grid.
- B: Form encoding isn't used for CloudEvents.
- C: Correct. Learn's REST example authenticates with aeg-sas-key.
- D: Correct. That's the content type for a single CloudEvent.

The REST API returns 200 OK when the event is accepted.

📘 Source: [Publish custom events from AI applications](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/5-publish-custom-events)

</details>

## 25. `lp7m2-025`

For each statement, select Yes if the statement is true. Otherwise, select No. A pipeline publishes five StageCompleted events using EventGridPublisherClient.

| Statement | Yes / No |
|---|---|
| Passing a list of five CloudEvents sends them in one HTTP request. | ☐ |
| Each event should include a pipeline run ID so subscribers can correlate stages. | ☐ |
| The producer must know which subscribers will receive the events. | ☐ |

<details><summary>💡 Hint</summary>

One request can carry several events. Correlation IDs tie the stages together.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Passing a list of five CloudEvents sends them in one HTTP request. | Yes | Batch publishing sends a list in a single request. |
| Each event should include a pipeline run ID so subscribers can correlate stages. | Yes | Include identifiers for correlation. |
| The producer must know which subscribers will receive the events. | No | Producers don't need to know who subscribes. |

Publish at natural checkpoints with correlation IDs; subscribers come and go independently.

📘 Source: [Publish custom events from AI applications](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/5-publish-custom-events)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
