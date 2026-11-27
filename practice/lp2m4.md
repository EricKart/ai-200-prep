# Practice: LP2 · M4 Run AI-generated code securely in Azure Container Apps dynamic sessions

> 26 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp2m4.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-2/dynamic-sessions-azure-container-apps)

## 1. `lp2m4-001`

What isolates each allocated dynamic session from the host and from other sessions?

- **A.** A namespace per user
- **B.** The backend API's own process boundary
- **C.** An environment per session
- **D.** A Hyper-V-isolated sandbox

<details><summary>💡 Hint</summary>

Each session gets a strong isolation boundary from a Windows virtualization technology.

</details>

<details><summary>✅ Answer</summary>

**D.** A Hyper-V-isolated sandbox

- A: Learn describes Hyper-V isolation, not namespaces.
- B: The point is to run code outside the backend process.
- C: Sessions come from one pool, not one environment each.
- D: Correct. Each session runs in its own Hyper-V-isolated sandbox.

Session pools allocate prewarmed, Hyper-V-isolated sandboxes in milliseconds.

📘 Source: [Choose a dynamic session pool](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/2-choose-dynamic-session-pool)

</details>

## 2. `lp2m4-002`

An agent writes short Python snippets to analyze an uploaded CSV and plot a chart. Which pool type should you choose?

- **A.** A custom container pool, because isolation requires it
- **B.** A separate container app for each request
- **C.** A custom container pool with your own Python image
- **D.** The built-in code interpreter pool

<details><summary>💡 Hint</summary>

Short Python, CSVs and charts, with no native dependencies. Choose the least complex option.

</details>

<details><summary>✅ Answer</summary>

**D.** The built-in code interpreter pool

- A: Both pool types provide isolation; that alone doesn't require a custom image.
- B: The pool already provides isolation without per-request apps.
- C: A custom image adds maintenance you don't need here.
- D: Correct. The built-in interpreter covers CSV analysis, calculations and charts.

Choose the least complex option that meets the execution contract.

📘 Source: [Choose a dynamic session pool](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/2-choose-dynamic-session-pool)

</details>

## 3. `lp2m4-003`

Agents must run a licensed document converter that ships as a native binary. What do you need?

- **A.** The built-in code interpreter pool with outbound network access enabled for downloads
- **B.** The built-in code interpreter with the binary uploaded to /mnt/data
- **C.** SessionsPythonREPLTool, because it supports native executables
- **D.** A custom container session pool in a workload profiles-enabled environment

<details><summary>💡 Hint</summary>

A native binary isn't available in the platform-managed runtime. You'd bring your own image, which needs a certain environment type.

</details>

<details><summary>✅ Answer</summary>

**D.** A custom container session pool in a workload profiles-enabled environment

- A: Egress doesn't change what the built-in runtime supports.
- B: The built-in interpreter isn't right for native executables or proprietary libraries.
- C: The LangChain tool uses the same built-in interpreter.
- D: Correct. Custom container pools suit specialized packages and require a workload profiles environment.

Native binaries, proprietary tools, other languages or custom protocols call for a custom container pool.

📘 Source: [Choose a dynamic session pool](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/2-choose-dynamic-session-pool)

</details>

## 4. `lp2m4-004`

For each statement, select Yes if the statement is true. Otherwise, select No. You're building a custom container session pool for a document tool.

| Statement | Yes / No |
|---|---|
| You must expose the application on the configured target port. | ☐ |
| Azure Container Apps builds and patches your custom image for you. | ☐ |
| A request to the pool endpoint path /api/convert reaches /api/convert in the session container. | ☐ |
| Custom containers lose Hyper-V isolation compared with the built-in interpreter. | ☐ |

<details><summary>💡 Hint</summary>

With a custom image, you own the image, the port and the API. The pool forwards the path unchanged.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| You must expose the application on the configured target port. | Yes | Application ingress on the target port is your responsibility. |
| Azure Container Apps builds and patches your custom image for you. | No | Image maintenance is your responsibility. |
| A request to the pool endpoint path /api/convert reaches /api/convert in the session container. | Yes | The path after the endpoint is forwarded to the container's target port. |
| Custom containers lose Hyper-V isolation compared with the built-in interpreter. | No | Custom container pools still provide Hyper-V isolation. |

