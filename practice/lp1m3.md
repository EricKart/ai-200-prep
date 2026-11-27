# Practice: LP1 · M3 Run sidecar-enabled AI applications on Azure App Service

> 33 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp1m3.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-1/deploy-sidecar-azure-app-service)

## 1. `lp1m3-001`

In a sidecar-enabled App Service app, which container receives external HTTP traffic?

- **A.** Only the container with isMain set to true
- **B.** Each sidecar, through its own public endpoint
- **C.** The container that was created first in the app
- **D.** Every container whose target port is 80 or 8080

<details><summary>💡 Hint</summary>

Only one container in the app is marked as the main one. Which container gets the public traffic?

</details>

<details><summary>✅ Answer</summary>

**A.** Only the container with isMain set to true

- A: Correct. App Service sends external HTTP traffic only to the main container.
- B: Sidecars aren't published as separate public endpoints.
- C: Creation order doesn't decide routing.
- D: Target port is metadata; routing depends on the main role.

Roles decide routing: isMain: true receives external traffic; sidecars are reachable only inside the shared network namespace.

📘 Source: [Choose the App Service sidecar pattern](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/2-choose-sidecar-pattern)

</details>

## 2. `lp1m3-002`

How many sidecar containers can a sidecar-enabled App Service app have alongside its main container?

- **A.** Up to nine
- **B.** Up to three
- **C.** Up to twenty
- **D.** Up to five

<details><summary>💡 Hint</summary>

There's a fixed limit of sidecars next to the one main container. It's a single digit.

</details>

<details><summary>✅ Answer</summary>

**A.** Up to nine

- A: Correct. One main container and up to nine sidecars.
- B: Learn gives a higher limit.
- C: Learn's limit is nine sidecars.
- D: Learn gives a higher limit.

A sidecar-enabled app has one main container and can have up to nine sidecar containers.

📘 Source: [Choose the App Service sidecar pattern](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/2-choose-sidecar-pattern)

</details>

## 3. `lp1m3-003`

An internal API sends prompts to a compact model server. Every API instance needs its own local model endpoint, the two must scale together, and the team wants to update the model image without rebuilding the API image. What should you use?

- **A.** Build the model server into the API image
- **B.** Host the model on a shared inference service used by all apps
- **C.** Run the model server as an App Service sidecar
- **D.** Run the model server in a second web app in the same plan

<details><summary>💡 Hint</summary>

One endpoint per API instance, scaling together, and separate images. Which App Service pattern runs containers side by side?

</details>

<details><summary>✅ Answer</summary>

**C.** Run the model server as an App Service sidecar

- A: Then any model update would mean rebuilding the API image.
- B: A shared service fits when several apps share a model. Here each API instance needs its own local endpoint.
- C: Correct. Separate images, one lifecycle, scaled as a set, with calls over localhost.
- D: A separate app scales on its own and needs a network endpoint, which the scenario wants to avoid.

Separate images, one lifecycle, scaled as a set, with calls over localhost.

📘 Source: [Choose the App Service sidecar pattern](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/2-choose-sidecar-pattern)

</details>

## 4. `lp1m3-004`

Five different apps will share one large language model, and model serving needs GPU hardware with its own scaling rule. Where should you run the model?

- **A.** In the /home volume shared by all the apps
- **B.** As the main container of one sidecar-enabled app
- **C.** In a separately deployed inference service
- **D.** As a sidecar in each of the five apps

<details><summary>💡 Hint</summary>

Many callers, special hardware and an independent scaling rule all point away from one app's instances.

</details>

<details><summary>✅ Answer</summary>

**C.** In a separately deployed inference service

- A: /home is file storage, not a model hosting option.
- B: Making it the main container doesn't give it independent scaling or sharing.
- C: Correct. Shared endpoints, GPU needs and different scaling favor a separate service.
- D: Sidecars suit one helper per instance with the same scaling, not a shared GPU model.

Learn lists shared endpoints, GPU hardware and a different scaling policy as reasons for a separately deployed service.

📘 Source: [Choose the App Service sidecar pattern](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/2-choose-sidecar-pattern)

</details>

## 5. `lp1m3-005`

For each statement, select Yes if the statement is true. Otherwise, select No. An API runs with a model-server sidecar, and the app scales from two to four instances.

