# Practice: LP2 · M2 Manage containers in Azure Container Apps

> 27 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp2m2.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-2/manage-containers-azure-container-apps)

## 1. `lp2m2-001`

You want to send 10% of traffic to a revision running a new model version and 90% to the current one. Which revision mode do you need?

- **A.** Inactive revision mode
- **B.** Multiple revision mode
- **C.** Labelled revision mode
- **D.** Single revision mode

<details><summary>💡 Hint</summary>

Sending a share of traffic to each of two revisions needs more than one active revision.

</details>

<details><summary>✅ Answer</summary>

**B.** Multiple revision mode

- A: Inactive is a revision state, not a mode.
- B: Correct. Multiple revision mode enables canary rollouts and traffic splitting.
- C: Learn describes only single and multiple revision modes.
- D: Single revision mode keeps only one active revision, so you can't split traffic.

Multiple revision mode allows several active revisions, which enables traffic splitting.

📘 Source: [Update images and manage revisions safely](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/2-update-images-manage-revisions)

</details>

## 2. `lp2m2-002`

What does it mean when a Container Apps revision is active?

- **A.** It has passed every health probe
- **B.** It is in a state where it can receive traffic
- **C.** It is the newest revision of the app
- **D.** It is stored with its image digest

<details><summary>💡 Hint</summary>

A revision can exist without receiving traffic. What does the word active add?

</details>

<details><summary>✅ Answer</summary>

**B.** It is in a state where it can receive traffic

- A: Health and active state are separate properties.
- B: Correct. Active is the operational state that lets a revision receive traffic.
- C: A newer revision can exist without being active.
- D: Activity isn't tied to how the image is referenced.

A revision can exist without being active; only active revisions can receive traffic.

📘 Source: [Update images and manage revisions safely](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/2-update-images-manage-revisions)

</details>

## 3. `lp2m2-003`

A new revision starts returning errors in production. You want it to stop receiving traffic while keeping the evidence for later analysis. What should you do first?

- **A.** Purge revisions with --max-inactive-revisions 0
- **B.** Restart the whole container app
- **C.** Delete the revision so no new replicas start
- **D.** Deactivate the revision to stop its traffic

<details><summary>💡 Hint</summary>

Stop the traffic but keep the evidence. Deleting removes evidence.

</details>

<details><summary>✅ Answer</summary>

**D.** Deactivate the revision to stop its traffic

- A: Purging removes inactive revisions you may need.
- B: A restart doesn't stop traffic to that revision and doesn't isolate it.
- C: Deletion destroys the evidence and the rollback option.
- D: Correct. Deactivation stops traffic while preserving evidence and rollback options.

Deactivation is a safer first step than deletion during an incident.

📘 Source: [Update images and manage revisions safely](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/2-update-images-manage-revisions)

</details>

## 4. `lp2m2-004`

For each statement, select Yes if the statement is true. Otherwise, select No. A team updates production with `az containerapp update --image myregistry.azurecr.io/ai-api@sha256:…`.

| Statement | Yes / No |
|---|---|
| Referencing the digest lets the team prove which artifact served requests during an incident. | ☐ |
| Container Apps keeps every inactive revision forever unless someone deletes it. | ☐ |
| The update creates a new revision with the updated template. | ☐ |
| A tag such as staging is a guarantee that the image content never changes. | ☐ |

<details><summary>💡 Hint</summary>

Digests prove which artifact ran. Think about what an image update creates and how inactive revisions are cleaned up.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Referencing the digest lets the team prove which artifact served requests during an incident. | Yes | Digests are immutable, so they give strong traceability. |
| Container Apps keeps every inactive revision forever unless someone deletes it. | No | Inactive revisions are purged automatically when you exceed 100. |
| The update creates a new revision with the updated template. | Yes | Updating the image creates a new revision. |
| A tag such as staging is a guarantee that the image content never changes. | No | Tags can change; treat them as a convenience. |

Use digests in production, check the new revision's health, and know the 100-revision purge threshold.

📘 Source: [Update images and manage revisions safely](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/2-update-images-manage-revisions)

