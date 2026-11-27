# Practice: LP7 · M5 Deliver real-time AI experiences with Azure Web PubSub

> 24 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp7m5.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-7/real-time-ai-web-pubsub)

## 1. `lp7m5-001`

An on-call developer, an incident commander and a database specialist must all watch the same AI investigation update live. Which approach fits best?

- **A.** Azure Web PubSub with an operation group
- **B.** An SSE stream tied to the developer's request
- **C.** Polling every 60 seconds
- **D.** Direct HTTP streaming to the first requester

<details><summary>💡 Hint</summary>

Several people, independently connected, all watching the same thing.

</details>

<details><summary>✅ Answer</summary>

**A.** Azure Web PubSub with an operation group

- A: Correct. One worker publish reaches every authorized connection in the group.
- B: SSE from one request doesn't fan out to others by itself.
- C: Polling is for infrequent changes and multiplies requests.
- D: The stream is tied to one request; others need a relay.

Choose Web PubSub when independent recipients or group delivery justify it.

📘 Source: [Choose a real-time client delivery approach](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/2-choose-real-time-client-delivery)

</details>

## 2. `lp7m5-002`

Which content type does a Server-Sent Events response use?

- **A.** application/cloudevents+json
- **B.** text/event-stream
- **C.** multipart/form-data
- **D.** application/json

<details><summary>💡 Hint</summary>

SSE responses have their own MIME type.

</details>

<details><summary>✅ Answer</summary>

**B.** text/event-stream

- A: That's for publishing CloudEvents to Event Grid.
- B: Correct. SSE uses a long-lived text/event-stream response.
- C: That's form uploads.
- D: That's ordinary JSON.

SSE adds event data, names and IDs on top of a long-lived HTTP response.

📘 Source: [Choose a real-time client delivery approach](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/2-choose-real-time-client-delivery)

</details>

## 3. `lp7m5-003`

For each statement, select Yes if the statement is true. Otherwise, select No. An assistant streams a log summary to the browser with SSE.

| Statement | Yes / No |
|---|---|
| The browser's EventSource normally tries to reconnect after an interruption. | ☐ |
| After reconnecting, missed events are replayed even if the server never stored them. | ☐ |
| Approving a finding should go through a separate authenticated HTTP request. | ☐ |
| SSE lets the browser send approvals back on the same event stream. | ☐ |

<details><summary>💡 Hint</summary>

EventSource reconnects by itself, but replay depends on what the server kept.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The browser's EventSource normally tries to reconnect after an interruption. | Yes | EventSource manages reconnection. |
| After reconnecting, missed events are replayed even if the server never stored them. | No | The server needs retained events and resume logic. |
| Approving a finding should go through a separate authenticated HTTP request. | Yes | SSE is one-way; commands use HTTP. |
| SSE lets the browser send approvals back on the same event stream. | No | SSE is one-way; commands go through separate HTTP requests. |

SSE is one-way with reconnection; resume depends on retained events.

📘 Source: [Choose a real-time client delivery approach](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/2-choose-real-time-client-delivery)

</details>

## 4. `lp7m5-004`

An existing app uses Azure SignalR Service hubs and client method invocation. A developer proposes swapping in the Web PubSub client library. What does Learn say?

- **A.** Web PubSub clients are drop-in replacements for SignalR clients
- **B.** Switch to polling first, then to Web PubSub
- **C.** SignalR is required for every WebSocket application
- **D.** Evaluate SignalR integration; it isn't drop-in

<details><summary>💡 Hint</summary>

SignalR and Web PubSub are related, but their programming models differ.

</details>

<details><summary>✅ Answer</summary>

**D.** Evaluate SignalR integration; it isn't drop-in

- A: Learn says not to assume this.
- B: Polling isn't a migration step for this.
- C: Web PubSub suits WebSocket apps with their own contract.
- D: Correct. SignalR has its own programming model (hubs, method invocation).

SignalR and Web PubSub are related but distinct services.

📘 Source: [Choose a real-time client delivery approach](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/2-choose-real-time-client-delivery)

</details>

## 5. `lp7m5-005`

