# LP7 · M3: Build serverless AI backends with Azure Functions

> **Learning path 7:** Integrate backend services for AI solutions · **Skill area 3:** Connect to and consume Azure services · about 98 min on Microsoft Learn  
> Study it interactively at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-7/build-backends-azure-functions)

Azure Functions runs event-driven code without servers. You'll learn the hosting plans, local development, triggers and bindings, app settings, and securing functions with identity.

**In this lesson**

1. [Understand Azure Functions hosting and scaling for AI workloads](#understand-azure-functions-hosting-and-scaling-for-ai-workloads)
2. [Set up the local development environment for Functions](#set-up-the-local-development-environment-for-functions)
3. [Create triggers and bindings for AI integration patterns](#create-triggers-and-bindings-for-ai-integration-patterns)
4. [Manage secrets and configuration in Functions](#manage-secrets-and-configuration-in-functions)
5. [Configure identity and access for Functions](#configure-identity-and-access-for-functions)

## Understand Azure Functions hosting and scaling for AI workloads

📘 Microsoft Learn: [Understand Azure Functions hosting and scaling for AI workloads](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/2-understand-hosting-scaling)

**Flex Consumption** is the default: pay for what runs, scale to zero, keep a few **always-ready** instances warm for the impatient endpoints. **Premium** keeps a worker always warm (no cold starts) for near-constant load or custom images. HTTP calls are cut off at **230 seconds**, so long AI jobs go through a queue.

**Key facts**

- **Cold start**: allocating an instance, loading the runtime and dependencies before the first request. Per instance only. AI libraries and connection warm-up make it longer.
- **Flex Consumption** (recommended default; **Linux only**): per-function scaling, instance memory **512 MB, 2,048 MB (default) or 4,096 MB**, VNet integration, **always-ready instances**, up to **1,000 instances**; billed on execution time plus any always-ready baseline.
- **Premium**: at least one **pre-warmed** worker always running (no cold starts), event-driven scaling, **custom Linux images**, VNet. For continuous load, larger sizes or custom containers.
- Other options: **Dedicated (App Service)** when spare App Service capacity exists; **Container Apps** for GPU, custom OS packages or alongside other containers; legacy **Consumption (Linux)** retires after **September 2028**.
- Per-function scaling: **all HTTP triggers scale together**; every other trigger type (queue, Service Bus, timer) scales on its own instances.
- Concurrency: lower = more instances, more isolation (good for heavy inference); higher = fewer instances, more memory per instance.
- CPU scales with memory: **2,048 MB = 1 vCPU**, **4,096 MB = 2 vCPU**.
- HTTP triggers time out after **230 seconds** (Azure Load Balancer), whatever functionTimeout says. Use **async request-reply**: HTTP function queues to Service Bus and returns **202 Accepted** with a status URL; a Service Bus-triggered function does the work (unbounded duration on Flex Consumption and Premium).

| Need | Choose |
|---|---|
| New serverless app, scale to zero, warm a few endpoints | Flex Consumption + always-ready |
| No cold starts, continuous load, custom image | Premium |
| GPU model inference | Container Apps hosting |
| Spare App Service capacity | Dedicated plan |

> [!WARNING]
> **Exam traps**
>
> - 230-second HTTP limit applies regardless of host.json functionTimeout.
> - Flex Consumption is Linux-only.
> - Legacy Linux Consumption retires after September 2028.

## Set up the local development environment for Functions

📘 Microsoft Learn: [Set up the local development environment for Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/3-set-up-local-development-environment)

Install **Core Tools** (the local Functions runtime) and the VS Code extension, press **F5**, and your functions run at `localhost:7071`. Keep local secrets in **local.settings.json** (never commit it) and point storage at the **Azurite** emulator.

**Key facts**

- **Azure Functions Core Tools** is the local runtime with the same trigger and binding logic as Azure. Install with Homebrew, apt/yum or `winget install Microsoft.Azure.FunctionsCoreTools`; check with `func --version`.
- VS Code **Azure Functions: Create Function...** scaffolds the project and generates `.vscode/launch.json`, `tasks.json`, `extensions.json`. `func init`/`func new` don't create .vscode files.
- `func start` or **F5** runs the host; HTTP endpoints at **http://localhost:7071**.
- Python v2 model: one **function_app.py** with decorators; split large apps with **blueprints**.
- **host.json**: global runtime config (timeouts, logging, extension bundles, trigger concurrency) for every function.
- **local.settings.json**: local app settings in `Values`, exposed as environment variables; excluded by .gitignore; **never commit it**. Commit the **.vscode** folder. **.funcignore** trims deployment packages.
- The runtime needs storage (**AzureWebJobsStorage**) for coordination, timers and keys; without it non-HTTP triggers don't work. Locally: `UseDevelopmentStorage=true` with **Azurite** (VS Code extension or `npm install -g azurite`).
- Local stand-ins: **Cosmos DB emulator** (NoSQL API; Docker on macOS); PostgreSQL and Redis via Docker (no Azure-specific emulators).
- Sync settings: Download Remote Settings / Upload Local Settings, `func azure functionapp fetch-app-settings`; protect with `func settings encrypt` (decryptable only on that machine).

| File | Purpose | Commit? |
|---|---|---|
| function_app.py | Function definitions (v2 decorators) | Yes |
| host.json | Global runtime settings | Yes |
| local.settings.json | Local settings and secrets | No |
| .vscode/ | Debug and task config | Yes |
| .funcignore | Exclude files from deployment | Yes |

> [!WARNING]
> **Exam traps**
>
> - No storage connection → queue and timer triggers don't run.
> - UseDevelopmentStorage=true only works locally.

## Create triggers and bindings for AI integration patterns

📘 Microsoft Learn: [Create triggers and bindings for AI integration patterns](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/4-create-triggers-bindings-ai-patterns)

A **trigger** is the doorbell that starts a function (exactly one). **Bindings** are the pipes that carry data in or out without SDK code (zero or more). For services with no binding, such as Azure OpenAI or Document Intelligence, create the SDK client **once, outside the handler**.

**Key facts**

- Every function has **exactly one trigger**; the trigger also acts as an input binding. **Bindings** (input/output) are optional; zero or many.
- **HTTP trigger**: `@app.route()`; auth levels **anonymous** (dev, health checks), **function** (recommended production baseline; key in `x-functions-key` header or `code` query), **admin** (master key). Keys don't replace Entra ID or API Management.
- **Service Bus queue trigger**: `@app.service_bus_queue_trigger(arg_name, queue_name, connection)`; handles retries, dead-lettering and scaling.
- host.json Service Bus settings: **maxConcurrentCalls** (1 gives each message the full instance) and **maxAutoLockRenewalDuration** (cover your longest processing time).
- maxDeliveryCount (default 10) is set on the **queue resource**; exceeded messages go to the DLQ.
- Output bindings: `@app.blob_output(path="results/{rand-guid}.json")`, `@app.cosmos_db_output(…)`, Service Bus output for fan-out. Multiple outputs via a custom return type.
- No binding for Azure AI Document Intelligence, Azure OpenAI, Azure AI Search: create SDK clients at **module level** so they persist across invocations; authenticate with DefaultAzureCredential.

| Need | Trigger / binding |
|---|---|
| Synchronous inference endpoint | HTTP trigger (@app.route) |
| Process queued work items | Service Bus queue trigger |
| Save processed text | Blob output binding |
| Write inference results as JSON documents | Cosmos DB output binding |
| Call Azure OpenAI | SDK client created at module level |

> [!WARNING]
> **Exam traps**
>
> - One trigger per function, always.
> - maxDeliveryCount lives on the queue, not in host.json.

## Manage secrets and configuration in Functions

📘 Microsoft Learn: [Manage secrets and configuration in Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/5-manage-secrets-configuration)

Settings become environment variables. Secrets live in **Key Vault**, and the app setting just points there (`@Microsoft.KeyVault(…)`). Shared, non-secret settings for many apps go to **App Configuration**.

**Key facts**

- App settings are injected as **environment variables**, encrypted at rest; read with `os.environ` (required) or `os.getenv` (default). Keep each setting a single value.
- Key Vault references: `@Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/AiServiceKey/)` or `@Microsoft.KeyVault(VaultName=myvault;SecretName=AiServiceKey)`.
- Needs a managed identity with **Key Vault Secrets User** on the vault; otherwise the setting resolves to an error.
- Versionless URIs pick up rotated secrets within **24 hours**; any config change refetches immediately; a versioned URI stays pinned.
- **App Configuration**: central non-secret settings and feature flags shared by many apps; Python `azure-appconfiguration-provider`; **label** filtering per environment; can hold Key Vault references.
- Local: local.settings.json mirrors app settings; fetch-app-settings and settings encrypt.

> [!WARNING]
> **Exam traps**
>
> - Missing Key Vault Secrets User → the setting shows an error, not the secret.
> - Versioned secret URIs don't follow rotation.

## Configure identity and access for Functions

📘 Microsoft Learn: [Configure identity and access for Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/6-configure-identity-access)

Swap connection strings for **identity-based connections**: the setting holds only the endpoint (`…__fullyQualifiedNamespace`), and the app's managed identity gets a role. For HTTP endpoints, **keys** are a basic gate, not identity.

**Key facts**

- Identity-based connections: enable a managed identity, assign roles on the target; settings use the connection prefix plus a **suffix** instead of a connection string.
- Runtime storage: `AzureWebJobsStorage__accountName`; minimum role **Storage Blob Data Owner**. Blob triggers also need **Storage Queue Data Contributor** and **Storage Account Contributor**.
- Service Bus: `ServiceBusConnection__fullyQualifiedNamespace`; **Azure Service Bus Data Receiver** for triggers, **Data Sender** for output bindings.
- Cosmos DB: `CosmosDBConnection__accountEndpoint`; **Cosmos DB Built-in Data Contributor**. Suffixes: storage __accountName, Cosmos __accountEndpoint, messaging __fullyQualifiedNamespace.
- SDK clients: DefaultAzureCredential at **module level**. Roles: Document Intelligence **Cognitive Services User**; AI Search **Search Index Data Reader/Contributor**; Azure OpenAI **Cognitive Services OpenAI User**.
- Keys: **function keys** (one function), **host keys** (all functions), **system keys** (extensions, e.g. mcp_extension), **master key** (admin, runtime APIs; never in clients).
- Keys don't verify identity: layer **API Management** (rate limiting, OAuth 2.0) or **Easy Auth** (Entra ID).

| Connection | Setting suffix | Role |
|---|---|---|
| Runtime storage | AzureWebJobsStorage__accountName | Storage Blob Data Owner |
| Service Bus trigger | __fullyQualifiedNamespace | Azure Service Bus Data Receiver |
| Service Bus output | __fullyQualifiedNamespace | Azure Service Bus Data Sender |
| Cosmos DB output | __accountEndpoint | Cosmos DB Built-in Data Contributor |

> [!WARNING]
> **Exam traps**
>
> - Blob triggers need extra storage roles beyond Blob Data Owner.
> - Never embed the master key in a client.

## Check yourself

- **Practice questions:** [lp7m3 on GitHub](../../practice/lp7m3.md), or [on the site](https://aryantripathi.dev/ai-200/lp-7/build-backends-azure-functions) with hints and saved progress
- **Cheat sheet:** [Learning path 7](../cheatsheets/lp7.md)
- **Microsoft Learn exercise:** [Create an MCP server with Azure Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/7-exercise-create-mcp-server)
- **Hands-on lab:** [labs/](../../labs/README.md) has a lab for this learning path

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
