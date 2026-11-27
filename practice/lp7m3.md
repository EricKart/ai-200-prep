# Practice: LP7 · M3 Build serverless AI backends with Azure Functions

> 25 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp7m3.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-7/build-backends-azure-functions)

## 1. `lp7m3-001`

A new serverless AI backend should scale to zero for most functions but keep the chat endpoint warm. Which plan does Learn recommend?

- **A.** Legacy Consumption on Linux
- **B.** Flex Consumption with always-ready instances
- **C.** Premium with one pre-warmed worker for every function
- **D.** Dedicated App Service plan

<details><summary>💡 Hint</summary>

The recommended default plan for new apps can keep a few instances warm.

</details>

<details><summary>✅ Answer</summary>

**B.** Flex Consumption with always-ready instances

- A: Legacy Linux Consumption retires after September 2028.
- B: Correct. Always-ready keeps chosen functions warm while others scale to zero.
- C: Premium keeps workers always running; you pay the always-on cost.
- D: Dedicated makes sense when spare App Service capacity exists.

Flex Consumption is the recommended default for new serverless apps.

📘 Source: [Understand Azure Functions hosting and scaling for AI workloads](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/2-understand-hosting-scaling)

</details>

## 2. `lp7m3-002`

What is the HTTP trigger timeout imposed by the Azure Load Balancer?

- **A.** 10 minutes
- **B.** 230 seconds
- **C.** Unbounded
- **D.** 30 seconds

<details><summary>💡 Hint</summary>

The load balancer cuts HTTP calls off after a fixed time, whatever the plan.

</details>

<details><summary>✅ Answer</summary>

**B.** 230 seconds

- A: functionTimeout can't extend the load balancer limit.
- B: Correct. HTTP-triggered functions time out after 230 seconds.
- C: Service Bus triggers can be unbounded on Flex and Premium; HTTP can't.
- D: 30 seconds is Event Grid's response wait.

Long work → async request-reply with a Service Bus-triggered function.

📘 Source: [Understand Azure Functions hosting and scaling for AI workloads](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/2-understand-hosting-scaling)

</details>

## 3. `lp7m3-003`

Document extraction takes 6–8 minutes per file and is started by an HTTP call. Which design does Learn recommend?

- **A.** Return 200 after 220 seconds and keep working in the same call
- **B.** Queue it to Service Bus, return 202, process in a queue-triggered function
- **C.** Raise functionTimeout in host.json to 10 minutes for the app
- **D.** Move to Premium so that HTTP calls can run for 10 minutes

<details><summary>💡 Hint</summary>

Long work started over HTTP must not keep the HTTP call open.

</details>

<details><summary>✅ Answer</summary>

**B.** Queue it to Service Bus, return 202, process in a queue-triggered function

- A: The client never gets the result, and the work isn't decoupled.
- B: Correct. Async request-reply avoids the 230-second HTTP limit.
- C: The load balancer limit applies regardless of functionTimeout.
- D: The 230-second limit applies on every plan.

Decouple ingestion from processing so each scales on its own.

📘 Source: [Understand Azure Functions hosting and scaling for AI workloads](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/2-understand-hosting-scaling)

</details>

## 4. `lp7m3-004`

For each statement, select Yes if the statement is true. Otherwise, select No. A Flex Consumption app has two HTTP functions, a Service Bus trigger and a timer trigger.

| Statement | Yes / No |
|---|---|
| The two HTTP functions scale together on the same instances. | ☐ |
| A surge of Service Bus messages competes with HTTP requests on the same instances. | ☐ |
| Choosing 4,096 MB instances gives each instance 2 vCPUs. | ☐ |
| The app can run on Windows if needed. | ☐ |

<details><summary>💡 Hint</summary>

Per-function scaling groups HTTP triggers together. Memory size sets the vCPUs.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The two HTTP functions scale together on the same instances. | Yes | All HTTP triggers scale together as a group. |
| A surge of Service Bus messages competes with HTTP requests on the same instances. | No | Non-HTTP triggers scale on their own independent instances. |
| Choosing 4,096 MB instances gives each instance 2 vCPUs. | Yes | CPU scales with memory: 4,096 MB = 2 vCPU. |
| The app can run on Windows if needed. | No | Flex Consumption is Linux-only. |

