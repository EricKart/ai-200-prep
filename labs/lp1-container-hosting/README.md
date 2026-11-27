# Lab LP1: Build, store and run containers on Azure

> Covers all of **Learning Path 1**: Container Registry (M1), containers on App Service (M2) and sidecars (M3). About 1.5 hours.
> You hit the three traps the exam asks about, see them fail, and fix them.
> Part of [AI-200 Prep](../../README.md) · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200)

## What you'll do

- Build two images **in the cloud** with ACR quick tasks (no Docker on your machine), then read tags and digests.
- Move a tag, create an **untagged** image on purpose, **lock** an image, and schedule an `acr purge` task safely.
- Run the API on App Service, pulling with a **managed identity** and **AcrPull**, not the admin user.
- Break it with the wrong port, then fix it with **WEBSITES_PORT**.
- Build a **sidecar-enabled** app: the main API container calls a model-server sidecar on **localhost**.
- Hit the main-container port trap (`--target-port 5000` never gets traffic), then fix it with **8080**.

## Before you start

- An Azure subscription where you can create resource groups and role assignments.
- A recent Azure CLI, signed in (`az login`). Tested with 2.90; older versions may not have `az webapp sitecontainers`. Cloud Shell works and stays up to date.
- A terminal: bash, zsh, Git Bash, Cloud Shell or PowerShell. Run the commands **from this folder** (`labs/lp1-container-hosting`), because the builds upload `app/`.
- No Docker, no Python: everything runs in Azure.

## Cost

