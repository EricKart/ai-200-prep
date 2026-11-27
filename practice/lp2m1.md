# Practice: LP2 · M1 Deploy containers to Azure Container Apps

> 25 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp2m1.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-2/deploy-containers-azure-container-apps)

## 1. `lp2m1-001`

An embedding service must be callable by the AI API in the same environment, but not from the internet. Which ingress setting should it use?

- **A.** No ingress, plus a public IP address
- **B.** --ingress external
- **C.** --ingress private-link
- **D.** --ingress internal

<details><summary>💡 Hint</summary>

Callers inside the environment need it, and the internet mustn't reach it. Which ingress mode keeps traffic inside?

</details>

<details><summary>✅ Answer</summary>

**D.** --ingress internal

- A: Learn uses ingress settings, not public IPs, to control reachability.
- B: External ingress exposes the app to callers outside the environment.
- C: private-link isn't one of the ingress values Learn describes.
- D: Correct. Internal ingress makes the service reachable only within the environment.

Use external ingress for public-facing APIs and internal ingress for services called only by other services in the environment.

📘 Source: [Explore Container Apps environments](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/2-container-apps-environments)

</details>

## 2. `lp2m1-002`

For each statement, select Yes if the statement is true. Otherwise, select No. You're planning environments for an AI solution with an API, a background processor, and dev, test and production stages.

| Statement | Yes / No |
|---|---|
| Putting the API and the background processor in the same environment lets them share networking and logging integration. | ☐ |
| Learn recommends one shared environment for dev, test and production to keep things simple. | ☐ |
| An environment is only a folder for resources and doesn't affect traffic between apps. | ☐ |

<details><summary>💡 Hint</summary>

Think about what an environment shares and why you'd separate lifecycle stages.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Putting the API and the background processor in the same environment lets them share networking and logging integration. | Yes | Related services are often grouped in one environment for shared networking and logging. |
| Learn recommends one shared environment for dev, test and production to keep things simple. | No | Learn recommends separate environments by lifecycle to reduce blast radius. |
| An environment is only a folder for resources and doesn't affect traffic between apps. | No | An environment influences internal traffic, logging connections and governance. |

Environments are an isolation and management model: group related services, separate lifecycles.

📘 Source: [Explore Container Apps environments](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/2-container-apps-environments)

</details>

## 3. `lp2m1-003`

Several apps will share one environment, and the platform team wants control over its name and lifecycle. Which approach fits best?

- **A.** Deploy each app with --ingress internal so they end up in one environment
- **B.** Let az containerapp up create a new environment for each app as it deploys
- **C.** Create the environment first with az containerapp env create, then deploy the apps into it
- **D.** Create a separate resource group per app; the environment follows from that

<details><summary>💡 Hint</summary>

Several apps share the environment, and you want control over its name. Should a deploy command create it implicitly?

</details>

<details><summary>✅ Answer</summary>

**C.** Create the environment first with az containerapp env create, then deploy the apps into it

- A: Ingress controls reachability, not which environment is created.
- B: containerapp up is fastest, but it makes the naming and lifecycle decisions for you.
- C: Correct. Creating the environment explicitly gives more control when multiple apps share it.
- D: Resource groups don't define a Container Apps environment.

Creating the environment first gives you control over naming and lifecycle, which helps when multiple apps share it.

📘 Source: [Explore Container Apps environments](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/2-container-apps-environments)

</details>

## 4. `lp2m1-004`

An AI API calls a private embedding processor, and the team validates new revisions in dev and test before production. Which environment layout follows Learn's guidance?

- **A.** Per-stage environments, each holding both services, with internal ingress on the processor
- **B.** One environment per stage, with the processor deployed outside Container Apps as a VM
- **C.** One shared environment for all three stages, with the processor's ingress set to external
- **D.** One environment for every app, so that the API and the processor never share networking

<details><summary>💡 Hint</summary>

Two guidelines apply: separate by lifecycle, and keep services that talk privately together.

