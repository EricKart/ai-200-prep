# Practice: LP7 · M4 Orchestrate durable AI workflows with Azure Durable Functions

> 23 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp7m4.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-7/orchestrate-durable-functions)

## 1. `lp7m4-001`

An orchestrator needs to call a classification model for each document. Where should the model call go?

- **A.** Directly in the orchestrator
- **B.** In an activity function
- **C.** In the client function
- **D.** In an entity function

<details><summary>💡 Hint</summary>

Orchestrators coordinate. The function type that does real I/O is a different one.

</details>

<details><summary>✅ Answer</summary>

**B.** In an activity function

- A: Orchestrators must stay deterministic and avoid external calls.
- B: Correct. Activities perform nondeterministic work such as model calls.
- C: Clients start and manage orchestrations.
- D: Entities manage small pieces of durable state.

The orchestrator schedules activities and records only their results.

📘 Source: [Separate orchestration logic from activity work](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/2-separate-orchestrator-activity-responsibilities)

</details>

## 2. `lp7m4-002`

Which API gives an orchestrator a replay-safe current time?

- **A.** datetime.now() in Python
- **B.** context.current_utc_datetime
- **C.** time.time() from the time module
- **D.** datetime.utcnow() in Python

<details><summary>💡 Hint</summary>

The context object gives you a time value that's the same on every replay.

</details>

<details><summary>✅ Answer</summary>

**B.** context.current_utc_datetime

- A: Language-native time APIs change between replays.
- B: Correct. It returns the same value during replay.
- C: Nondeterministic across replays.
- D: Nondeterministic across replays.

Use context.current_utc_datetime and context.new_uuid() in orchestrators.

📘 Source: [Separate orchestration logic from activity work](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/2-separate-orchestrator-activity-responsibilities)

</details>

## 3. `lp7m4-003`

For each statement, select Yes if the statement is true. Otherwise, select No. A developer reviews an orchestrator function.

| Statement | Yes / No |
|---|---|
| Using time.sleep(60) to pause between steps is acceptable. | ☐ |
| Branching on the result returned by an activity is acceptable. | ☐ |
| Calling uuid.uuid4() for an operation ID is acceptable. | ☐ |
| Passing a blob URL instead of the whole document to an activity is recommended. | ☐ |

<details><summary>💡 Hint</summary>

No sleeping, no random IDs in the orchestrator. Branching on results is fine.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Using time.sleep(60) to pause between steps is acceptable. | No | Blocking waits aren't allowed; use durable timers. |
| Branching on the result returned by an activity is acceptable. | Yes | Results of durable tasks are safe inputs to decisions. |
| Calling uuid.uuid4() for an operation ID is acceptable. | No | Use context.new_uuid() for a deterministic identifier. |
| Passing a blob URL instead of the whole document to an activity is recommended. | Yes | Pass references to keep history small. |

Orchestrators coordinate deterministically; activities do the I/O.

📘 Source: [Separate orchestration logic from activity work](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/2-separate-orchestrator-activity-responsibilities)

</details>

## 4. `lp7m4-004`

Logs show the same "Starting classification" orchestrator message five times for one workflow, although the activity ran once. Why, and what's the fix?

- **A.** The client started five orchestrations; use a fixed instance ID
- **B.** Application Insights duplicates logs; turn off sampling for it
- **C.** The activity ran five times; add a retry policy to it
- **D.** Replay reruns the log line; check context.is_replaying

<details><summary>💡 Hint</summary>

Orchestrator code runs more than once. Is there a way to tell when it's running again?

</details>

<details><summary>✅ Answer</summary>

**D.** Replay reruns the log line; check context.is_replaying

- A: One instance replaying explains this.
- B: Duplicates come from replay, not sampling.
- C: The activity ran once; the duplicates come from replay.
- D: Correct. Replay can run orchestrator log statements again.

Activity logs reflect real work; orchestrator logs can repeat during replay.

