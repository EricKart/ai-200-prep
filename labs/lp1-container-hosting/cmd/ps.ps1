# @@ vars
$RG = "rg-ai200-lp1"
$LOC = "centralindia"
$SUFFIX = Get-Random -Minimum 100000000 -Maximum 999999999
$ACR = "acrai200$SUFFIX"
$PLAN = "plan-ai200-lp1"
$APP = "app-ai200-api-$SUFFIX"
$SIDE = "app-ai200-side-$SUFFIX"
Write-Output "Registry: $ACR   Web apps: $APP and $SIDE"

# @@ group
az group create --name $RG --location $LOC -o table

# @@ acr
# Basic tier: cheapest, includes ACR Tasks. Admin user stays OFF: apps pull with managed identity.
az acr create --resource-group $RG --name $ACR --sku Basic -o table
$ACR_ID = az acr show --name $ACR --query id -o tsv
$LOGIN = az acr show --name $ACR --query loginServer -o tsv
Write-Output "Login server: $LOGIN"

# @@ build
# Quick tasks: ACR builds in the cloud from your local folder. No Docker needed on your machine.
az acr build --registry $ACR --image inference-api:v1 --image inference-api:stable app/inference-api
az acr build --registry $ACR --image model-server:v1 app/model-server

# @@ inspect
az acr repository list --name $ACR -o table
az acr repository show-tags --name $ACR --repository inference-api -o table
# The digest identifies one exact image. Tags can move; digests can't.
$DIGEST = az acr repository show --name $ACR --image inference-api:v1 --query digest -o tsv
Write-Output "inference-api:v1 is $LOGIN/inference-api@$DIGEST"

# @@ retag
# Build v2 and move the "stable" tag to it. The image stable used to point at keeps its v1 tag.
az acr build --registry $ACR --image inference-api:v2 --image inference-api:stable `
  --build-arg APP_VERSION=v2 app/inference-api
# Now push the "nightly" tag twice. The first nightly image loses its only tag and becomes UNTAGGED.
az acr build --registry $ACR --image inference-api:nightly --build-arg APP_VERSION=nightly-1 app/inference-api
az acr build --registry $ACR --image inference-api:nightly --build-arg APP_VERSION=nightly-2 app/inference-api
# One row has no tags: that's the orphan. It still takes storage until something deletes it.
az acr manifest list-metadata --registry $ACR --name inference-api `
  --query "[].{digest:digest, tags:join(',', tags || ``[]``)}" -o table

# @@ lock
# Lock v1: it can't be overwritten or deleted.
az acr repository update --name $ACR --image inference-api:v1 --write-enabled false -o table
# Try to overwrite it. This build FAILS on purpose at the push step.
az acr build --registry $ACR --image inference-api:v1 --build-arg APP_VERSION=v1-overwrite app/inference-api
if ($LASTEXITCODE -ne 0) { Write-Output ">> Push refused: v1 is locked. That's the point." }

# @@ purge-task
# A scheduled ACR task that runs "acr purge" daily. --dry-run only lists what it would delete.
# Careful: the filter is a regex on TAG names, and purge deletes matching tags older than --ago.
# 'inference-api:.*' with --ago 0d would delete v2 and stable too. '^$' matches no tag name,
# so only untagged manifests are removed. (In production you'd use something like --ago 30d.)
az acr task create --registry $ACR --name purge-untagged `
  --cmd "acr purge --filter 'inference-api:^$' --untagged --ago 0d --dry-run" `
  --schedule "0 1 * * *" --context /dev/null -o table
# Don't wait for 01:00 UTC. Run it now and read its log.
az acr task run --registry $ACR --name purge-untagged

# @@ plan
# One Linux B1 plan hosts both web apps in this lab.
az appservice plan create --resource-group $RG --name $PLAN --is-linux --sku B1 -o table

# @@ webapp
# A classic single-container app. The system-assigned identity gets AcrPull and pulls the image.
az webapp create --resource-group $RG --plan $PLAN --name $APP `
  --container-image-name "$LOGIN/inference-api:v1" `
  --assign-identity "[system]" --role AcrPull --scope "$ACR_ID" `
  --acr-use-identity --acr-identity "[system]" -o none
az webapp config appsettings set --resource-group $RG --name $APP `
  --settings MODEL_URL=http://localhost:11434/generate -o none
Write-Output "https://$APP.azurewebsites.net"

# @@ port-bug
# The container listens on 5000, but App Service sends traffic to port 80 by default.
# Give it a minute to start, then call it. Expect a timeout or an error code, not JSON.
Start-Sleep -Seconds 60
try { (Invoke-WebRequest "https://$APP.azurewebsites.net/health" -TimeoutSec 30).StatusCode }
catch { Write-Output "Failed as expected: $($_.Exception.Message)" }

# @@ port-fix
az webapp config appsettings set --resource-group $RG --name $APP --settings WEBSITES_PORT=5000 -o none
# The setting restarts the app. Try again until it answers (up to about 3 minutes).
foreach ($i in 1..18) {
  try { $code = (Invoke-WebRequest "https://$APP.azurewebsites.net/health" -TimeoutSec 20).StatusCode } catch { $code = 0 }
  Write-Output "try ${i}: HTTP $code"; if ($code -eq 200) { break }; Start-Sleep -Seconds 10
}
Invoke-RestMethod "https://$APP.azurewebsites.net/"