| Statement | Yes / No |
|---|---|
| Each of the two new instances gets its own model-server sidecar. | ☐ |
| The model server can scale on its own rule while the API stays at four. | ☐ |
| The sidecar's memory use comes out of the same App Service plan as the API. | ☐ |
| The sidecar can run any public image, because it's isolated from the main app. | ☐ |

<details><summary>💡 Hint</summary>

Sidecars are part of each instance. Do they scale on their own, and whose resources do they use?

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Each of the two new instances gets its own model-server sidecar. | Yes | Scale out adds the main container and all configured sidecars to each new instance. |
| The model server can scale on its own rule while the API stays at four. | No | The plan doesn't scale the model server independently from the API. |
| The sidecar's memory use comes out of the same App Service plan as the API. | Yes | All containers on an instance consume capacity from the same plan. |
| The sidecar can run any public image, because it's isolated from the main app. | No | Containers share a trust boundary, so run only trusted images. |

Sidecars share lifecycle, scale, capacity and trust boundary with the main app.

📘 Source: [Choose the App Service sidecar pattern](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/2-choose-sidecar-pattern)

</details>

## 6. `lp1m3-006`

For each statement about App Service sidecars, select Yes if it's true. Otherwise, select No.

| Statement | Yes / No |
|---|---|
| An app can have one main container and up to nine sidecar containers. | ☐ |
| External HTTP traffic is routed to any container that declares a target port. | ☐ |
| When the app scales in, App Service removes the main container and its sidecars together. | ☐ |

<details><summary>💡 Hint</summary>

Count the containers, check which one gets external traffic, and think about how scaling treats the group.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| An app can have one main container and up to nine sidecar containers. | Yes | That's the documented limit. |
| External HTTP traffic is routed to any container that declares a target port. | No | External HTTP traffic goes only to the container with isMain: true. |
| When the app scales in, App Service removes the main container and its sidecars together. | Yes | Scale-in removes the complete set of containers on an instance. |

An app has one main container and up to nine sidecars. Only the main container (isMain) receives external HTTP traffic, and the main container and its sidecars scale in and out together.

📘 Source: [Choose the App Service sidecar pattern](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/2-choose-sidecar-pattern)

</details>

## 7. `lp1m3-007`

You convert a classic Linux custom-container app that uses WEBSITES_PORT=8000 and DOCKER_REGISTRY_SERVER_PASSWORD to the sitecontainers model. What should you plan for?

- **A.** Both settings keep working unchanged after the conversion
- **B.** WEBSITES_PORT carries over, but the registry settings need replacing
- **C.** Conversion moves both values into a Docker Compose file for you
- **D.** Both settings no longer configure the containers, so replace them

<details><summary>💡 Hint</summary>

The sitecontainers model configures each container explicitly. Do the classic single-container settings still apply?

</details>

<details><summary>✅ Answer</summary>

**D.** Both settings no longer configure the containers, so replace them

- A: Learn says these classic settings don't configure sidecar-enabled containers.
- B: Neither setting configures sidecar-enabled containers.
- C: Sitecontainers replaces Docker Compose; it doesn't generate one.
- D: Correct. Plan replacement settings (target ports, image authentication) before converting production.

Sitecontainers apps define ports, roles and image authentication in container resources; WEBSITES_PORT and DOCKER_REGISTRY_SERVER_* don't apply.

📘 Source: [Choose the App Service sidecar pattern](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/2-choose-sidecar-pattern)

</details>

## 8. `lp1m3-008`

The model sidecar uses most of the instance's memory. The API slows down even though the API itself uses little memory. Why?

- **A.** The sidecar takes the API's external traffic
- **B.** The API's image is pulled again whenever the sidecar uses memory
- **C.** The containers share the plan's CPU and memory
- **D.** Sidecars run on a lower-priority CPU tier

<details><summary>💡 Hint</summary>

The containers run on the same instance. What do they share?

</details>

<details><summary>✅ Answer</summary>

**C.** The containers share the plan's CPU and memory

- A: External traffic goes only to the main container.
- B: Memory use doesn't trigger image pulls.
- C: Correct. The plan doesn't scale the model server separately from the API.
- D: There's no separate tier. They share the instance's resources.

The plan doesn't scale the model server separately from the API.

📘 Source: [Choose the App Service sidecar pattern](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/2-choose-sidecar-pattern)

</details>

## 9. `lp1m3-009`

Which LinuxFxVersion value does a sidecar-enabled app use?