You own the image, ingress, logging and health checks; the pool still provides allocation, isolation and cleanup.

📘 Source: [Choose a dynamic session pool](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/2-choose-dynamic-session-pool)

</details>

## 5. `lp2m4-005`

A LangChain agent needs Python execution, but the backend must upload source files first, download specific artifacts and control identifier mapping. Which integration fits best?

- **A.** Direct REST calls to the pool management API
- **B.** A custom container pool that wraps the LangChain agent
- **C.** SessionsPythonREPLTool from langchain-azure-dynamic-sessions
- **D.** Running the code inside the agent process for speed

<details><summary>💡 Hint</summary>

The backend needs fine control over files and identifiers. Is an adapter or the raw API better for that?

</details>

<details><summary>✅ Answer</summary>

**A.** Direct REST calls to the pool management API

- A: Correct. Direct REST gives full control of file exchange, responses and identifier mapping.
- B: The runtime need is Python, which the built-in interpreter covers.
- C: The adapter suits agents that mainly need a Python tool, with less explicit control.
- D: Running generated code beside the API is exactly what sessions avoid.

Choose direct REST for complete control; choose the LangChain tool when an agent mainly needs Python execution.

📘 Source: [Choose a dynamic session pool](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/2-choose-dynamic-session-pool)

</details>

## 6. `lp2m4-006`

A developer proposes running the agent's generated Python with exec() inside the API container, to avoid adding another service. What is the main risk Learn points out?

- **A.** The code would run slower than in a session because sessions use GPUs
- **B.** exec() can't import third-party packages, so most generated analysis code would fail at runtime
- **C.** It shares the API's resources and could read its files, variables or credentials
- **D.** The API container can't return files, so charts would be lost

<details><summary>💡 Hint</summary>

Think about what generated code can see and use when it runs in the same process as your API.

</details>

<details><summary>✅ Answer</summary>

**C.** It shares the API's resources and could read its files, variables or credentials

- A: Sessions aren't described as GPU-backed. The issue is the security boundary.
- B: Python's exec can import packages. The concern is isolation, not features.
- C: Correct. A long-running app container isn't an equivalent boundary to a Hyper-V-isolated session.
- D: An API can return files. The issue is what untrusted code can reach.

If generated code runs beside the API, it can compete for the API's resources and might access its files, environment variables or credentials. Sessions run code in a separate Hyper-V-isolated sandbox.

📘 Source: [Choose a dynamic session pool](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/2-choose-dynamic-session-pool)

</details>

## 7. `lp2m4-007`

You're building a custom container image for a session pool that runs a document converter. Which two responsibilities are yours, not the platform's? (Select two.)

- **A.** Delete idle sessions when the cooldown ends
- **B.** Provide Hyper-V isolation between sessions
- **C.** Write application logs to standard output or standard error
- **D.** Provide health endpoints that show whether the container can accept work

<details><summary>💡 Hint</summary>

The platform still gives you the pool, isolation and cleanup. Think about what your own image must do.

</details>

<details><summary>✅ Answer</summary>

**C.** Write application logs to standard output or standard error  
**D.** Provide health endpoints that show whether the container can accept work

- A: Automatic cleanup is still provided by the pool.
- B: The pool provides Hyper-V isolation for custom containers too.
- C: Correct. Logging from the custom app is your responsibility.
- D: Correct. Health checks are part of the custom environment you own.

For custom container pools, Azure Container Apps provides the pool, rapid allocation, Hyper-V isolation and automatic cleanup. You own image maintenance, ingress on the target port, logging to stdout/stderr, and health checks.

📘 Source: [Choose a dynamic session pool](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/2-choose-dynamic-session-pool)

</details>

## 8. `lp2m4-008`

Each tenant of a learning platform needs its own isolated workspace that runs a specialized development environment, not just Python snippets. Which pool type fits?