# @@ logs
# Container logs. Turn on file-system logging, then download the last lines.
az webapp log config --resource-group $RG --name $APP --docker-container-logging filesystem -o none
Invoke-RestMethod "https://$APP.azurewebsites.net/" | Out-Null
az webapp log download --resource-group $RG --name $APP --log-file lp1-logs.zip
Expand-Archive lp1-logs.zip -DestinationPath lp1-logs -Force
Get-ChildItem lp1-logs -Recurse -File | Select-String "ContainerStream: inference-api" | Select-Object -Last 5 | ForEach-Object Line
# Live stream instead (Ctrl+C to stop): az webapp log tail --resource-group $RG --name $APP

# @@ predict-no-sidecar
# /predict needs the model server. This app has no sidecar, so expect HTTP 503 "model server unreachable".
try { Invoke-RestMethod -Method Post "https://$APP.azurewebsites.net/predict" -ContentType "application/json" -Body '{"text":"hello"}' }
catch { Write-Output $_.ErrorDetails.Message }

# @@ side-app
# A sidecar-enabled app (LinuxFxVersion = sitecontainers). Containers are added one by one.
az webapp create --resource-group $RG --plan $PLAN --name $SIDE --sitecontainers-app `
  --assign-identity "[system]" --role AcrPull --scope "$ACR_ID" -o none
az webapp show --resource-group $RG --name $SIDE --query siteConfig.linuxFxVersion -o tsv

# @@ side-containers
# Main container: the API. Sidecar: the model server. Both pull with the app's system identity.
# Trap on purpose: --target-port 5000 for the main container.
az webapp sitecontainers create --resource-group $RG --name $SIDE --container-name inference-api `
  --image "$LOGIN/inference-api:v1" --target-port 5000 --is-main true --system-assigned-identity true -o none
az webapp sitecontainers create --resource-group $RG --name $SIDE --container-name model-server `
  --image "$LOGIN/model-server:v1" --target-port 11434 --is-main false --system-assigned-identity true -o none
az webapp sitecontainers list --resource-group $RG --name $SIDE `
  --query "[].{name:name, image:image, port:targetPort, main:isMain}" -o table

# @@ side-bug
# Wait for both containers to start, then call the API.
Start-Sleep -Seconds 90
try { (Invoke-WebRequest "https://$SIDE.azurewebsites.net/health" -TimeoutSec 30).StatusCode }
catch { Write-Output "Failed: $($_.Exception.Message)" }
az webapp sitecontainers status --resource-group $RG --name $SIDE --container-name inference-api -o json |
  Select-String '"(state|status|message)"' | Select-Object -First 5 | ForEach-Object Line

# @@ side-fix
# The main container must listen on 80 or 8080. Start the API on 8080 and set the target port to match.
az webapp sitecontainers update --resource-group $RG --name $SIDE --container-name inference-api `
  --image "$LOGIN/inference-api:v1" --target-port 8080 --is-main true --system-assigned-identity true `
  --startup-cmd "python3 app.py --port 8080" -o none
foreach ($i in 1..24) {
  try { $code = (Invoke-WebRequest "https://$SIDE.azurewebsites.net/health" -TimeoutSec 20).StatusCode } catch { $code = 0 }
  Write-Output "try ${i}: HTTP $code"; if ($code -eq 200) { break }; Start-Sleep -Seconds 10
}

# @@ side-predict
# The API reaches the sidecar on localhost:11434. Containers in one app share one network.
Invoke-RestMethod -Method Post "https://$SIDE.azurewebsites.net/predict" -ContentType "application/json" `
  -Body '{"text":"containers share localhost"}'
# The sidecar's own log shows the request arriving. (Live stream instead, Ctrl+C to stop:
#   az webapp sitecontainers log --resource-group $RG --name $SIDE --container-name model-server)
az webapp log download --resource-group $RG --name $SIDE --log-file lp1-side-logs.zip
Expand-Archive lp1-side-logs.zip -DestinationPath lp1-side-logs -Force
Get-ChildItem lp1-side-logs -Recurse -File | Select-String 'model-server (listening|"POST)' | Select-Object -Last 5 | ForEach-Object Line

# @@ reconnect
# New terminal? Run this instead of the vars step. It finds the names you already created.
$RG = "rg-ai200-lp1"
$PLAN = "plan-ai200-lp1"
$ACR = az acr list --resource-group $RG --query "[0].name" -o tsv
$ACR_ID = az acr show --name $ACR --query id -o tsv
$LOGIN = az acr show --name $ACR --query loginServer -o tsv
$APP = az webapp list --resource-group $RG --query "[?starts_with(name,'app-ai200-api-')].name | [0]" -o tsv
$SIDE = az webapp list --resource-group $RG --query "[?starts_with(name,'app-ai200-side-')].name | [0]" -o tsv
Write-Output "Registry: $ACR   Web apps: $APP and $SIDE"

# @@ clean-up
# Deletes the registry, the plan and both apps. Nothing in this lab is soft-deleted.
az group delete --name $RG --yes
Remove-Item -Recurse -Force lp1-logs, lp1-logs.zip, lp1-side-logs, lp1-side-logs.zip -ErrorAction SilentlyContinue