</details>

## 5. `lp2m2-005`

Your app uses the default single revision mode. You update the image, and the new revision becomes healthy. How many revisions can be active now?

- **A.** Up to 100, after which inactive ones are purged
- **B.** Two, so that traffic can be split during the rollout
- **C.** One
- **D.** As many as the app's maximum replica count

<details><summary>💡 Hint</summary>

The mode's name tells you the answer.

</details>

<details><summary>✅ Answer</summary>

**C.** One

- A: 100 is the default purge threshold for inactive revisions, not a limit on active ones.
- B: Traffic splitting needs multiple revision mode, which isn't the default.
- C: Correct. Single revision mode keeps only one active revision.
- D: Replica limits count running instances. They don't decide how many revisions are active.

Revision mode determines how many revisions can be active at once. Single revision mode keeps only one active revision; multiple revision mode allows canary rollouts and traffic splitting.

📘 Source: [Update images and manage revisions safely](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/2-update-images-manage-revisions)

</details>

## 6. `lp2m2-006`

You updated a production app to an image digest. Before routing traffic, you want to confirm the platform recorded exactly the image you expect. Which command shows it?

- **A.** az containerapp logs show --type system
- **B.** az containerapp env show --query properties.containers
- **C.** az acr repository show-manifests --name myregistry
- **D.** az containerapp show --query properties.template.containers

<details><summary>💡 Hint</summary>

The image reference lives in the app's template. Show the app and query that part.

</details>

<details><summary>✅ Answer</summary>

**D.** az containerapp show --query properties.template.containers

- A: System logs show platform events. They don't list the configured image reference.
- B: Containers are defined in each app's template, not in the environment.
- C: That lists manifests in the registry, not what the container app is configured to run.
- D: Correct. The container template shows the image reference the platform recorded.

After an update, inspect the container template with az containerapp show --query properties.template.containers to confirm the image you expect.

📘 Source: [Update images and manage revisions safely](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/2-update-images-manage-revisions)

</details>

## 7. `lp2m2-007`

Auditors want inactive revisions kept far longer than usual, so that up to 300 old revisions remain available for incident review. What should you change?

- **A.** Raise --max-inactive-revisions above the default threshold of 100
- **B.** Switch the app to multiple revision mode so that inactive revisions are kept longer
- **C.** Deactivate each revision manually, since purging applies to deleted revisions
- **D.** Tag each revision's image with a stable tag so that the platform keeps it

<details><summary>💡 Hint</summary>

There's a default number of inactive revisions kept, and a parameter that changes it.

</details>

<details><summary>✅ Answer</summary>

**A.** Raise --max-inactive-revisions above the default threshold of 100

- A: Correct. Container Apps purges inactive revisions beyond 100 by default, and --max-inactive-revisions adjusts that threshold.
- B: Revision mode controls how many revisions are active. It doesn't change the purge threshold.
- C: Deactivated revisions are exactly the inactive ones that the purge threshold applies to.
- D: Image tags don't affect how many inactive revisions Container Apps keeps.

Container Apps automatically purges inactive revisions when you exceed 100. Adjust the threshold with --max-inactive-revisions as part of a retention strategy.

📘 Source: [Update images and manage revisions safely](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/2-update-images-manage-revisions)

</details>

## 8. `lp2m2-008`

Revision ai-api--v7 fails while ai-api--v6 works. You want to compare the two revisions' configuration side by side. Which command retrieves one revision's details?

- **A.** az containerapp replica list --revision ai-api--v7
- **B.** az containerapp logs show --revision ai-api--v7 --follow
- **C.** az containerapp revision show --revision ai-api--v7
- **D.** az containerapp revision deactivate --revision ai-api--v7

<details><summary>💡 Hint</summary>

List shows all revisions. Which verb gives you the details of one?

</details>

<details><summary>✅ Answer</summary>

**C.** az containerapp revision show --revision ai-api--v7

