# Hands-on labs

> Real Azure, real commands, Bash and PowerShell. Every lab lists its cost upfront and ends with a clean-up step.  
> Part of [AI-200 Prep](../README.md) · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200)

| Learning path | Lab | Status |
|---|---|---|
| 1. Implement container application hosting on Azure | [Build, store and run containers: ACR, App Service, sidecars](lp1-container-hosting/README.md) | ✅ Tested live (bash) |
| 2. Deploy and manage apps on Azure Container Apps | Microsoft Learn exercises: [M1](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/7-exercise-deploy-backend-api) · [M2](https://learn.microsoft.com/en-us/training/modules/manage-containers-azure-container-apps/7-exercise-diagnose-fix-failing-deployment) · [M3](https://learn.microsoft.com/en-us/training/modules/scale-containers-azure-container-apps/7-exercise-configure-autoscaling-keda) · [M4](https://learn.microsoft.com/en-us/training/modules/dynamic-sessions-azure-container-apps/6-exercise-execute-code-dynamic-session) | Our lab is being built and tested |
| 3. Deploy and monitor applications on Azure Kubernetes Service | Microsoft Learn exercises: [M1](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/5-exercise-deploy-ai-api) · [M2](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/5-exercise-configure-apps) · [M3](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/5-exercise-troubleshoot-apps) | Our lab is being built and tested |
| 4. Develop AI solutions with Azure Cosmos DB for NoSQL | Microsoft Learn exercises: [M1](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/5-exercise-build-rag-document-store) · [M2](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/6-exercise-build-semantic-search) · [M3](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/7-exercise-optimize-query-performance) | Our lab is being built and tested |
| 5. Develop AI solutions with Azure Database for PostgreSQL | Microsoft Learn exercises: [M1](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/7-exercise-build-agent-tool-backend) · [M2](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/7-exercise-implement-vector-search) · [M3](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/7-exercise-optimize-vector-search) | Our lab is being built and tested |
| 6. Enhance AI solutions with Azure Managed Redis | Microsoft Learn exercises: [M1](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/5-exercise-data-operations) · [M2](https://learn.microsoft.com/en-us/training/modules/implement-event-messaging-azure-managed-redis/5-exercise-publish-subscribe-events-redis) · [M3](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/5-exercise-semantic-search-azure-managed-redis) | Our lab is being built and tested |
| 7. Integrate backend services for AI solutions | Microsoft Learn exercises: [M1](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/6-exercise-process-messages) · [M2](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/6-exercise-publish-receive-events) · [M3](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/7-exercise-create-mcp-server) · [M4](https://learn.microsoft.com/en-us/training/modules/orchestrate-durable-functions/6-exercise-build-durable-document-processing-workflow) · [M5](https://learn.microsoft.com/en-us/training/modules/real-time-ai-web-pubsub/8-exercise-stream-ai-investigation-updates) | Our lab is being built and tested |
| 8. Manage application secrets and configuration for AI solutions | [Secrets and configuration: Key Vault + App Configuration](lp8-secrets-config/README.md) | ✅ Tested live |
| 9. Observe and troubleshoot apps on Azure | [Observe and troubleshoot: OpenTelemetry, KQL, workbooks, alerts](lp9-observability/README.md) | ✅ Tested live |

## Rules every lab follows

- **Cost first.** The README states the official price of every resource and what the lab costs in total.
- **Clean up.** The last step deletes everything. Soft-deleted resources (Key Vault, App Configuration) are purged too.
- **Two shells.** `cmd/bash.sh` and `cmd/ps.ps1` have the same named steps (`# @@ step-name`). Lab READMEs show each step's commands, filled in from those files by `npm run build:labs`, so the README and the scripts never disagree.
- **Recover from a new terminal.** Each guide has a block that restores your variables and venv without creating new resources.
- **Tested.** Each lab is run live before release. Anything not yet run is marked as untested.

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200)