📘 Source: [Separate orchestration logic from activity work](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/2-separate-orchestrator-activity-responsibilities)

</details>

## 5. `lp7m4-005`

Orchestrations that pass full extracted text and model responses between steps have become slow, and history storage is growing. What does Learn recommend?

- **A.** Move the model calls into the orchestrator to avoid passing data
- **B.** Switch the storage provider to Azure Storage
- **C.** Store content in Blob Storage; pass references
- **D.** Compress the payloads inside the orchestrator with a random salt

<details><summary>💡 Hint</summary>

Everything passed between steps is saved in history. Keep it small.

</details>

<details><summary>✅ Answer</summary>

**C.** Store content in Blob Storage; pass references

- A: Model calls in the orchestrator break determinism.
- B: The provider choice doesn't fix oversized history.
- C: Correct. Large payloads increase storage operations, replay time and memory.
- D: Random values don't belong in orchestrators, and the payload stays in history.

Activities read and write large content; orchestrators get IDs, URLs and scores.

📘 Source: [Separate orchestration logic from activity work](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/2-separate-orchestrator-activity-responsibilities)

</details>

## 6. `lp7m4-006`

You're starting a new Durable Functions application and choosing a storage provider. Which one does Microsoft recommend for new apps?

- **A.** The Azure Storage provider
- **B.** Azure Cache for Redis
- **C.** Azure Cosmos DB as a custom provider
- **D.** Durable Task Scheduler

<details><summary>💡 Hint</summary>

Microsoft now offers a managed backend built specifically for durable task state.

</details>

<details><summary>✅ Answer</summary>

**D.** Durable Task Scheduler

- A: It's still available for existing apps or when you want to manage storage yourself, but it isn't the recommendation for new apps.
- B: Redis isn't a Durable Functions storage provider.
- C: Learn's recommendation for new apps is the managed Durable Task Scheduler.
- D: Correct. It's the recommended managed storage provider for new Durable Functions apps.

For new Durable Functions applications, Microsoft recommends Durable Task Scheduler as the managed storage provider. The Azure Storage provider remains for existing apps or self-managed storage.

📘 Source: [Separate orchestration logic from activity work](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/2-separate-orchestrator-activity-responsibilities)

</details>

## 7. `lp7m4-007`

An orchestrator passes a model API key to each activity as part of the activity input, so that activities can call the model. What's wrong with this design?

- **A.** Activities can't receive string inputs
- **B.** The key makes the orchestrator non-deterministic
- **C.** Inputs are saved in orchestration history, so the key is stored there; use managed identity and Key Vault instead
- **D.** Nothing, as long as the key is rotated every month

<details><summary>💡 Hint</summary>

Think about where Durable Functions keeps inputs and outputs.

</details>

<details><summary>✅ Answer</summary>

**C.** Inputs are saved in orchestration history, so the key is stored there; use managed identity and Key Vault instead

- A: Activities take serializable inputs, including strings.
- B: The key is the same every time. The problem is where it's stored.
- C: Correct. Don't place secrets in orchestration inputs or outputs.
- D: Rotation helps, but the secret would still be kept in durable history.

Orchestration inputs and outputs are serialized into durable history. Don't put secrets, access tokens or model credentials there; use managed identities and a service such as Azure Key Vault.

📘 Source: [Separate orchestration logic from activity work](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/2-separate-orchestrator-activity-responsibilities)

</details>

## 8. `lp7m4-008`

An orchestrator must classify 20 independent images in parallel and then summarise. What should it do?

- **A.** Yield each call_activity in a loop, one after another
- **B.** Create 20 tasks, then yield task_all
- **C.** Call the model 20 times directly in the orchestrator
- **D.** Start 20 separate client functions

<details><summary>💡 Hint</summary>

Start all the work before you wait for any of it.

</details>

<details><summary>✅ Answer</summary>

**B.** Create 20 tasks, then yield task_all

