# Practice: LP7 · M1 Queue and process AI operations with Azure Service Bus

> 25 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp7m1.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-7/queue-process-operations-service-bus)

## 1. `lp7m1-001`

Inference requests arrive in bursts of 5,000 per minute, but the GPU pool can handle an average of 1,000 per minute. Which pattern lets you size workers for the average without dropping requests?

- **A.** A larger API thread pool
- **B.** Receive-and-delete mode
- **C.** Synchronous calls with longer timeouts
- **D.** Load leveling with a queue

<details><summary>💡 Hint</summary>

Something has to hold the extra requests during a burst.

</details>

<details><summary>✅ Answer</summary>

**D.** Load leveling with a queue

- A: More threads just block on the same slow inference.
- B: That's a receive mode, and it risks losing messages.
- C: Synchronous calls still overwhelm processors during spikes.
- D: Correct. The queue absorbs the burst and workers drain it at a steady rate.

Load leveling removes the need to provision compute for peak traffic.

📘 Source: [Explore Azure Service Bus concepts and messaging in AI architectures](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/2-explore-service-bus-concepts)

</details>

## 2. `lp7m1-002`

What is the maximum message size in the Service Bus Standard tier?

- **A.** 100 MB
- **B.** 256 KB
- **C.** 64 KB
- **D.** 1 MB

<details><summary>💡 Hint</summary>

Standard has a much smaller message limit than Premium.

</details>

<details><summary>✅ Answer</summary>

**B.** 256 KB

- A: 100 MB is Premium over AMQP.
- B: Correct. Standard supports messages up to 256 KB.
- C: Standard allows more than this.
- D: 1 MB is Premium over HTTP.

Standard 256 KB; Premium up to 100 MB with AMQP (1 MB HTTP).

📘 Source: [Explore Azure Service Bus concepts and messaging in AI architectures](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/2-explore-service-bus-concepts)

</details>

## 3. `lp7m1-003`

For each statement, select Yes if the statement is true. Otherwise, select No. Five worker instances read from the same Service Bus queue.

| Statement | Yes / No |
|---|---|
| Each message is delivered to exactly one of the workers. | ☐ |
| Adding a sixth worker requires changing the producer's code. | ☐ |
| If a worker crashes mid-processing, its unacknowledged messages become available again. | ☐ |

<details><summary>💡 Hint</summary>

Competing consumers: each message goes to one worker, and unfinished messages come back.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Each message is delivered to exactly one of the workers. | Yes | Competing consumers: one message, one consumer. |
| Adding a sixth worker requires changing the producer's code. | No | Adding workers increases throughput without code changes. |
| If a worker crashes mid-processing, its unacknowledged messages become available again. | Yes | Unacknowledged messages are redelivered. |

The competing consumers pattern scales AI processing horizontally.

📘 Source: [Explore Azure Service Bus concepts and messaging in AI architectures](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/2-explore-service-bus-concepts)

</details>

## 4. `lp7m1-004`

All inference processors are offline for a 20-minute deployment, but the API must keep accepting requests. Which property of queue-based messaging makes this work?

- **A.** Load leveling: the queue processes messages itself
- **B.** Sessions: messages wait in FIFO order per session
- **C.** Fan-out: each message is copied to every processor
- **D.** Temporal decoupling: messages wait for processors

<details><summary>💡 Hint</summary>

Producers and consumers don't have to be online at the same time.

</details>

<details><summary>✅ Answer</summary>

**D.** Temporal decoupling: messages wait for processors

- A: The queue stores messages; it doesn't process them.
- B: Sessions are about ordering, not offline tolerance.
- C: Fan-out is a topic feature and doesn't explain offline tolerance.
- D: Correct. Producers and consumers needn't be online at the same time.

Messages persist durably until consumers come back online.

📘 Source: [Explore Azure Service Bus concepts and messaging in AI architectures](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/2-explore-service-bus-concepts)

</details>

## 5. `lp7m1-005`

An AI pipeline sends 20 MB scanned documents through Service Bus, must use private endpoints, and needs predictable latency. Which tier fits?

- **A.** Basic, with sessions on
- **B.** Standard, using the claim-check pattern
- **C.** Standard, with batching on
- **D.** The Premium tier, dedicated