</details>

<details><summary>✅ Answer</summary>

**A.** Per-stage environments, each holding both services, with internal ingress on the processor

- A: Correct. Separate environments per lifecycle stage reduce blast radius, and services that talk privately belong in the same environment with internal ingress.
- B: Nothing in the scenario needs a VM. Both services fit in the same environment.
- C: A shared environment removes the isolation between stages, and external ingress exposes a service that should stay private.
- D: Splitting the API and processor apart breaks the simple private communication that a shared environment gives them.

Learn recommends separate environments for development, test and production, and placing services that must communicate privately in the same environment with internal ingress.

📘 Source: [Explore Container Apps environments](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/2-container-apps-environments)

</details>

## 5. `lp2m1-005`

A new revision of your AI API fails at startup, and you want to query its container logs and the platform's system logs together, in one place. What does a Container Apps environment commonly integrate with for this?

- **A.** Azure DevOps pipeline history
- **B.** Azure Container Registry webhooks
- **C.** Azure Monitor logs
- **D.** Azure Key Vault diagnostics

<details><summary>💡 Hint</summary>

You want one queryable store for logs. Which Azure monitoring service holds logs?

</details>

<details><summary>✅ Answer</summary>

**C.** Azure Monitor logs

- A: Pipeline history shows deployments you ran, not the app's runtime logs.
- B: Registry webhooks notify about image pushes. They don't collect logs.
- C: Correct. An environment commonly integrates with Azure Monitor logs, so you can query container and system logs in one place.
- D: Key Vault holds secrets. It isn't where Container Apps logs go.

A Container Apps environment commonly integrates with Azure Monitor logs, so you can query container logs and system logs in one place.

📘 Source: [Explore Container Apps environments](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/2-container-apps-environments)

</details>

## 6. `lp2m1-006`

Which command is the fastest way to deploy a first version of a container app, creating the environment if needed?

- **A.** az containerapp up
- **B.** az containerapp update
- **C.** az containerapp env create
- **D.** az containerapp create

<details><summary>💡 Hint</summary>

One command can create the environment and the app together. It's the quickest path to a first deployment.

</details>

<details><summary>✅ Answer</summary>

**A.** az containerapp up

- A: Correct. up can create the environment and supporting resources and returns the FQDN.
- B: update changes an existing app.
- C: env create only creates the environment, not the app.
- D: create is the more explicit option and expects an existing environment.

az containerapp up is the fastest initial deployment; az containerapp create is the more explicit path.

📘 Source: [Deploy a container app using the Azure CLI and YAML](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/3-deploy-container-app)

</details>

## 7. `lp2m1-007`

You run `az containerapp update --yaml ./containerapp.yml --image myregistry.azurecr.io/ai-api:v3`, but the app keeps the image named in the YAML file. Why?

- **A.** The YAML file is applied first and then overwritten by the flag
- **B.** Image changes need az containerapp up instead of update
- **C.** When --yaml is used, other flags are ignored
- **D.** The registry has to be set again before each image change

<details><summary>💡 Hint</summary>

The command used a YAML file and a flag. Which one does Container Apps treat as the source of truth?

</details>

<details><summary>✅ Answer</summary>

**C.** When --yaml is used, other flags are ignored

- A: It's the other way round: the flag is ignored entirely.
- B: update can change images; the issue is the --yaml behavior.
- C: Correct. The YAML becomes the source of truth, so --image is ignored.
- D: Registry configuration isn't required again for each update.

With --yaml, the YAML file is the full configuration source and other flags are ignored.

📘 Source: [Deploy a container app using the Azure CLI and YAML](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/3-deploy-container-app)

</details>

## 8. `lp2m1-008`

You're preparing a new machine to deploy Container Apps from the CLI. Put the steps in the order Learn's quickstart uses.

- az extension add --name containerapp --upgrade
- az login
- az provider register --namespace Microsoft.App
- az upgrade