- A: Yielding each call immediately runs them sequentially.
- B: Correct. Schedule all tasks first, then wait for the group.
- C: Model calls belong in activities.
- D: Clients start orchestrations; this is fan-out inside one orchestration.

Fan-out: create tasks without yielding; fan-in: yield task_all.

📘 Source: [Process independent work with fan-out/fan-in](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/3-apply-fan-out-fan-in)

</details>

## 9. `lp7m4-009`

For each statement, select Yes if the statement is true. Otherwise, select No. An orchestrator yields `context.task_all(tasks)` for five document tasks, and task 3 finishes first.

| Statement | Yes / No |
|---|---|
| The result list has task 3's result first. | ☐ |
| If one activity fails, task_all surfaces a failure to the orchestrator. | ☐ |
| Each activity should return the full extracted text for aggregation. | ☐ |

<details><summary>💡 Hint</summary>

Results come back in task order. One failure surfaces. Keep outputs small.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The result list has task 3's result first. | No | Results match the order of the task list. |
| If one activity fails, task_all surfaces a failure to the orchestrator. | Yes | The orchestrator can then fail, compensate or route the batch. |
| Each activity should return the full extracted text for aggregation. | No | Return compact fields and a result URL. |

Ordered results, explicit failure handling, compact outputs.

📘 Source: [Process independent work with fan-out/fan-in](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/3-apply-fan-out-fan-in)

</details>

## 10. `lp7m4-010`

A batch of 10,000 documents fans out all at once and the model endpoint starts throttling. What does Learn suggest?

- **A.** Return the model responses to the orchestrator to retry them there
- **B.** Increase the function app's instance memory to 4,096 MB
- **C.** Process bounded batches, one batch at a time
- **D.** Add time.sleep() between activity calls in the orchestrator

<details><summary>💡 Hint</summary>

Too much at once hits quotas. Limit how many run together.

</details>

<details><summary>✅ Answer</summary>

**C.** Process bounded batches, one batch at a time

- A: Large responses bloat history and retries belong to activities.
- B: Memory doesn't change the model's rate limits.
- C: Correct. Bounded batches limit scheduled work to fit downstream quotas.
- D: Never sleep in an orchestrator; use durable timers if a pause is needed.

Choose batch size from model quotas, item duration and concurrency.

📘 Source: [Process independent work with fan-out/fan-in](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/3-apply-fan-out-fan-in)

</details>

## 11. `lp7m4-011`

A claim archive of a million documents makes one orchestrator's fan-in a bottleneck. Which design helps?

- **A.** Running all aggregation inside the client function
- **B.** A parent with sub-orchestrations per partition
- **C.** Removing fan-in and letting activities write a shared counter
- **D.** One orchestrator that loads every individual result for aggregation

<details><summary>💡 Hint</summary>

One orchestrator can only aggregate so much. Split the work into child orchestrations.

</details>

<details><summary>✅ Answer</summary>

**B.** A parent with sub-orchestrations per partition

- A: Clients manage orchestrations; they don't aggregate durable results.
- B: Correct. Each child handles a partition and returns counts and locations.
- C: Shared counters lose the durable coordination.
- D: That's the bottleneck being fixed.

Introduce sub-orchestrations when batch size or aggregation cost justifies them.

📘 Source: [Process independent work with fan-out/fan-in](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/3-apply-fan-out-fan-in)

</details>

## 12. `lp7m4-012`

An orchestration must wait up to 48 hours for an adjuster's decision, then take a timeout path. What should it use?

- **A.** An activity that blocks until the adjuster answers
- **B.** A loop that polls the approval table every minute
- **C.** task_any() racing the event against a timer
- **D.** time.sleep() for 48 hours, then check the database

<details><summary>💡 Hint</summary>

Wait for an event or a deadline, whichever comes first.

</details>

<details><summary>✅ Answer</summary>

**C.** task_any() racing the event against a timer

- A: An activity would hold a worker for days.
- B: Polling from the orchestrator is inefficient; events resume it.
- C: Correct. Whichever completes first decides the path.
- D: Blocking waits aren't allowed in orchestrators.