- A: This lists running instances, not the revision's configuration.
- B: Logs show runtime output. Comparing configuration needs the revision's details.
- C: Correct. revision show returns a specific revision's details, so you can compare it with a working one.
- D: Deactivation stops traffic to the revision. It doesn't show its configuration.

Listing revisions confirms which is active; az containerapp revision show retrieves a specific revision so you can compare a working and a failing configuration.

📘 Source: [Update images and manage revisions safely](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/2-update-images-manage-revisions)

</details>

## 9. `lp2m2-009`

An upstream model provider is down, and you must guarantee that the app doesn't start any replicas until it's back. What should you do?

- **A.** Rely on scale to zero
- **B.** Run az containerapp stop
- **C.** Lower the CPU allocation
- **D.** Run az containerapp restart

<details><summary>💡 Hint</summary>

Scaling rules can still start replicas. Which explicit action guarantees none start?

</details>

<details><summary>✅ Answer</summary>

**B.** Run az containerapp stop

- A: Scale to zero depends on scale rules; incoming work can still start replicas.
- B: Correct. Stop is an explicit action that guarantees no replicas start.
- C: CPU size doesn't stop replicas from starting.
- D: Restart starts replicas again.

Stopping is an explicit operational action; scale to zero is automatic and can scale back out.

📘 Source: [Manage the container app lifecycle](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/3-app-lifecycle-management)

</details>

## 10. `lp2m2-010`

Match each failing revision symptom to the checklist category.

Choices: **Image pull failure** · **Port mismatch** · **Probe failure** · **Resource pressure**

- Registry credentials are missing, so the revision never starts
- The container listens on 5000 but ingress targets 8000
- Readiness checks /healthz but the app serves /health
- Replicas are killed while loading a large model

<details><summary>💡 Hint</summary>

Each symptom points to one category: registry, port, probe or resources.

</details>

<details><summary>✅ Answer</summary>

- Registry credentials are missing, so the revision never starts → **Image pull failure**. Missing or invalid credentials or a wrong image reference cause pull failures.
- The container listens on 5000 but ingress targets 8000 → **Port mismatch**. The container listens on a different port than ingress expects.
- Readiness checks /healthz but the app serves /health → **Probe failure**. Probes target the wrong path.
- Replicas are killed while loading a large model → **Resource pressure**. Containers killed at memory limits are resource pressure.

Learn's repeatable checklist: image pull, port, missing configuration, probes, resource pressure.

📘 Source: [Manage the container app lifecycle](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/3-app-lifecycle-management)

</details>

## 11. `lp2m2-011`

Only the newest revision is failing; two older revisions in multiple revision mode are serving traffic fine. Which first step limits the blast radius best?

- **A.** Restart the container app to clear the bad state
- **B.** Stop the container app until the cause is known
- **C.** Delete the two older revisions to avoid confusion
- **D.** Deactivate the failing revision and keep the others serving

<details><summary>💡 Hint</summary>

Only one revision is bad. App-level actions affect every revision.

</details>

<details><summary>✅ Answer</summary>

**D.** Deactivate the failing revision and keep the others serving

- A: A restart affects the whole app and isn't a root-cause fix.
- B: Stop is app-level and would take the healthy revisions down too.
- C: The older revisions are healthy and are your rollback path.
- D: Correct. Deactivating one revision isolates the bad release.

Start, stop and restart act on the whole app. For one bad release, deactivate that revision.

📘 Source: [Manage the container app lifecycle](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/3-app-lifecycle-management)

</details>

## 12. `lp2m2-012`

After a configuration change, you want the change to take effect immediately. You also suspect one replica is stuck in a deadlock. Which lifecycle action fits?

- **A.** az containerapp stop
- **B.** az containerapp revision deactivate
- **C.** az containerapp restart
- **D.** Set the minimum replicas to zero and wait

<details><summary>💡 Hint</summary>

You want running replicas to start again, not to disappear.

</details>

<details><summary>✅ Answer</summary>

**C.** az containerapp restart