Per-function scaling isolates trigger types; instance size sets memory and CPU.

📘 Source: [Understand Azure Functions hosting and scaling for AI workloads](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/2-understand-hosting-scaling)

</details>

## 5. `lp7m3-005`

Inference functions need a GPU and custom OS-level packages, and must run next to other containerized microservices. Which hosting option fits?

- **A.** Flex Consumption with 4,096 MB instances
- **B.** Dedicated App Service plan
- **C.** Azure Container Apps hosting
- **D.** Premium plan with pre-warmed workers

<details><summary>💡 Hint</summary>

GPU and custom OS packages next to other containers.

</details>

<details><summary>✅ Answer</summary>

**C.** Azure Container Apps hosting

- A: Flex Consumption doesn't provide GPUs.
- B: Dedicated is for reusing spare App Service capacity.
- C: Correct. Container Apps hosting suits GPU access, custom OS packages and side-by-side containers.
- D: Premium supports custom images but Learn points to Container Apps for GPU.

Pick Container Apps when functions need GPU or custom OS packages.

📘 Source: [Understand Azure Functions hosting and scaling for AI workloads](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/2-understand-hosting-scaling)

</details>

## 6. `lp7m3-006`

A Flex Consumption function loads a large model and needs two vCPUs and stable per-call performance. What should you choose?

- **A.** 2,048 MB instances with always-ready instances set
- **B.** 512 MB instances with many more instances
- **C.** 4,096 MB instances, lower concurrency
- **D.** 2,048 MB instances with higher concurrency

<details><summary>💡 Hint</summary>

CPU grows with instance memory, and concurrency decides how many calls share an instance.

</details>

<details><summary>✅ Answer</summary>

**C.** 4,096 MB instances, lower concurrency

- A: Always-ready avoids cold starts, but each instance still has 1 vCPU.
- B: Small instances don't give two vCPUs to one invocation.
- C: Correct. 4,096 MB gives 2 vCPUs, and lower concurrency gives each invocation more dedicated resources.
- D: 2,048 MB gives 1 vCPU, and higher concurrency makes invocations share it.

Flex Consumption instance sizes are 512, 2,048 and 4,096 MB; CPU scales with memory (4,096 MB = 2 vCPUs). Lower concurrency spreads load across more instances and isolates resources per invocation.

📘 Source: [Understand Azure Functions hosting and scaling for AI workloads](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/2-understand-hosting-scaling)

</details>

## 7. `lp7m3-007`

A team is starting a new Linux function app and plans to use the Consumption plan because their older apps use it. What should you tell them?

- **A.** Linux Consumption is still the recommended default for new apps
- **B.** It's a legacy plan retiring in 2028; use Flex Consumption
- **C.** Linux Consumption is fine, because it now supports always-ready instances
- **D.** Use the Dedicated plan, because serverless plans don't run Python

<details><summary>💡 Hint</summary>

One of the serverless plans is being retired.

</details>

<details><summary>✅ Answer</summary>

**B.** It's a legacy plan retiring in 2028; use Flex Consumption

- A: Flex Consumption is the recommended default for new serverless apps.
- B: Correct. New projects should use Flex Consumption.
- C: Always-ready instances are a Flex Consumption feature.
- D: Serverless plans run Python. The issue is the legacy plan.

The Linux Consumption plan is legacy; running function apps on Linux in a Consumption plan retires after September 2028. New projects should use Flex Consumption.

📘 Source: [Understand Azure Functions hosting and scaling for AI workloads](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/2-understand-hosting-scaling)

</details>

## 8. `lp7m3-008`

You run a function app locally with Core Tools. At which address are HTTP triggers exposed by default?

- **A.** http://localhost:7071
- **B.** http://localhost:5000
- **C.** https://localhost:443
- **D.** http://localhost:10000

<details><summary>💡 Hint</summary>

Core Tools runs the host on localhost with a default port.

</details>

<details><summary>✅ Answer</summary>

**A.** http://localhost:7071

- A: Correct. Core Tools exposes HTTP endpoints on port 7071 by default.
- B: 5000 isn't the Functions default.
- C: 443 isn't used locally by Core Tools.
- D: 10000 is the Azure Managed Redis port.