<details><summary>💡 Hint</summary>

Large messages, private endpoints and predictable latency: which tier has all three?

</details>

<details><summary>✅ Answer</summary>

**D.** The Premium tier, dedicated

- A: Learn covers the Standard and Premium tiers only.
- B: Claim-check handles size, but private endpoints and predictable latency still need Premium.
- C: Batching doesn't raise the 256 KB limit or add private endpoints.
- D: Correct. Premium offers dedicated resources, up to 100 MB via AMQP, predictable latency and private endpoints.

Premium: dedicated capacity, large messages, VNet integration, private endpoints and availability zones.

📘 Source: [Explore Azure Service Bus concepts and messaging in AI architectures](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/2-explore-service-bus-concepts)

</details>

## 6. `lp7m1-006`

A developer creates a ServiceBusReceiver for an inference queue without setting receive_mode. Messages aren't removed when they're received, and the code must settle each one. Which mode is the receiver using?

- **A.** Read-and-release
- **B.** Peek-lock, the default
- **C.** Defer-and-lock
- **D.** Receive-and-delete, the default

<details><summary>💡 Hint</summary>

One mode removes messages straight away. The other waits for you to say what happened.

</details>

<details><summary>✅ Answer</summary>

**B.** Peek-lock, the default

- A: There's no such receive mode in Service Bus.
- B: Correct. Peek-lock locks the message and waits for the consumer to settle it.
- C: There's no such receive mode. Deferral is a settlement action.
- D: Receive-and-delete removes messages on delivery, and it isn't the default.

Peek-lock is the default and recommended mode: the message is locked, not removed, until the consumer completes, abandons, dead-letters or defers it. Receive-and-delete removes it on delivery.

📘 Source: [Explore Azure Service Bus concepts and messaging in AI architectures](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/2-explore-service-bus-concepts)

</details>

## 7. `lp7m1-007`

When a document analysis completes, a notification service, an audit service and a dashboard must each receive the result independently. What should you use?

- **A.** A queue with sessions enabled
- **B.** Three messages to one queue
- **C.** A topic with three subscriptions
- **D.** A queue with three competing consumers

<details><summary>💡 Hint</summary>

Three services each need their own copy.

</details>

<details><summary>✅ Answer</summary>

**C.** A topic with three subscriptions

- A: Sessions order messages; they don't fan out.
- B: Sending three messages couples the producer to every consumer.
- C: Correct. Each subscription gets its own copy and processes independently.
- D: Competing consumers each get different messages, not copies.

Topics fan out; queues give each message to one consumer.

📘 Source: [Choose between queues and topics with subscriptions](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/3-choose-queues-topics-subscriptions)

</details>

## 8. `lp7m1-008`

Which subscription filter type is most efficient for exact-match routing on a property value?

- **A.** A SQL filter
- **B.** A correlation filter
- **C.** The FalseFilter
- **D.** The TrueFilter

<details><summary>💡 Hint</summary>

One filter type is built for exact matches on properties and is cheaper to evaluate.

</details>

<details><summary>✅ Answer</summary>

**B.** A correlation filter

- A: SQL filters are flexible but less efficient for exact matches.
- B: Correct. Correlation filters match specific values efficiently.
- C: FalseFilter rejects every message.
- D: TrueFilter accepts every message.

Boolean, SQL and correlation filters run at the broker.

📘 Source: [Choose between queues and topics with subscriptions](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/3-choose-queues-topics-subscriptions)

</details>

## 9. `lp7m1-009`

A multi-step pipeline must process extraction before classification for each document, while different documents run in parallel. Which feature helps?

- **A.** Duplicate detection on the message ID
- **B.** Sessions, with the document ID as the session ID
- **C.** Receive-and-delete mode
- **D.** A TrueFilter on the subscription

<details><summary>💡 Hint</summary>

Per-document order with parallelism across documents: group the messages by an ID.

</details>

<details><summary>✅ Answer</summary>

**B.** Sessions, with the document ID as the session ID

- A: Duplicate detection drops repeats; it doesn't order messages.
- B: Correct. Sessions give FIFO, single-receiver processing per session group.
- C: That mode only changes acknowledgment, and risks loss.
- D: TrueFilter accepts everything; it doesn't order.