- A: Stop keeps the app from starting replicas at all. It's for incidents, not for applying a change.
- B: Deactivation removes a revision from traffic. It doesn't restart replicas.
- C: Correct. Restart forces replicas to restart, which applies configuration immediately and can clear a stuck process.
- D: Scale to zero depends on traffic and rules, so it doesn't apply a change right away.

Restart is useful when configuration changes should take effect immediately, or when a process is stuck because of a deadlock or a transient dependency issue. Pair it with log inspection.

📘 Source: [Manage the container app lifecycle](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/3-app-lifecycle-management)

</details>

## 13. `lp2m2-013`

For each statement, select Yes if the statement is true. Otherwise, select No. An AI API loads a large model at startup, and the on-call engineer often restarts it when latency rises.

| Statement | Yes / No |
|---|---|
| Frequent restarts can increase how often users hit cold starts. | ☐ |
| A restart that makes latency normal again proves the root cause is fixed. | ☐ |
| Stopping the app affects every revision, not only the one with problems. | ☐ |

<details><summary>💡 Hint</summary>

Think about what a restart costs a model-loading API, what it proves, and how wide stop reaches.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Frequent restarts can increase how often users hit cold starts. | Yes | Each restart reloads the model, so restarting too aggressively increases cold starts. |
| A restart that makes latency normal again proves the root cause is fixed. | No | Restart isn't a substitute for root cause. Pair it with log inspection to see whether it fixed or delayed the failure. |
| Stopping the app affects every revision, not only the one with problems. | Yes | Start and stop are app-level actions, which can be too broad when one revision is the problem. |

Restart clears transient states but isn't a root-cause fix, and frequent restarts increase cold starts for model-loading services. Start and stop are app-level, so revision deactivation is safer for one bad release.

📘 Source: [Manage the container app lifecycle](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/3-app-lifecycle-management)

</details>

## 14. `lp2m2-014`

During an incident, you want one table that shows every revision's name, whether it's active, and its health state. Which command does Learn use as a starting point?

- **A.** az containerapp logs show --type system --query revisions -o table
- **B.** az containerapp show --query properties.template.revisions -o table
- **C.** az containerapp revision list with --query "[].{name:name,active:properties.active,health:properties.healthState}" -o table
- **D.** az containerapp replica list --query "[].{name:name,health:properties.healthState}" -o table

<details><summary>💡 Hint</summary>

You're listing revisions and picking three fields with a JMESPath query.

</details>

<details><summary>✅ Answer</summary>

**C.** az containerapp revision list with --query "[].{name:name,active:properties.active,health:properties.healthState}" -o table

- A: Logs are a stream of events, not a status table of revisions.
- B: The app's template describes the current container definition, not every revision's status.
- C: Correct. This query compares revision status at a glance.
- D: Replicas are running instances. The question asks about revisions.

Learn's checklist starts by confirming which revision is failing; az containerapp revision list with a --query for name, active and healthState compares revisions at a glance.

📘 Source: [Manage the container app lifecycle](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/3-app-lifecycle-management)

</details>

## 15. `lp2m2-015`

Which two fields does Learn recommend adding to an AI API's application logs? (Select two.)

- **A.** A request identifier propagated across services
- **B.** The full text of the user's prompt, for exact replay later
- **C.** The model version used for the request
- **D.** The raw document that was processed, for later debugging

<details><summary>💡 Hint</summary>

Two fields help you tie a request to the exact path and model that served it.

</details>

<details><summary>✅ Answer</summary>

**A.** A request identifier propagated across services  
**C.** The model version used for the request

- A: Correct. A correlation ID ties logs together across services.
- B: Log identifiers and metadata rather than prompts.
- C: Correct. The model deployment name or version helps explain behavior.
- D: Avoid logging raw documents; they can be sensitive.

Recommended fields: request id, revision or build id, model version, latency breakdown.

📘 Source: [Monitor logs and troubleshoot issues](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/4-monitor-logs-troubleshoot)

</details>

## 16. `lp2m2-016`

A new revision fails in production. Put Learn's incident workflow in order.

- Apply a targeted fix and validate that the next revision becomes ready
- Compare the configuration of a working and the failing revision
- Confirm which revision is active and which is failing
- Stream logs while you reproduce the issue