func start or F5 launches the host on localhost:7071.

📘 Source: [Set up the local development environment for Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/3-set-up-local-development-environment)

</details>

## 9. `lp7m3-009`

Locally, HTTP functions work but a queue trigger and a timer trigger never fire. AzureWebJobsStorage is empty. What should you set?

- **A.** UseDevelopmentStorage=true, with Azurite
- **B.** A Cosmos DB emulator connection string
- **C.** FUNCTIONS_WORKER_RUNTIME set to python
- **D.** A longer functionTimeout in host.json

<details><summary>💡 Hint</summary>

Non-HTTP triggers need a storage connection, even locally.

</details>

<details><summary>✅ Answer</summary>

**A.** UseDevelopmentStorage=true, with Azurite

- A: Correct. The runtime needs storage for non-HTTP triggers; Azurite emulates it locally.
- B: Cosmos DB isn't the runtime's storage dependency.
- C: The worker runtime isn't the missing piece here.
- D: Timeouts don't make triggers fire.

Without a valid storage connection, non-HTTP triggers don't work.

📘 Source: [Set up the local development environment for Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/3-set-up-local-development-environment)

</details>

## 10. `lp7m3-010`

For each statement, select Yes if the statement is true. Otherwise, select No. A team sets up a Python Functions project in VS Code.

| Statement | Yes / No |
|---|---|
| local.settings.json should be committed so teammates get the same secrets. | ☐ |
| The .vscode folder should be committed for a consistent F5 experience. | ☐ |
| func init and func new also generate the .vscode configuration files. | ☐ |
| Changes in host.json affect every function in the app. | ☐ |

<details><summary>💡 Hint</summary>

Commit code and editor config. Keep local secrets out of Git.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| local.settings.json should be committed so teammates get the same secrets. | No | Never commit it; it often contains secrets. |
| The .vscode folder should be committed for a consistent F5 experience. | Yes | Learn says to commit these files. |
| func init and func new also generate the .vscode configuration files. | No | They don't; use Create Function... or add them manually. |
| Changes in host.json affect every function in the app. | Yes | host.json is shared runtime configuration. |

Commit code and editor config; keep local secrets out of source control.

📘 Source: [Set up the local development environment for Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/3-set-up-local-development-environment)

</details>

## 11. `lp7m3-011`

You fetched production settings into local.settings.json with Core Tools and now worry about secrets on your laptop. What does Learn suggest?

- **A.** Run func settings encrypt
- **B.** Rename the file to .env
- **C.** Set IsEncrypted to true by hand
- **D.** Commit the file to a private repository

<details><summary>💡 Hint</summary>

Core Tools has a command that protects the local settings file.

</details>

<details><summary>✅ Answer</summary>

**A.** Run func settings encrypt

- A: Correct. Core Tools encrypts the file; only Core Tools on the same machine can decrypt it.
- B: Renaming doesn't protect the values.
- C: Editing the flag doesn't encrypt the values.
- D: Committing secrets is exactly what to avoid.

func azure functionapp fetch-app-settings downloads; func settings encrypt protects.

📘 Source: [Set up the local development environment for Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/3-set-up-local-development-environment)

</details>

## 12. `lp7m3-012`

How many triggers can an Azure Function have?

- **A.** Exactly one
- **B.** Any number
- **C.** Zero or one
- **D.** Up to two

<details><summary>💡 Hint</summary>

Bindings can be many. Triggers can't.

</details>

<details><summary>✅ Answer</summary>

**A.** Exactly one

- A: Correct. Every function has exactly one trigger.
- B: Bindings can be many; triggers can't.
- C: Every function has a trigger.
- D: Learn says exactly one.

One trigger; zero or more input and output bindings.

📘 Source: [Create triggers and bindings for AI integration patterns](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/4-create-triggers-bindings-ai-patterns)

</details>

## 13. `lp7m3-013`

Each Service Bus message triggers memory-heavy inference, and processing can take 4 minutes. Which host.json settings does Learn recommend tuning?

- **A.** maxDeliveryCount 1 and functionTimeout 230 s
- **B.** authLevel function and concurrency set to 0
- **C.** maxConcurrentCalls 1; lock renewal over 4 min
- **D.** prefetchCount 0 and maxConcurrentCalls 100