<details><summary>💡 Hint</summary>

Sign in, update the CLI, add the extension, then register the provider.

</details>

<details><summary>✅ Answer</summary>

1. az login
2. az upgrade
3. az extension add --name containerapp --upgrade
4. az provider register --namespace Microsoft.App

Sign in, update the CLI, add or upgrade the containerapp extension, then register the Microsoft.App (and Microsoft.OperationalInsights) providers.

📘 Source: [Deploy a container app using the Azure CLI and YAML](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/3-deploy-container-app)

</details>

## 9. `lp2m1-009`

A deployment of `myregistry.azurecr.io/Team/AI-Api:v1` fails with what looks like an authentication error, although the credentials are correct. What should you check first?

- **A.** Whether the YAML file in source control was reviewed
- **B.** Whether the provider Microsoft.OperationalInsights is registered
- **C.** Whether the app was created with az containerapp up or create
- **D.** Whether the repository name in the image reference is lower case

<details><summary>💡 Hint</summary>

Pull failures can look like authentication errors. Check the case of the image path.

</details>

<details><summary>✅ Answer</summary>

**D.** Whether the repository name in the image reference is lower case

- A: Code review doesn't affect the image pull.
- B: Provider registration problems don't show up as image pull auth errors.
- C: Both commands pull the image the same way.
- D: Correct. Learn warns that non-lower-case repository names cause pull failures that look like authentication errors.

Keep the repository portion of the image reference lower case to avoid misleading pull failures.

📘 Source: [Deploy a container app using the Azure CLI and YAML](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/3-deploy-container-app)

</details>

## 10. `lp2m1-010`

Your first az containerapp create in a new subscription fails with a message that the subscription isn't registered to use the namespace Microsoft.OperationalInsights. What should you run?

- **A.** az upgrade --namespace Microsoft.OperationalInsights
- **B.** az provider register --namespace Microsoft.OperationalInsights
- **C.** az containerapp env create --logs-destination none
- **D.** az extension add --name containerapp --upgrade

<details><summary>💡 Hint</summary>

The error names a resource provider. Which az command family registers providers in a subscription?

</details>

<details><summary>✅ Answer</summary>

**B.** az provider register --namespace Microsoft.OperationalInsights

- A: az upgrade updates the CLI itself, and it has no namespace parameter.
- B: Correct. The quickstart setup registers both Microsoft.App and Microsoft.OperationalInsights.
- C: Changing log options avoids the question. The quickstart flow registers the provider.
- D: The extension adds CLI commands. It doesn't register resource providers in the subscription.

Before deploying, register the resource providers: az provider register --namespace Microsoft.App and --namespace Microsoft.OperationalInsights.

📘 Source: [Deploy a container app using the Azure CLI and YAML](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/3-deploy-container-app)

</details>

## 11. `lp2m1-011`

You run az containerapp update --image myregistry.azurecr.io/ai-api:v2 on a running app. You want to validate the change before it takes all traffic. What does the update create?

- **A.** A new environment that copies the app's settings
- **B.** An in-place restart of the existing replicas
- **C.** A new revision that represents the new configuration
- **D.** A replacement app with a new FQDN for the v2 image

<details><summary>💡 Hint</summary>

Container Apps versions every configuration change. What's the name for one version of an app?

</details>

<details><summary>✅ Answer</summary>

**C.** A new revision that represents the new configuration

- A: Updating an app doesn't create an environment. Environments are created separately.
- B: Container Apps versions configuration changes as revisions rather than patching running replicas.
- C: Correct. Updates usually create a new revision, which lets you validate it before shifting all traffic.
- D: The app keeps its identity and FQDN. The change is versioned as a revision.

Container Apps uses revisions to version configuration changes. An update such as a new image tag creates a new revision.

📘 Source: [Deploy a container app using the Azure CLI and YAML](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/3-deploy-container-app)

</details>

## 12. `lp2m1-012`