Human interaction pattern: wait_for_external_event + create_timer + task_any.

📘 Source: [Coordinate human approval with external events](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/4-wait-human-approval-external-events)

</details>

## 13. `lp7m4-013`

For each statement, select Yes if the statement is true. Otherwise, select No. An approval orchestration races an ApprovalResponse event against a 48-hour timer.

| Statement | Yes / No |
|---|---|
| The suspended orchestration holds a worker for the full 48 hours. | ☐ |
| If the event wins, the orchestrator should cancel the pending timer. | ☐ |
| An event sent before the orchestrator starts waiting is lost. | ☐ |
| Knowing the instance ID is enough proof that the caller may approve. | ☐ |

<details><summary>💡 Hint</summary>

Waiting costs almost nothing. Cancel the timer you didn't need, and secure the endpoint.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The suspended orchestration holds a worker for the full 48 hours. | No | It doesn't hold a worker or active invocation while waiting. |
| If the event wins, the orchestrator should cancel the pending timer. | Yes | Every pending timer must be waited for or cancelled before exit. |
| An event sent before the orchestrator starts waiting is lost. | No | Early events are persisted and consumed later. |
| Knowing the instance ID is enough proof that the caller may approve. | No | Authenticate and authorize callers; the ID is just an address. |

Durable waits are cheap, but endpoints must still be secured.

📘 Source: [Coordinate human approval with external events](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/4-wait-human-approval-external-events)

</details>

## 14. `lp7m4-014`

A reviewer double-clicks Approve and two ApprovalResponse events arrive; a stale review link also sends an old decision. How should the workflow cope?

- **A.** Accept whichever of the events arrives last
- **B.** Accept every event and create one approval record for each
- **C.** Use request ID and version; record the first valid decision once
- **D.** Turn off at-least-once delivery for the external events

<details><summary>💡 Hint</summary>

Expect duplicates and old decisions.

</details>

<details><summary>✅ Answer</summary>

**C.** Use request ID and version; record the first valid decision once

- A: Arrival order alone isn't a reliable policy.
- B: Duplicates would create duplicate approvals.
- C: Correct. Versioned, idempotent recording handles duplicates and out-of-order responses.
- D: At-least-once delivery isn't something you switch off.

Design for duplicates and stale responses explicitly.

📘 Source: [Coordinate human approval with external events](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/4-wait-human-approval-external-events)

</details>

## 15. `lp7m4-015`

A client function raises the ApprovalResponse event after authorizing the reviewer. What should its HTTP response be?

- **A.** 204 No Content after the orchestration completes
- **B.** 409 Conflict
- **C.** 202 Accepted
- **D.** 200 OK with the final claim result

<details><summary>💡 Hint</summary>

Raising an event is asynchronous, so don't promise the outcome yet.

</details>

<details><summary>✅ Answer</summary>

**C.** 202 Accepted

- A: The client doesn't wait for completion.
- B: Nothing conflicts in the normal path.
- C: Correct. Event delivery resumes the orchestration asynchronously.
- D: The final result isn't available yet.

Raising an event is asynchronous; return 202 and let callers track status.

📘 Source: [Coordinate human approval with external events](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/4-wait-human-approval-external-events)

</details>

## 16. `lp7m4-016`

An HTTP-triggered client function receives a reviewer's approval for orchestration instance claim-482. Which call delivers it to the waiting orchestration?

- **A.** client.start_new("approval", instance_id, data)
- **B.** client.terminate(instance_id, "approved")
- **C.** context.wait_for_external_event("ApprovalResponse")
- **D.** client.raise_event(instance_id, "ApprovalResponse", data)

<details><summary>💡 Hint</summary>

The orchestrator waits for a named event. Which client method sends one?

</details>

<details><summary>✅ Answer</summary>

**D.** client.raise_event(instance_id, "ApprovalResponse", data)

