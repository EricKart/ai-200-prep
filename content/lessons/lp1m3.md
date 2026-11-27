# LP1 · M3: Run sidecar-enabled AI applications on Azure App Service

> **Learning path 1:** Implement container application hosting on Azure · **Skill area 1:** Develop and deploy containerized solutions · about 85 min on Microsoft Learn  
> Study it interactively at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-1/deploy-sidecar-azure-app-service)

A sidecar runs next to your main container on the same App Service instance, for example a small model server beside an API. You'll learn when sidecars fit, how to configure them, how containers talk and share files, and how to diagnose failures.

**In this lesson**

1. [Choose the App Service sidecar pattern](#choose-the-app-service-sidecar-pattern)
2. [Configure main and sidecar containers](#configure-main-and-sidecar-containers)
3. [Connect containers and share files](#connect-containers-and-share-files)
4. [Diagnose sidecar failures](#diagnose-sidecar-failures)

## Choose the App Service sidecar pattern

📘 Microsoft Learn: [Choose the App Service sidecar pattern](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/2-choose-sidecar-pattern)

A sidecar is a **helper container that rides along** with your main app on every instance: same start, same stop, same scale. It's great when each API copy needs its own small local model server. If the helper needs its own GPU, its own scaling or serves many apps, give it **its own house** (a separate service) instead.

**Key facts**

- A sidecar is an **auxiliary container** in the same environment as the main **Linux** app container: local AI inference, telemetry collection or caching without putting them in the main image.
- One **main** container plus **up to nine** sidecars. Each keeps its own image, startup command and container-specific configuration.
- The main container has **isMain: true** and is the only one that receives **external HTTP traffic**. Sidecars use isMain: false and are reachable through the **shared network namespace**.
- Lifecycle: containers start and stop together; **scale out** adds the main container and all sidecars to each new instance; scale in removes the complete set. A config deployment can update a sidecar image independently but it's still the same app.
- Sidecars share the trust boundary (run only **trusted images**) and the **same App Service plan capacity**; the plan doesn't scale the model server separately.
- Good fit: exactly one local helper per instance, same lifecycle and scaling, meaningful latency or data-boundary benefit, combined CPU and memory fit the plan, trusted images.
- Use a **separate service** when several apps share the endpoint, model serving needs **GPU** or a different scaling policy, a separate network or security boundary is needed, it must stay up while the app restarts or scales to zero, or its failures shouldn't consume the app's resources.
- Configuration model: **sitecontainers**. Each container is a `Microsoft.Web/sites/sitecontainers` resource and the app has `LinuxFxVersion=sitecontainers` (classic apps use `DOCKER|<image>`; older multi-container apps use Docker Compose).
- After conversion, classic settings such as **WEBSITES_PORT** and **DOCKER_REGISTRY_SERVER_*** don't configure the containers.
- Capacity planning: measure model load memory, CPU and memory under concurrent requests, include **startup overlap**, choose a plan for combined peak plus headroom, then review metrics and test scale out.

| Situation | Sidecar | Separate service |
|---|---|---|
| One internal API needs a compact local model | ✔ |  |
| Several apps share one model endpoint |  | ✔ |
| Model needs GPU or its own scaling rule |  | ✔ |
| Helper must stay up while the app scales to zero |  | ✔ |
| Local call cuts latency; resources fit the plan | ✔ |  |

> [!WARNING]
> **Exam traps**
>
> - Only the **isMain: true** container gets external HTTP traffic.
> - Up to **nine** sidecars per app.
> - WEBSITES_PORT and DOCKER_REGISTRY_SERVER_* **don't** configure sidecar-enabled containers.

## Configure main and sidecar containers

📘 Microsoft Learn: [Configure main and sidecar containers](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/3-configure-sidecar-containers)

Each container gets its own **name card**: image, role (main or not), the port it listens on and how it logs in to the registry. App settings are a **shared notice board** every container can read; container-specific variables are **private notes** for one container.

**Key facts**

- Create a new sidecar-enabled app with `az webapp create … --sitecontainers-app`; convert an existing eligible app with `az webapp sitecontainers convert --mode sitecontainers` (validate in nonproduction first).
- Every container needs a **unique name** and a full image reference. Exactly one has **isMain: true** (`--is-main`); omitting it leaves false.
- The main process must listen on **port 80 or 8080**. Each listening process needs a **unique port**, because containers share one network namespace.
- **Target port** is metadata: it doesn't control routing or reconfigure the process. A sidecar that accepts no connections can omit it.
- **App settings** are available to **all containers**; container-specific environment variables belong to one definition. In a site container resource, `environmentVariables[].value` names an **App Setting**, not a literal value.
- Apply a full spec with `az webapp sitecontainers create --sitecontainers-spec-file ./spec.json`; other input arguments are then ignored. Don't put credentials in the spec file.
- Private pulls from ACR use **managed identity** (system- or user-assigned; user-assigned uses `authType: UserAssigned` and the identity's **client ID**).
- The registry must accept **Azure Resource Manager audience tokens** (check with `az acr config authentication-as-arm show`); otherwise you see **UNAUTHORIZED … token validation failed**.
- Pull role depends on the registry's permissions mode: **AcrPull** for RBAC Registry Permissions; **Container Registry Repository Reader** for RBAC Registry + ABAC Repository Permissions.
- Role assignments take time to **propagate**. Use **immutable tags or digests**. Verify with `az webapp sitecontainers list` and `show`.

| Setting | Applies to | Note |
|---|---|---|
| App setting | All containers | Source value referenced by name |
| Container environment variable | One container | value = name of an App Setting |
| isMain / --is-main | Exactly one container | Gets external traffic; port 80 or 8080 |
| targetPort | Each listening container | Metadata only; must be unique |
| authType: UserAssigned + client ID | Private image pulls | Identity needs the pull role |

> [!WARNING]
> **Exam traps**
>
> - The main container listens on **80 or 8080** only.
> - environmentVariables[].value is the **name of an App Setting**, not the secret itself.
> - ABAC repository permissions mode needs **Container Registry Repository Reader**, not AcrPull.

## Connect containers and share files

📘 Microsoft Learn: [Connect containers and share files](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/4-connect-containers-share-files)

Containers in one app are **roommates in the same flat**: they call each other on **localhost** (each on its own port) and leave files for each other in the shared **/home** folder. But a roommate can still be asleep or slow, so the main API needs timeouts, and /home isn't a safe-deposit box.

**Key facts**

- Containers share **one network namespace**: call another container at **localhost:`<port>`**, not by container or service name. Each process needs a **unique port**.
- On each instance, the main container calls the sidecar **on that same instance**.
- Use a short **connection timeout** and an overall request deadline. The main app stays the **external security boundary**: authentication, authorization, validation and response filtering.
- Request policy: short connect timeout, request deadline, cancellation, a **limited retry only for idempotent, transient errors**, clear error mapping, correlation ids in both containers' logs.
- Readiness: the main container can start before the model loads; return a temporary unavailable response until a sidecar health request succeeds.
- App Service mounts the same **/home** volume into every container by default (unless **WEBSITES_ENABLE_APP_SERVICE_STORAGE=false**), so containers can share /home/models without volumeMounts.
- Don't add **volumeMounts** when /home is enough: explicit mounts change the file-system view and can stop the app or SCM endpoint from starting.
- Write to a **temporary name, then rename** so readers never see a partial file.
- /home fits temporary files, generated config, recreatable model metadata and short-lived artifacts. Use **Blob Storage or Azure Files** for durable data and a managed data service for shared, consistent access.
- Avoid exposing a **generic proxy** to the sidecar; expose narrow health or inference operations.

| Need | Use |
|---|---|
| Main API calls the model server | http://localhost:11434 |
| Share a manifest between containers | /home/models (default mount, no volumeMounts) |
| Avoid half-written files | Write .tmp, then rename |
| Durable system of record | Azure Blob Storage or Azure Files |

> [!WARNING]
> **Exam traps**
>
> - Use **localhost**, not the container name.
> - Retry only **idempotent** operations with **transient** errors.
> - WEBSITES_ENABLE_APP_SERVICE_STORAGE=false removes the shared /home mount.

## Diagnose sidecar failures

📘 Microsoft Learn: [Diagnose sidecar failures](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/5-diagnose-sidecar-failures)

A sidecar problem usually shows up as an **error from the main app**. Work from the outside in, one boundary at a time: did the definition arrive, did the image pull, did the process start and stay up, is memory squeezed, does localhost connect, is the request right? Change one thing at a time.

**Key facts**

- Symptom-first order: definitions reached App Service → image pulled → process starts and stays up → CPU/memory pressure → localhost connection → request/response at the sidecar.
- Commands: `az webapp sitecontainers list` (missing sidecar, wrong tag, several main roles), `show` (one definition), `status` (is it running), `log --container-name model-server` (that container's output).
- Image pull fails **before** the process starts: wrong image reference, missing authorization, or a registry network restriction. Check identity assignment, pull role, auth type and client ID, ARM audience tokens, firewall or private endpoint/DNS/VNet integration, and **Pull image over VNet** when pulling through VNet integration.
- If you just granted a role, allow for **propagation** before switching to stored registry credentials.
- Startup failures: entry point or startup command, main process not staying in the **foreground**, missing env vars or paths, architecture mismatch, port mismatch, model file permissions. Repeated restarts without an app error can mean **memory pressure** while loading the model.
- Resource pressure: review CPU, memory, response time, HTTP queue and restarts; scaling out adds another model server per instance. Fixes: reduce concurrency, smaller model, scale the plan, or host inference separately. **Don't use scaling to hide** a crash, missing setting or wrong tag.
- Connectivity: **connection refused** = nothing listening on that port; **timeout** = slow startup, pressure or long work; **HTTP error** = connection worked, check request, auth or model behavior.
- File failures: WEBSITES_ENABLE_APP_SERVICE_STORAGE set to false, different paths, explicit volumeMounts, permissions, or assuming files appear on every instance.
- Use container logs plus Azure Monitor and **Diagnose and solve problems**; record app, slot, instance, container, image tag or digest, timestamps, metrics and correlation id.

| Signal | Meaning | Next step |
|---|---|---|
| Connection refused | No process accepted on that port | Compare client port with the target port and listener logs |
| Timeout | Slow start, resource pressure or long work | Check memory/CPU and model load timing |
| HTTP 4xx/5xx from the sidecar | Connection worked | Check request format, authorization, model-server behavior |
| Restarts with no app error | Possible memory pressure during model load | Measure memory; smaller model or bigger plan |

> [!WARNING]
> **Exam traps**
>
> - An HTTP error response means the **network connection succeeded**.
> - Don't scale the plan to cover a crash or a wrong image tag.
> - Image pull problems happen before the process starts, so app logs won't explain them.

## Check yourself

- **Practice questions:** [lp1m3 on GitHub](../../practice/lp1m3.md), or [on the site](https://aryantripathi.dev/ai-200/lp-1/deploy-sidecar-azure-app-service) with hints and saved progress
- **Cheat sheet:** [Learning path 1](../cheatsheets/lp1.md)
- **Microsoft Learn exercise:** [Deploy an AI API with a local model-serving sidecar](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/6-exercise-deploy-ai-api-sidecar)
- **Hands-on lab:** [labs/](../../labs/README.md) has a lab for this learning path

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