- **A.** DOCKER|`<image>`
- **B.** sidecar
- **C.** sitecontainers
- **D.** isMain

<details><summary>💡 Hint</summary>

A sidecar-enabled app has a special LinuxFxVersion value. It names the feature.

</details>

<details><summary>✅ Answer</summary>

**C.** sitecontainers

- A: That's the classic single-container value.
- B: That isn't the value App Service uses.
- C: Correct. Each container is then a Microsoft.Web/sites/sitecontainers resource.
- D: isMain is a property of a container, not a LinuxFxVersion value.

Each container is then a Microsoft.Web/sites/sitecontainers resource.

📘 Source: [Choose the App Service sidecar pattern](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/2-choose-sidecar-pattern)

</details>

## 10. `lp1m3-010`

You're choosing an App Service plan for a sidecar-enabled AI app. What should the capacity estimate be based on?

- **A.** Combined peak of all containers, plus startup overlap
- **B.** The sidecar's image size
- **C.** The main API's steady-state usage only
- **D.** The number of sidecars times a fixed per-container quota

<details><summary>💡 Hint</summary>

All the containers run at once on each instance, and a restart can briefly overlap old and new.

</details>

<details><summary>✅ Answer</summary>

**A.** Combined peak of all containers, plus startup overlap

- A: Correct. Include model-load memory, peak concurrency and overlap during deployment or scale-out.
- B: Image size affects pull time, not runtime CPU and memory.
- C: The model sidecar shares the same instance, and peaks matter.
- D: There's no fixed quota. You measure real usage.

Include model-load memory, peak concurrency and overlap during deployment or scale-out.

📘 Source: [Choose the App Service sidecar pattern](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/2-choose-sidecar-pattern)

</details>

## 11. `lp1m3-011`

You create the main API container for a sidecar-enabled app. On which port must the main process listen?

- **A.** Port 2222, so SSH and HTTP share it
- **B.** Port 11434, the model-server default
- **C.** Any port, as long as WEBSITES_PORT matches it
- **D.** Port 80 or 8080 for external HTTP traffic

<details><summary>💡 Hint</summary>

External HTTP traffic reaches the main container only on certain default ports.

</details>

<details><summary>✅ Answer</summary>

**D.** Port 80 or 8080 for external HTTP traffic

- A: 2222 is the App Service SSH port for custom containers.
- B: That's the sidecar port in the Learn example, not the main container's.
- C: WEBSITES_PORT doesn't configure sidecar-enabled containers.
- D: Correct. App Service supports only 80 or 8080 for external HTTP traffic to the main container.

Exactly one container is main, and its process must listen on port 80 or 8080.

📘 Source: [Configure main and sidecar containers](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/3-configure-sidecar-containers)

</details>

## 12. `lp1m3-012`

The main container's API listens on port 5000. After you create it with --is-main and --target-port 5000, external requests never reach it. What should you change?

- **A.** Mark the model-server container as main instead
- **B.** Remove the target port from the main container
- **C.** Add the app setting WEBSITES_PORT=5000
- **D.** Make the API process listen on port 8080 instead

<details><summary>💡 Hint</summary>

Target port is a setting, not the port the process uses. Which ports does App Service route external traffic to?

</details>

<details><summary>✅ Answer</summary>

**D.** Make the API process listen on port 8080 instead

- A: Only the API should take external traffic. Moving the main role doesn't fix the port.
- B: The target port is metadata, and the process still listens on an unsupported port.
- C: Classic WEBSITES_PORT doesn't configure sidecar-enabled containers.
- D: Correct. The main container must listen on 80 or 8080 for external HTTP.

The main container must listen on 80 or 8080 for external HTTP.

📘 Source: [Configure main and sidecar containers](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/3-configure-sidecar-containers)

</details>

## 13. `lp1m3-013`

Both the main API and the model server need MODEL_NAME. In the site container JSON, what goes in environmentVariables[].value?

- **A.** The name of an App Setting, such as MODEL_NAME_VALUE
- **B.** A Key Vault secret URI copied from the vault
- **C.** The client ID of the user-assigned identity
- **D.** The literal model name, such as support-model, typed into the JSON

<details><summary>💡 Hint</summary>

Values in the container JSON don't hold the secret itself. They point to something defined elsewhere on the app.

</details>

<details><summary>✅ Answer</summary>