An archived-log analysis takes several minutes and only ever shows three states: queued, processing and completed. One user watches it. Which delivery approach does Learn suggest evaluating first?

- **A.** A WebSocket that the browser holds open for the whole analysis
- **B.** Periodic status requests against a status endpoint
- **C.** Azure Web PubSub with a group per user
- **D.** Azure SignalR Service hubs

<details><summary>💡 Hint</summary>

Start with the simplest option that meets the experience you need.

</details>

<details><summary>✅ Answer</summary>

**B.** Periodic status requests against a status endpoint

- A: A live channel adds complexity that three state changes don't justify.
- B: Correct. Infrequent background status changes can be served by polling, without a live messaging channel.
- C: Web PubSub fits many independent recipients or group delivery, which this scenario doesn't need.
- D: SignalR is for hub-based app models, which isn't needed for three status updates.

Begin with the client experience. For a single generated answer, evaluate HTTP streaming or SSE; for infrequent background status, evaluate polling; choose Web PubSub for independently connected recipients, group delivery or connection scale.

📘 Source: [Choose a real-time client delivery approach](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/2-choose-real-time-client-delivery)

</details>

## 6. `lp7m5-006`

A FastAPI endpoint streams a generated answer with SSE, and locally the text appears word by word. In production, behind a reverse proxy, the whole answer appears at once at the end. What's the likely cause?

- **A.** The model sends the whole answer at once in production
- **B.** A proxy, compression layer or framework is buffering the response
- **C.** The browser's EventSource waits for the connection to close
- **D.** SSE only works over HTTP/1.0

<details><summary>💡 Hint</summary>

It works locally. What sits between the app and the browser in production?

</details>

<details><summary>✅ Answer</summary>

**B.** A proxy, compression layer or framework is buffering the response

- A: It streams locally with the same model, which points to buffering along the way.
- B: Correct. Verify incremental delivery through the actual hosting stack, because layers in between can buffer.
- C: EventSource processes events as they arrive when nothing buffers them.
- D: That isn't the issue. The response is being held back somewhere between the app and the browser.

An HTTP stream isn't automatically visible as soon as the backend writes a chunk: a reverse proxy, compression layer or framework can buffer it. Verify incremental delivery through the real hosting stack.

📘 Source: [Choose a real-time client delivery approach](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/2-choose-real-time-client-delivery)

</details>

## 7. `lp7m5-007`

A developer proposes publishing new investigation requests to a Web PubSub group so that "a worker picks them up". What's wrong?

- **A.** Web PubSub can't carry JSON payloads to clients
- **B.** Groups can hold at most one connection each
- **C.** Groups broadcast; they don't assign work to one worker
- **D.** Groups require Durable Functions to work at all

<details><summary>💡 Hint</summary>

A group delivers to everyone in it. It doesn't hand one job to one worker.

</details>

<details><summary>✅ Answer</summary>

**C.** Groups broadcast; they don't assign work to one worker

- A: Web PubSub carries JSON envelopes.
- B: Groups collect many connections; the issue is broadcast vs reliable assignment.
- C: Correct. Use a queue or workflow for backend processing.
- D: Web PubSub doesn't require Durable Functions.

A group isn't a Service Bus subscription or competing-consumer queue.

📘 Source: [Separate client delivery from backend coordination](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/3-separate-client-delivery-backend-coordination)

</details>

## 8. `lp7m5-008`

For each statement, select Yes if the statement is true. Otherwise, select No. A worker stores a completed report, then crashes before publishing the completion notification.

| Statement | Yes / No |
|---|---|
| Connected browsers might keep showing older progress. | ☐ |
| Clients can recover the completed result through the status endpoint. | ☐ |
| The AI operation must be repeated to send the notification. | ☐ |
| A Web PubSub group publish and the database write commit as one atomic transaction. | ☐ |

<details><summary>💡 Hint</summary>