Engineers deploy the AI API with ad-hoc CLI flags, and test and production configurations keep drifting apart. The team wants every change reviewed. What does Learn recommend?

- **A.** Use az containerapp up for every deployment so that defaults stay the same
- **B.** Make changes in the Azure portal so that the activity log records them
- **C.** Keep containerapp.yml in source control and apply it with --yaml after code review
- **D.** Combine --yaml with extra CLI flags for the values that differ per stage

<details><summary>💡 Hint</summary>

You want a file the whole team can approve before it's applied the same way every time.

</details>

<details><summary>✅ Answer</summary>

**C.** Keep containerapp.yml in source control and apply it with --yaml after code review

- A: az containerapp up is for fast first deployments. It doesn't create a reviewable record of configuration.
- B: Portal changes are for one-off work. They aren't reviewed before they're applied.
- C: Correct. YAML in source control makes deployments repeatable and reviewable and reduces drift.
- D: With --yaml, other flags are ignored, so the per-stage flags would silently do nothing.

Store the YAML file in source control and apply changes through code review. With --yaml, the YAML becomes the source of truth and other flags are ignored.

📘 Source: [Deploy a container app using the Azure CLI and YAML](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/3-deploy-container-app)

</details>

## 13. `lp2m1-013`

The AI API needs the embeddings API key as the variable EMBEDDINGS_API_KEY, and the key is already stored as the secret embeddings-api-key. What value should the variable have?

- **A.** secretref:embeddings-api-key
- **B.** $(embeddings-api-key)
- **C.** The key itself, pasted into --set-env-vars
- **D.** keyvault:embeddings-api-key

<details><summary>💡 Hint</summary>

Environment variables can point to a secret by name with a special prefix.

</details>

<details><summary>✅ Answer</summary>

**A.** secretref:embeddings-api-key

- A: Correct. secretref:`<secret-name>` maps the secret to the variable without exposing its value.
- B: That isn't Container Apps syntax.
- C: Pasting the value exposes it in shell history and config.
- D: That isn't the Container Apps reference syntax.

Set the variable to secretref:`<secret-name>` (secretRef in YAML).

📘 Source: [Configure runtime settings with environment variables and secrets](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/4-configure-runtime)

</details>

## 14. `lp2m1-014`

You need to change LOG_LEVEL to debug on a running app without removing its other environment variables. Which command should you use?

- **A.** az containerapp update --set-env-vars LOG_LEVEL=debug
- **B.** az containerapp registry set --env-vars LOG_LEVEL=debug
- **C.** az containerapp create --env-vars LOG_LEVEL=debug
- **D.** az containerapp secret set --secrets LOG_LEVEL=debug

<details><summary>💡 Hint</summary>

One flag replaces the variable list and the other adds or updates. Which keeps existing variables?

</details>

<details><summary>✅ Answer</summary>

**A.** az containerapp update --set-env-vars LOG_LEVEL=debug

- A: Correct. --set-env-vars adds or updates variables without removing existing ones.
- B: registry set configures image pull authentication.
- C: create is for new apps.
- D: A log level isn't sensitive and doesn't belong in secrets.

Use --env-vars on create and --set-env-vars on update for non-sensitive settings.

📘 Source: [Configure runtime settings with environment variables and secrets](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/4-configure-runtime)

</details>

## 15. `lp2m1-015`

For each statement, select Yes if the statement is true. Otherwise, select No. A team stores `containerapp.yml` in Git and uses secrets for provider API keys.

| Statement | Yes / No |
|---|---|
| The YAML file in Git should contain the API key values so deployments are complete. | ☐ |
| Rotating a Container Apps secret requires rebuilding the container image. | ☐ |
| A Key Vault reference lets the app fetch a secret whose system of record is Key Vault. | ☐ |
| After a registry change, deploying a new revision and checking it starts validates the change. | ☐ |

<details><summary>💡 Hint</summary>