**A.** The name of an App Setting, such as MODEL_NAME_VALUE

- A: Correct. The value identifies an App Setting by name; create that setting first.
- B: Learn's pattern maps App Settings, not raw secret URIs, into container variables.
- C: The client ID is used for image pull authentication.
- D: Site container variables reference App Settings by name rather than holding literal values.

In a site container resource, each environmentVariables[].value names an App Setting that holds the actual value.

📘 Source: [Configure main and sidecar containers](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/3-configure-sidecar-containers)

</details>

## 14. `lp1m3-014`

A sidecar pull with a user-assigned identity fails with `UNAUTHORIZED: token validation failed`. The identity has AcrPull and has had it for a day. What should you check next?

- **A.** Whether the registry accepts ARM audience tokens
- **B.** Whether WEBSITES_PORT is set to the sidecar's target port
- **C.** Whether the image tag is latest rather than an immutable tag
- **D.** Whether the sidecar container has isMain set to true

<details><summary>💡 Hint</summary>

The role is correct and old enough. Pull tokens can be refused because of what they were issued for.

</details>

<details><summary>✅ Answer</summary>

**A.** Whether the registry accepts ARM audience tokens

- A: Correct. Learn says this error can mean the registry doesn't accept ARM audience tokens (az acr config authentication-as-arm show).
- B: WEBSITES_PORT doesn't apply to sidecar-enabled apps and isn't related to pull auth.
- C: Tag choice affects reproducibility, not token validation.
- D: The role flag doesn't affect registry authentication.

Managed-identity pulls need the registry to accept ARM audience tokens. Propagation delay is ruled out because the role is a day old.

📘 Source: [Configure main and sidecar containers](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/3-configure-sidecar-containers)

</details>

## 15. `lp1m3-015`

For each statement, select Yes if the statement is true. Otherwise, select No. A registry uses **RBAC Registry + ABAC Repository Permissions**. You're configuring the model-server sidecar.

| Statement | Yes / No |
|---|---|
| Granting the identity Container Registry Repository Reader can give it pull access. | ☐ |
| Changing the targetPort metadata to 9000 makes the process inside the image listen on 9000. | ☐ |
| When you pass --sitecontainers-spec-file, other site container input arguments are ignored. | ☐ |
| Putting the registry password in the spec file is the recommended way to authenticate. | ☐ |

<details><summary>💡 Hint</summary>

ABAC mode uses repository-level roles. Target port is only metadata, and a spec file overrides other arguments.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Granting the identity Container Registry Repository Reader can give it pull access. | Yes | In the ABAC repository mode, Learn names Container Registry Repository Reader, optionally with a repository condition. |
| Changing the targetPort metadata to 9000 makes the process inside the image listen on 9000. | No | Target port is metadata; it doesn't reconfigure the process. |
| When you pass --sitecontainers-spec-file, other site container input arguments are ignored. | Yes | Learn says the command ignores other input arguments with a spec file. |
| Putting the registry password in the spec file is the recommended way to authenticate. | No | Don't place credentials in the spec file; use managed identity. |

Pick the pull role that matches the registry's permissions mode; target port is only metadata; keep credentials out of the spec.

📘 Source: [Configure main and sidecar containers](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/3-configure-sidecar-containers)

</details>

## 16. `lp1m3-016`

Your registry's role assignment permissions mode is RBAC Registry + ABAC Repository Permissions. Which role should the app's managed identity get so it can pull the sidecar image?

- **A.** AcrPull
- **B.** AcrPush
- **C.** Container Registry Repository Reader
- **D.** Contributor on the registry

<details><summary>💡 Hint</summary>

In ABAC mode, registry-wide roles don't grant repository permissions. Which role is about reading repositories?

</details>

<details><summary>✅ Answer</summary>

**C.** Container Registry Repository Reader

- A: AcrPull applies when the registry uses RBAC Registry Permissions.
- B: Push rights are more than the app needs, and the mode calls for a repository role.
- C: Correct. Use it for the ABAC repository mode, optionally with a repository condition.
- D: Far broader than the pull permission needed.

Use it for the ABAC repository mode, optionally with a repository condition.

📘 Source: [Configure main and sidecar containers](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/3-configure-sidecar-containers)

</details>

## 17. `lp1m3-017`

You change the model-server definition's --target-port from 11434 to 9000. The image is unchanged, and the API now calls localhost:9000 and gets connection refused. Why?