<details><summary>💡 Hint</summary>

Heavy messages: process fewer at once, and keep the lock longer than the work.

</details>

<details><summary>✅ Answer</summary>

**C.** maxConcurrentCalls 1; lock renewal over 4 min

- A: maxDeliveryCount is set on the queue resource; 230 s is the HTTP limit.
- B: Auth level applies to HTTP triggers.
- C: Correct. One message per instance gets full resources, and lock renewal covers the long call.
- D: High concurrency shares resources across messages.

Tune concurrency and lock renewal for resource-heavy AI processing.

📘 Source: [Create triggers and bindings for AI integration patterns](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/4-create-triggers-bindings-ai-patterns)

</details>

## 14. `lp7m3-014`

For each statement, select Yes if the statement is true. Otherwise, select No. A function calls Azure AI Document Intelligence on every Service Bus message.

| Statement | Yes / No |
|---|---|
| There's a dedicated Functions binding for Document Intelligence. | ☐ |
| Creating the client at module level lets it persist across invocations. | ☐ |
| DefaultAzureCredential uses the app's managed identity in Azure and developer credentials locally. | ☐ |

<details><summary>💡 Hint</summary>

No binding exists for every service. Create SDK clients once, outside the handler.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| There's a dedicated Functions binding for Document Intelligence. | No | Services without bindings need SDK clients in code. |
| Creating the client at module level lets it persist across invocations. | Yes | Initialize clients outside the handler. |
| DefaultAzureCredential uses the app's managed identity in Azure and developer credentials locally. | Yes | Same code in both environments. |

Bindings for supported services; module-level SDK clients for the rest.

📘 Source: [Create triggers and bindings for AI integration patterns](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/4-create-triggers-bindings-ai-patterns)

</details>

## 15. `lp7m3-015`

A production inference endpoint must not be callable anonymously, but full identity checks are handled later by API Management. Which HTTP auth level is the recommended baseline?

- **A.** system
- **B.** anonymous
- **C.** function
- **D.** admin

<details><summary>💡 Hint</summary>

Keys are a basic barrier. Identity checks come from another layer.

</details>

<details><summary>✅ Answer</summary>

**C.** function

- A: System isn't an HTTP auth level; system keys are for extensions.
- B: Anonymous requires no key.
- C: Correct. Function-level keys are the recommended production baseline.
- D: Admin needs the master key and is for administrative operations.

Keys are a basic barrier; layer API Management or Easy Auth for identity.

📘 Source: [Create triggers and bindings for AI integration patterns](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/4-create-triggers-bindings-ai-patterns)

</details>

## 16. `lp7m3-016`

A function app setting uses a Key Vault reference but resolves to an error. The app has a managed identity. What's most likely missing?

- **A.** Key Vault Secrets User on the vault
- **B.** A Key Vault binding in function_app.py
- **C.** An App Configuration store for the app
- **D.** A value for the AzureWebJobsStorage setting

<details><summary>💡 Hint</summary>

Key Vault references are resolved by the app's identity. Which data-plane role lets it read values?

</details>

<details><summary>✅ Answer</summary>

**A.** Key Vault Secrets User on the vault

- A: Correct. Without the role, the runtime can't retrieve the secret.
- B: References are resolved by the platform; no binding is needed.
- C: App Configuration isn't required for Key Vault references.
- D: Storage is unrelated to Key Vault resolution.

Key Vault references need a managed identity with Key Vault Secrets User.

📘 Source: [Manage secrets and configuration in Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/5-manage-secrets-configuration)

</details>

## 17. `lp7m3-017`

Ten function apps and microservices share the same inference threshold and feature flags, which change weekly. Where should these non-secret values live?

- **A.** Azure App Configuration
- **B.** Each app's local.settings.json
- **C.** host.json in each app
- **D.** A Key Vault secret per app

<details><summary>💡 Hint</summary>

Shared, non-secret settings that change often belong in a central store.

</details>

<details><summary>✅ Answer</summary>

**A.** Azure App Configuration

- A: Correct. Change once, and all connected apps get the update.
- B: local.settings.json is for local development only.
- C: host.json is runtime configuration, not shared app settings.
- D: Key Vault is for secrets.

App Configuration for shared non-secret settings; Key Vault for secrets.