Secrets stay out of Git and images. Key Vault can be the system of record.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The YAML file in Git should contain the API key values so deployments are complete. | No | Keep secret values out of YAML; store only secret names. |
| Rotating a Container Apps secret requires rebuilding the container image. | No | Secrets let you rotate values without rebuilding or redeploying the image. |
| A Key Vault reference lets the app fetch a secret whose system of record is Key Vault. | Yes | The CLI supports a Key Vault reference format for secrets. |
| After a registry change, deploying a new revision and checking it starts validates the change. | Yes | Learn recommends validating auth during rollout this way. |

Secrets stay out of YAML and images; Key Vault can be the system of record; validate registry changes with a new revision.

📘 Source: [Configure runtime settings with environment variables and secrets](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/4-configure-runtime)

</details>

## 16. `lp2m1-016`

Your containerapp.yml is stored in Git. EMBEDDINGS_API_KEY must come from the Container Apps secret embeddings-api-key. How should the env entry for the ai-api container look?

- **A.** name: EMBEDDINGS_API_KEY, with value: set to the key copied from the provider
- **B.** name: EMBEDDINGS_API_KEY, with valueFrom: secretKeyRef: embeddings-api-key
- **C.** name: EMBEDDINGS_API_KEY, with value: ${embeddings-api-key}
- **D.** name: EMBEDDINGS_API_KEY, with secretRef: embeddings-api-key

<details><summary>💡 Hint</summary>

The CLI and YAML both refer to the secret by name, but YAML uses a dedicated field instead of the value.

</details>

<details><summary>✅ Answer</summary>

**D.** name: EMBEDDINGS_API_KEY, with secretRef: embeddings-api-key

- A: That puts the secret value in Git, which the guidance says to avoid.
- B: That's Kubernetes Pod syntax. Container Apps YAML uses secretRef.
- C: Container Apps doesn't expand shell-style placeholders in YAML values.
- D: Correct. In YAML, secretRef names the secret, so only the secret's name is stored in source control.

In YAML, an env entry uses secretRef: `<secret-name>`. In the CLI, you set the value to secretref:`<secret-name>`. Either way, only the secret's name is stored.

📘 Source: [Configure runtime settings with environment variables and secrets](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/4-configure-runtime)

</details>

## 17. `lp2m1-017`

Twenty container apps pull images from one ACR registry, and rotating the registry password across all of them is costly. Which two steps follow Learn's guidance? (Select two.)

- **A.** Omit credentials so the CLI infers them in production
- **B.** Grant each app's identity only the AcrPull role
- **C.** Run az containerapp registry set with --identity system
- **D.** Grant each app's identity the Owner role on the registry

<details><summary>💡 Hint</summary>

Learn's advice for many apps pulling from ACR is to avoid long-lived credentials and grant least privilege.

</details>

<details><summary>✅ Answer</summary>

**B.** Grant each app's identity only the AcrPull role  
**C.** Run az containerapp registry set with --identity system

- A: Learn says to prefer an explicit authentication method in production.
- B: Correct. Grant least privilege: only AcrPull for identities that pull images.
- C: Correct. Managed identity avoids storing long-lived registry credentials.
- D: Owner is far more than pulling needs; Learn says least privilege.

Prefer managed identity for ACR and assign only AcrPull.

📘 Source: [Configure image pull authentication for private registries](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/5-connect-to-registries)

</details>

## 18. `lp2m1-018`

A vendor's model image is in a third-party private registry that doesn't support Azure managed identities. How should you configure the container app to pull it?

- **A.** az containerapp registry set with --server, --username and --password
- **B.** Grant the app's managed identity the AcrPull role on the vendor's registry
- **C.** Store the vendor password in an environment variable named REGISTRY_PASSWORD
- **D.** az containerapp registry set with --server and --identity system

<details><summary>💡 Hint</summary>

Managed identity isn't an option for this registry. What's the simplest credential type that works with any registry?

</details>

<details><summary>✅ Answer</summary>