- **A.** Sidecars can't declare a target port
- **B.** The API must call model-server:9000 instead of localhost
- **C.** Target port is metadata; the process didn't change
- **D.** Ports above 8080 are blocked between containers

<details><summary>💡 Hint</summary>

Changing a setting in App Service doesn't change what the process inside the image does.

</details>

<details><summary>✅ Answer</summary>

**C.** Target port is metadata; the process didn't change

- A: A networked sidecar should declare its listener port as metadata.
- B: Containers reach each other through localhost, not container names.
- C: Correct. Changing the metadata doesn't reconfigure the process inside the image.
- D: Internal communication can use any available unique port.

Changing the metadata doesn't reconfigure the process inside the image.

📘 Source: [Configure main and sidecar containers](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/3-configure-sidecar-containers)

</details>

## 18. `lp1m3-018`

You're creating a new Linux web app that will host a main container and a sidecar. Which az webapp create option prepares it for site containers?

- **A.** --sitecontainers-app
- **B.** --multicontainer-config-type compose
- **C.** --is-main
- **D.** --container-image-name

<details><summary>💡 Hint</summary>

A new web app needs an option at creation time that says it will host site containers.

</details>

<details><summary>✅ Answer</summary>

**A.** --sitecontainers-app

- A: Correct. It configures the app to use site container resources.
- B: Docker Compose is the older multi-container model.
- C: --is-main belongs to az webapp sitecontainers create.
- D: This sets a classic single container image.

It configures the app to use site container resources.

📘 Source: [Configure main and sidecar containers](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/3-configure-sidecar-containers)

</details>

## 19. `lp1m3-019`

Both the main API and a telemetry sidecar are configured to listen on port 8080. What goes wrong?

- **A.** The second process can't bind 8080 on the shared network
- **B.** App Service splits external traffic across both containers
- **C.** Nothing, because each container has its own network
- **D.** The telemetry sidecar becomes the main container

<details><summary>💡 Hint</summary>

All the containers share one network namespace. What happens when two processes want the same port?

</details>

<details><summary>✅ Answer</summary>

**A.** The second process can't bind 8080 on the shared network

- A: Correct. Each listening process needs a unique port.
- B: External traffic goes only to the main container.
- C: All containers share one network namespace.
- D: isMain decides the role, not the port.

Each listening process needs a unique port.

📘 Source: [Configure main and sidecar containers](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/3-configure-sidecar-containers)

</details>

## 20. `lp1m3-020`

The main API must call the model-server sidecar, which listens on port 11434. Which URL should the API use?

- **A.** https://`<app-name>`.azurewebsites.net:11434
- **B.** http://model-server:11434
- **C.** http://`<app-name>`.scm.azurewebsites.net:11434
- **D.** http://localhost:11434

<details><summary>💡 Hint</summary>

The containers share a network. What host name reaches a process on the same instance?

</details>

<details><summary>✅ Answer</summary>

**D.** http://localhost:11434

- A: Sidecars aren't published on the public hostname.
- B: Containers don't reach each other by container name in App Service sidecars.
- C: The SCM site is the Kudu diagnostic site, not the sidecar.
- D: Correct. Containers share a network namespace and use localhost:`<port>`.

All containers share one network namespace, so each instance's main API calls its own sidecar on localhost.

📘 Source: [Connect containers and share files](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/4-connect-containers-share-files)

</details>

## 21. `lp1m3-021`

The main API calls a local model server that sometimes restarts while loading. Which two practices does Learn recommend for these calls? (Select two.)

- **A.** Retry every failed request until the model server answers
- **B.** Use a short connection timeout and an overall request deadline
- **C.** Retry only transient errors, and only for idempotent operations
- **D.** Expose a generic proxy so clients can call the sidecar directly

<details><summary>💡 Hint</summary>

Fail fast on connection, cap the total time, and retry only when trying again is safe.

</details>

<details><summary>✅ Answer</summary>

**B.** Use a short connection timeout and an overall request deadline  
**C.** Retry only transient errors, and only for idempotent operations

- A: Retrying everything can duplicate work and add pressure during a sidecar failure.
- B: Correct. A short connect timeout detects a missing listener; a deadline fits the client latency target.
- C: Correct. A small retry budget for transient errors on idempotent operations avoids duplicate work.
- D: Learn says to avoid a generic proxy; the main API stays the security boundary.