- **A.** A custom container session pool with the tenant's own image
- **B.** The built-in code interpreter pool, because it's already isolated
- **C.** A code interpreter pool with egress enabled
- **D.** One container app per tenant, created on each request

<details><summary>💡 Hint</summary>

Both pool types are isolated. What decides the choice is the runtime each tenant needs.

</details>

<details><summary>✅ Answer</summary>

**A.** A custom container session pool with the tenant's own image

- A: Correct. An isolated tenant workspace with a specialized environment calls for a custom container.
- B: Isolation alone doesn't decide the pool type. The interpreter API doesn't provide a specialized environment.
- C: Network access doesn't turn the interpreter into a specialized workspace.
- D: That adds startup and lifecycle work that a session pool already handles.

Choose a custom container when each tenant needs a specialized application or development environment rather than the interpreter API. Runtime and protocol requirements usually decide the pool type.

📘 Source: [Choose a dynamic session pool](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/2-choose-dynamic-session-pool)

</details>

## 9. `lp2m4-009`

What is the default outbound network behavior for dynamic sessions?

- **A.** Outbound traffic is allowed and logged
- **B.** Outbound traffic follows the backend's settings
- **C.** Outbound network traffic is blocked
- **D.** Allowed to Azure only

<details><summary>💡 Hint</summary>

Generated code shouldn't be able to reach the internet unless you allow it.

</details>

<details><summary>✅ Answer</summary>

**C.** Outbound network traffic is blocked

- A: Egress isn't allowed by default.
- B: Egress is a pool-level setting, not inherited from the backend.
- C: Correct. Sessions block egress by default.
- D: Learn says sessions block outbound traffic by default.

Blocking egress stops generated code from downloading programs or sending data out.

📘 Source: [Configure a secure session pool](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/3-configure-secure-session-pool)

</details>

## 10. `lp2m4-010`

Fifty users are online, but usually only about ten analyze documents at the same moment. What is a sensible starting value for maximum concurrent sessions?

- **A.** About 10, then confirm with load testing
- **B.** 1, to minimize cost
- **C.** 50, one session for each user who is online
- **D.** 500, to leave a lot of headroom

<details><summary>💡 Hint</summary>

Size the limit for concurrent use, not for registered users.

</details>

<details><summary>✅ Answer</summary>

**A.** About 10, then confirm with load testing

- A: Correct. Size from concurrent use, then load test the boundary.
- B: One session would force everyone to wait.
- C: Learn says to base it on expected concurrency, not users online.
- D: An oversized limit removes the cost and safety boundary.

The maximum also acts as a cost and downstream safety boundary, so start near real concurrency.

📘 Source: [Configure a secure session pool](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/3-configure-secure-session-pool)

</details>

## 11. `lp2m4-011`

One team's trusted workload needs to call an external API from its sessions; another team runs untrusted AI-generated code. Which two actions follow Learn's guidance? (Select two.)

- **A.** Enable egress on one shared pool and filter in code
- **B.** Put the two workloads in separate session pools
- **C.** Give both pools the backend's identity for runtime access
- **D.** Enable egress only on the trusted workload's pool

<details><summary>💡 Hint</summary>

Egress is set per pool. Mixing trust levels in one pool weakens it.

</details>

<details><summary>✅ Answer</summary>

**B.** Put the two workloads in separate session pools  
**D.** Enable egress only on the trusted workload's pool

- A: Egress is a pool-level choice, so a shared pool would expose the untrusted code.
- B: Correct. Use different pools for code with different egress, identity or data-access needs.
- C: Don't reuse the backend's broader identity for runtime access.
- D: Correct. Egress is pool-wide, so enable it only where it's justified.

Separate trust levels into different pools and keep egress disabled for untrusted code.

📘 Source: [Configure a secure session pool](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/3-configure-secure-session-pool)

</details>

## 12. `lp2m4-012`

For each statement, select Yes if the statement is true. Otherwise, select No. A Python code interpreter pool has a 300-second cooldown and egress disabled.