- A: start_new starts a new instance. It doesn't deliver an event to a running one.
- B: terminate stops the orchestration instead of letting it continue.
- C: That's what the orchestrator calls to wait. A client function can't use it.
- D: Correct. raise_event sends a named external event to that instance, and the name must match what the orchestrator waits for.

A client function uses raise_event(instance_id, event_name, data) to send a named external event to a specific instance. The orchestrator waits with wait_for_external_event(name).

📘 Source: [Coordinate human approval with external events](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/4-wait-human-approval-external-events)

</details>

## 17. `lp7m4-017`

A caller starts a long document workflow over HTTP and needs a way to check its progress later. What does Learn say an HTTP-triggered client function often returns?

- **A.** The final result, after waiting for the orchestration to finish
- **B.** The orchestrator's replay history
- **C.** Status URLs that the caller can use to track the workflow
- **D.** A function key for the orchestrator

<details><summary>💡 Hint</summary>

The work takes a long time. What lets the caller come back and ask how it's going?

</details>

<details><summary>✅ Answer</summary>

**C.** Status URLs that the caller can use to track the workflow

- A: Long workflows would hit HTTP timeouts. The client returns quickly with tracking information.
- B: History is internal state, not something to hand to callers.
- C: Correct. Client functions start orchestrations and often return status URLs for long-running workflows.
- D: Keys don't track progress, and you shouldn't give them out this way.

Client functions start orchestrations, query status, terminate them and send external events. An HTTP-triggered client often returns status URLs for tracking a long-running workflow.

📘 Source: [Coordinate human approval with external events](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/4-wait-human-approval-external-events)

</details>

## 18. `lp7m4-018`

Match each failure to the handling Learn recommends.

Choices: **Bounded retry** · **Terminal outcome after validation** · **Explicit business branch**

- The model endpoint returns a throttling response
- The upload is an unsupported content type
- Classification confidence is below the threshold

<details><summary>💡 Hint</summary>

Throttling is transient, bad input is terminal, and low confidence is a business rule.

</details>

<details><summary>✅ Answer</summary>

- The model endpoint returns a throttling response → **Bounded retry**. Transient failures can succeed later.
- The upload is an unsupported content type → **Terminal outcome after validation**. Permanent failures won't succeed on retry.
- Classification confidence is below the threshold → **Explicit business branch**. Expected decisions aren't infrastructure errors.

Classify failures before retrying.

📘 Source: [Design reliable workflow steps](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/5-design-reliable-workflow-steps)

</details>

## 19. `lp7m4-019`

An activity writes a result blob, then the host crashes before the result is recorded, so the activity runs again. How should it avoid a duplicate?

- **A.** Generate a new uuid.uuid4() blob name on each attempt
- **B.** Name the blob with a stable operation ID; skip if present
- **C.** Write the result from the orchestrator instead of the activity
- **D.** Disable retries for the activity so it can't run twice

<details><summary>💡 Hint</summary>

The write must land in the same place every time the activity runs.

</details>

<details><summary>✅ Answer</summary>

**B.** Name the blob with a stable operation ID; skip if present

- A: A new ID per attempt makes each retry look like new work.
- B: Correct. The retry recognizes the existing result and returns the same URL.
- C: Orchestrators must not do I/O.
- D: Retries are needed for transient failures.

Pass an operation ID (from input or context.new_uuid()) for idempotent writes.

📘 Source: [Design reliable workflow steps](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/5-design-reliable-workflow-steps)

</details>

## 20. `lp7m4-020`

For each statement, select Yes if the statement is true. Otherwise, select No. A step races a processing activity against a 10-minute durable timer, and the timer wins.

| Statement | Yes / No |
|---|---|
| The running activity is cancelled automatically. | ☐ |
| The workflow should ignore a late result after its terminal deadline. | ☐ |
| A model-call timeout means the whole claim must be marked invalid. | ☐ |

<details><summary>💡 Hint</summary>