Treat the local call as a fallible dependency: timeouts, deadlines, cancellation, limited retries and clear error mapping.

📘 Source: [Connect containers and share files](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/4-connect-containers-share-files)

</details>

## 22. `lp1m3-022`

The model server writes /home/models/manifest.json, and the API sometimes reads a half-written file. What should the model server do?

- **A.** Add a volumeMounts entry for /home/models to both container definitions
- **B.** Write manifest.json.tmp first, then rename it to manifest.json
- **C.** Set WEBSITES_ENABLE_APP_SERVICE_STORAGE to false for the app
- **D.** Write the manifest to /tmp in its own container instead

<details><summary>💡 Hint</summary>

A reader can see a file while it's still being written. How do you make the file appear all at once?

</details>

<details><summary>✅ Answer</summary>

**B.** Write manifest.json.tmp first, then rename it to manifest.json

- A: Explicit mounts aren't needed and can stop the app or SCM site from starting.
- B: Correct. Writing to a temporary name and renaming prevents partial reads.
- C: That removes the shared /home mount the containers rely on.
- D: Another container can't read a file in the writer's own /tmp.

Learn's ownership protocol: write to a temporary name, then rename, or publish a manifest only when all artifacts are ready.

📘 Source: [Connect containers and share files](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/4-connect-containers-share-files)

</details>

## 23. `lp1m3-023`

For each statement, select Yes if the statement is true. Otherwise, select No. The API and model server exchange files through `/home/models`, with default settings.

| Statement | Yes / No |
|---|---|
| Both containers see the same /home volume without any volumeMounts entries. | ☐ |
| /home/models is a good place for the audit store of every model answer. | ☐ |
| Adding explicit volumeMounts can prevent the app or SCM endpoint from starting. | ☐ |
| Files that must outlive the app are best kept in /home rather than in Blob Storage. | ☐ |

<details><summary>💡 Hint</summary>

/home is shared by default. Think about what extra mounts can break and what belongs in durable storage.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Both containers see the same /home volume without any volumeMounts entries. | Yes | App Service mounts the same /home volume into the main container and every sidecar by default. |
| /home/models is a good place for the audit store of every model answer. | No | Learn says not to treat /home as an audit store or durable system of record. |
| Adding explicit volumeMounts can prevent the app or SCM endpoint from starting. | Yes | Explicit mounts change the file-system view and can conflict with the runtime. |
| Files that must outlive the app are best kept in /home rather than in Blob Storage. | No | Use Azure Blob Storage or Azure Files when data needs a durable storage boundary outside the web app. |

Use /home for recreatable, operational files; move durable artifacts to Azure Storage.

📘 Source: [Connect containers and share files](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/4-connect-containers-share-files)

</details>

## 24. `lp1m3-024`

A developer wants to add an endpoint to the main API that forwards any request straight to the model sidecar, for debugging. What does the guidance advise?

- **A.** Expose only narrow health or inference operations
- **B.** Add it, since the sidecar is only reachable on localhost anyway
- **C.** Mark the sidecar isMain: true while debugging
- **D.** Publish the sidecar's target port externally

<details><summary>💡 Hint</summary>

A generic pass-through endpoint widens what the model server exposes. What does the guidance prefer?

</details>

<details><summary>✅ Answer</summary>

**A.** Expose only narrow health or inference operations

- A: Correct. This keeps the main API as the external security boundary.
- B: A generic proxy would turn the main API into an open door to the sidecar.
- C: That would route external traffic away from the API.
- D: A sidecar target port isn't published as a public endpoint.

This keeps the main API as the external security boundary.

📘 Source: [Connect containers and share files](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/4-connect-containers-share-files)

</details>

## 25. `lp1m3-025`

After you add volumeMounts entries to both site container definitions, the app and its SCM endpoint stop starting. What should you do first?

- **A.** Add a third container to own the mount
- **B.** Set WEBSITES_ENABLE_APP_SERVICE_STORAGE=false
- **C.** Scale the plan up to a larger tier
- **D.** Remove volumeMounts and restore the working definitions

<details><summary>💡 Hint</summary>

The app worked before you changed the mounts. What's the quickest way back to a working state?

</details>

<details><summary>✅ Answer</summary>

**D.** Remove volumeMounts and restore the working definitions