The durable record is the truth. A missed notification doesn't undo completed work.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Connected browsers might keep showing older progress. | Yes | The publish never happened. |
| Clients can recover the completed result through the status endpoint. | Yes | The durable record is authoritative. |
| The AI operation must be repeated to send the notification. | No | Recovery via status avoids repeating the AI work. |
| A Web PubSub group publish and the database write commit as one atomic transaction. | No | A database write and a Web PubSub publish aren't one atomic transaction. |

Persist first; use an outbox when eventual notification is required.

📘 Source: [Separate client delivery from backend coordination](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/3-separate-client-delivery-backend-coordination)

</details>

## 9. `lp7m5-009`

A responder closes the browser tab during an investigation. What should happen to the backend work?

- **A.** It's cancelled automatically when the connection drops
- **B.** It continues; cancelling is a separate command
- **C.** It pauses until any responder reconnects
- **D.** It's marked failed because delivery failed

<details><summary>💡 Hint</summary>

Closing a tab isn't a decision to stop the investigation.

</details>

<details><summary>✅ Answer</summary>

**B.** It continues; cancelling is a separate command

- A: Disconnecting isn't a cancellation.
- B: Correct. Lost connections don't cancel work; cancellation is a deliberate command.
- C: Work doesn't depend on a connected browser.
- D: Delivery problems don't turn successful processing into failure.

Separate processing outcomes from delivery problems.

📘 Source: [Separate client delivery from backend coordination](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/3-separate-client-delivery-backend-coordination)

</details>

## 10. `lp7m5-010`

A worker updates the operation record in the database and must eventually publish a matching Web PubSub notification, even if it crashes right after the database write. Which pattern fits?

- **A.** Publish the notification first, then write to the database
- **B.** A transactional outbox: store the notification with the state change, and let a publisher send pending ones
- **C.** Ask each browser to reconnect every minute
- **D.** Rely on Web PubSub to retry the notification after the crash

<details><summary>💡 Hint</summary>

Put the notification somewhere durable, in the same transaction as the state change.

</details>

<details><summary>✅ Answer</summary>

**B.** A transactional outbox: store the notification with the state change, and let a publisher send pending ones

- A: Clients could then see "completed" before the result exists.
- B: Correct. Recording the notification in the same transaction means a separate publisher can send it later.
- C: Reconnecting doesn't produce the missing notification. Clients would need to read the status API.
- D: Web PubSub can't send something the crashed worker never published.

Persist state before notifying. When eventual publishing is required, record the notification with the state change in a transactional outbox; a separate publisher sends pending notifications and marks them sent.

📘 Source: [Separate client delivery from backend coordination](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/3-separate-client-delivery-backend-coordination)

</details>

## 11. `lp7m5-011`

A browser should only observe updates for one investigation. Which role should its Web PubSub token include?

- **A.** Web PubSub Service Owner
- **B.** `webpubsub.joinLeaveGroup.<that-group>`
- **C.** `webpubsub.joinLeaveGroup` (unrestricted)
- **D.** `webpubsub.sendToGroup`

<details><summary>💡 Hint</summary>

Observers need to join one group and nothing more.

</details>

<details><summary>✅ Answer</summary>

**B.** `webpubsub.joinLeaveGroup.<that-group>`

- A: That's an Azure RBAC role for backend identities.
- B: Correct. It permits joining and leaving that one group, not publishing.
- C: Unrestricted join lets it join any group.
- D: That lets the client publish to groups.

Grant the smallest group-scoped role for receive-only clients.

📘 Source: [Negotiate authenticated client connections](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/4-negotiate-authenticated-client-connections)

</details>

## 12. `lp7m5-012`

The negotiation endpoint receives userId and groupName in the request body from the browser. What should the backend do?

- **A.** Derive identity and group on the server
- **B.** Copy them into the token after URL-encoding them
- **C.** Use the values if they contain no forward slashes
- **D.** Trust the values, since the user is already signed in

<details><summary>💡 Hint</summary>

Never trust what the browser says about who it is.

</details>

<details><summary>✅ Answer</summary>

**A.** Derive identity and group on the server

- A: Correct. Browser-supplied IDs and group names aren't identity assertions.
- B: Encoding doesn't authorize anything.
- C: Format checks don't establish authorization.
- D: Signed-in status doesn't make client fields trustworthy.