Group related messages with a session ID for ordered processing.

📘 Source: [Choose between queues and topics with subscriptions](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/3-choose-queues-topics-subscriptions)

</details>

## 10. `lp7m1-010`

For each statement, select Yes if the statement is true. Otherwise, select No. Inference results go to a topic with subscriptions **notifications**, **audit** and **high-priority** (filter: priority = 'high').

| Statement | Yes / No |
|---|---|
| Messages that don't match the high-priority filter are never delivered to that subscription. | ☐ |
| Completing a message on the audit subscription removes it from the notifications subscription. | ☐ |
| A new retraining subscription can be added later without changing the producer. | ☐ |
| The producer has to know how many subscriptions exist. | ☐ |

<details><summary>💡 Hint</summary>

Each subscription is its own queue. Filters run at the broker. Subscriptions can be added later.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Messages that don't match the high-priority filter are never delivered to that subscription. | Yes | Filters are evaluated at the broker. |
| Completing a message on the audit subscription removes it from the notifications subscription. | No | Each subscription keeps its own copy. |
| A new retraining subscription can be added later without changing the producer. | Yes | New subscriptions don't affect the publisher. |
| The producer has to know how many subscriptions exist. | No | Topics decouple the sender from the receivers. |

Topics give independent copies, broker-side filtering and easy extension.

📘 Source: [Choose between queues and topics with subscriptions](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/3-choose-queues-topics-subscriptions)

</details>

## 11. `lp7m1-011`

In the Python SDK, how do you read messages from the audit subscription of the inference-results topic?

- **A.** get_queue_receiver(queue_name="audit") on the same client
- **B.** get_subscription_receiver(topic_name="inference-results", subscription_name="audit")
- **C.** get_queue_receiver(queue_name="inference-results/audit") on the client
- **D.** get_topic_sender(topic_name="inference-results") followed by .receive()

<details><summary>💡 Hint</summary>

The same client gives you a receiver for a subscription when you name the topic and subscription.

</details>

<details><summary>✅ Answer</summary>

**B.** get_subscription_receiver(topic_name="inference-results", subscription_name="audit")

- A: audit is a subscription, not a queue.
- B: Correct. Subscription receivers connect to a specific subscription of a topic.
- C: Queue receivers are for queues, not topic subscriptions.
- D: Senders send; they don't receive.

Same ServiceBusClient; get_subscription_receiver for subscriptions.

📘 Source: [Choose between queues and topics with subscriptions](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/3-choose-queues-topics-subscriptions)

</details>

## 12. `lp7m1-012`

The urgent-review subscription should receive only messages whose application property priority is 'high' or whose confidence is below 0.5. Consumer code must not filter. What should you configure?

- **A.** A separate namespace for urgent requests
- **B.** An if-check in the consumer after each message arrives
- **C.** A correlation filter on the priority property
- **D.** A SQL filter rule on that subscription

<details><summary>💡 Hint</summary>

You need an expression with OR and a comparison, evaluated before delivery.

</details>

<details><summary>✅ Answer</summary>

**D.** A SQL filter rule on that subscription

- A: A namespace doesn't route messages by property.
- B: That's filtering in the consumer, which wastes deliveries and isn't allowed here.
- C: Correlation filters do exact matches. They can't express "below 0.5" or an OR.
- D: Correct. SQL filters evaluate expressions on message properties at the broker.

Subscription filters run at the broker. Boolean filters accept or reject all; SQL filters evaluate SQL-like expressions over properties; correlation filters do efficient exact matches.

📘 Source: [Choose between queues and topics with subscriptions](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/3-choose-queues-topics-subscriptions)

</details>

## 13. `lp7m1-013`

Support engineers need to trace one user's request from the API through the processor to the results store. Which message property should carry the shared ID?

- **A.** time_to_live
- **B.** content_type
- **C.** sequence_number
- **D.** correlation_id

<details><summary>💡 Hint</summary>

One property exists to tie related messages together across services.

</details>

<details><summary>✅ Answer</summary>

**D.** correlation_id

- A: time_to_live controls expiry.
- B: content_type describes the body's encoding.
- C: sequence_number is assigned by the broker per entity.
- D: Correct. correlation_id gives end-to-end tracking across the pipeline.