- A: More containers don't fix a conflicting mount.
- B: That would remove the built-in shared /home mount.
- C: This is a configuration conflict, not a capacity problem.
- D: Correct. Explicit mounts can conflict with the runtime. /home already provides file exchange.

Explicit mounts can conflict with the runtime. /home already provides file exchange.

📘 Source: [Connect containers and share files](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/4-connect-containers-share-files)

</details>

## 26. `lp1m3-026`

The main API calls its model sidecar. Match each result to what it tells you.

Choices: **No process accepted on that port** · **Connection worked; check the request** · **Slow startup, pressure or long work**

- Connection refused
- HTTP 400 returned by the model server
- Request timed out

<details><summary>💡 Hint</summary>

Each error tells you how far the request got: no listener, a reply, or no reply in time.

</details>

<details><summary>✅ Answer</summary>

- Connection refused → **No process accepted on that port**. Refused means nothing was listening on the requested local port.
- HTTP 400 returned by the model server → **Connection worked; check the request**. An HTTP error means the network connection succeeded.
- Request timed out → **Slow startup, pressure or long work**. A timeout can mean slow startup, resource pressure, blocked work or a long request.

Separate the failure categories before changing ports, capacity or the request.

📘 Source: [Diagnose sidecar failures](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/5-diagnose-sidecar-failures)

</details>

## 27. `lp1m3-027`

A health call from the API to the sidecar returns HTTP 400. What does this tell you?

- **A.** No process is listening on the sidecar port
- **B.** The request ran past the timeout budget
- **C.** The connection worked; check the request
- **D.** The registry rejected the image pull

<details><summary>💡 Hint</summary>

A 400 is an HTTP response. What does getting any HTTP response prove?

</details>

<details><summary>✅ Answer</summary>

**C.** The connection worked; check the request

- A: That would be a connection refusal, not an HTTP response.
- B: A timeout raises a timeout error, not a 400 status.
- C: Correct. An HTTP error status means the network connection succeeded.
- D: A running sidecar that answers has already pulled its image.

An HTTP error status means the network connection succeeded.

📘 Source: [Diagnose sidecar failures](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/5-diagnose-sidecar-failures)

</details>

## 28. `lp1m3-028`

Users get errors from the API. You suspect the model-server sidecar never received the new image tag in the last release. Which command checks this first?

- **A.** az acr task logs to read the output of the last build
- **B.** az webapp sitecontainers show for model-server
- **C.** az webapp config appsettings list for the app settings
- **D.** az webapp log tail to stream output for the whole app

<details><summary>💡 Hint</summary>

Before reading logs, confirm App Service actually has the configuration you think you released.

</details>

<details><summary>✅ Answer</summary>

**B.** az webapp sitecontainers show for model-server

- A: Build logs show the image was built, not what the app is configured to run.
- B: Correct. show returns the deployed definition, including its image, so you can compare it with the release.
- C: App settings don't hold the site container image.
- D: The app log stream mixes containers and can't show a setting that never reached the resource.

Inspect configuration first: a runtime log can't show a setting that never reached the resource.

📘 Source: [Diagnose sidecar failures](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/5-diagnose-sidecar-failures)

</details>

## 29. `lp1m3-029`

Users report errors from a sidecar-enabled app. Following the symptom-first workflow, what do you confirm first?

- **A.** That the API can reach localhost
- **B.** That the definitions reached App Service
- **C.** That the plan has enough CPU and memory
- **D.** That the model returns sensible answers

<details><summary>💡 Hint</summary>

Symptom-first: rule out the simplest explanation, which is that the configuration didn't arrive.

</details>

<details><summary>✅ Answer</summary>

**B.** That the definitions reached App Service

- A: Connectivity comes after confirming the configuration, pull and process state.
- B: Correct. Use list and show to spot a missing sidecar, a wrong tag or two main containers.
- C: Resource pressure comes later in the sequence.
- D: App-layer validation is the last step.

Use list and show to spot a missing sidecar, a wrong tag or two main containers.

📘 Source: [Diagnose sidecar failures](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/5-diagnose-sidecar-failures)

</details>

## 30. `lp1m3-030`

The sidecar restarts every few minutes while loading the model. Its log shows no stack trace or exit error, and memory spikes at each start. What does Learn suggest?