| Statement | Yes / No |
|---|---|
| Each new request to a session resets its idle timer. | ☐ |
| The cooldown guarantees that results are kept for 300 seconds after the last request, so no other storage is needed. | ☐ |
| Uploading an API key into the session keeps it hidden from the code that runs there. | ☐ |
| End users should never receive the token for the Session Executor identity. | ☐ |

<details><summary>💡 Hint</summary>

Requests reset the idle timer. The cooldown isn't storage, and session code can read what you upload.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Each new request to a session resets its idle timer. | Yes | Every request resets the idle timer. |
| The cooldown guarantees that results are kept for 300 seconds after the last request, so no other storage is needed. | No | Don't rely on the cooldown as durable retention; a session can disappear after inactivity or a failure. |
| Uploading an API key into the session keeps it hidden from the code that runs there. | No | Code in a session can access that session's files, environment variables and credentials. |
| End users should never receive the token for the Session Executor identity. | Yes | The backend uses that identity; end users never receive its token. |

Cooldown resets on each request but isn't durable storage; anything placed in a session is visible to its code.

📘 Source: [Configure a secure session pool](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/3-configure-secure-session-pool)

</details>

## 13. `lp2m4-013`

Users of a custom container session pool wait several seconds for the first response because the image's app is slow to start. Interactive latency matters more than idle cost. What should you adjust?

- **A.** Shorten the cooldown period
- **B.** Enable egress so that the container can preload packages
- **C.** Increase readySessionInstances to keep started environments waiting
- **D.** Increase maxConcurrentSessions so that more sessions can be allocated at once

<details><summary>💡 Hint</summary>

Which setting keeps environments running before anyone asks for them?

</details>

<details><summary>✅ Answer</summary>

**C.** Increase readySessionInstances to keep started environments waiting

- A: A shorter cooldown removes idle sessions sooner, which can make first responses slower.
- B: Egress is a security decision, and it doesn't fix a slow startup.
- C: Correct. Ready instances reduce allocation latency because the app is already running, at the cost of more idle compute.
- D: That raises the ceiling on parallel sessions. It doesn't make allocation faster.

A custom container pool can keep ready session instances. A higher ready count improves responsiveness but keeps more compute running when demand is low, so measure startup time first.

📘 Source: [Configure a secure session pool](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/3-configure-secure-session-pool)

</details>

## 14. `lp2m4-014`

Code in a custom container session must read one blob container that's protected by Microsoft Entra ID. The backend already has a managed identity with broad access. What should you do?

- **A.** Upload the backend's access token as a file into the session
- **B.** Give the session a separate identity scoped to that one blob container
- **C.** Reuse the backend's identity so that there's only one identity to manage
- **D.** Enable egress on the pool so that the code can sign in with a user's password

<details><summary>💡 Hint</summary>

The code in the session can use whatever identity the session has. How much access should that be?

</details>

<details><summary>✅ Answer</summary>

**B.** Give the session a separate identity scoped to that one blob container

- A: Anything in the session is readable by the code you run, so this exposes the token.
- B: Correct. Untrusted code can request tokens for the session identity, so it should have the smallest possible scope.
- C: Generated code could then request tokens with the backend's broader access.
- D: Egress doesn't solve identity, and putting credentials in the session exposes them.

If a session needs runtime access, use a separate identity with the smallest possible scope. Don't reuse the backend's broader identity, because untrusted code in the session can request tokens for it.

📘 Source: [Configure a secure session pool](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/3-configure-secure-session-pool)

</details>

## 15. `lp2m4-015`

Your backend calls the session pool management API with a managed identity. Which token audience must it request?

- **A.** https://management.azure.com
- **B.** https://dynamicsessions.io
- **C.** https://containerapps.io
- **D.** https://vault.azure.net

<details><summary>💡 Hint</summary>

Tokens for the pool management API are issued for a specific audience URL.

</details>

<details><summary>✅ Answer</summary>

**B.** https://dynamicsessions.io

- A: That's the Azure Resource Manager audience, not the dynamic sessions API.
- B: Correct. The token audience must be https://dynamicsessions.io.
- C: That isn't the dynamic sessions audience.
- D: That's for Key Vault.

