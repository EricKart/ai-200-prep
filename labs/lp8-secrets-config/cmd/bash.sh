# @@ vars
# Git Bash on Windows rewrites anything that starts with "/" (like /subscriptions/...).
# This line turns that off. On Mac, Linux and Cloud Shell it does nothing, so keep it.
export MSYS_NO_PATHCONV=1

RG="rg-ai200-lp8"
LOCATION="centralindia"
SUFFIX=$RANDOM$RANDOM
KV="kv-ai200-$SUFFIX"
AC="appcs-ai200-$SUFFIX"
SA="stai200lp8$SUFFIX"
ME=$(az ad signed-in-user show --query id -o tsv)

echo "Key Vault: $KV | App Config: $AC | Storage: $SA | Your object id: $ME"

# @@ rg_kv
az group create --name $RG --location $LOCATION -o table

az keyvault create --name $KV --resource-group $RG --location $LOCATION \
  --enable-rbac-authorization true --retention-days 7 -o table

# @@ role_kv
KV_ID=$(az keyvault show --name $KV --query id -o tsv)

az role assignment create --assignee-object-id $ME --assignee-principal-type User \
  --role "Key Vault Secrets Officer" --scope $KV_ID --query "{principalType:principalType, createdOn:createdOn}" -o table

# @@ storage
az storage account create --name $SA --resource-group $RG --location $LOCATION \
  --sku Standard_LRS --kind StorageV2 --min-tls-version TLS1_2 -o table

CONN=$(az storage account show-connection-string --name $SA --resource-group $RG \
  --key key1 --query connectionString -o tsv)

az storage queue create --name kv-events --connection-string "$CONN" -o table

# @@ secrets
# Wait until your new role works (usually under a minute; prints a dot every 15 s).
until az keyvault secret list --vault-name $KV -o none 2>/dev/null; do printf "."; sleep 15; done; echo " role is active"

az keyvault secret set --vault-name $KV --name openai-api-key \
  --value "sk-demo-111111" --content-type text/plain \
  --tags environment=dev team=ai-platform rotation-policy=90-days -o none

az keyvault secret set --vault-name $KV --name cosmosdb-connection-string \
  --value "AccountEndpoint=https://demo.documents.azure.com:443/;AccountKey=demo-key-v1;" \
  --content-type text/plain --tags environment=dev -o none

az keyvault secret set --vault-name $KV --name storage-connection-string \
  --value "$CONN" --content-type text/plain --tags rotation=dual-key -o none

az keyvault secret list --vault-name $KV --query "[].{name:name, contentType:contentType}" -o table

# @@ env
export KEY_VAULT_URL="https://$KV.vault.azure.net/"
export AZURE_APPCONFIG_ENDPOINT="https://$AC.azconfig.io"
export STORAGE_ACCOUNT="$SA"
echo $KEY_VAULT_URL

# @@ rotate
# 1) Regenerate key2 (the spare key). No app uses it yet, so nothing breaks.
az storage account keys renew --account-name $SA --resource-group $RG --key key2 -o none

# 2) Save a connection string that uses key2 as a NEW secret version.
CONN2=$(az storage account show-connection-string --name $SA --resource-group $RG \
  --key key2 --query connectionString -o tsv)
az keyvault secret set --vault-name $KV --name storage-connection-string --value "$CONN2" -o none
echo "New version stored. Now WAIT about 25 seconds and watch terminal 1."

# @@ rotate_finish
# 3) Every app now uses key2. Regenerate key1 (the old one dies).
az storage account keys renew --account-name $SA --resource-group $RG --key key1 -o none
echo "key1 regenerated. Terminal 1 should still say OK."

# @@ rotate_fast
# Store the (new) key1 as the next version...
CONN3=$(az storage account show-connection-string --name $SA --resource-group $RG \
  --key key1 --query connectionString -o tsv)
az keyvault secret set --vault-name $KV --name storage-connection-string --value "$CONN3" -o none
# ...and kill key2 straight away, WITHOUT waiting.
az storage account keys renew --account-name $SA --resource-group $RG --key key2 -o none

# @@ eventgrid
az provider register --namespace Microsoft.EventGrid --wait

SA_ID=$(az storage account show --name $SA --resource-group $RG --query id -o tsv)

az eventgrid event-subscription create --name kv-secret-events \
  --source-resource-id $KV_ID \
  --endpoint-type storagequeue \
  --endpoint $SA_ID/queueServices/default/queues/kv-events \
  --included-event-types Microsoft.KeyVault.SecretNewVersionCreated \
  --query "{name:name, state:provisioningState}" -o table

# @@ eventgrid_fire
az keyvault secret set --vault-name $KV --name openai-api-key --value "sk-demo-NEW-333333" -o none

# @@ appconfig
az appconfig create --name $AC --resource-group $RG --location $LOCATION --sku Free -o table

AC_ID=$(az appconfig show --name $AC --resource-group $RG --query id -o tsv)

az role assignment create --assignee-object-id $ME --assignee-principal-type User \
  --role "App Configuration Data Owner" --scope $AC_ID --query "{principalType:principalType, createdOn:createdOn}" -o table

# @@ ac_import
# Wait until the App Configuration role works (prints a dot every 15 s).
until az appconfig kv list --name $AC --auth-mode login --top 1 -o none 2>/dev/null; do printf "."; sleep 15; done; echo " role is active"

