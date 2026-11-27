# LP1 cheat sheet: Implement container application hosting on Azure

> Skill area 1 · one page to review before the exam · full lessons in [content/lessons](../lessons/) · practise at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-1)

## Which one?

| You need… | Answer | Don't confuse with |
|---|---|---|
| Exact same image on every node | Pull by digest (repo@sha256:…) | Tags (even stable ones) can move |
| Geo-replication, private endpoints, content trust | ACR Premium tier | Basic/Standard lack these |
| Build an image without local Docker | az acr build (quick task) | az acr run runs a command in an existing image |
| Rebuild when the base image is patched | ACR base image trigger | Source code trigger = commits |
| Container listens on 8000 in App Service | WEBSITES_PORT=8000 | Not used by sidecar-enabled apps |
| Files must survive restarts and be shared by instances | WEBSITES_ENABLE_APP_SERVICE_STORAGE=true (/home) | Container file system is ephemeral |
| Value must not swap to production | Slot setting | Normal app settings swap |
| One local helper process per instance, same lifecycle | App Service sidecar | Shared/GPU model → separate service |
| Sidecar call from the main container | `http://localhost:<port>` | Not the container name |

## Must remember

### M1: Store and manage containers in Azure Container Registry

- Geo-replication, private endpoints and content trust need the **Premium** tier.
- A tag can move; a digest can't. "Exact same image on every node" means **pull by digest** (or a unique tag).
- Namespaces are part of the **repository** name (`team/image`), not separate registries.
- Private base image triggers work when base and app images are in the **same registry**.
- `{{.Run.ID}}` gives each triggered build a **unique tag**.
- `/dev/null` as the context means "no source files", used with az acr run and cleanup tasks.
- A locked image (`--write-enabled false`) can't be deleted or overwritten, and retention policies skip it.
- Retention policies need **Premium**; in other tiers, schedule an **acr purge** task.
- Learn recommends **stable tags for base images** and **unique tags for production deployments**.

Lesson: [lp1m1](../lessons/lp1m1.md) · Practice: [lp1m1](../../practice/lp1m1.md)

### M2: Deploy containers to Azure App Service

- Same tag, new image: App Service **doesn't notice**. Restart, or enable continuous deployment with a registry webhook.
- Managed identity must have **AcrPull** on the registry.
- Docker Hub server URL: `https://index.docker.io/v1/`; GitHub Container Registry: `https://ghcr.io`.
- The startup command replaces **CMD**, not ENTRYPOINT.
- Always-on isn't available on the Free tier; Learn says **Basic or higher**.
- /home is shared by all instances when persistent storage is on.
- A connection string named DefaultConnection of type SQLAzure appears as **SQLAZURECONNSTR_DefaultConnection**.
- Colons in .NET keys become **__** on Linux.
- Rotated Key Vault secrets refresh within **24 hours**, or immediately on a restart-causing config change.
- Kudu can't see the container's full file system or processes; use **SSH** for that.
- SSH in App Service custom containers uses port **2222** and root password **Docker!**.
- Bind to **0.0.0.0**, not localhost.

Lesson: [lp1m2](../lessons/lp1m2.md) · Practice: [lp1m2](../../practice/lp1m2.md)

### M3: Run sidecar-enabled AI applications on Azure App Service

- Only the **isMain: true** container gets external HTTP traffic.
- Up to **nine** sidecars per app.
- WEBSITES_PORT and DOCKER_REGISTRY_SERVER_* **don't** configure sidecar-enabled containers.
- The main container listens on **80 or 8080** only.
- environmentVariables[].value is the **name of an App Setting**, not the secret itself.
- ABAC repository permissions mode needs **Container Registry Repository Reader**, not AcrPull.
- Use **localhost**, not the container name.
- Retry only **idempotent** operations with **transient** errors.
- WEBSITES_ENABLE_APP_SERVICE_STORAGE=false removes the shared /home mount.
- An HTTP error response means the **network connection succeeded**.
- Don't scale the plan to cover a crash or a wrong image tag.
- Image pull problems happen before the process starts, so app logs won't explain them.

Lesson: [lp1m3](../lessons/lp1m3.md) · Practice: [lp1m3](../../practice/lp1m3.md)

## Commands and syntax you'll see

```text
az acr build --registry myregistry --image inference-api:v1.0.0 .
az acr task create … --git-access-token $PAT
az acr run --cmd '<image> <command>' /dev/null
az acr task logs
az acr repository update --image … --write-enabled false
az acr update --admin-enabled true
az webapp create --plan … --container-image-name myregistry.azurecr.io/docprocessor:v1
az webapp config container set --container-image-name …:v2
az webapp deployment container config --enable-cd true
az webapp show --query defaultHostName
az webapp config set --startup-file "…"
az webapp config appsettings set --settings A=1 B=2
az webapp config appsettings list --output json > settings.json
az webapp log config --docker-container-logging filesystem
az webapp log tail
az webapp create … --sitecontainers-app
az webapp sitecontainers convert --mode sitecontainers
az webapp sitecontainers create --sitecontainers-spec-file ./spec.json
az acr config authentication-as-arm show
az webapp sitecontainers list
```

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