Set correlation_id from the client or API request ID and search logs and DLQs by it.

📘 Source: [Structure messages for AI workloads](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/4-structure-messages-ai-workloads)

</details>

## 14. `lp7m1-014`

A Standard-tier pipeline must send 8 MB PDF files for summarization without changing tier. What should the producer do?

- **A.** Compress the PDF and set a longer time_to_live
- **B.** Split each PDF across many messages with the same message_id
- **C.** Use ServiceBusMessageBatch so the size limit doesn't apply
- **D.** Upload each PDF to Blob Storage; send its URI

<details><summary>💡 Hint</summary>

Too big for the tier: store the file somewhere else and send a pointer.

</details>

<details><summary>✅ Answer</summary>

**D.** Upload each PDF to Blob Storage; send its URI

- A: TTL doesn't change size limits.
- B: Reusing message_id with duplicate detection can drop messages, and reassembly is complex.
- C: Batches are still bounded by the tier's maximum size.
- D: Correct. The claim-check pattern keeps messages small and works in any tier.

Claim-check: store the payload, send a reference.

📘 Source: [Structure messages for AI workloads](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/4-structure-messages-ai-workloads)

</details>

## 15. `lp7m1-015`

For each statement, select Yes if the statement is true. Otherwise, select No. A queue has duplicate detection enabled and dead-lettering on message expiration turned on.

| Statement | Yes / No |
|---|---|
| Two different requests sent with the same message_id inside the detection window might be treated as duplicates. | ☐ |
| A real-time request with time_to_live of 5 minutes that isn't processed in time can end up in the dead-letter queue. | ☐ |
| Setting content_type to application/json makes Service Bus validate the JSON body. | ☐ |

<details><summary>💡 Hint</summary>

Duplicate detection looks at message_id. Expired messages can be dead-lettered.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Two different requests sent with the same message_id inside the detection window might be treated as duplicates. | Yes | Service Bus uses message_id to discard duplicates within the window. |
| A real-time request with time_to_live of 5 minutes that isn't processed in time can end up in the dead-letter queue. | Yes | Expired messages go to the DLQ when dead-lettering on expiration is enabled. |
| Setting content_type to application/json makes Service Bus validate the JSON body. | No | content_type signals the encoding to clients and processors. |

Generate unique message IDs and pick TTLs that match how time-sensitive the request is.

📘 Source: [Structure messages for AI workloads](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/4-structure-messages-ai-workloads)

</details>

## 16. `lp7m1-016`

A batch sender calls add_message() in a loop and gets MessageSizeExceededError partway through 2,000 messages. What does Learn's pattern do?

- **A.** Retry add_message() on the same batch until it succeeds
- **B.** Drop the message that didn't fit and continue
- **C.** Switch to Premium so the batch has no limit
- **D.** Send the full batch, then start a new one

<details><summary>💡 Hint</summary>

A batch tells you when the next message won't fit.

</details>

<details><summary>✅ Answer</summary>

**D.** Send the full batch, then start a new one

- A: The same batch stays full.
- B: Dropping messages loses requests.
- C: Premium raises the size limit, but batches still have a maximum.
- D: Correct. Send the current batch and start a new one so every message is sent.

ServiceBusMessageBatch respects the tier's size limit; roll over to a new batch.

📘 Source: [Structure messages for AI workloads](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/4-structure-messages-ai-workloads)

</details>

## 17. `lp7m1-017`

After duplicate detection is turned on for a queue, some distinct inference requests silently disappear. What's the most likely cause?

- **A.** Producers share one correlation_id across every stage
- **B.** Messages don't set content_type to application/json
- **C.** Producers reuse one message_id for different requests
- **D.** The queue's max_delivery_count is too low

<details><summary>💡 Hint</summary>

Duplicate detection decides what counts as "the same" by one property.

</details>

<details><summary>✅ Answer</summary>

**C.** Producers reuse one message_id for different requests

- A: correlation_id is for tracing, and duplicate detection doesn't use it.
- B: content_type is informational. It doesn't cause drops.
- C: Correct. Duplicate detection drops messages whose message_id it has already seen within the window.
- D: Delivery count affects retries of received messages, not messages vanishing on send.

Duplicate detection uses message_id to discard repeats within the detection window. Generate a unique message_id per message; use correlation_id for tracing.