az appconfig kv import --name $AC --auth-mode login --source file \
  --path settings/defaults.json --format json --separator ":" --yes

# @@ ac_labels
az appconfig kv set --name $AC --auth-mode login --yes \
  --key "DocPipeline:Pipeline:BatchSize" --value 200 --label Production -o none

az appconfig kv set --name $AC --auth-mode login --yes \
  --key "DocPipeline:OpenAI:Endpoint" --value "https://prod-openai.openai.azure.com/" --label Production -o none

az appconfig kv set --name $AC --auth-mode login --yes \
  --key "DocPipeline:Pipeline:BatchSize" --value 50 --label Staging -o none

az appconfig kv list --name $AC --auth-mode login --key "DocPipeline:Pipeline:BatchSize" \
  --label "*" --query "[].{key:key, label:label, value:value}" -o table

# @@ ac_flags
az appconfig feature set --name $AC --auth-mode login --yes \
  --feature UseNewEmbeddingsModel --description "Route embeddings to the new model" -o none

az appconfig feature set --name $AC --auth-mode login --yes --feature ClassificationStage -o none
az appconfig feature enable --name $AC --auth-mode login --yes --feature ClassificationStage -o none

az appconfig feature set --name $AC --auth-mode login --yes --feature EnableBatchProcessing -o none
az appconfig feature enable --name $AC --auth-mode login --yes --feature EnableBatchProcessing -o none

az appconfig feature list --name $AC --auth-mode login --query "[].{name:name, state:state}" -o table

# @@ ac_flip
az appconfig feature disable --name $AC --auth-mode login --yes --feature ClassificationStage -o none
az appconfig feature enable --name $AC --auth-mode login --yes --feature UseNewEmbeddingsModel -o none

# @@ ac_kvref
az appconfig kv set-keyvault --name $AC --auth-mode login --yes \
  --key "DocPipeline:OpenAI:ApiKey" \
  --secret-identifier "https://$KV.vault.azure.net/secrets/openai-api-key" -o none

az appconfig kv list --name $AC --auth-mode login --key "DocPipeline:OpenAI:*" --label "*" \
  --query "[].{key:key, label:label, value:value}" -o table

# @@ ac_refresh_1
# Change a setting but NOT the sentinel. Watch terminal 1 for 20 seconds: nothing changes.
az appconfig kv set --name $AC --auth-mode login --yes \
  --key "DocPipeline:Pipeline:BatchSize" --value 25 -o none
az appconfig kv set --name $AC --auth-mode login --yes \
  --key "DocPipeline:Pipeline:RetryCount" --value 5 -o none

# @@ ac_refresh_2
# Now bump the sentinel. Within ~10 s BOTH changes appear together.
az appconfig kv set --name $AC --auth-mode login --yes --key "Sentinel" --value 2 -o none

# @@ ac_refresh_3
# Feature flags refresh on their own, no sentinel needed.
az appconfig feature disable --name $AC --auth-mode login --yes --feature UseNewEmbeddingsModel -o none

# Rotate the secret in Key Vault. App Config is NOT touched. It shows up within ~60 s.
az keyvault secret set --vault-name $KV --name openai-api-key --value "sk-demo-ROTATED-444444" -o none

# @@ reconnect
# 1) Go to the lab folder (Step 1 put it in your home folder) and turn on the venv.
cd ~/ai200-lp8-lab
[ -f lab_env.py ] || echo "!! Not in the lab folder. cd into your ai200-lp8-lab folder yourself, then paste this block again."
if [ -f .venv/Scripts/activate ]; then source .venv/Scripts/activate; else source .venv/bin/activate; fi
# 2) Ask Azure for the names of what you ALREADY created (no new names are made).
export MSYS_NO_PATHCONV=1
RG="rg-ai200-lp8"
LOCATION="centralindia"
KV=$(az keyvault list --resource-group $RG --query "[0].name" -o tsv)
SA=$(az storage account list --resource-group $RG --query "[0].name" -o tsv)
AC=$(az appconfig list --resource-group $RG --query "[0].name" -o tsv)
# Before Step 14 the App Configuration store doesn't exist yet, so its name is worked out from the vault's number.
[ -z "$AC" ] && AC="appcs-ai200-${KV#kv-ai200-}"
[ -n "$KV" ] && KV_ID=$(az keyvault show --name $KV --query id -o tsv)
ME=$(az ad signed-in-user show --query id -o tsv)
# 3) The environment variables the Python scripts read.
export KEY_VAULT_URL="https://$KV.vault.azure.net/"
export AZURE_APPCONFIG_ENDPOINT="https://$AC.azconfig.io"
export STORAGE_ACCOUNT="$SA"
echo "Key Vault: $KV | App Config: $AC | Storage: $SA"
[ -z "$KV" ] && echo "!! No Key Vault found in $RG. Saw a Traceback ending in PermissionError? Run: cd ~  then paste this block again. Otherwise check az account show (same subscription as before?) and the RG name."

# @@ cleanup
az group delete --name $RG --yes

az keyvault purge --name $KV --location $LOCATION

az keyvault list-deleted --query "[].name" -o tsv
az appconfig list-deleted --query "[].name" -o tsv