Authorize the operation, then derive user ID and group on the server.

📘 Source: [Negotiate authenticated client connections](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/4-negotiate-authenticated-client-connections)

</details>

## 13. `lp7m5-013`

For each statement, select Yes if the statement is true. Otherwise, select No. A backend uses its managed identity with Microsoft Entra ID to generate client tokens.

| Statement | Yes / No |
|---|---|
| The identity needs the generateToken action and clientConnection/write. | ☐ |
| Web PubSub Service Owner includes both permissions but grants broader access. | ☐ |
| Developer role assignments automatically apply to the deployed managed identity. | ☐ |

<details><summary>💡 Hint</summary>

Token generation needs two permissions. Developer role assignments don't carry over.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The identity needs the generateToken action and clientConnection/write. | Yes | Both permissions are required. |
| Web PubSub Service Owner includes both permissions but grants broader access. | Yes | A custom role can be narrower. |
| Developer role assignments automatically apply to the deployed managed identity. | No | Assign deployed identities their own roles. |

Backend Azure permissions and client token roles are separate boundaries.

📘 Source: [Negotiate authenticated client connections](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/4-negotiate-authenticated-client-connections)

</details>

## 14. `lp7m5-014`

A responder is removed from an incident while their browser tab is still connected. What should the backend do?

- **A.** Deny negotiation, revoke permission, remove from group
- **B.** Send a message asking the browser to leave the group
- **C.** Nothing; the client token will expire on its own soon
- **D.** Rotate the Web PubSub access key for the service

<details><summary>💡 Hint</summary>

Removing access means stopping future connections and cutting off the current one.

</details>

<details><summary>✅ Answer</summary>

**A.** Deny negotiation, revoke permission, remove from group

- A: Correct. Expiry doesn't revoke active connections; act on each tracked connection.
- B: The browser isn't trusted to enforce access.
- C: Expiry only blocks new connections.
- D: Key rotation doesn't target this user's connection.

Track connection IDs; use revoke_permission() and remove_connection_from_group().

📘 Source: [Negotiate authenticated client connections](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/4-negotiate-authenticated-client-connections)

</details>

## 15. `lp7m5-015`

An operation group's name must not expose tenant or operation IDs, and IDs may contain delimiter characters. How does Learn suggest naming the group?

- **A.** Join the tenant and operation IDs with a hyphen
- **B.** Use the signed-in user's email address
- **C.** Hash an unambiguous encoding of the tenant and operation IDs into a stable, opaque name
- **D.** Let the browser choose a random group name and send it to the backend

<details><summary>💡 Hint</summary>

You want a name that's stable, collision-free, and reveals nothing.

</details>

<details><summary>✅ Answer</summary>

**C.** Hash an unambiguous encoding of the tenant and operation IDs into a stable, opaque name

- A: Delimiters inside IDs could collide, and the IDs would be exposed.
- B: That exposes personal data and scopes the group to the user, not to the operation.
- C: Correct. This avoids collisions from delimiters and keeps IDs out of routing names.
- D: Browser-supplied group names aren't trusted.

Derive a stable, opaque group name by hashing an unambiguous encoding of tenant and operation IDs. That avoids collisions from delimiters and avoids exposing IDs in routing names.

📘 Source: [Negotiate authenticated client connections](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/4-negotiate-authenticated-client-connections)

</details>

## 16. `lp7m5-016`

Which Python client callback type delivers messages that a service publishes to a group?

- **A.** CallbackType.GROUP_MESSAGE
- **B.** CallbackType.CONNECTED
- **C.** CallbackType.SERVER_MESSAGE
- **D.** CallbackType.REJOIN_GROUP_FAILED

<details><summary>💡 Hint</summary>

The callback type is named after where the message was sent.

</details>

<details><summary>✅ Answer</summary>

**A.** CallbackType.GROUP_MESSAGE

- A: Correct. Group broadcasts arrive through GROUP_MESSAGE.
- B: CONNECTED reports connection, not messages.
- C: SERVER_MESSAGE is for messages sent directly to a connection or user.
- D: That reports a failed rejoin.