<details><summary>💡 Hint</summary>

Scope first, then watch, then compare, then fix and confirm.

</details>

<details><summary>✅ Answer</summary>

1. Confirm which revision is active and which is failing
2. Stream logs while you reproduce the issue
3. Compare the configuration of a working and the failing revision
4. Apply a targeted fix and validate that the next revision becomes ready

Narrow the scope first, gather live evidence, compare configs, then fix and validate.

📘 Source: [Monitor logs and troubleshoot issues](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/4-monitor-logs-troubleshoot)

</details>

## 17. `lp2m2-017`

Some prompts make the AI API fail, and developers want the logs to help debug them. Security forbids storing sensitive user content in logs. What should the API log?

- **A.** Identifiers and metadata such as request ID and model version
- **B.** The full prompt and response, encrypted with a key in Key Vault
- **C.** HTTP status codes alone, so that no request detail is stored
- **D.** The full prompt and response, but just for requests that fail

<details><summary>💡 Hint</summary>

You want enough context to trace a request without keeping what the user wrote.

</details>

<details><summary>✅ Answer</summary>

**A.** Identifiers and metadata such as request ID and model version

- A: Correct. Logging identifiers and metadata rather than raw prompts gives context without sensitive content.
- B: Encryption still stores the sensitive content, which the guidance avoids.
- C: Status codes alone don't give enough context to debug input-dependent failures.
- D: Failed requests can still contain sensitive content, so this still logs it.

AI services behave differently for different inputs. Log identifiers and metadata (request ID, revision or build ID, model version, latency breakdown) instead of raw documents or prompts.

📘 Source: [Monitor logs and troubleshoot issues](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/4-monitor-logs-troubleshoot)

</details>

## 18. `lp2m2-018`

What happens when a liveness probe fails for a replica?

- **A.** The revision is deactivated
- **B.** The replica stops receiving traffic but keeps running
- **C.** The platform restarts the replica
- **D.** The app scales to zero

<details><summary>💡 Hint</summary>

One probe decides about traffic, and the other decides about restarts.

</details>

<details><summary>✅ Answer</summary>

**C.** The platform restarts the replica

- A: Probes act on replicas, not on revision activation.
- B: That's the readiness behavior.
- C: Correct. If liveness fails, the platform restarts the replica.
- D: Probe failures don't trigger scale to zero.

Readiness controls traffic; liveness controls restarts.

📘 Source: [Configure health probes and troubleshoot failures](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/5-health-probes)

</details>

## 19. `lp2m2-019`

An AI API loads a 3 GB model at startup. New revisions are restarted again and again by the liveness probe about 20 seconds after starting, before the model finishes loading. What should you change?

- **A.** Raise initialDelaySeconds and failureThreshold to match the model load time
- **B.** Point the liveness probe at a downstream dependency's health URL
- **C.** Remove the readiness probe so traffic reaches the replica sooner
- **D.** Restart the container app after each deployment

<details><summary>💡 Hint</summary>

The probe fires before the model finishes loading. Give the process more time before failures count.

</details>

<details><summary>✅ Answer</summary>

**A.** Raise initialDelaySeconds and failureThreshold to match the model load time

- A: Correct. Tune these values so the process has enough time to reach a ready state.
- B: Probe endpoints shouldn't depend on external systems.
- C: Removing readiness sends traffic to replicas that can't serve it.
- D: Restarts make the cold-start problem worse.

Liveness failures shortly after startup usually mean the probe is too aggressive for the real startup time.

📘 Source: [Configure health probes and troubleshoot failures](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/5-health-probes)

</details>

## 20. `lp2m2-020`

For each statement, select Yes if the statement is true. Otherwise, select No. A new revision fails its probes during rollout.

| Statement | Yes / No |
|---|---|
| Revision status shows whether the platform considers the revision healthy. | ☐ |
| A probe failure is almost always a bug in the application code. | ☐ |
| A readiness endpoint that calls an external API can fail during that API's outage. | ☐ |
| Making liveness more aggressive reduces cold starts for model-heavy apps. | ☐ |