📘 Source: [Structure messages for AI workloads](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/4-structure-messages-ai-workloads)

</details>

## 18. `lp7m1-018`

Real-time classification results are useless after five minutes, and the team needs to see which requests weren't processed in time. What should you configure?

- **A.** A 5-minute time_to_live plus dead-lettering on message expiration
- **B.** A 5-minute lock duration plus abandon on timeout
- **C.** Defer each message for up to 5 minutes
- **D.** A 5-minute time_to_live plus max_delivery_count of 1

<details><summary>💡 Hint</summary>

One setting gives each request a lifetime. Another keeps a record of the ones that ran out.

</details>

<details><summary>✅ Answer</summary>

**A.** A 5-minute time_to_live plus dead-lettering on message expiration

- A: Correct. Expired messages then go to the DLQ, where you can see which requests were late.
- B: Lock duration controls processing time per delivery, not the request's useful lifetime.
- C: Deferral postpones processing. It doesn't express when a request becomes useless.
- D: The TTL expires stale requests, but without dead-lettering on expiration you lose sight of them.

Set time_to_live to match how time-sensitive a request is, and enable dead-lettering on message expiration so expired requests are visible in the DLQ.

📘 Source: [Structure messages for AI workloads](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/4-structure-messages-ai-workloads)

</details>

## 19. `lp7m1-019`

A message contains malformed JSON that will never parse, however often it's retried. Which settlement should the processor use?

- **A.** abandon_message() for a retry
- **B.** dead_letter_message() with a reason
- **C.** complete_message() on it
- **D.** defer_message() until later

<details><summary>💡 Hint</summary>

A message that can never be processed shouldn't be retried.

</details>

<details><summary>✅ Answer</summary>

**B.** dead_letter_message() with a reason

- A: Abandoning retries a message that will never succeed.
- B: Correct. Dead-letter it with a reason and description for investigation.
- C: Completing hides the failure as a success.
- D: Deferring is for messages you expect to handle later.

Dead-letter permanent failures immediately; abandon transient ones.

📘 Source: [Process messages reliably](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/5-process-messages-reliably)

</details>

## 20. `lp7m1-020`

What is the default max_delivery_count for a Service Bus queue?

- **A.** 5
- **B.** 10
- **C.** 100
- **D.** 3

<details><summary>💡 Hint</summary>

There's a default number of delivery attempts before dead-lettering.

</details>

<details><summary>✅ Answer</summary>

**B.** 10

- A: Learn suggests 3–5 as a lower setting, not the default.
- B: Correct. The default is 10.
- C: That isn't the default.
- D: Learn suggests 3–5 as a lower setting, not the default.

Exceeding it dead-letters the message with MaxDeliveryCountExceeded.

📘 Source: [Process messages reliably](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/5-process-messages-reliably)

</details>

## 21. `lp7m1-021`

Match each processing outcome to the settlement call.

Choices: **complete_message()** · **abandon_message()** · **dead_letter_message()** · **defer_message()**

- The result was written to the results store
- The model service timed out; a retry may work
- The request names a model that isn't supported
- A required dependency isn't available yet; handle it later by sequence number

<details><summary>💡 Hint</summary>

Done, try again, never, or later by sequence number.

</details>

<details><summary>✅ Answer</summary>

- The result was written to the results store → **complete_message()**. Normal success path.
- The model service timed out; a retry may work → **abandon_message()**. Transient error: release the lock for redelivery.
- The request names a model that isn't supported → **dead_letter_message()**. Will never succeed: dead-letter with a reason.
- A required dependency isn't available yet; handle it later by sequence number → **defer_message()**. Defer, then receive_deferred_messages().

Peek-lock lets the processor report each outcome explicitly.

📘 Source: [Process messages reliably](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/5-process-messages-reliably)

</details>

## 22. `lp7m1-022`

For each statement, select Yes if the statement is true. Otherwise, select No. A team inspects a queue's dead-letter queue.

| Statement | Yes / No |
|---|---|
| The DLQ must be created before messages can be dead-lettered. | ☐ |
| Messages stay in the DLQ until someone receives and completes them. | ☐ |
| Messages dead-lettered after too many deliveries carry the reason MaxDeliveryCountExceeded. | ☐ |
| Building the path `<queue>`/$deadletterqueue by hand is the recommended way to read it. | ☐ |