Route group notifications through validated handlers under a lock.

📘 Source: [Publish AI updates to operation groups](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/5-publish-ai-updates-operation-groups)

</details>

## 17. `lp7m5-017`

For each statement, select Yes if the statement is true. Otherwise, select No. A worker publishes notification `op42-event-15` with sequence 15.

| Statement | Yes / No |
|---|---|
| If the publish is retried, it should reuse event ID op42-event-15 and sequence 15. | ☐ |
| A successful send_to_group() proves every responder saw the update. | ☐ |
| The final text batch alone shows the operation succeeded. | ☐ |

<details><summary>💡 Hint</summary>

Retries keep the same identity. Sending isn't proof of reading. Notifications don't replace durable state.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| If the publish is retried, it should reuse event ID op42-event-15 and sequence 15. | Yes | One logical update keeps its IDs across retries. |
| A successful send_to_group() proves every responder saw the update. | No | Publish success doesn't prove browser processing or human receipt. |
| The final text batch alone shows the operation succeeded. | No | Wait for operation.completed; validation or persistence can still fail. |

Persist, then publish with stable IDs; completion is its own event.

📘 Source: [Publish AI updates to operation groups](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/5-publish-ai-updates-operation-groups)

</details>

## 18. `lp7m5-018`

Generated findings arrive as Markdown and the browser renders them as HTML. What does Learn require?

- **A.** Strip the sequence numbers before rendering
- **B.** Render raw HTML for richer formatting
- **C.** Trust it because it came from your own model
- **D.** Render as text; sanitize Markdown-to-HTML

<details><summary>💡 Hint</summary>

Generated text is untrusted, so render it safely.

</details>

<details><summary>✅ Answer</summary>

**D.** Render as text; sanitize Markdown-to-HTML

- A: Sequences are needed for ordering, and aren't the issue.
- B: Raw HTML risks script injection.
- C: Model output is untrusted.
- D: Correct. Model output isn't trusted browser markup.

Validate payloads before mutating view state.

📘 Source: [Publish AI updates to operation groups](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/5-publish-ai-updates-operation-groups)

</details>

## 19. `lp7m5-019`

The browser has applied updates through sequence 15 and receives sequence 17. What should it do?

- **A.** Hold 17 and fetch current operation state
- **B.** Close the connection and reload the whole page
- **C.** Apply 17 and continue with the stream
- **D.** Ignore 17 because it's a duplicate

<details><summary>💡 Hint</summary>

Sequence 16 is missing. Don't apply 17 on top of a gap.

</details>

<details><summary>✅ Answer</summary>

**A.** Hold 17 and fetch current operation state

- A: Correct. A gap means a missed update; reconcile with a snapshot.
- B: Reloading isn't the recovery step Learn describes.
- C: Applying out of order can corrupt generated text.
- D: Duplicates have the same or lower sequence.

Duplicate → ignore; next → apply; gap → hold and fetch state.

📘 Source: [Design reconnection and operation recovery](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/6-design-reconnection-operation-recovery)

</details>

## 20. `lp7m5-020`

Put Learn's recovery flow for an operation in order.

- Buffer notifications while requesting the status snapshot
- Connect and wait for operation-group membership
- Discard buffered events at or below the watermark and apply newer ones
- Register handlers and mark the view unsynchronized
- Replace the view with the snapshot and set last_sequence to its watermark

<details><summary>💡 Hint</summary>

Mark the view unsynchronized, connect and join, buffer, then rebuild from the snapshot.

</details>

<details><summary>✅ Answer</summary>

1. Register handlers and mark the view unsynchronized
2. Connect and wait for operation-group membership
3. Buffer notifications while requesting the status snapshot
4. Replace the view with the snapshot and set last_sequence to its watermark
5. Discard buffered events at or below the watermark and apply newer ones

Subscribing before requesting the snapshot avoids losing updates in between.

📘 Source: [Design reconnection and operation recovery](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/6-design-reconnection-operation-recovery)

</details>

## 21. `lp7m5-021`

For each statement, select Yes if the statement is true. Otherwise, select No. A browser reconnects with a brand-new connection after the reliable session couldn't be recovered.