Request a token for https://dynamicsessions.io/.default; DefaultAzureCredential handles caching and renewal.

📘 Source: [Execute code and exchange files](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/4-execute-code-exchange-files)

</details>

## 16. `lp2m4-016`

Where does a code interpreter session place files you upload, so later executions with the same identifier can read them?

- **A.** /home/data
- **B.** /var/session
- **C.** /tmp/uploads
- **D.** /mnt/data

<details><summary>💡 Hint</summary>

Uploaded files land in one fixed folder that later executions can read.

</details>

<details><summary>✅ Answer</summary>

**D.** /mnt/data

- A: /home is the App Service shared volume, not the session upload location.
- B: Learn names /mnt/data.
- C: Learn names /mnt/data.
- D: Correct. Code interpreter sessions put uploads in /mnt/data.

Uploads go to /mnt/data and stay available while the session exists.

📘 Source: [Execute code and exchange files](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/4-execute-code-exchange-files)

</details>

## 17. `lp2m4-017`

For each statement, select Yes if the statement is true. Otherwise, select No. A chat app maps each conversation to a dynamic session.

| Statement | Yes / No |
|---|---|
| The browser should send the session identifier it wants to use. | ☐ |
| A random UUID generated on the server is a suitable identifier. | ☐ |
| Knowing a session identifier is enough to call the pool API. | ☐ |

<details><summary>💡 Hint</summary>

Identifiers route to state. Who should create them, and are they enough on their own?

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The browser should send the session identifier it wants to use. | No | Don't accept an arbitrary identifier from the client; generate it on the server. |
| A random UUID generated on the server is a suitable identifier. | Yes | A random UUID is unpredictable and meets the identifier format. |
| Knowing a session identifier is enough to call the pool API. | No | The identifier alone doesn't authenticate; every request needs the backend's token. |

Identifiers are sensitive routing keys: server-generated, mapped server-side, never trusted from clients.

📘 Source: [Execute code and exchange files](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/4-execute-code-exchange-files)

</details>

## 18. `lp2m4-018`

The team registered one SessionsPythonREPLTool instance as a shared singleton for all users. Users report seeing each other's files. What should you change?

- **A.** Shorten the pool cooldown so files are deleted sooner
- **B.** Switch to a custom container session pool so that each user gets stronger isolation
- **C.** Enable egress so each user can store files externally
- **D.** Create a separate tool and agent context for each user or conversation

<details><summary>💡 Hint</summary>

Think about what a single shared instance means for session identifiers.

</details>

<details><summary>✅ Answer</summary>

**D.** Create a separate tool and agent context for each user or conversation

- A: A shorter cooldown doesn't separate users who share one session.
- B: Isolation is per session; the issue is that everyone uses the same session.
- C: Egress doesn't separate session state.
- D: Correct. One tool instance reuses one session identifier, so it must not be shared across users.

The tool generates one identifier per instance. Separate instances per user keep files and Python state apart.

📘 Source: [Execute code and exchange files](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/4-execute-code-exchange-files)

</details>

## 19. `lp2m4-019`

Your backend's managed identity must call one session pool's management API and no other pools. Which role assignment does Learn show?

- **A.** Reader role on the session pool, so the backend can see the pool's endpoint
- **B.** Azure ContainerApps Session Executor, scoped to that session pool
- **C.** Azure ContainerApps Session Executor, scoped to the subscription
- **D.** Contributor on the resource group that holds the pool

<details><summary>💡 Hint</summary>

There's a specific role for calling the pool, and you can choose how widely to assign it.

</details>

<details><summary>✅ Answer</summary>

**B.** Azure ContainerApps Session Executor, scoped to that session pool

- A: Reader can view the pool but can't call the management API to run code.
- B: Correct. This role lets the identity call the pool API, and pool scope keeps it out of unrelated pools.
- C: Subscription scope would let the identity execute code in unrelated pools.
- D: Contributor manages resources. It's broader than needed and isn't the role for executing code.