<details><summary>💡 Hint</summary>

Every queue gets a DLQ automatically. Messages stay there until handled, and the SDK can build the path for you.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The DLQ must be created before messages can be dead-lettered. | No | It exists automatically for every queue and subscription. |
| Messages stay in the DLQ until someone receives and completes them. | Yes | DLQ messages persist until explicitly handled. |
| Messages dead-lettered after too many deliveries carry the reason MaxDeliveryCountExceeded. | Yes | That's the reason Service Bus sets. |
| Building the path `<queue>`/$deadletterqueue by hand is the recommended way to read it. | No | Use sub_queue=ServiceBusSubQueue.DEAD_LETTER. |

Monitor DLQ counts and reprocess only after fixing the root cause.

📘 Source: [Process messages reliably](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/5-process-messages-reliably)

</details>

## 23. `lp7m1-023`

Summarizing a long document takes about 3 minutes, and the same messages are being processed twice. The queue uses default settings. What is the cause and the fix?

- **A.** Receive-and-delete mode is redelivering; switch to peek-lock
- **B.** Duplicate detection is off; turn it on to stop the second delivery
- **C.** The 1-minute lock expires during processing; use AutoLockRenewer
- **D.** max_delivery_count is 10; lower it to 1

<details><summary>💡 Hint</summary>

The default lock is shorter than the processing time.

</details>

<details><summary>✅ Answer</summary>

**C.** The 1-minute lock expires during processing; use AutoLockRenewer

- A: Receive-and-delete never redelivers; peek-lock is already the default.
- B: Duplicate detection drops duplicate sends, not redeliveries after lock expiry.
- C: Correct. The lock (1 minute by default, 5 maximum) expires and another consumer receives the message; renew it.
- D: That would dead-letter messages after one attempt instead of fixing the lock.

Renew locks (renew_message_lock or AutoLockRenewer) or use a two-phase approach for long work.

📘 Source: [Process messages reliably](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/5-process-messages-reliably)

</details>

## 24. `lp7m1-024`

After fixing a parser bug, you want to retry 2,000 dead-lettered requests. What is the correct reprocessing pattern?

- **A.** Abandon each DLQ message so it returns to the main queue
- **B.** Delete the queue and recreate it to clear out the DLQ
- **C.** Set max_delivery_count to 0 so the DLQ empties by itself
- **D.** Resend a copy to the original queue, then complete the DLQ message

<details><summary>💡 Hint</summary>

Don't move the dead-lettered message itself.

</details>

<details><summary>✅ Answer</summary>

**D.** Resend a copy to the original queue, then complete the DLQ message

- A: Abandoning in the DLQ doesn't move it back to the main queue.
- B: That loses every message.
- C: That isn't how DLQ messages are released.
- D: Correct. Resubmit a new message with the same body and properties, then complete the DLQ copy.

Confirm the fix first, or messages will cycle back into the DLQ.

📘 Source: [Process messages reliably](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/5-process-messages-reliably)

</details>

## 25. `lp7m1-025`

Each scanned document takes about 8 minutes to process, and other workers start processing the same message partway through. What is the best fix?

- **A.** Set the queue's lock duration to 10 minutes
- **B.** Switch the receiver to receive-and-delete mode
- **C.** Raise max_delivery_count to 20
- **D.** Register each message with AutoLockRenewer for 10 minutes

<details><summary>💡 Hint</summary>

The lock can't be set long enough on the queue. Something has to keep extending it while you work.

</details>

<details><summary>✅ Answer</summary>

**D.** Register each message with AutoLockRenewer for 10 minutes

- A: Queue lock duration can be at most 5 minutes, so 10 isn't possible.
- B: That removes the message on delivery, so a crash would lose the document.
- C: More attempts don't stop the lock from expiring mid-processing.
- D: Correct. AutoLockRenewer keeps renewing the lock in the background, which keeps other workers from getting the message.

Queue lock duration defaults to 1 minute and can be set to at most 5. For longer work, renew the lock (renew_message_lock or AutoLockRenewer) or use a two-phase approach.

📘 Source: [Process messages reliably](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/5-process-messages-reliably)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
