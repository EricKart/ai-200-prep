# LP1 · M2: Deploy containers to Azure App Service

> **Learning path 1:** Implement container application hosting on Azure · **Skill area 1:** Develop and deploy containerized solutions · about 74 min on Microsoft Learn  
> Study it interactively at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-1/deploy-containers-azure-app-service)

App Service can run your container as a managed web app without you looking after servers. You'll learn how it pulls images, which settings control ports, storage and startup, and how to troubleshoot a container that won't respond.

**In this lesson**

1. [Deploy containers to Azure App Service](#deploy-containers-to-azure-app-service)
2. [Configure container runtime behavior](#configure-container-runtime-behavior)
3. [Configure application settings](#configure-application-settings)
4. [Observe and troubleshoot containerized apps](#observe-and-troubleshoot-containerized-apps)

## Deploy containers to Azure App Service

📘 Microsoft Learn: [Deploy containers to Azure App Service](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/2-deploy-containers)

App Service is a **managed host for your container**: you tell it which image to pull and how to log in to the registry, and it handles servers, load balancing and scaling. Managed identity is like a **staff badge** the app shows to ACR, so no password is stored anywhere.

**Key facts**

- App Service runs **custom Linux containers** as web apps (Web App for Containers). It handles provisioning, load balancing and scaling.
- Image sources: **Azure Container Registry** (recommended for production; Entra ID auth, managed identity, geo-replication, image scanning, private network access) or **Other container registries** (any HTTPS registry supporting the Docker Registry HTTP API V2: Docker Hub, GitHub Container Registry, self-hosted). Private images need server URL, username and password; public images need only the image name.
- Portal: Create a resource → Web App → Publish: **Container**, OS: **Linux** → plan → **Container** tab for the image source.
- ACR authentication: **managed identity** (recommended for production; the identity needs the **AcrPull** role) or **admin credentials** (simpler for development; enable with `az acr update --admin-enabled true`; stored in config, manual rotation).
- **System-assigned** identity is tied to the web app's lifecycle. **User-assigned** identity is a separate resource you can assign to several apps and grant permissions before the app exists.
- CLI: `az webapp create --plan … --container-image-name myregistry.azurecr.io/docprocessor:v1`. Other registries add `--docker-registry-server-url` (Docker Hub `https://index.docker.io/v1/`, GHCR `https://ghcr.io`) plus user and password for private images.
- VS Code: Docker extension → REGISTRIES view → right-click the tag → **Deploy Image to Azure App Service**.
- New tag: `az webapp config container set --container-image-name …:v2`; App Service restarts and pulls on each instance.
- Pushing to the **same tag** isn't detected automatically: restart manually or enable **continuous deployment** (`az webapp deployment container config --enable-cd true` returns a **webhook URL** to add to the registry for push events).
- Pull behavior: full pull on first deploy or image change; on restart only **changed layers**; each new instance pulls on **scale out**; a **pricing tier change** can pull fresh.
- Verify with `az webapp show --query defaultHostName` and open the URL.

| Auth method | Best for | Notes |
|---|---|---|
| System-assigned managed identity | Production, one app | Created and deleted with the app; needs AcrPull |
| User-assigned managed identity | Production, several apps | Separate resource; grant AcrPull before creating the app |
| Admin credentials | Development | Enable the admin user; stored in config; rotate manually |

> [!WARNING]
> **Exam traps**
>
> - Same tag, new image: App Service **doesn't notice**. Restart, or enable continuous deployment with a registry webhook.
> - Managed identity must have **AcrPull** on the registry.
> - Docker Hub server URL: `https://index.docker.io/v1/`; GitHub Container Registry: `https://ghcr.io`.

## Configure container runtime behavior

📘 Microsoft Learn: [Configure container runtime behavior](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/3-configure-runtime)

Runtime settings are the **house rules** App Service applies to your container: which command starts it, which door (port) traffic comes through, which folder (`/home`) survives a restart, whether it may fall asleep, and which URL tells App Service it's still alive.

**Key facts**

- A **startup command** (`az webapp config set --startup-file "…"`) replaces the Dockerfile **CMD**; the **ENTRYPOINT** stays. For shell processing, prefix with `/bin/bash -c '…'`.
- Ports: App Service routes automatically when the container listens on **80 or 8080**. Otherwise set the **WEBSITES_PORT** app setting. Only **one port** is exposed for HTTP. TLS is terminated before traffic reaches the container.
- Defaults from the Learn table: Node.js Express 3000, Python Gunicorn 8000, Spring Boot 8080, ASP.NET Core 80 (no change needed).
- The container file system is **ephemeral**. Set **WEBSITES_ENABLE_APP_SERVICE_STORAGE=true** to persist **/home** (disabled by default for Linux custom containers); /home is **shared across all instances** and holds /home/LogFiles.
- Storage quota is shared by all apps in the plan. For large volumes or high I/O, mount **Azure Storage** as an extra volume.
- Apps can idle after about **20 minutes**; the next request is a cold start. **Always-on** (`--always-on true`) keeps the app warm and needs the **Basic tier or higher**.
- **Health checks** (`healthCheckPath`) ping the path **every minute**; after repeated failures (by default **10**) the instance leaves the load balancer rotation and can be replaced. Changing health check config **restarts the app**.
- A health endpoint returns **200** when healthy and can return **503** when a dependency check fails.

| Setting | Fixes | Value |
|---|---|---|
| WEBSITES_PORT | Container listens on a port other than 80/8080 | e.g. 8000 for Gunicorn |
| WEBSITES_ENABLE_APP_SERVICE_STORAGE | Files lost on restart | true → /home persists and is shared |
| --always-on true | Cold starts after idle | Basic tier or higher |
| healthCheckPath | Unhealthy instances keep getting traffic | e.g. /health returning 200 |
| --startup-file | Need different runtime arguments | Replaces CMD, keeps ENTRYPOINT |

> [!WARNING]
> **Exam traps**
>
> - The startup command replaces **CMD**, not ENTRYPOINT.
> - Always-on isn't available on the Free tier; Learn says **Basic or higher**.
> - /home is shared by all instances when persistent storage is on.

## Configure application settings

📘 Microsoft Learn: [Configure application settings](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/4-configure-settings)

App settings are **notes App Service slips into the container's pocket** as environment variables when it starts. The same image can run in test and production with different notes. Slot settings are notes that **stay with the room** (slot) when you swap, and Key Vault references are notes that say "fetch the real secret from the vault".

**Key facts**

- **App settings** are name-value pairs injected as **environment variables**; set with `az webapp config appsettings set --settings A=1 B=2`. All settings are **encrypted at rest**.
- Names use only letters, numbers and underscores. On Linux, .NET nested keys use **double underscores**: `ConnectionStrings__DefaultConnection`.
- **Connection strings** get a type prefix: SQLCONNSTR_, **SQLAZURECONNSTR_**, MYSQLCONNSTR_, POSTGRESQLCONNSTR_, CUSTOMCONNSTR_. For Python, Node.js and similar runtimes, use plain **app settings** for database connections.
- **Bulk editing**: `az webapp config appsettings list --output json > settings.json`, edit, then `--settings @settings.json`. The portal has **Advanced edit** under Environment variables.
- **Deployment slots** run versions side by side in the same plan, each with its own hostname and config, sharing compute. Swap to promote staging to production.
- **Slot settings** (`--slot-settings`) stay with the slot during a swap: environment identifiers, environment-specific endpoints, feature flags, diagnostic settings.
- **Key Vault references**: `@Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/api-key)`. Requires a **managed identity** on the app with permission to read secrets. The app reads a normal environment variable.
- References without a version resolve to the **latest version**; after rotation App Service refreshes within **24 hours**, and any config change that restarts the app forces an immediate refetch.
- Verify on the SCM (Kudu) site: `https://<app-name>.scm.azurewebsites.net/Env`.

| Need | Use |
|---|---|
| Non-secret config such as LOG_LEVEL | App setting |
| Database connection for a .NET app expecting typed strings | Connection string (SQLAZURECONNSTR_…) |
| Database connection for Python or Node.js | App setting |
| ENVIRONMENT=staging must not swap to production | Slot setting |
| Rotated API key with audit trail | Key Vault reference + managed identity |

> [!WARNING]
> **Exam traps**
>
> - A connection string named DefaultConnection of type SQLAzure appears as **SQLAZURECONNSTR_DefaultConnection**.
> - Colons in .NET keys become **__** on Linux.
> - Rotated Key Vault secrets refresh within **24 hours**, or immediately on a restart-causing config change.

## Observe and troubleshoot containerized apps

📘 Microsoft Learn: [Observe and troubleshoot containerized apps](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/5-observe-troubleshoot)

When a container misbehaves, App Service gives you a **live microphone** (log stream), a **back office** (Kudu, the SCM site) to check environment variables and log files, a **long-term archive** (Log Analytics) and, if your image allows it, a **door into the container** (SSH).

**Key facts**

- Enable container logging with `az webapp log config --docker-container-logging filesystem`; logs land in **/home/LogFiles/**. Captured: stdout, stderr, framework logs and platform messages.
- **Log stream** (`az webapp log tail`, or Log stream under Monitoring) shows real-time output from **all instances**, each line with an instance id.
- **Kudu / SCM site** (`https://<app-name>.scm.azurewebsites.net`): Environment page, Debug console for files under /home, diagnostic dump ZIP. It's a **separate site**, so it can't browse the full container file system or running processes.
- **Diagnostic settings** send logs to Log Analytics, Event Hubs or storage. Categories: **AppServiceConsoleLogs** (stdout/stderr), **AppServiceHTTPLogs**, **AppServicePlatformLogs** (container lifecycle), **AppServiceAppLogs**.
- **SSH** needs the image to install openssh-server, listen on **port 2222**, set the root password to **Docker!**, and start sshd with the app. Then use SSH under Development Tools.
- Container fails to start: missing env vars, **WEBSITES_PORT mismatch**, crashes from missing dependencies.
- 404 after deployment: app bound to **localhost** instead of **0.0.0.0**, wrong port, or routes not configured.
- Missing env vars: settings not saved, typos, or the app checking before injection. Check Kudu /Env.
- Slow cold starts: enable always-on, use smaller base images and **multi-stage builds**, defer heavy initialization.

| Symptom | Look here first | Likely cause |
|---|---|---|
| Container won't start | Log stream | Missing env var, port mismatch, missing dependency |
| Starts but every request is 404 | WEBSITES_PORT and the bind address | Bound to localhost, wrong port |
| App says a setting is undefined | Kudu /Env | Not saved, typo, read too early |
| Slow first request after idle | Always-on setting, image size | App idled; large image |

> [!WARNING]
> **Exam traps**
>
> - Kudu can't see the container's full file system or processes; use **SSH** for that.
> - SSH in App Service custom containers uses port **2222** and root password **Docker!**.
> - Bind to **0.0.0.0**, not localhost.

## Check yourself

- **Practice questions:** [lp1m2 on GitHub](../../practice/lp1m2.md), or [on the site](https://aryantripathi.dev/ai-200/lp-1/deploy-containers-azure-app-service) with hints and saved progress
- **Cheat sheet:** [Learning path 1](../cheatsheets/lp1.md)
- **Microsoft Learn exercise:** [Deploy a container to Azure App Service](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/6-exercise)
- **Hands-on lab:** [labs/](../../labs/README.md) has a lab for this learning path

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