📘 Source: [Manage secrets and configuration in Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/5-manage-secrets-configuration)

</details>

## 18. `lp7m3-018`

For each statement, select Yes if the statement is true. Otherwise, select No. A setting is `@Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/AiServiceKey/)`, with no version.

| Statement | Yes / No |
|---|---|
| After the secret rotates, the app uses the new version within 24 hours. | ☐ |
| Changing any other app setting forces an immediate refetch. | ☐ |
| The function code must call the Key Vault SDK to read the value. | ☐ |

<details><summary>💡 Hint</summary>

Versionless URIs follow rotation, and config changes force a refresh.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| After the secret rotates, the app uses the new version within 24 hours. | Yes | Versionless URIs pick up new versions within 24 hours. |
| Changing any other app setting forces an immediate refetch. | Yes | Configuration changes trigger an immediate refetch. |
| The function code must call the Key Vault SDK to read the value. | No | Code reads os.environ as usual. |

Use versionless URIs for secrets that rotate on a schedule.

📘 Source: [Manage secrets and configuration in Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/5-manage-secrets-configuration)

</details>

## 19. `lp7m3-019`

A Service Bus trigger uses an identity-based connection named ServiceBusConnection. Which app setting should exist?

- **A.** ServiceBusConnection__fullyQualifiedNamespace
- **B.** ServiceBusConnection__accountEndpoint set to its URL
- **C.** ServiceBusConnection holding a full SAS connection string
- **D.** ServiceBusConnection__accountName set to the namespace

<details><summary>💡 Hint</summary>

Identity-based connections replace the connection string with the namespace address.

</details>

<details><summary>✅ Answer</summary>

**A.** ServiceBusConnection__fullyQualifiedNamespace

- A: Correct. Messaging services use __fullyQualifiedNamespace, e.g. mynamespace.servicebus.windows.net.
- B: __accountEndpoint is the Cosmos DB suffix.
- C: That's a connection string, which identity-based connections replace.
- D: __accountName is the storage suffix.

Assign Azure Service Bus Data Receiver to the app's identity.

📘 Source: [Configure identity and access for Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/6-configure-identity-access)

</details>

## 20. `lp7m3-020`

Match each identity-based connection to the role the function app's identity needs.

Choices: **Storage Blob Data Owner** · **Azure Service Bus Data Receiver** · **Azure Service Bus Data Sender** · **Cosmos DB Built-in Data Contributor**

- AzureWebJobsStorage__accountName for the runtime
- Service Bus queue trigger
- Service Bus output binding
- Cosmos DB output binding

<details><summary>💡 Hint</summary>

Each connection needs its own data-plane role.

</details>

<details><summary>✅ Answer</summary>

- AzureWebJobsStorage__accountName for the runtime → **Storage Blob Data Owner**. Minimum role for host-level coordination.
- Service Bus queue trigger → **Azure Service Bus Data Receiver**. Triggers receive messages.
- Service Bus output binding → **Azure Service Bus Data Sender**. Output bindings send messages.
- Cosmos DB output binding → **Cosmos DB Built-in Data Contributor**. Writes items to the container.

Each binding extension documents its identity properties and roles.

📘 Source: [Configure identity and access for Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/6-configure-identity-access)

</details>

## 21. `lp7m3-021`

For each statement, select Yes if the statement is true. Otherwise, select No. A function app with identity-based storage uses a **blob trigger** and calls Azure OpenAI.

| Statement | Yes / No |
|---|---|
| Storage Blob Data Owner alone is enough for the blob trigger. | ☐ |
| The identity needs Cognitive Services OpenAI User to call Azure OpenAI. | ☐ |
| Host keys grant access to every HTTP-triggered function in the app. | ☐ |
| Function keys verify the caller's Entra ID identity. | ☐ |

<details><summary>💡 Hint</summary>

Blob triggers need more than host storage roles. Keys aren't identity.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Storage Blob Data Owner alone is enough for the blob trigger. | No | Blob triggers also need Storage Queue Data Contributor and Storage Account Contributor. |
| The identity needs Cognitive Services OpenAI User to call Azure OpenAI. | Yes | That's the least-privilege role Learn names. |
| Host keys grant access to every HTTP-triggered function in the app. | Yes | Host keys are scoped to all functions. |
| Function keys verify the caller's Entra ID identity. | No | Keys are a basic barrier; use API Management or Easy Auth for identity. |

