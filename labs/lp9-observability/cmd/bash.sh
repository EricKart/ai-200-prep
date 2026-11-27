# @@ vars
# Git Bash on Windows rewrites anything that starts with "/" (like /subscriptions/...).
# This line turns that off. On Mac, Linux and Cloud Shell it does nothing, so keep it.
export MSYS_NO_PATHCONV=1

RG="rg-ai200-lp9"
LOCATION="centralindia"
SUFFIX=$RANDOM$RANDOM
LAW="log-ai200-$SUFFIX"
AI="appi-ai200-$SUFFIX"
EMAIL="you@example.com"     # <-- put YOUR email here (alert notifications go to it)

echo "Workspace: $LAW | App Insights: $AI | Alerts to: $EMAIL"

# @@ ext
az extension add --name application-insights --upgrade --yes
az extension add --name scheduled-query --upgrade --yes

# @@ create
az group create --name $RG --location $LOCATION -o table

az monitor log-analytics workspace create --resource-group $RG \
  --workspace-name $LAW --location $LOCATION -o table

az monitor app-insights component create --app $AI --resource-group $RG \
  --location $LOCATION --workspace $LAW --kind web --application-type web \
  --query "{name:name, kind:kind, state:provisioningState}" -o table

# @@ env
AI_ID=$(az monitor app-insights component show --app $AI --resource-group $RG --query id -o tsv)
export APPLICATIONINSIGHTS_CONNECTION_STRING=$(az monitor app-insights component show \
  --app $AI --resource-group $RG --query connectionString -o tsv)
export APPINSIGHTS_RESOURCE_ID="$AI_ID"
echo $APPLICATIONINSIGHTS_CONNECTION_STRING

# @@ cli_query
az monitor app-insights query --app $AI --resource-group $RG --offset 1h \
  --analytics-query "requests | summarize count() by cloud_RoleName" \
  --query "tables[0].rows" -o table

# @@ workbook
az deployment group create --resource-group $RG --name rag-workbook \
  --template-file templates/workbook.json \
  --parameters appInsightsId=$AI_ID \
  --query "properties.provisioningState" -o tsv

# @@ actiongroup
az monitor action-group create --name ag-ai200-oncall --resource-group $RG \
  --short-name ai200oncal --action email oncall $EMAIL \
  --query "{name:name, enabled:enabled}" -o table

AG_ID=$(az monitor action-group show --name ag-ai200-oncall --resource-group $RG --query id -o tsv)

# @@ logalert
az monitor scheduled-query create --name alert-failure-spike --resource-group $RG \
  --scopes $AI_ID \
  --condition "count 'FailedServices' > 0" \
  --condition-query "FailedServices=requests | where success == false | summarize failedCount = count() by cloud_RoleName | where failedCount > 10" \
  --window-size 5m --evaluation-frequency 5m --severity 1 \
  --action-groups $AG_ID \
  --description "A service had more than 10 failed requests in 5 minutes" \
  --query "{name:name, enabled:enabled, severity:severity}" -o table

# @@ p95alert
az monitor scheduled-query create --name alert-p95-latency --resource-group $RG \
  --scopes $AI_ID \
  --condition "count 'SlowServices' > 0" \
  --condition-query "SlowServices=requests | summarize p95Duration = percentile(duration, 95) by cloud_RoleName | where p95Duration > 3000" \
  --window-size 15m --evaluation-frequency 5m --severity 2 \
  --action-groups $AG_ID \
  --description "p95 response time above 3 seconds" \
  --query "{name:name, enabled:enabled, severity:severity}" -o table

# @@ metricalert
az monitor metrics alert create --name alert-failed-requests-metric --resource-group $RG \
  --scopes $AI_ID \
  --condition "count requests/failed > 5" \
  --window-size 5m --evaluation-frequency 1m --severity 2 \
  --action $AG_ID \
  --description "Metric alert: more than 5 failed requests in 5 minutes" \
  --query "{name:name, enabled:enabled, severity:severity}" -o table

# @@ alerts_list
az monitor scheduled-query list --resource-group $RG --query "[].{name:name, severity:severity, enabled:enabled}" -o table
az monitor metrics alert list --resource-group $RG --query "[].{name:name, severity:severity, enabled:enabled}" -o table

# @@ fired
SUB=$(az account show --query id -o tsv)
az rest --method get \
  --url "https://management.azure.com/subscriptions/$SUB/providers/Microsoft.AlertsManagement/alerts" \
  --url-parameters api-version=2019-05-05-preview timeRange=1h \
  --query "value[].{alert:name, severity:properties.essentials.severity, state:properties.essentials.monitorCondition, fired:properties.essentials.startDateTime}" -o table

# @@ reconnect
# 1) Go to the lab folder (Step 1 put it in your home folder) and turn on the venv.
cd ~/ai200-lp9-lab
[ -f run_demo.py ] || echo "!! Not in the lab folder. cd into your ai200-lp9-lab folder yourself, then paste this block again."
if [ -f .venv/Scripts/activate ]; then source .venv/Scripts/activate; else source .venv/bin/activate; fi
# 2) Ask Azure for the names of what you ALREADY created (no new names are made).
export MSYS_NO_PATHCONV=1
RG="rg-ai200-lp9"
LOCATION="centralindia"
EMAIL="you@example.com"     # <-- your email again (only Step 13 uses it)
AI=$(az monitor app-insights component show --resource-group $RG --query "[0].name" -o tsv)
AG_ID=$(az monitor action-group show --name ag-ai200-oncall --resource-group $RG --query id -o tsv 2>/dev/null)
# 3) The environment variables the Python scripts read (only if Application Insights was found).
if [ -n "$AI" ]; then
  AI_ID=$(az monitor app-insights component show --app $AI --resource-group $RG --query id -o tsv)
  export APPLICATIONINSIGHTS_CONNECTION_STRING=$(az monitor app-insights component show --app $AI --resource-group $RG --query connectionString -o tsv)
  export APPINSIGHTS_RESOURCE_ID="$AI_ID"
fi
echo "App Insights: $AI"
[ -z "$AI" ] && echo "!! No Application Insights found in $RG. Did Step 4 finish? Check az account show (same subscription as before?)."

# @@ cleanup
az group delete --name $RG --yes