<details><summary>💡 Hint</summary>

Probe failures are often configuration. Revision status and dependency calls matter.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Revision status shows whether the platform considers the revision healthy. | Yes | Combine revision status with logs. |
| A probe failure is almost always a bug in the application code. | No | Learn says probe failures are frequently configuration issues. |
| A readiness endpoint that calls an external API can fail during that API's outage. | Yes | Probe endpoints shouldn't depend on external systems that might be unavailable. |
| Making liveness more aggressive reduces cold starts for model-heavy apps. | No | Aggressive liveness causes unnecessary restarts and more cold starts. |

Check port, path, timeouts and startup dependencies first; tune probes to the real startup behavior.

📘 Source: [Configure health probes and troubleshoot failures](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/5-health-probes)

</details>

## 21. `lp2m2-021`

Each new replica of an AI API spends 40 seconds loading a model. During that time, requests that reach it fail. Which probe should protect users from this?

- **A.** A readiness probe that succeeds only after the model is loaded
- **B.** A liveness probe on the same path as the readiness probe
- **C.** A liveness probe with a very short timeout
- **D.** A startup command that sleeps for 40 seconds

<details><summary>💡 Hint</summary>

One probe asks "can this replica receive traffic right now?"

</details>

<details><summary>✅ Answer</summary>

**A.** A readiness probe that succeeds only after the model is loaded

- A: Correct. Readiness decides whether a replica can receive traffic, so it guards model loading.
- B: Sharing a path doesn't stop traffic reaching an unready replica. That's readiness's job.
- C: Liveness decides whether to restart a replica. A short timeout would cause restarts during loading.
- D: A sleep doesn't tell the platform when the replica can take traffic.

Readiness answers "Can this replica receive traffic right now?" If it fails, the platform stops routing to that replica. Use it to guard model loading and dependency readiness.

📘 Source: [Configure health probes and troubleshoot failures](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/5-health-probes)

</details>

## 22. `lp2m2-022`

A new revision's readiness probe calls /health/ready on port 80, but the API serves on port 8080. Logs show the API started normally. What is the most likely fix?

- **A.** Change the probe's port to 8080
- **B.** Remove the readiness probe so that traffic flows straight away
- **C.** Rewrite the /health/ready handler, because probe failures usually mean an application bug
- **D.** Lower the liveness probe's failureThreshold to 1

<details><summary>💡 Hint</summary>

The app is fine, and the probe is knocking on a door nobody is behind.

</details>

<details><summary>✅ Answer</summary>

**A.** Change the probe's port to 8080

- A: Correct. A probe that targets the wrong port is one of the most common probe failures.
- B: That sends traffic to replicas before you know they're ready.
- C: Probe failures are frequently configuration issues. The app started normally.
- D: That makes liveness more aggressive and doesn't fix the readiness probe's port.

Common probe failure causes: wrong port, wrong path, timeouts too short for model loading, and slow or failing dependency calls at startup. Check configuration before chasing code.

📘 Source: [Configure health probes and troubleshoot failures](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/5-health-probes)

</details>

## 23. `lp2m2-023`

A background worker keeps restarting, and logs show out-of-memory kills while it processes large batches. What should you increase first?

- **A.** CPU per replica
- **B.** Memory per replica
- **C.** Minimum replica count
- **D.** Maximum inactive revisions

<details><summary>💡 Hint</summary>

Out-of-memory kills point to one resource. Size for the bottleneck.

</details>

<details><summary>✅ Answer</summary>

**B.** Memory per replica

- A: CPU addresses throttling, not out-of-memory restarts.
- B: Correct. Size for the bottleneck: memory for out-of-memory restarts.
- C: More replicas don't give each replica more memory.
- D: Revision retention doesn't affect memory.

Increase CPU when you see throttling and memory when you see out-of-memory restarts.

📘 Source: [Optimize container resources and scaling](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/6-optimize-container-settings)

</details>

## 24. `lp2m2-024`