Assign least-privilege roles per service; keys aren't identity.

📘 Source: [Configure identity and access for Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/6-configure-identity-access)

</details>

## 22. `lp7m3-022`

A monitoring tool must call every HTTP function in one app, and you want to avoid handing out the master key. Which key type fits?

- **A.** Anonymous auth level on every function
- **B.** A host key
- **C.** The master key
- **D.** A system key

<details><summary>💡 Hint</summary>

One key type opens every function in the app without being the master key.

</details>

<details><summary>✅ Answer</summary>

**B.** A host key

- A: Anonymous removes the key barrier for every caller, not just the tool.
- B: Correct. Host keys cover all functions in the app and suit monitoring agents.
- C: The master key is highly sensitive and grants admin access.
- D: System keys are for extensions, not shared tools.

Function keys: one function. Host keys: all functions. Master: admin.

📘 Source: [Configure identity and access for Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/6-configure-identity-access)

</details>

## 23. `lp7m3-023`

A function app uses identity-based AzureWebJobsStorage__accountName and has a blob trigger. Which roles does the app identity need on the storage account?

- **A.** Storage Blob Data Reader and Storage Queue Data Reader
- **B.** Storage Account Contributor alone, at subscription scope
- **C.** Storage Blob Data Owner only, as for host coordination
- **D.** Blob Data Owner, Queue Data Contributor, Account Contributor

<details><summary>💡 Hint</summary>

The host needs one role. Blob triggers also use storage queues behind the scenes.

</details>

<details><summary>✅ Answer</summary>

**D.** Blob Data Owner, Queue Data Contributor, Account Contributor

- A: Reader roles can't write the receipts and state the trigger needs.
- B: That's a management role. It doesn't give data access, and the scope is too broad.
- C: That's the minimum for the host. Blob triggers need more.
- D: Correct. Blob triggers use queues for blob receipts, so they need more than the host's minimum role.

With identity-based AzureWebJobsStorage, the minimum is Storage Blob Data Owner. Blob triggers also need Storage Queue Data Contributor and Storage Account Contributor.

📘 Source: [Configure identity and access for Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/6-configure-identity-access)

</details>

## 24. `lp7m3-024`

Your function app hosts an MCP server through the MCP extension. Which kind of key does the extension use to authenticate MCP client connections?

- **A.** The mcp_extension system key that the extension manages
- **B.** An Entra ID token for each client's user
- **C.** The master key, shared with every client
- **D.** A function key on each MCP tool function

<details><summary>💡 Hint</summary>

Some extensions get their own key type for internal operations.

</details>

<details><summary>✅ Answer</summary>

**A.** The mcp_extension system key that the extension manages

- A: Correct. Extensions use system keys for internal operations.
- B: Learn names the mcp_extension system key for MCP client connections.
- C: The master key is for administration and should never be handed to clients.
- D: Function keys cover one HTTP function. The extension uses its own system key.

Key types: function keys (one function), host keys (all functions), the master key (admin), and system keys used by extensions, for example the MCP extension's mcp_extension key.

📘 Source: [Configure identity and access for Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/6-configure-identity-access)

</details>

## 25. `lp7m3-025`

A production inference endpoint must verify each caller's Microsoft Entra identity, not just check for a key. What does Learn recommend layering on top of function keys?

- **A.** The admin authorization level
- **B.** An anonymous authorization level with an IP allow list
- **C.** A second function key that only trusted callers receive
- **D.** Azure API Management or Easy Auth

<details><summary>💡 Hint</summary>

Keys say "has the secret". You need "who is calling".

</details>

<details><summary>✅ Answer</summary>

**D.** Azure API Management or Easy Auth

- A: Admin needs the master key, which is meant for administration.
- B: Anonymous removes the key barrier, and IP lists don't identify callers.
- C: More keys are still shared secrets, not identity.
- D: Correct. Keys are a basic barrier; these add caller identity verification.

Access keys provide a basic access barrier but don't replace authentication. For caller identity verification, layer Azure API Management or App Service Authentication (Easy Auth).

📘 Source: [Configure identity and access for Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/6-configure-identity-access)

</details>


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