- **A.** Scale the app out to more instances so that each instance carries less load
- **B.** Add a volumeMounts entry for the model files to fix permissions
- **C.** Switch the image pull to registry admin credentials, then redeploy
- **D.** Measure memory, then reduce load, use a smaller model or scale the plan

<details><summary>💡 Hint</summary>

No crash message, but memory spikes at startup. Learn's advice starts with checking numbers before changing anything.

</details>

<details><summary>✅ Answer</summary>

**D.** Measure memory, then reduce load, use a smaller model or scale the plan

- A: Each new instance adds another model server, so per-instance memory pressure stays the same.
- B: Explicit mounts aren't needed here and can cause new failures.
- C: Image auth doesn't cause restarts after a successful pull.
- D: Correct. Repeated starts without an app error can indicate memory pressure during model loading.

Align memory metrics with sidecar logs. If demand exceeds safe capacity, reduce concurrency, use a smaller model, scale the plan or host inference separately.

📘 Source: [Diagnose sidecar failures](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/5-diagnose-sidecar-failures)

</details>

## 31. `lp1m3-031`

For each statement, select Yes if the statement is true. Otherwise, select No. The model-server image pull fails for an ACR registry that sits behind a private endpoint, using VNet integration.

| Statement | Yes / No |
|---|---|
| The Pull image over VNet option should be enabled for this setup. | ☐ |
| Because the pull failed, the sidecar's application logs will show the cause. | ☐ |
| If you granted the pull role five minutes ago, waiting and retrying is reasonable. | ☐ |
| Scaling the App Service plan up is a good fix for a pull failure. | ☐ |

<details><summary>💡 Hint</summary>

A private endpoint needs pulls to go through the VNet. Pull failures happen before the app writes any logs.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The Pull image over VNet option should be enabled for this setup. | Yes | Enable Pull image over VNet when the image must be pulled through VNet integration. |
| Because the pull failed, the sidecar's application logs will show the cause. | No | Pull failures happen before the process starts, so look at pull and container logs, not app output. |
| If you granted the pull role five minutes ago, waiting and retrying is reasonable. | Yes | Role assignments take time to propagate; retry before replacing correct identity settings. |
| Scaling the App Service plan up is a good fix for a pull failure. | No | Don't use scaling to hide a configuration problem. |

For pull failures check image reference, identity and role, ARM tokens, and network path (firewall or private endpoint, DNS, VNet integration, Pull image over VNet).

📘 Source: [Diagnose sidecar failures](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/5-diagnose-sidecar-failures)

</details>

## 32. `lp1m3-032`

You granted the web app's managed identity AcrPull two minutes ago, and the sidecar pull still fails. The identity settings in the container definition are correct. What should you do?

- **A.** Switch the container to stored registry credentials
- **B.** Delete the identity and create a new one
- **C.** Wait for the role to propagate, then retry
- **D.** Mark the sidecar as the main container

<details><summary>💡 Hint</summary>

Role assignments take a little time to apply. The configuration is already correct.

</details>

<details><summary>✅ Answer</summary>

**C.** Wait for the role to propagate, then retry

- A: The guidance says not to replace correct identity settings with stored credentials.
- B: A new identity would need the same role and the same propagation time.
- C: Correct. Role assignments can take time to propagate.
- D: The role doesn't affect image pulls.

Role assignments can take time to propagate.

📘 Source: [Diagnose sidecar failures](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/5-diagnose-sidecar-failures)

</details>

## 33. `lp1m3-033`

ACR is reachable only through a private endpoint, and the web app uses virtual network integration. Sidecar image pulls fail even though DNS and the identity's pull role are correct. Which App Service option should you check?

- **A.** Pull image over VNet
- **B.** WEBSITES_ENABLE_APP_SERVICE_STORAGE
- **C.** Always On
- **D.** The target port of the main container

<details><summary>💡 Hint</summary>

The registry is only reachable privately. One App Service option changes the route that image pulls take.

</details>

<details><summary>✅ Answer</summary>

**A.** Pull image over VNet

- A: Correct. It must be enabled when the image is pulled through VNet integration.
- B: That controls /home storage.
- C: Always On keeps the app warm. It doesn't affect the pull path.
- D: Ports don't affect image pulls.

It must be enabled when the image is pulled through VNet integration.

📘 Source: [Diagnose sidecar failures](https://learn.microsoft.com/en-us/training/modules/deploy-sidecar-azure-app-service/5-diagnose-sidecar-failures)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