**A.** az containerapp registry set with --server, --username and --password

- A: Correct. Username and password works with registries that don't support Azure-managed identities.
- B: AcrPull is an Azure Container Registry role. It can't be assigned on a third-party registry.
- C: Container Apps doesn't read registry credentials from app environment variables.
- D: Managed identity pulls need a registry that accepts Azure identities, such as ACR.

Container Apps supports registry authentication with username and password, and with managed identity when the registry is ACR. For registries without Azure-managed identity support, use username and password.

📘 Source: [Configure image pull authentication for private registries](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/5-connect-to-registries)

</details>

## 19. `lp2m1-019`

The same app is deployed to dev, test and prod, and you suspect a different registry is configured in one of them. Which command shows the registries configured on an app?

- **A.** az containerapp registry list
- **B.** az containerapp revision list
- **C.** az containerapp env show
- **D.** az acr repository list

<details><summary>💡 Hint</summary>

Registry configuration belongs to the app. Look for the registry sub-command of az containerapp.

</details>

<details><summary>✅ Answer</summary>

**A.** az containerapp registry list

- A: Correct. It lists the registries configured on the app, which helps you spot drift between environments.
- B: This lists revisions and their state, not registry configuration.
- C: This shows the environment. Registry settings belong to each app.
- D: This lists repositories inside a registry. It doesn't show which registries an app is set up to use.

Use az containerapp registry list (or show --server) to confirm which registries an app is configured to use, for example to detect drift across environments.

📘 Source: [Configure image pull authentication for private registries](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/5-connect-to-registries)

</details>

## 20. `lp2m1-020`

For each statement, select Yes if the statement is true. Otherwise, select No. You're switching a production container app to pull from ACR with managed identity.

| Statement | Yes / No |
|---|---|
| The app's identity should get the AcrPush role so that future CI changes don't need new role assignments. | ☐ |
| Image references should use fully qualified names that include the registry hostname. | ☐ |
| Because the CLI can sometimes infer ACR credentials, production scripts can safely leave authentication out. | ☐ |
| You should deploy a new revision and confirm it starts before assuming the registry change works. | ☐ |

<details><summary>💡 Hint</summary>

Think least privilege, unambiguous image names, explicit auth, and proving the change with a real revision.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The app's identity should get the AcrPush role so that future CI changes don't need new role assignments. | No | Grant least privilege: an identity that only pulls images needs only AcrPull. |
| Image references should use fully qualified names that include the registry hostname. | Yes | Fully qualified names avoid ambiguity about which registry an image comes from. |
| Because the CLI can sometimes infer ACR credentials, production scripts can safely leave authentication out. | No | Learn says to prefer an explicit authentication approach in production so behavior is predictable. |
| You should deploy a new revision and confirm it starts before assuming the registry change works. | Yes | Validating auth during rollout catches pull failures before you rely on the change. |

Best practices: prefer managed identity for ACR, grant only AcrPull, use fully qualified image names, and validate the change by deploying a new revision and checking that it starts.

📘 Source: [Configure image pull authentication for private registries](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/5-connect-to-registries)

</details>

## 21. `lp2m1-021`

Match each verification need to the command.

Choices: **az containerapp logs show --type system** · **az containerapp revision list --all** · **az containerapp replica list**

- Check for a platform-level issue
- Include inactive revisions while debugging
- See whether any instances of the revision are running

<details><summary>💡 Hint</summary>

System logs, all revisions, and running instances each have their own command.

</details>

<details><summary>✅ Answer</summary>

- Check for a platform-level issue → **az containerapp logs show --type system**. --type system returns platform system logs.
- Include inactive revisions while debugging → **az containerapp revision list --all**. --all includes inactive revisions.
- See whether any instances of the revision are running → **az containerapp replica list**. Replicas are the running instances of a revision.

Logs explain errors, revisions show versions, replicas show what's running.

📘 Source: [Verify deployments with logs and status](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/6-verify-deployment)