A synchronous chat API must avoid cold-start delays, and the team accepts a higher baseline cost. What should you configure?

- **A.** A liveness probe with a lower threshold
- **B.** Single revision mode for the app
- **C.** Scale to zero with a short cooldown period
- **D.** A minimum replica count above zero

<details><summary>💡 Hint</summary>

Cold starts are avoided by keeping replicas warm, at a cost.

</details>

<details><summary>✅ Answer</summary>

**D.** A minimum replica count above zero

- A: An aggressive liveness probe causes more restarts.
- B: Revision mode doesn't keep replicas warm.
- C: Scale to zero is what causes cold starts here.
- D: Correct. Minimum replicas reduce cold starts but increase baseline cost.

Use minimum replicas intentionally: fewer cold starts, more baseline cost.

📘 Source: [Optimize container resources and scaling](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/6-optimize-container-settings)

</details>

## 25. `lp2m2-025`

After a model upgrade, p95 latency doubled. You plan to raise CPU, raise memory and change the replica limits. What does Learn recommend?

- **A.** Change the three settings together to fix the problem fastest
- **B.** Roll back the model, since resource changes won't affect model latency
- **C.** Change one variable at a time and measure after each change
- **D.** Set the minimum replicas equal to the maximum to take scaling out of the picture

<details><summary>💡 Hint</summary>

Several changes at once hide which one helped.

</details>

<details><summary>✅ Answer</summary>

**C.** Change one variable at a time and measure after each change

- A: Several changes at once mask which one fixed it.
- B: Learn says to reassess resources after model changes, not to rule them out.
- C: Correct. Optimization is iterative; change one variable at a time.
- D: Fixing replicas at the maximum just raises cost.

Use logs and metrics to find the bottleneck, then change one variable at a time.

📘 Source: [Optimize container resources and scaling](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/6-optimize-container-settings)

</details>

## 26. `lp2m2-026`

Under high concurrency, an AI API's latency spikes, and metrics show CPU throttling. Memory use is low, and there are no restarts. What should you change first?

- **A.** Restart the app every hour
- **B.** Increase CPU per replica
- **C.** Set the minimum replicas to zero
- **D.** Increase memory per replica

<details><summary>💡 Hint</summary>

Match the fix to the metric that's under pressure.

</details>

<details><summary>✅ Answer</summary>

**B.** Increase CPU per replica

- A: Restarts don't add CPU, and they add cold starts for a model-loading API.
- B: Correct. Size for the bottleneck: increase CPU when you see throttling.
- C: Scale to zero adds cold starts and doesn't address throttling.
- D: Memory raises help with out-of-memory restarts, which aren't happening here.

Size for the bottleneck: increase CPU when you see throttling, and increase memory when you see out-of-memory restarts. Validate that per-replica CPU supports your concurrency.

📘 Source: [Optimize container resources and scaling](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/6-optimize-container-settings)

</details>

## 27. `lp2m2-027`

An event-driven background worker summarizes documents a few times a day and can drain its work safely when it scales down. The team wants the lowest cost. How should you set its minimum replicas?

- **A.** Keep at least one replica so that it never cold-starts
- **B.** Allow scale to zero
- **C.** Set the minimum to two for redundancy
- **D.** Match the minimum to the maximum so that capacity is fixed

<details><summary>💡 Hint</summary>

Compare a synchronous API, which needs warm replicas, with a worker whose work can wait.

</details>

<details><summary>✅ Answer</summary>

**B.** Allow scale to zero

- A: A minimum replica avoids cold starts but adds baseline cost, which this worker doesn't need.
- B: Correct. Event-driven workers that drain work safely can often tolerate scale to zero, which keeps the baseline cost low.
- C: Two idle replicas raise baseline cost for work that only arrives a few times a day.
- D: Fixed capacity pays for idle replicas most of the day.

A synchronous API often needs a minimum replica count to reduce cold starts. A background worker that's event-driven and drains work safely can often tolerate scale to zero.

📘 Source: [Optimize container resources and scaling](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/6-optimize-container-settings)

</details>


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