A timer winning doesn't stop work already started.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The running activity is cancelled automatically. | No | A winning timer doesn't cancel a started activity. |
| The workflow should ignore a late result after its terminal deadline. | Yes | Design to ignore late results and keep writes idempotent. |
| A model-call timeout means the whole claim must be marked invalid. | No | Choose the narrowest timeout; retry, fall back or send to manual review. |

Timeouts bound waiting; they don't undo work already in flight.

📘 Source: [Design reliable workflow steps](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/5-design-reliable-workflow-steps)

</details>

## 21. `lp7m4-021`

Document processing exhausts its retries after a provisional summary was published. What should the orchestrator do?

- **A.** Retry the activity forever until it finally succeeds
- **B.** Delete every audit record of the provisional summary
- **C.** Run an idempotent compensation activity, then rethrow
- **D.** Catch the exception and report the workflow as Completed

<details><summary>💡 Hint</summary>

Retries are exhausted. Undo what was published, then fail honestly.

</details>

<details><summary>✅ Answer</summary>

**C.** Run an idempotent compensation activity, then rethrow

- A: Retries must be bounded.
- B: Preserve audit evidence; compensation is a new business action.
- C: Correct. Compensate the earlier side effect and keep a Failed terminal status.
- D: Hiding the failure misreports the outcome.

Compensation addresses completed side effects without pretending to roll back.

📘 Source: [Design reliable workflow steps](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/5-design-reliable-workflow-steps)

</details>

## 22. `lp7m4-022`

An activity should run at most 3 times, waiting 5 seconds before the first retry. Which Python code is correct?

- **A.** context.call_activity("Classify", df.RetryOptions(5_000, 3), doc)
- **B.** context.call_activity_with_retry("Classify", df.RetryOptions(5_000, 3), doc)
- **C.** context.call_activity_with_retry("Classify", df.RetryOptions(3, 5_000), doc)
- **D.** context.call_activity_with_retry("Classify", df.RetryOptions(5, 3), doc)

<details><summary>💡 Hint</summary>

Check the units of the first argument, and which call accepts a retry policy.

</details>

<details><summary>✅ Answer</summary>

**B.** context.call_activity_with_retry("Classify", df.RetryOptions(5_000, 3), doc)

- A: Plain call_activity doesn't apply a retry policy.
- B: Correct. RetryOptions takes the first retry interval in milliseconds, then the max number of attempts.
- C: The arguments are swapped: that's a 3 ms first interval and 5,000 attempts.
- D: The interval is in milliseconds, so 5 means 5 ms, not 5 seconds.

df.RetryOptions(first_retry_interval_in_milliseconds, max_number_of_attempts) is used with context.call_activity_with_retry().

📘 Source: [Design reliable workflow steps](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/5-design-reliable-workflow-steps)

</details>

## 23. `lp7m4-023`

A retried activity creates its operation ID with uuid.uuid4(), and duplicate result blobs appear. What's the best fix?

- **A.** Create the ID in the orchestrator with context.new_uuid() and pass it to the activity
- **B.** Write the result blob with overwrite=True
- **C.** Lower the retry policy to a single attempt
- **D.** Call uuid.uuid4() in the orchestrator and pass it in

<details><summary>💡 Hint</summary>

The ID has to be the same every time the step runs, and that includes replays.

</details>

<details><summary>✅ Answer</summary>

**A.** Create the ID in the orchestrator with context.new_uuid() and pass it to the activity

- A: Correct. The ID stays the same across retries and replays, so repeated writes land in the same place.
- B: With a new ID each time, each retry writes a different blob, so overwriting doesn't help.
- C: Activities can still run more than once, and you lose resilience.
- D: uuid4 in an orchestrator gives a new value on each replay, which breaks determinism.

Activities run at least once, so the operation ID must be stable. Create it deterministically in the orchestrator with context.new_uuid() (or derive it from input) and pass it to the activity.

📘 Source: [Design reliable workflow steps](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/5-design-reliable-workflow-steps)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