| Statement | Yes / No |
|---|---|
| It needs fresh negotiation and its group membership restored. | ☐ |
| auto_rejoin_groups also recreates memberships the server assigned to the old connection. | ☐ |
| A snapshot whose lastSequence is lower than what the view shows should replace the view. | ☐ |
| If completion was the last event and was missed, no later gap will reveal it. | ☐ |

<details><summary>💡 Hint</summary>

A new connection means new negotiation, and server-assigned groups don't come back by themselves.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| It needs fresh negotiation and its group membership restored. | Yes | New connections reauthorize and restore membership. |
| auto_rejoin_groups also recreates memberships the server assigned to the old connection. | No | It tracks only groups joined by client code. |
| A snapshot whose lastSequence is lower than what the view shows should replace the view. | No | Don't replace newer output with an older snapshot. |
| If completion was the last event and was missed, no later gap will reveal it. | Yes | Reconcile after reconnects and inactivity, not only on gaps. |

Recovery = reauthorize, restore membership, reconcile durable state.

📘 Source: [Design reconnection and operation recovery](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/6-design-reconnection-operation-recovery)

</details>

## 22. `lp7m5-022`

A batcher only checks elapsed time when a new token arrives, and during model pauses short batches sit unsent. What fixes this?

- **A.** Lower the item threshold to a single fragment
- **B.** Publish every model token immediately instead
- **C.** Flush on a timer, not only on new fragments
- **D.** Increase the batch size budget for each batch

<details><summary>💡 Hint</summary>

A batch that waits for the next token never flushes during a pause.

</details>

<details><summary>✅ Answer</summary>

**C.** Flush on a timer, not only on new fragments

- A: One-item batches defeat batching.
- B: Per-token publishing adds overhead and fan-out traffic.
- C: Correct. Time-based flushing must not depend on the next fragment arriving.
- D: Larger batches make the delay worse.

Flush on time, count, size or operation boundary.

📘 Source: [Batch updates and support slow clients](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/7-batch-updates-support-slow-clients)

</details>

## 23. `lp7m5-023`

Match each update type to Learn's overflow policy.

Choices: **Keep only the newest** · **Preserve order, or restore from durable state** · **Persist and keep discoverable via status**

- Progress snapshots
- Generated-text deltas
- Approval requests and terminal outcomes

<details><summary>💡 Hint</summary>

Some updates can be replaced by newer ones. Others must never be dropped.

</details>

<details><summary>✅ Answer</summary>

- Progress snapshots → **Keep only the newest**. A newer snapshot replaces older ones.
- Generated-text deltas → **Preserve order, or restore from durable state**. Deltas depend on earlier deltas.
- Approval requests and terminal outcomes → **Persist and keep discoverable via status**. They must survive missed delivery.

Define which updates can be coalesced before choosing an overflow policy.

📘 Source: [Batch updates and support slow clients](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/7-batch-updates-support-slow-clients)

</details>

## 24. `lp7m5-024`

During heavy load, a worker can't keep up with publishing a progress snapshot for every log file it scans. Which overflow policy does Learn give for progress snapshots?

- **A.** Persist every snapshot and keep each one discoverable
- **B.** Preserve every snapshot in order
- **C.** Keep only the newest snapshot and drop older pending ones
- **D.** Block the AI work until every snapshot is delivered

<details><summary>💡 Hint</summary>

Which kind of update makes the previous one useless?

</details>

<details><summary>✅ Answer</summary>

**C.** Keep only the newest snapshot and drop older pending ones

- A: That policy is for approval requests and terminal outcomes.
- B: Strict order is for generated-text deltas, which can't be skipped.
- C: Correct. A newer snapshot replaces older progress, so older ones can be dropped.
- D: Slowing the work for progress messages isn't the policy Learn gives.

Overflow policies differ by update type: progress snapshots keep only the newest; generated-text deltas preserve order or restore from durable state; approval requests and terminal outcomes are persisted and stay discoverable via status.

📘 Source: [Batch updates and support slow clients](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/7-batch-updates-support-slow-clients)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