Official pricing for Central India, November 2026 ([ACR](https://azure.microsoft.com/pricing/details/container-registry/), [App Service](https://azure.microsoft.com/pricing/details/app-service/linux/)).

| Resource | Price | This lab |
|---|---|---|
| Container Registry **Basic** | $0.1666 per day, 10 GB storage included | one day |
| ACR Tasks (builds, purge) | $0.0001 per vCPU-second after a free monthly allowance | 8 short builds, under a minute each |
| App Service plan **B1 Linux** | $0.018 per hour (both apps share one plan) | about 1.5 hours |

Expect **about ₹20 in total** if you clean up the same day. The plan bills by the hour even when the apps are idle, so don't leave it running.

## The app

Two tiny containers using only the Python standard library, so builds take seconds:

| Container | Port | What it does |
|---|---|---|
| [`app/inference-api`](app/inference-api/app.py) | 5000 (change with `--port` or `PORT`) | `GET /`, `GET /health`, `POST /predict` → calls the model server |
| [`app/model-server`](app/model-server/server.py) | 11434 (where a local model runtime would listen) | `POST /generate` → a fake "model" answer |

## Steps

Commands for each step are below: bash first, PowerShell in the fold. They're the same as [cmd/bash.sh](cmd/bash.sh) and [cmd/ps.ps1](cmd/ps.ps1).

### 1. Names and resource group

Every name gets a random suffix, because registry and web app names must be unique across Azure. Run this **once**. In a new terminal later, run [Reconnect](#reconnect) instead.

<!-- step:vars -->
```bash
# Git Bash on Windows rewrites anything that starts with "/" (like /subscriptions/...).
# This line turns that off. On Mac, Linux and Cloud Shell it does nothing, so keep it.
export MSYS_NO_PATHCONV=1
RG=rg-ai200-lp1
LOC=centralindia
SUFFIX=$RANDOM$RANDOM
ACR=acrai200$SUFFIX
PLAN=plan-ai200-lp1
APP=app-ai200-api-$SUFFIX
SIDE=app-ai200-side-$SUFFIX
echo "Registry: $ACR   Web apps: $APP and $SIDE"
```

<details><summary>PowerShell</summary>

```powershell
$RG = "rg-ai200-lp1"
$LOC = "centralindia"
$SUFFIX = Get-Random -Minimum 100000000 -Maximum 999999999
$ACR = "acrai200$SUFFIX"
$PLAN = "plan-ai200-lp1"
$APP = "app-ai200-api-$SUFFIX"
$SIDE = "app-ai200-side-$SUFFIX"
Write-Output "Registry: $ACR   Web apps: $APP and $SIDE"
```

</details>
<!-- /step -->

<!-- step:group -->
```bash
az group create --name $RG --location $LOC -o table
```

<details><summary>PowerShell</summary>

```powershell
az group create --name $RG --location $LOC -o table
```

</details>
<!-- /step -->

### 2. Create the registry ([M1](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/))

<!-- step:acr -->
```bash
# Basic tier: cheapest, includes ACR Tasks. Admin user stays OFF: apps pull with managed identity.
az acr create --resource-group $RG --name $ACR --sku Basic -o table
ACR_ID=$(az acr show --name $ACR --query id -o tsv)
LOGIN=$(az acr show --name $ACR --query loginServer -o tsv)
echo "Login server: $LOGIN"
```

<details><summary>PowerShell</summary>

```powershell
# Basic tier: cheapest, includes ACR Tasks. Admin user stays OFF: apps pull with managed identity.
az acr create --resource-group $RG --name $ACR --sku Basic -o table
$ACR_ID = az acr show --name $ACR --query id -o tsv
$LOGIN = az acr show --name $ACR --query loginServer -o tsv
Write-Output "Login server: $LOGIN"
```

</details>
<!-- /step -->

### 3. Build in the cloud

`az acr build` uploads the folder, builds it on an ACR agent and pushes the image. One build can apply several tags (`v1` and `stable`).

<!-- step:build -->
```bash
# Quick tasks: ACR builds in the cloud from your local folder. No Docker needed on your machine.
az acr build --registry $ACR --image inference-api:v1 --image inference-api:stable app/inference-api
az acr build --registry $ACR --image model-server:v1 app/model-server
```

<details><summary>PowerShell</summary>

```powershell
# Quick tasks: ACR builds in the cloud from your local folder. No Docker needed on your machine.
az acr build --registry $ACR --image inference-api:v1 --image inference-api:stable app/inference-api
az acr build --registry $ACR --image model-server:v1 app/model-server
```

</details>
<!-- /step -->

<!-- step:inspect -->
```bash
az acr repository list --name $ACR -o table
az acr repository show-tags --name $ACR --repository inference-api -o table
# The digest identifies one exact image. Tags can move; digests can't.
DIGEST=$(az acr repository show --name $ACR --image inference-api:v1 --query digest -o tsv)
echo "inference-api:v1 is $LOGIN/inference-api@$DIGEST"
```

<details><summary>PowerShell</summary>

```powershell
az acr repository list --name $ACR -o table
az acr repository show-tags --name $ACR --repository inference-api -o table
# The digest identifies one exact image. Tags can move; digests can't.
$DIGEST = az acr repository show --name $ACR --image inference-api:v1 --query digest -o tsv
Write-Output "inference-api:v1 is $LOGIN/inference-api@$DIGEST"
```

</details>
<!-- /step -->

**You should see** two repositories, the tags `stable` and `v1`, and a digest like `sha256:0721f9…`. In production, deploy by digest: a tag can be moved to another image, a digest can't.

### 4. Move a tag, make an orphan

<!-- step:retag -->
```bash
# Build v2 and move the "stable" tag to it. The image stable used to point at keeps its v1 tag.
az acr build --registry $ACR --image inference-api:v2 --image inference-api:stable \
  --build-arg APP_VERSION=v2 app/inference-api
# Now push the "nightly" tag twice. The first nightly image loses its only tag and becomes UNTAGGED.
az acr build --registry $ACR --image inference-api:nightly --build-arg APP_VERSION=nightly-1 app/inference-api
az acr build --registry $ACR --image inference-api:nightly --build-arg APP_VERSION=nightly-2 app/inference-api
# One row has no tags: that's the orphan. It still takes storage until something deletes it.
az acr manifest list-metadata --registry $ACR --name inference-api \
  --query "[].{digest:digest, tags:join(',', tags || \`[]\`)}" -o table
```

<details><summary>PowerShell</summary>

```powershell
# Build v2 and move the "stable" tag to it. The image stable used to point at keeps its v1 tag.
az acr build --registry $ACR --image inference-api:v2 --image inference-api:stable `
  --build-arg APP_VERSION=v2 app/inference-api
# Now push the "nightly" tag twice. The first nightly image loses its only tag and becomes UNTAGGED.
az acr build --registry $ACR --image inference-api:nightly --build-arg APP_VERSION=nightly-1 app/inference-api
az acr build --registry $ACR --image inference-api:nightly --build-arg APP_VERSION=nightly-2 app/inference-api
# One row has no tags: that's the orphan. It still takes storage until something deletes it.
az acr manifest list-metadata --registry $ACR --name inference-api `
  --query "[].{digest:digest, tags:join(',', tags || ``[]``)}" -o table
```

</details>
<!-- /step -->

**You should see** `stable,v2` on one row, `nightly` on another, `v1` on a third, and **one row with no tags**. That's the first nightly image. Pushing a tag again doesn't delete the old image; it just leaves it untagged, still using storage.

### 5. Lock an image

<!-- step:lock -->
```bash
# Lock v1: it can't be overwritten or deleted.
az acr repository update --name $ACR --image inference-api:v1 --write-enabled false -o table
# Try to overwrite it. This build FAILS on purpose at the push step.
az acr build --registry $ACR --image inference-api:v1 --build-arg APP_VERSION=v1-overwrite app/inference-api \
  || echo ">> Push refused: v1 is locked. That's the point."
```

<details><summary>PowerShell</summary>

```powershell
# Lock v1: it can't be overwritten or deleted.
az acr repository update --name $ACR --image inference-api:v1 --write-enabled false -o table
# Try to overwrite it. This build FAILS on purpose at the push step.
az acr build --registry $ACR --image inference-api:v1 --build-arg APP_VERSION=v1-overwrite app/inference-api
if ($LASTEXITCODE -ne 0) { Write-Output ">> Push refused: v1 is locked. That's the point." }
```

</details>
<!-- /step -->

**You should see** the build succeed and then the push fail with `The operation is disallowed`. A locked image can't be overwritten or deleted, and retention policies skip it.

### 6. Schedule a safe purge

<!-- step:purge-task -->
```bash
# A scheduled ACR task that runs "acr purge" daily. --dry-run only lists what it would delete.
# Careful: the filter is a regex on TAG names, and purge deletes matching tags older than --ago.
# 'inference-api:.*' with --ago 0d would delete v2 and stable too. '^$' matches no tag name,
# so only untagged manifests are removed. (In production you'd use something like --ago 30d.)
az acr task create --registry $ACR --name purge-untagged \
  --cmd "acr purge --filter 'inference-api:^$' --untagged --ago 0d --dry-run" \
  --schedule "0 1 * * *" --context /dev/null -o table
# Don't wait for 01:00 UTC. Run it now and read its log.
az acr task run --registry $ACR --name purge-untagged
```

<details><summary>PowerShell</summary>

```powershell
# A scheduled ACR task that runs "acr purge" daily. --dry-run only lists what it would delete.
# Careful: the filter is a regex on TAG names, and purge deletes matching tags older than --ago.
# 'inference-api:.*' with --ago 0d would delete v2 and stable too. '^$' matches no tag name,
# so only untagged manifests are removed. (In production you'd use something like --ago 30d.)
az acr task create --registry $ACR --name purge-untagged `
  --cmd "acr purge --filter 'inference-api:^$' --untagged --ago 0d --dry-run" `
  --schedule "0 1 * * *" --context /dev/null -o table
# Don't wait for 01:00 UTC. Run it now and read its log.
az acr task run --registry $ACR --name purge-untagged
```

</details>
<!-- /step -->

**You should see** `Number of tags to be deleted: 0` and one manifest: the orphan from step 4.

> [!WARNING]
> `acr purge` deletes **tags** that match `--filter` and are older than `--ago`, then (with `--untagged`) manifests with no tags. A filter like `inference-api:.*` with `--ago 0d` would delete `v2` and `stable` too. We tested this: the dry run listed both. Always run with `--dry-run` first. Retention policies, which remove untagged manifests automatically, need the **Premium** tier.

### 7. Run the API on App Service ([M2](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/))

The app gets a **system-assigned managed identity** with the **AcrPull** role on the registry, and pulls with it (`--acr-use-identity`). No passwords anywhere.

<!-- step:plan -->
```bash
# One Linux B1 plan hosts both web apps in this lab.
az appservice plan create --resource-group $RG --name $PLAN --is-linux --sku B1 -o table
```

<details><summary>PowerShell</summary>

```powershell
# One Linux B1 plan hosts both web apps in this lab.
az appservice plan create --resource-group $RG --name $PLAN --is-linux --sku B1 -o table
```

</details>
<!-- /step -->

<!-- step:webapp -->
```bash
# A classic single-container app. The system-assigned identity gets AcrPull and pulls the image.
az webapp create --resource-group $RG --plan $PLAN --name $APP \
  --container-image-name "$LOGIN/inference-api:v1" \
  --assign-identity "[system]" --role AcrPull --scope "$ACR_ID" \
  --acr-use-identity --acr-identity "[system]" -o none
az webapp config appsettings set --resource-group $RG --name $APP \
  --settings MODEL_URL=http://localhost:11434/generate -o none
echo "https://$APP.azurewebsites.net"
```

<details><summary>PowerShell</summary>

```powershell
# A classic single-container app. The system-assigned identity gets AcrPull and pulls the image.
az webapp create --resource-group $RG --plan $PLAN --name $APP `
  --container-image-name "$LOGIN/inference-api:v1" `
  --assign-identity "[system]" --role AcrPull --scope "$ACR_ID" `
  --acr-use-identity --acr-identity "[system]" -o none
az webapp config appsettings set --resource-group $RG --name $APP `
  --settings MODEL_URL=http://localhost:11434/generate -o none
Write-Output "https://$APP.azurewebsites.net"
```

</details>
<!-- /step -->

### 8. The port trap

The API listens on **5000**. App Service only routes to **80** or **8080** unless you tell it otherwise.

<!-- step:port-bug -->
```bash
# The container listens on 5000, but App Service sends traffic to port 80 by default.
# Give it a minute to start, then call it. Expect an error page or a timeout, not JSON.
sleep 60
curl -s -m 30 -o /dev/null -w "HTTP %{http_code}\n" "https://$APP.azurewebsites.net/health"
```

<details><summary>PowerShell</summary>

```powershell
# The container listens on 5000, but App Service sends traffic to port 80 by default.
# Give it a minute to start, then call it. Expect a timeout or an error code, not JSON.
Start-Sleep -Seconds 60
try { (Invoke-WebRequest "https://$APP.azurewebsites.net/health" -TimeoutSec 30).StatusCode }
catch { Write-Output "Failed as expected: $($_.Exception.Message)" }
```

</details>
<!-- /step -->

**You should see** `HTTP 000` (a timeout). The container started fine, but nothing reaches it.

<!-- step:port-fix -->
```bash
az webapp config appsettings set --resource-group $RG --name $APP --settings WEBSITES_PORT=5000 -o none
# The setting restarts the app. Try again until it answers (up to about 3 minutes).
for i in $(seq 1 18); do
  code=$(curl -s -m 20 -o /dev/null -w "%{http_code}" "https://$APP.azurewebsites.net/health")
  echo "try $i: HTTP $code"; [ "$code" = "200" ] && break; sleep 10
done
curl -s "https://$APP.azurewebsites.net/"; echo
```

<details><summary>PowerShell</summary>

```powershell
az webapp config appsettings set --resource-group $RG --name $APP --settings WEBSITES_PORT=5000 -o none
# The setting restarts the app. Try again until it answers (up to about 3 minutes).
foreach ($i in 1..18) {
  try { $code = (Invoke-WebRequest "https://$APP.azurewebsites.net/health" -TimeoutSec 20).StatusCode } catch { $code = 0 }
  Write-Output "try ${i}: HTTP $code"; if ($code -eq 200) { break }; Start-Sleep -Seconds 10
}
Invoke-RestMethod "https://$APP.azurewebsites.net/"
```

</details>
<!-- /step -->

**You should see** `HTTP 200` after a few tries, then the app's JSON with a container host name.

### 9. Read the container logs

<!-- step:logs -->
```bash
# Container logs. Turn on file-system logging, then download the last lines.
az webapp log config --resource-group $RG --name $APP --docker-container-logging filesystem -o none
curl -s -o /dev/null "https://$APP.azurewebsites.net/"
az webapp log download --resource-group $RG --name $APP --log-file lp1-logs.zip
unzip -o -q lp1-logs.zip -d lp1-logs && grep -rhE 'ContainerStream: inference-api' lp1-logs | tail -5
# Live stream instead (Ctrl+C to stop): az webapp log tail --resource-group $RG --name $APP
```

<details><summary>PowerShell</summary>

```powershell
# Container logs. Turn on file-system logging, then download the last lines.
az webapp log config --resource-group $RG --name $APP --docker-container-logging filesystem -o none
Invoke-RestMethod "https://$APP.azurewebsites.net/" | Out-Null
az webapp log download --resource-group $RG --name $APP --log-file lp1-logs.zip
Expand-Archive lp1-logs.zip -DestinationPath lp1-logs -Force
Get-ChildItem lp1-logs -Recurse -File | Select-String "ContainerStream: inference-api" | Select-Object -Last 5 | ForEach-Object Line
# Live stream instead (Ctrl+C to stop): az webapp log tail --resource-group $RG --name $APP
```

</details>
<!-- /step -->

**You should see** `inference-api v1 listening on 0.0.0.0:5000`. If you see `GET /robots933456.txt` with a 404, that's App Service's own warm-up check and it's harmless.

<!-- step:predict-no-sidecar -->
```bash
# /predict needs the model server. This app has no sidecar, so expect HTTP 503 "model server unreachable".
curl -s -X POST "https://$APP.azurewebsites.net/predict" -H "Content-Type: application/json" -d '{"text":"hello"}'; echo
```

<details><summary>PowerShell</summary>

```powershell
# /predict needs the model server. This app has no sidecar, so expect HTTP 503 "model server unreachable".
try { Invoke-RestMethod -Method Post "https://$APP.azurewebsites.net/predict" -ContentType "application/json" -Body '{"text":"hello"}' }
catch { Write-Output $_.ErrorDetails.Message }
```

</details>
<!-- /step -->

**You should see** `model server unreachable`. This app has only one container, so nothing listens on localhost:11434. That's what the sidecar is for.

### 10. A sidecar-enabled app ([M3](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/))

A sidecar-enabled app has `LinuxFxVersion = SITECONTAINERS`. Each container is a separate resource, and exactly one is the **main** container (`--is-main true`), which gets the external traffic. In this mode, `WEBSITES_PORT` and the `DOCKER_REGISTRY_SERVER_*` settings no longer configure anything.

<!-- step:side-app -->
```bash
# A sidecar-enabled app (LinuxFxVersion = sitecontainers). Containers are added one by one.
az webapp create --resource-group $RG --plan $PLAN --name $SIDE --sitecontainers-app \
  --assign-identity "[system]" --role AcrPull --scope "$ACR_ID" -o none
az webapp show --resource-group $RG --name $SIDE --query siteConfig.linuxFxVersion -o tsv
```

<details><summary>PowerShell</summary>

```powershell
# A sidecar-enabled app (LinuxFxVersion = sitecontainers). Containers are added one by one.
az webapp create --resource-group $RG --plan $PLAN --name $SIDE --sitecontainers-app `
  --assign-identity "[system]" --role AcrPull --scope "$ACR_ID" -o none
az webapp show --resource-group $RG --name $SIDE --query siteConfig.linuxFxVersion -o tsv
```

</details>
<!-- /step -->

<!-- step:side-containers -->
```bash
# Main container: the API. Sidecar: the model server. Both pull with the app's system identity.
# Trap on purpose: --target-port 5000 for the main container.
az webapp sitecontainers create --resource-group $RG --name $SIDE --container-name inference-api \
  --image "$LOGIN/inference-api:v1" --target-port 5000 --is-main true --system-assigned-identity true -o none
az webapp sitecontainers create --resource-group $RG --name $SIDE --container-name model-server \
  --image "$LOGIN/model-server:v1" --target-port 11434 --is-main false --system-assigned-identity true -o none
az webapp sitecontainers list --resource-group $RG --name $SIDE \
  --query "[].{name:name, image:image, port:targetPort, main:isMain}" -o table
```

<details><summary>PowerShell</summary>

```powershell
# Main container: the API. Sidecar: the model server. Both pull with the app's system identity.
# Trap on purpose: --target-port 5000 for the main container.
az webapp sitecontainers create --resource-group $RG --name $SIDE --container-name inference-api `
  --image "$LOGIN/inference-api:v1" --target-port 5000 --is-main true --system-assigned-identity true -o none
az webapp sitecontainers create --resource-group $RG --name $SIDE --container-name model-server `
  --image "$LOGIN/model-server:v1" --target-port 11434 --is-main false --system-assigned-identity true -o none
az webapp sitecontainers list --resource-group $RG --name $SIDE `
  --query "[].{name:name, image:image, port:targetPort, main:isMain}" -o table
```

</details>
<!-- /step -->

### 11. The main-container port trap

<!-- step:side-bug -->
```bash
# Wait for both containers to start, then call the API.
sleep 90
curl -s -m 30 -o /dev/null -w "HTTP %{http_code}\n" "https://$SIDE.azurewebsites.net/health"
az webapp sitecontainers status --resource-group $RG --name $SIDE --container-name inference-api -o json \
  | grep -iE '"(state|status|message)"' | head -5
```

<details><summary>PowerShell</summary>

```powershell
# Wait for both containers to start, then call the API.
Start-Sleep -Seconds 90
try { (Invoke-WebRequest "https://$SIDE.azurewebsites.net/health" -TimeoutSec 30).StatusCode }
catch { Write-Output "Failed: $($_.Exception.Message)" }
az webapp sitecontainers status --resource-group $RG --name $SIDE --container-name inference-api -o json |
  Select-String '"(state|status|message)"' | Select-Object -First 5 | ForEach-Object Line
```

</details>
<!-- /step -->

**You should see** `HTTP 000` while the container status says `Running`. "Running" only means the process started; the main container must listen on **80 or 8080** to get traffic.

<!-- step:side-fix -->
```bash
# The main container must listen on 80 or 8080. Start the API on 8080 and set the target port to match.
az webapp sitecontainers update --resource-group $RG --name $SIDE --container-name inference-api \
  --image "$LOGIN/inference-api:v1" --target-port 8080 --is-main true --system-assigned-identity true \
  --startup-cmd "python3 app.py --port 8080" -o none
for i in $(seq 1 24); do
  code=$(curl -s -m 20 -o /dev/null -w "%{http_code}" "https://$SIDE.azurewebsites.net/health")
  echo "try $i: HTTP $code"; [ "$code" = "200" ] && break; sleep 10
done
```

<details><summary>PowerShell</summary>

```powershell
# The main container must listen on 80 or 8080. Start the API on 8080 and set the target port to match.
az webapp sitecontainers update --resource-group $RG --name $SIDE --container-name inference-api `
  --image "$LOGIN/inference-api:v1" --target-port 8080 --is-main true --system-assigned-identity true `
  --startup-cmd "python3 app.py --port 8080" -o none
foreach ($i in 1..24) {
  try { $code = (Invoke-WebRequest "https://$SIDE.azurewebsites.net/health" -TimeoutSec 20).StatusCode } catch { $code = 0 }
  Write-Output "try ${i}: HTTP $code"; if ($code -eq 200) { break }; Start-Sleep -Seconds 10
}
```

</details>
<!-- /step -->

### 12. Call the sidecar over localhost

<!-- step:side-predict -->
```bash
# The API reaches the sidecar on localhost:11434. Containers in one app share one network.
curl -s -X POST "https://$SIDE.azurewebsites.net/predict" -H "Content-Type: application/json" \
  -d '{"text":"containers share localhost"}'; echo
# The sidecar's own log shows the request arriving. (Live stream instead, Ctrl+C to stop:
#   az webapp sitecontainers log --resource-group $RG --name $SIDE --container-name model-server)
az webapp log download --resource-group $RG --name $SIDE --log-file lp1-side-logs.zip
unzip -o -q lp1-side-logs.zip -d lp1-side-logs && grep -rhE 'model-server (listening|"POST)' lp1-side-logs | tail -5
```

<details><summary>PowerShell</summary>

```powershell
# The API reaches the sidecar on localhost:11434. Containers in one app share one network.
Invoke-RestMethod -Method Post "https://$SIDE.azurewebsites.net/predict" -ContentType "application/json" `
  -Body '{"text":"containers share localhost"}'
# The sidecar's own log shows the request arriving. (Live stream instead, Ctrl+C to stop:
#   az webapp sitecontainers log --resource-group $RG --name $SIDE --container-name model-server)
az webapp log download --resource-group $RG --name $SIDE --log-file lp1-side-logs.zip
Expand-Archive lp1-side-logs.zip -DestinationPath lp1-side-logs -Force
Get-ChildItem lp1-side-logs -Recurse -File | Select-String 'model-server (listening|"POST)' | Select-Object -Last 5 | ForEach-Object Line
```

</details>
<!-- /step -->

**You should see** `"model": "tiny-echo"` in the answer, and `model-server "POST /generate" 200` in the sidecar's log. Containers in one app share one network namespace: the API calls `http://localhost:11434`, never `http://model-server:11434`.

### Reconnect

Opened a new terminal? This finds the names you created, without creating anything.

<!-- step:reconnect -->
```bash
# New terminal? Run this instead of the vars step. It finds the names you already created.
export MSYS_NO_PATHCONV=1
RG=rg-ai200-lp1
PLAN=plan-ai200-lp1
ACR=$(az acr list --resource-group $RG --query "[0].name" -o tsv)
ACR_ID=$(az acr show --name "$ACR" --query id -o tsv)
LOGIN=$(az acr show --name "$ACR" --query loginServer -o tsv)
APP=$(az webapp list --resource-group $RG --query "[?starts_with(name,'app-ai200-api-')].name | [0]" -o tsv)
SIDE=$(az webapp list --resource-group $RG --query "[?starts_with(name,'app-ai200-side-')].name | [0]" -o tsv)
echo "Registry: $ACR   Web apps: $APP and $SIDE"
```

<details><summary>PowerShell</summary>

```powershell
# New terminal? Run this instead of the vars step. It finds the names you already created.
$RG = "rg-ai200-lp1"
$PLAN = "plan-ai200-lp1"
$ACR = az acr list --resource-group $RG --query "[0].name" -o tsv
$ACR_ID = az acr show --name $ACR --query id -o tsv
$LOGIN = az acr show --name $ACR --query loginServer -o tsv
$APP = az webapp list --resource-group $RG --query "[?starts_with(name,'app-ai200-api-')].name | [0]" -o tsv
$SIDE = az webapp list --resource-group $RG --query "[?starts_with(name,'app-ai200-side-')].name | [0]" -o tsv
Write-Output "Registry: $ACR   Web apps: $APP and $SIDE"
```

</details>
<!-- /step -->

## Clean up

Delete everything as soon as you finish. Nothing in this lab is soft-deleted, so this removes it all.

<!-- step:clean-up -->
```bash
# Deletes the registry, the plan and both apps. Nothing in this lab is soft-deleted.
az group delete --name $RG --yes
rm -rf lp1-logs lp1-logs.zip lp1-side-logs lp1-side-logs.zip
```

<details><summary>PowerShell</summary>

```powershell
# Deletes the registry, the plan and both apps. Nothing in this lab is soft-deleted.
az group delete --name $RG --yes
Remove-Item -Recurse -Force lp1-logs, lp1-logs.zip, lp1-side-logs, lp1-side-logs.zip -ErrorAction SilentlyContinue
```

</details>
<!-- /step -->

Check with `az group exists --name rg-ai200-lp1`. It should print `false`.

## What the exam asks about this

| Trap | What you saw |
|---|---|
| The container listens on a port other than 80/8080 | Timeout until `WEBSITES_PORT=5000` (classic app) |
| The main container in a sidecar app uses another port | `Running`, but no traffic until 8080 |
| Call a sidecar by container name | Use `localhost:<port>` |
| Pull from ACR without passwords | Managed identity + **AcrPull** |
| Pushing a tag again | The old image stays, untagged, until purged |
| A locked image | Push refused; retention skips it |

## Tested

The bash steps were tested live in Central India on 27 Nov 2026, from a new resource group through clean-up, including the Reconnect step from a new terminal. Two findings from testing are now in the steps: `az webapp sitecontainers log` streams until you press Ctrl+C, so step 12 downloads the log instead, and a broad purge filter deletes tags (see the warning in step 6).
The PowerShell blocks are a line-by-line translation and **haven't been run live yet**. Please [report](../../CONTRIBUTING.md) anything that fails.

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200)