The calling identity needs the Azure ContainerApps Session Executor role. Assign it at the session pool scope so the identity can't execute code in unrelated pools.

📘 Source: [Execute code and exchange files](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/4-execute-code-exchange-files)

</details>

## 20. `lp2m4-020`

A user asks the agent to analyze a 400 MB export in a code interpreter session. The upload fails. What does Learn suggest?

- **A.** Split the file into chunks and upload each chunk under a different session identifier
- **B.** Send a smaller approved input, or use a custom architecture
- **C.** Increase the cooldown period so that the upload has more time
- **D.** Enable egress so that the session downloads the file itself

<details><summary>💡 Hint</summary>

Code interpreter uploads have a size limit, well under 400 MB.

</details>

<details><summary>✅ Answer</summary>

**B.** Send a smaller approved input, or use a custom architecture

- A: Different identifiers address different sessions, so the chunks wouldn't be together.
- B: Correct. The code interpreter upload limit is 128 MB, so redesign the task or the architecture.
- C: The cooldown is about idle time. It doesn't change the file size limit.
- D: Egress is a security trade-off. Learn's guidance for the size limit is to redesign the input or architecture.

The code interpreter file upload limit is 128 MB. For larger data, give the session a smaller approved input or use a custom execution architecture.

📘 Source: [Execute code and exchange files](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/4-execute-code-exchange-files)

</details>

## 21. `lp2m4-021`

The backend downloads files the generated code created and saves each one locally under the file name the session reported. What's the risk, and the fix?

- **A.** File names expire with the cooldown; rename them to UUIDs inside the session
- **B.** The session could delete the file first; download it before running code
- **C.** Large files could time out, so download every generated file together in one batched request
- **D.** Path traversal: validate each name and encode it as one URL path segment

<details><summary>💡 Hint</summary>

The generated code chooses the file name. What could a malicious name do on your server?

</details>

<details><summary>✅ Answer</summary>

**D.** Path traversal: validate each name and encode it as one URL path segment

- A: The risk is on the backend's file system, not in the session.
- B: Files are produced by the code, so you can't download them before it runs.
- C: Timeouts are a separate concern. The danger is an untrusted name choosing where data is written.
- D: Correct. Never build a local path from an untrusted file name without validating it, and encode the name in the URL.

Encode the service-side file name as a single URL path segment, and never construct a local destination from an untrusted file name without validation, because path traversal could overwrite an unintended file.

📘 Source: [Execute code and exchange files](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/4-execute-code-exchange-files)

</details>

## 22. `lp2m4-022`

Classify each outcome from a dynamic session call.

Choices: **Transport failure** · **Execution failure** · **Validation failure**

- The pool API returns 403 because the identity lacks the role
- The request succeeds, but the Python code raises an exception
- The code finishes, but the required chart file wasn't produced

<details><summary>💡 Hint</summary>

Did the API call fail, did the code fail, or did the code finish but produce the wrong output?

</details>

<details><summary>✅ Answer</summary>

- The pool API returns 403 because the identity lacks the role → **Transport failure**. Authentication and authorization errors stop the API operation from completing.
- The request succeeds, but the Python code raises an exception → **Execution failure**. The session ran the payload, but the code failed.
- The code finishes, but the required chart file wasn't produced → **Validation failure**. Output that omits a required artifact is a validation failure.

Keep transport, execution, validation and success distinct for monitoring and callers.

📘 Source: [Manage lifecycle and execution failures](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/5-manage-lifecycle-failures)

</details>

## 23. `lp2m4-023`

After a user's 20-minute break, analysis code reports that /mnt/data/operational-data.csv doesn't exist, although the backend used the same identifier. What should the backend do?

- **A.** Generate a new identifier and ask the user to upload the file again
- **B.** Return an error telling the user the session identifier is invalid
- **C.** Increase the pool's cooldown to 24 hours so that the file stays available between user breaks
- **D.** Retrieve the source from durable storage, upload it again and rerun the idempotent step

<details><summary>💡 Hint</summary>

The session expired, and the identifier now gets a new, empty session.

</details>

<details><summary>✅ Answer</summary>