</details>

## 22. `lp2m1-022`

After an update, users still get the old behavior. You want to confirm that the update created a new revision and that it became healthy. Which command should you run?

- **A.** az containerapp registry list
- **B.** az containerapp revision list
- **C.** az containerapp env show
- **D.** az containerapp secret list

<details><summary>💡 Hint</summary>

You want to see whether the update produced a new version and whether it's healthy.

</details>

<details><summary>✅ Answer</summary>

**B.** az containerapp revision list

- A: registry list shows pull configuration only.
- B: Correct. Listing revisions confirms a new revision exists and becomes active.
- C: env show describes the environment, not app revisions.
- D: secret list doesn't show revision state.

Use revisions for rollout validation: list them after updates.

📘 Source: [Verify deployments with logs and status](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/6-verify-deployment)

</details>

## 23. `lp2m1-023`

For each statement, select Yes if the statement is true. Otherwise, select No. You're investigating a startup failure of a new AI API revision.

| Statement | Yes / No |
|---|---|
| az containerapp logs show is a good first step to capture startup errors. | ☐ |
| By default, az containerapp logs show streams every line ever written by the app. | ☐ |
| If replica list shows zero replicas, the revision has crashed. | ☐ |

<details><summary>💡 Hint</summary>

Logs are the first step. Think about how many lines logs show returns by default, and what zero replicas can mean.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| az containerapp logs show is a good first step to capture startup errors. | Yes | Learn says to start with logs. |
| By default, az containerapp logs show streams every line ever written by the app. | No | By default it returns a limited number of lines; use --follow and --tail to stream. |
| If replica list shows zero replicas, the revision has crashed. | No | Zero replicas can also mean the app scaled to zero. |

Start with logs; replicas help detect scale-to-zero, crash loops or missing traffic.

📘 Source: [Verify deployments with logs and status](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/6-verify-deployment)

</details>

## 24. `lp2m1-024`

A web client can't reach your newly deployed AI API. Before reading any logs, you want to confirm the ingress settings and get the FQDN. Which command should you run?

- **A.** az containerapp show
- **B.** az containerapp logs show --type system
- **C.** az containerapp env show
- **D.** az containerapp replica list

<details><summary>💡 Hint</summary>

You want the app's own configuration, not its logs or instances.

</details>

<details><summary>✅ Answer</summary>

**A.** az containerapp show

- A: Correct. It shows the app's configuration, including ingress, so you can spot internal-vs-external mistakes and get the FQDN.
- B: System logs help with platform issues, but they don't show the app's ingress configuration.
- C: The environment doesn't hold each app's ingress settings or FQDN.
- D: Replicas tell you whether instances are running, not how ingress is configured.

Before diving into logs, confirm app configuration and ingress with az containerapp show. It catches mistakes such as internal ingress where you expected external, and it returns the FQDN.

📘 Source: [Verify deployments with logs and status](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/6-verify-deployment)

</details>

## 25. `lp2m1-025`

While you send test traffic to the AI API, you want to watch new log lines as they arrive, with more history than the default. Which command fits?

- **A.** az containerapp logs show --type system
- **B.** az containerapp revision list --all
- **C.** az containerapp logs show --follow --tail 30
- **D.** az containerapp replica list --revision latest

<details><summary>💡 Hint</summary>

You need two options: one keeps the stream open, and one sets how many lines come back.

</details>

<details><summary>✅ Answer</summary>

**C.** az containerapp logs show --follow --tail 30

- A: This switches to platform logs. It doesn't follow new output.
- B: This lists revisions, including inactive ones. It doesn't show logs.
- C: Correct. --follow streams logs in real time, and --tail raises the number of lines returned.
- D: This lists running instances. It doesn't stream their output.

az containerapp logs show returns a limited number of lines by default. Add --follow to tail in real time and --tail to increase the count.

📘 Source: [Verify deployments with logs and status](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-container-apps/6-verify-deployment)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