**D.** Retrieve the source from durable storage, upload it again and rerun the idempotent step

- A: The backend already has the source in durable storage and can recover itself.
- B: The identifier is fine; the original session simply expired.
- C: Cooldown isn't a retention guarantee, and longer retention raises risk for untrusted code.
- D: Correct. The session expired; restore inputs from durable storage and rerun safely.

After cooldown, the same identifier can map to a new empty session. Design workflows to recognize missing temporary state.

📘 Source: [Manage lifecycle and execution failures](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/5-manage-lifecycle-failures)

</details>

## 24. `lp2m4-024`

A request that runs generated code which posts a message to an external system times out on the client side. What should the backend do?

- **A.** Retry immediately, because 504 is in the transient set
- **B.** Retry three times with jitter, then report success
- **C.** Not retry automatically; check the outcome first
- **D.** Delete the session, then run the same code in a new one

<details><summary>💡 Hint</summary>

Code with side effects might already have run.

</details>

<details><summary>✅ Answer</summary>

**C.** Not retry automatically; check the outcome first

- A: The operation isn't idempotent, so an automatic retry could post the message twice.
- B: Retries don't make a non-idempotent operation safe, and success can't be assumed.
- C: Correct. A timeout is ambiguous; don't repeat side-effecting code without verifying the state.
- D: Running it again elsewhere still duplicates the side effect.

Retry only bounded, idempotent operations after evaluating the observed state.

📘 Source: [Manage lifecycle and execution failures](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/5-manage-lifecycle-failures)

</details>

## 25. `lp2m4-025`

For each statement, select Yes if the statement is true. Otherwise, select No. A conversation ends, and the backend wants the session's temporary data gone now.

| Statement | Yes / No |
|---|---|
| The backend can send DELETE …/session?identifier=… before the cooldown expires. | ☐ |
| A 204 No Content response confirms the environment no longer exists. | ☐ |
| It's safe to delete while another request for the same conversation is still running. | ☐ |
| If the DELETE fails, the backend can quietly report cleanup as done, because cooldown will handle it. | ☐ |

<details><summary>💡 Hint</summary>

Deleting ends the session right away. Think about requests still in flight.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The backend can send DELETE …/session?identifier=… before the cooldown expires. | Yes | The backend can delete a code interpreter session early. |
| A 204 No Content response confirms the environment no longer exists. | Yes | Treat 204 No Content as confirmation of deletion. |
| It's safe to delete while another request for the same conversation is still running. | No | Don't delete a session while another request for the conversation is running. |
| If the DELETE fails, the backend can quietly report cleanup as done, because cooldown will handle it. | No | Report the failure in telemetry; data or capacity may remain until cooldown. |

Clean up intentionally, confirm with 204, and keep failed deletions visible.

📘 Source: [Manage lifecycle and execution failures](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/5-manage-lifecycle-failures)

</details>

## 26. `lp2m4-026`

You want to tell a user that their analysis workspace will expire soon. How can the backend get the session's creation, last-access and expiry details?

- **A.** Query the Container Apps environment's system logs for the session's events
- **B.** Call GET …/session?identifier=`<id>` on the pool's management endpoint
- **C.** Read /mnt/data/session.json inside the session
- **D.** Run az containerapp sessionpool show for the pool

<details><summary>💡 Hint</summary>

The pool management API can describe a session by its identifier.

</details>

<details><summary>✅ Answer</summary>

**B.** Call GET …/session?identifier=`<id>` on the pool's management endpoint

- A: System logs aren't the documented way to read one session's expiry.
- B: Correct. The session query returns those details, though the backend must still handle the session disappearing.
- C: Session lifecycle data isn't exposed as a file in /mnt/data.
- D: That returns pool properties such as the management endpoint, not one session's status.

GET `<POOL_MANAGEMENT_ENDPOINT>`/session?identifier=`<SESSION_ID>` returns creation, last-access and expiration information. It's useful for diagnostics and user messaging, but the session can still disappear before the next call.

📘 Source: [Manage lifecycle and execution failures](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/5-manage-lifecycle-failures)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
