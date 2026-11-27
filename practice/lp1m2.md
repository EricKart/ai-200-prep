# Practice: LP1 · M2 Deploy containers to Azure App Service

> 36 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp1m2.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-1/deploy-containers-azure-app-service)

## 1. `lp1m2-001`

Your web app pulls from ACR using its system-assigned managed identity, and the first deployment fails with an authorization error. Which role does the identity need on the registry?

- **A.** AcrPull
- **B.** AcrPush
- **C.** Reader
- **D.** Owner

<details><summary>💡 Hint</summary>

Pulling images from ACR is a read-only job. Which built-in ACR role allows only pulls?

</details>

<details><summary>✅ Answer</summary>

**A.** AcrPull

- A: Correct. The identity must have the AcrPull role on the registry.
- B: AcrPush is for pushing images; the web app only needs to pull.
- C: Reader isn't the role Learn names for pulling images.
- D: Owner grants far more than pulling an image needs.

With managed identity authentication, the identity must have the AcrPull role on the registry.

📘 Source: [Deploy containers to Azure App Service](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/2-deploy-containers)

</details>

## 2. `lp1m2-002`

Which statement describes a user-assigned managed identity?

- **A.** Azure deletes it automatically when you delete the web app
- **B.** It stores the registry admin username and password in app settings
- **C.** It's a separate resource you can assign to several web apps
- **D.** It can be enabled once the web app already exists, not before

<details><summary>💡 Hint</summary>

System-assigned identities live and die with one resource. What's different about the other kind?

</details>

<details><summary>✅ Answer</summary>

**C.** It's a separate resource you can assign to several web apps

- A: That's the system-assigned identity, tied to the app's lifecycle.
- B: That's admin credentials authentication, not an identity.
- C: Correct. User-assigned identities exist independently and can be shared by several apps.
- D: You can create a user-assigned identity and grant permissions before the app exists.

User-assigned identities exist independently, so several apps can share registry access and permissions can be set up first.

📘 Source: [Deploy containers to Azure App Service](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/2-deploy-containers)

</details>

## 3. `lp1m2-003`

Three web apps must pull images from the same ACR without stored credentials. The security team wants to grant registry access before any of the apps is created. Which authentication should the apps use?

- **A.** The registry's admin credentials stored in app settings
- **B.** A user-assigned managed identity with the AcrPull role
- **C.** A Docker Hub username and password for each app
- **D.** A system-assigned managed identity on each app

<details><summary>💡 Hint</summary>

Access must exist before the apps do, and three apps share it. Which identity type is its own resource?

</details>

<details><summary>✅ Answer</summary>

**B.** A user-assigned managed identity with the AcrPull role

- A: This stores credentials in App Service config and needs manual rotation, the opposite of the requirement.
- B: Correct. It exists independently, can be shared by several apps, and can get permissions in advance.
- C: These are credentials for other registries. They also store secrets, which the requirement rules out.
- D: A system-assigned identity is created with the app, so it can't be granted access before the app exists.

It exists independently, can be shared by several apps, and can get permissions in advance.

📘 Source: [Deploy containers to Azure App Service](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/2-deploy-containers)

</details>

## 4. `lp1m2-004`

You push a fixed image to `docprocessor:latest`, the tag the web app already uses. An hour later the app still runs the old code. What is the cause?

- **A.** App Service doesn't detect a new image pushed to the same tag by itself
- **B.** The AcrPull role has to be granted again after each push to the registry
- **C.** Images tagged latest can't be pulled by App Service on Linux at all
- **D.** App Service caches the image for 24 hours before checking the registry again

<details><summary>💡 Hint</summary>

Pushing to the same tag doesn't notify anyone. What makes App Service pull an image again?

</details>

<details><summary>✅ Answer</summary>

**A.** App Service doesn't detect a new image pushed to the same tag by itself

- A: Correct. Restart the app or enable continuous deployment so a webhook triggers the restart.
- B: Role assignments don't expire per push.
- C: latest can be pulled; Learn uses nginx:latest as an example.
- D: Learn doesn't describe a 24-hour cache; App Service pulls on restart.

Pushing to the same tag isn't detected. App Service runs docker pull on restart and pulls only changed layers.

📘 Source: [Deploy containers to Azure App Service](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/2-deploy-containers)

</details>

## 5. `lp1m2-005`

You want every push to ACR to redeploy the web app automatically. Put the steps in order.

- Copy the webhook URL that the command returns
- Create a webhook in the ACR registry that triggers on push events
- Push a new image to the registry so the webhook restarts the app
- Run az webapp deployment container config --enable-cd true

<details><summary>💡 Hint</summary>

The webhook needs a URL to call, and that URL appears only after continuous deployment is turned on.

</details>

<details><summary>✅ Answer</summary>

1. Run az webapp deployment container config --enable-cd true
2. Copy the webhook URL that the command returns
3. Create a webhook in the ACR registry that triggers on push events
4. Push a new image to the registry so the webhook restarts the app

Enabling continuous deployment returns a webhook URL. Add it to the registry as a push-event webhook; later pushes trigger the restart.

📘 Source: [Deploy containers to Azure App Service](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/2-deploy-containers)

</details>

## 6. `lp1m2-006`

You ran the command below for your document processor. What else is needed so that pushes to ACR redeploy the app automatically?

```text
az webapp deployment container config \
  --resource-group myResourceGroup \
  --name myDocumentProcessor --enable-cd true
```

- **A.** Add an ACR webhook that calls the returned URL
- **B.** Turn on Always On so the app polls the registry
- **C.** Set WEBSITES_ENABLE_APP_SERVICE_STORAGE to true
- **D.** Enable the admin user on the registry

<details><summary>💡 Hint</summary>

Turning on continuous deployment gives you a URL. Something must call that URL when an image is pushed.

</details>

<details><summary>✅ Answer</summary>

**A.** Add an ACR webhook that calls the returned URL

- A: Correct. The command returns a webhook URL, and the registry must call it when images are pushed.
- B: Always On keeps the app warm. It doesn't watch the registry.
- C: That controls /home persistence, not deployments.
- D: The admin user is an authentication option. It has nothing to do with triggering redeploys.

The command returns a webhook URL, and the registry must call it when images are pushed.

📘 Source: [Deploy containers to Azure App Service](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/2-deploy-containers)

</details>

## 7. `lp1m2-007`

For each statement, select Yes if the statement is true. Otherwise, select No. A web app runs `myregistry.azurecr.io/docprocessor:v1` on three instances.

| Statement | Yes / No |
|---|---|
| Running az webapp config container set with :v2 swaps the image without restarting the app. | ☐ |
| After a plain restart with an unchanged image, App Service downloads every layer again. | ☐ |
| When the app scales out to a fourth instance, that instance pulls the image. | ☐ |
| Moving the app to a different pricing tier can cause a fresh image pull. | ☐ |

<details><summary>💡 Hint</summary>

App Service reuses cached layers when it can. Think about restarts, new instances and tier changes separately.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Running az webapp config container set with :v2 swaps the image without restarting the app. | No | Changing the image tag restarts the app, and each instance pulls the new image. |
| After a plain restart with an unchanged image, App Service downloads every layer again. | No | On restart it checks for changes and pulls only modified layers. |
| When the app scales out to a fourth instance, that instance pulls the image. | Yes | Each new instance pulls the image on scale out. |
| Moving the app to a different pricing tier can cause a fresh image pull. | Yes | A tier change might allocate new infrastructure, which pulls the image fresh. |

Full pull on first deploy or image change; only changed layers on restart; new instances and tier changes can pull fresh.

📘 Source: [Deploy containers to Azure App Service](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/2-deploy-containers)

</details>

## 8. `lp1m2-008`

Your image is private on GitHub Container Registry. When you create the web app with az webapp create, what do you pass as --docker-registry-server-url?

- **A.** `https://index.docker.io/v1/`
- **B.** `https://ghcr.io`
- **C.** `https://myregistry.azurecr.io`
- **D.** `https://github.com`

<details><summary>💡 Hint</summary>

The registry server URL is the registry's own address, including the scheme.

</details>

<details><summary>✅ Answer</summary>

**B.** `https://ghcr.io`

- A: That's Docker Hub's server URL.
- B: Correct. This is the server URL for GitHub Container Registry.
- C: That's an ACR login server, not GitHub's.
- D: That's the website, not the container registry endpoint.

This is the server URL for GitHub Container Registry.

📘 Source: [Deploy containers to Azure App Service](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/2-deploy-containers)

</details>

## 9. `lp1m2-009`

A web app pulls from ACR with its system-assigned managed identity. The app is deleted. What happens to that identity?

- **A.** Azure deletes it together with the web app
- **B.** It remains, ready to assign to another app
- **C.** It keeps AcrPull but loses all other roles
- **D.** It turns into a user-assigned identity

<details><summary>💡 Hint</summary>

A system-assigned identity is tied to the lifecycle of one resource.

</details>

<details><summary>✅ Answer</summary>

**A.** Azure deletes it together with the web app

- A: Correct. A system-assigned identity is tied to the app's lifecycle.
- B: That describes a user-assigned identity.
- C: The identity itself is removed, so it holds no roles.
- D: Identities don't change type.

A system-assigned identity is tied to the app's lifecycle.

📘 Source: [Deploy containers to Azure App Service](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/2-deploy-containers)

</details>

## 10. `lp1m2-010`

With the image source set to Other container registries, what must the registry support?

- **A.** Geo-replication across Azure regions
- **B.** HTTPS and the Docker Registry HTTP API V2
- **C.** Microsoft Entra ID authentication for every pull
- **D.** Storage of Helm charts alongside images

<details><summary>💡 Hint</summary>

App Service speaks a standard registry protocol over a secure connection.

</details>

<details><summary>✅ Answer</summary>

**B.** HTTPS and the Docker Registry HTTP API V2

- A: Geo-replication isn't required to serve images to App Service.
- B: Correct. Any registry that meets both works, such as Docker Hub or GHCR.
- C: Entra ID integration is an ACR benefit, not a requirement for other registries.
- D: Helm support has nothing to do with App Service image pulls.

Any registry that meets both works, such as Docker Hub or GHCR.

📘 Source: [Deploy containers to Azure App Service](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/2-deploy-containers)

</details>

## 11. `lp1m2-011`

A Python container runs Gunicorn on port 8000, and App Service returns errors because traffic goes to the wrong port. Which app setting fixes this?

- **A.** WEBSITES_PORT=8000
- **B.** EXPOSE=8000
- **C.** ASPNETCORE_URLS=8000
- **D.** PORT_FORWARD=8000

<details><summary>💡 Hint</summary>

App Service has to know which port the container listens on when it isn't 80 or 8080. Which setting tells it?

</details>

<details><summary>✅ Answer</summary>

**A.** WEBSITES_PORT=8000

- A: Correct. WEBSITES_PORT tells App Service which container port receives HTTP requests.
- B: EXPOSE is a Dockerfile instruction, not an app setting App Service reads for routing.
- C: That setting configures ASP.NET Core, not App Service routing.
- D: PORT_FORWARD isn't an App Service setting.

App Service routes automatically to 80 or 8080. For any other port, set WEBSITES_PORT.

📘 Source: [Configure container runtime behavior](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/3-configure-runtime)

</details>

## 12. `lp1m2-012`

A document processor writes output files, and they disappear whenever the app restarts. The app runs on three instances that must see the same files. What should you do?

- **A.** Write the files to /tmp, which App Service keeps between restarts
- **B.** Set WEBSITES_ENABLE_APP_SERVICE_STORAGE=true and write output under /home
- **C.** Enable always-on so the container stays loaded and keeps the files
- **D.** Add a startup command that copies files back from the image on each start

<details><summary>💡 Hint</summary>

Container file systems are temporary, and the files must be shared by three instances. Which path can be persistent?

</details>

<details><summary>✅ Answer</summary>

**B.** Set WEBSITES_ENABLE_APP_SERVICE_STORAGE=true and write output under /home

- A: /tmp is part of the ephemeral container file system.
- B: Correct. /home then persists across restarts and is shared by all instances.
- C: Always-on prevents idling; restarts and moves still lose ephemeral files.
- D: Copying from the image restores only what was baked in, not new output.

Container writes are ephemeral. With app service storage enabled, /home persists and is shared across instances.

📘 Source: [Configure container runtime behavior](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/3-configure-runtime)

</details>

## 13. `lp1m2-013`

A Linux custom container app runs on three instances with WEBSITES_ENABLE_APP_SERVICE_STORAGE=true. For each statement, select Yes if it's true. Otherwise, select No.

| Statement | Yes / No |
|---|---|
| Files written to /home/output survive an app restart. | ☐ |
| Each instance has its own separate copy of /home. | ☐ |
| Files written to /tmp also survive an app restart. | ☐ |

<details><summary>💡 Hint</summary>

Only one path is backed by persistent shared storage. Is it per instance or shared?

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Files written to /home/output survive an app restart. | Yes | With the setting enabled, /home persists across restarts. |
| Each instance has its own separate copy of /home. | No | All instances of a scaled-out app share the same /home content. |
| Files written to /tmp also survive an app restart. | No | Writes outside /home stay ephemeral and are lost on restart. |

With WEBSITES_ENABLE_APP_SERVICE_STORAGE=true, /home is persistent storage shared by all instances and kept across restarts. Other paths, such as /tmp, are lost on restart.

📘 Source: [Configure container runtime behavior](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/3-configure-runtime)

</details>

## 14. `lp1m2-014`

For each statement, select Yes if the statement is true. Otherwise, select No. You run `az webapp config set --startup-file "gunicorn --bind=0.0.0.0:8000 app:application"` on a custom container.

| Statement | Yes / No |
|---|---|
| The startup command replaces the CMD instruction from the Dockerfile. | ☐ |
| The startup command also replaces the ENTRYPOINT from the Dockerfile. | ☐ |
| To run migrations first, you can use "/bin/bash -c 'python migrate.py && gunicorn app:application'". | ☐ |

<details><summary>💡 Hint</summary>

A startup command replaces one Dockerfile instruction and leaves the other alone. Shell operators need a shell.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The startup command replaces the CMD instruction from the Dockerfile. | Yes | The startup command replaces CMD. |
| The startup command also replaces the ENTRYPOINT from the Dockerfile. | No | ENTRYPOINT remains unchanged unless you change the container configuration directly. |
| To run migrations first, you can use "/bin/bash -c 'python migrate.py && gunicorn app:application'". | Yes | Learn shows the shell prefix for commands that need shell processing. |

Startup commands override CMD but keep ENTRYPOINT; wrap in /bin/bash -c when you need shell features.

📘 Source: [Configure container runtime behavior](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/3-configure-runtime)

</details>

## 15. `lp1m2-015`

A production inference API on the Basic tier has slow first requests after quiet periods, and one instance sometimes hangs while still receiving traffic. Which two settings address these problems? (Select two.)

- **A.** Set WEBSITES_ENABLE_APP_SERVICE_STORAGE to false
- **B.** Enable always-on for the web app
- **C.** Set WEBSITES_PORT to 80 for every container
- **D.** Set a health check path such as /health

<details><summary>💡 Hint</summary>

One symptom comes from idling, the other from a sick instance that still gets traffic. One setting for each.

</details>

<details><summary>✅ Answer</summary>

**B.** Enable always-on for the web app  
**D.** Set a health check path such as /health

- A: Persistent storage is about files, not cold starts or unhealthy instances.
- B: Correct. Always-on keeps the app warm, removing cold starts after idle periods (Basic tier or higher).
- C: The port setting must match the app; it doesn't fix idling or hung instances.
- D: Correct. Health checks take an instance that keeps failing out of load balancer rotation.

Always-on prevents idle cold starts. Health checks ping every minute and remove instances that keep failing (default 10 failures).

📘 Source: [Configure container runtime behavior](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/3-configure-runtime)

</details>

## 16. `lp1m2-016`

Users complain that the first request after a quiet period takes a long time. You try to enable Always On, but the app's plan is on the Free tier. What do you need to do?

- **A.** Enable persistent storage at /home
- **B.** Configure a health check path for the app first
- **C.** Set WEBSITES_PORT to 80
- **D.** Scale the plan up to Basic or higher

<details><summary>💡 Hint</summary>

Always On isn't available on every tier. Which tiers include it?

</details>

<details><summary>✅ Answer</summary>

**D.** Scale the plan up to Basic or higher

- A: Storage persistence is unrelated to Always On.
- B: Health checks remove unhealthy instances. They don't unlock Always On.
- C: The port setting affects routing, not idle behavior.
- D: Correct. Always On requires the Basic pricing tier or higher.

Always On requires the Basic pricing tier or higher.

📘 Source: [Configure container runtime behavior](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/3-configure-runtime)

</details>

## 17. `lp1m2-017`

A health check path of /health is configured. One instance starts returning 503 on every ping. With default settings, what does App Service do?

- **A.** Restarts every instance after the first failed ping
- **B.** Stops routing to it after repeated failed pings
- **C.** Switches the app to a different pricing tier
- **D.** Keeps routing traffic to it but raises an alert

<details><summary>💡 Hint</summary>

A health check exists to take bad instances out of rotation. What does it do after repeated failures?

</details>

<details><summary>✅ Answer</summary>

**B.** Stops routing to it after repeated failed pings

- A: One failure doesn't trigger action, and healthy instances aren't touched.
- B: Correct. By default, after 10 failed pings the instance leaves rotation, and it can be replaced if it stays unhealthy.
- C: Health checks don't change pricing tiers.
- D: The purpose of the health check is to stop routing to unhealthy instances.

By default, after 10 failed pings the instance leaves rotation, and it can be replaced if it stays unhealthy.

📘 Source: [Configure container runtime behavior](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/3-configure-runtime)

</details>

## 18. `lp1m2-018`

An inference API's /health endpoint returns 200 whenever the web server process is running. Last night the API couldn't reach its blob storage for an hour, yet health checks stayed green and traffic kept going to the broken instances. How should you change /health?

- **A.** Point the health check path at the home page instead of the /health endpoint
- **B.** Turn on Always On so that App Service recycles a stuck instance more often
- **C.** Make /health return its 200 response faster so the platform's ping doesn't time out
- **D.** Check the API's dependencies and return 503 if one fails

<details><summary>💡 Hint</summary>

The process was alive, but the API couldn't do its job. What should a health check test, and what should it return on failure?

</details>

<details><summary>✅ Answer</summary>

**D.** Check the API's dependencies and return 503 if one fails

- A: The home page may not touch blob storage either, so it would still report healthy.
- B: Always On keeps the app loaded. It doesn't restart instances or check dependencies.
- C: A faster 200 still says the instance is healthy when it can't serve real requests.
- D: Correct. A health check that verifies dependencies and returns an error status lets App Service take instances that can't serve requests out of rotation.

For more useful health checks, verify dependencies and return an error status code such as 503 when one fails. App Service then removes instances that keep failing (after 10 failed pings by default) from the load balancer rotation.

📘 Source: [Configure container runtime behavior](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/3-configure-runtime)

</details>

## 19. `lp1m2-019`

An ASP.NET Core container listens on port 80. What port configuration does App Service need?

- **A.** WEBSITES_PORT=80
- **B.** No port setting is needed
- **C.** A second exposed port for HTTPS
- **D.** WEBSITES_PORT=8080

<details><summary>💡 Hint</summary>

App Service checks some ports by default. Is 80 one of them?

</details>

<details><summary>✅ Answer</summary>

**B.** No port setting is needed

- A: Not needed. App Service already routes to port 80 automatically, and the guidance says no change is needed for ASP.NET Core.
- B: Correct. App Service routes automatically when the container listens on 80 or 8080.
- C: App Service ends TLS and supports only one HTTP port for a custom container.
- D: That would point traffic away from the port the app listens on.

App Service routes automatically when the container listens on 80 or 8080.

📘 Source: [Configure container runtime behavior](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/3-configure-runtime)

</details>

## 20. `lp1m2-020`

For each statement about App Service custom containers, select Yes if it's true. Otherwise, select No.

| Statement | Yes / No |
|---|---|
| A custom container can expose several ports for HTTP requests. | ☐ |
| The container receives plain HTTP even when clients connect over HTTPS. | ☐ |
| App Service pings the health check path every minute. | ☐ |

<details><summary>💡 Hint</summary>

Think about how many ports can take HTTP traffic, where TLS ends, and how often the health check pings.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| A custom container can expose several ports for HTTP requests. | No | App Service supports exposing only one port for HTTP requests to a custom container. |
| The container receives plain HTTP even when clients connect over HTTPS. | Yes | TLS ends at the platform before traffic reaches the container. |
| App Service pings the health check path every minute. | Yes | That's the documented ping interval. |

A custom container exposes one port for HTTP. TLS ends at the App Service front end, so the container receives plain HTTP. The health check path is pinged every minute.

📘 Source: [Configure container runtime behavior](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/3-configure-runtime)

</details>

## 21. `lp1m2-021`

An internal document-classification API on App Service gets a few requests each morning and is quiet the rest of the day. Users say the first request after a quiet spell is slow. What is happening?

- **A.** The TLS certificate is renewed by the front end on the first request of the day
- **B.** The app idles after about 20 minutes, so the next request cold-starts it
- **C.** The health check marked the only instance unhealthy, and requests wait for a replacement
- **D.** App Service pulls the full image again from the registry before each request

<details><summary>💡 Hint</summary>

The delay only happens after periods with no traffic. What does App Service do with an app nobody is using?

</details>

<details><summary>✅ Answer</summary>

**B.** The app idles after about 20 minutes, so the next request cold-starts it

- A: Certificates don't renew per request. The slowness comes from the app idling and starting again.
- B: Correct. App Service apps can become idle after about 20 minutes of inactivity, and the next request has to start the app again.
- C: An unhealthy instance shows up as failed or rerouted requests, not as a slow first request after quiet periods.
- D: Restarts reuse cached layers. App Service doesn't pull the image again for every request.

App Service apps can become idle after about 20 minutes of inactivity. The next request triggers a cold start. Always On (Basic tier and above) keeps the app loaded.

📘 Source: [Configure container runtime behavior](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/3-configure-runtime)

</details>

## 22. `lp1m2-022`

You add a connection string named DefaultConnection with type SQLAzure. Which environment variable does the container see?

- **A.** APPSETTING_SQLAzure_DefaultConnection
- **B.** DefaultConnection
- **C.** SQLAZURECONNSTR_DefaultConnection
- **D.** CUSTOMCONNSTR_DefaultConnection

<details><summary>💡 Hint</summary>

Connection strings get a prefix that depends on their type. Which prefix goes with SQLAzure?

</details>

<details><summary>✅ Answer</summary>

**C.** SQLAZURECONNSTR_DefaultConnection

- A: That isn't the format App Service uses.
- B: Connection strings always get a type prefix.
- C: Correct. SQL Azure connection strings get the SQLAZURECONNSTR_ prefix.
- D: CUSTOMCONNSTR_ is the prefix for the Custom type.

Connection strings are injected with a type prefix such as SQLAZURECONNSTR_, MYSQLCONNSTR_ or POSTGRESQLCONNSTR_.

📘 Source: [Configure application settings](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/4-configure-settings)

</details>

## 23. `lp1m2-023`

A .NET app on a Linux container reads the key ConnectionStrings:DefaultConnection. What name should the app setting use?

- **A.** `CONNECTIONSTRINGS_DEFAULTCONNECTION`
- **B.** `ConnectionStrings:DefaultConnection`
- **C.** `ConnectionStrings__DefaultConnection`
- **D.** `ConnectionStrings.DefaultConnection`

<details><summary>💡 Hint</summary>

Linux environment variable names can't contain a colon. What do .NET apps use as the separator instead?

</details>

<details><summary>✅ Answer</summary>

**C.** `ConnectionStrings__DefaultConnection`

- A: A single underscore doesn't express nesting.
- B: Setting names can contain only letters, numbers and underscores, so a colon isn't allowed.
- C: Correct. On Linux containers, nested .NET keys use double underscores.
- D: A dot isn't allowed in setting names.

For Linux containers, replace the colon in nested .NET keys with a double underscore.

📘 Source: [Configure application settings](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/4-configure-settings)

</details>

## 24. `lp1m2-024`

A Python service on App Service needs a PostgreSQL connection string. Which approach does the guidance recommend for a non-.NET app?

- **A.** Add the value as an ordinary app setting
- **B.** Bake the value into the image at build time
- **C.** Add a connection string of type Custom
- **D.** Add a connection string of type PostgreSQL

<details><summary>💡 Hint</summary>

Connection strings mostly exist for .NET. What does the guidance suggest for other languages?

</details>

<details><summary>✅ Answer</summary>

**A.** Add the value as an ordinary app setting

- A: Correct. For Python and Node.js, app settings are simpler, and the type prefix adds no benefit.
- B: This defeats the purpose of per-environment settings and forces rebuilds.
- C: A Custom type still adds the CUSTOMCONNSTR_ prefix with no benefit.
- D: It works, but it creates a POSTGRESQLCONNSTR_ variable whose prefix adds complexity for non-.NET apps.

For Python and Node.js, app settings are simpler, and the type prefix adds no benefit.

📘 Source: [Configure application settings](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/4-configure-settings)

</details>

## 25. `lp1m2-025`

Staging has ENVIRONMENT=staging and an API endpoint for the test backend. After a swap, production must keep its own values. What should you do in the staging slot?

- **A.** Move both values into the Dockerfile as ENV instructions
- **B.** Store both values as connection strings of type Custom
- **C.** Add both values with --slot-settings so they stay with the slot
- **D.** Export the settings to JSON and import them again after the swap

<details><summary>💡 Hint</summary>

Some values must stay with their slot during a swap. What marks a setting as sticky?

</details>

<details><summary>✅ Answer</summary>

**C.** Add both values with --slot-settings so they stay with the slot

- A: Baking values into the image means they'd swap with the image.
- B: Connection string type doesn't decide whether a value swaps.
- C: Correct. Slot settings remain with the slot during swap operations.
- D: Re-importing after each swap is a manual fix, not the feature for this.

Mark environment identifiers and environment-specific endpoints as slot settings so they don't move during a swap.

📘 Source: [Configure application settings](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/4-configure-settings)

</details>

## 26. `lp1m2-026`

In the staging slot, ENVIRONMENT=staging is marked as a slot setting and LOG_LEVEL=DEBUG isn't. You swap staging into production. For each statement, select Yes if it's true. Otherwise, select No.

| Statement | Yes / No |
|---|---|
| After the swap, the production slot still has ENVIRONMENT=production. | ☐ |
| After the swap, the production slot has LOG_LEVEL=DEBUG. | ☐ |
| The staging slot runs on separate compute outside the production App Service plan. | ☐ |

<details><summary>💡 Hint</summary>

Sticky settings stay with their slot. Settings that aren't sticky move with the swap. Slots share the plan.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| After the swap, the production slot still has ENVIRONMENT=production. | Yes | Slot settings stay with their slot during a swap. |
| After the swap, the production slot has LOG_LEVEL=DEBUG. | Yes | Settings that aren't slot settings move with the swapped app. |
| The staging slot runs on separate compute outside the production App Service plan. | No | Slots share the underlying compute of the same App Service plan. |

Slot settings stay with their slot during a swap, and other settings move with the app. Every slot runs on the same App Service plan as production.

📘 Source: [Configure application settings](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/4-configure-settings)

</details>

## 27. `lp1m2-027`

For each statement, select Yes if the statement is true. Otherwise, select No. An app setting is `API_KEY=@Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/api-key)`, with no version in the URI.

| Statement | Yes / No |
|---|---|
| The web app needs a managed identity that can read secrets from the vault. | ☐ |
| The application code must call the Key Vault SDK to read API_KEY. | ☐ |
| After the secret is rotated, App Service picks up the new version within 24 hours. | ☐ |
| The setting must include the secret version, or the reference fails. | ☐ |

<details><summary>💡 Hint</summary>

A Key Vault reference needs access to the vault, and a reference with no version tracks the latest secret.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The web app needs a managed identity that can read secrets from the vault. | Yes | Key Vault references require a managed identity with access to read secrets. |
| The application code must call the Key Vault SDK to read API_KEY. | No | App Service resolves the reference; the app reads a normal environment variable. |
| After the secret is rotated, App Service picks up the new version within 24 hours. | Yes | References without a version resolve to the latest; refresh happens within 24 hours. |
| The setting must include the secret version, or the reference fails. | No | References without a version resolve to the latest version. |

Key Vault references need a managed identity, need no code changes, and refresh within 24 hours or on a restart-causing config change.

📘 Source: [Configure application settings](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/4-configure-settings)

</details>

## 28. `lp1m2-028`

An app setting holds a Key Vault reference to a model API key. The key was rotated in Key Vault five days ago, but the app still sends the old key. No other app settings changed. What is the most likely cause?

- **A.** The SecretUri in the reference includes a specific secret version
- **B.** The managed identity's role covers the original secret version but not new ones
- **C.** The setting isn't marked as a deployment slot setting, so it doesn't refresh
- **D.** App Service resolves a Key Vault reference once, when the app is created

<details><summary>💡 Hint</summary>

Five days is far longer than the refresh window. What in the reference could stop it from following the latest value?

</details>

<details><summary>✅ Answer</summary>

**A.** The SecretUri in the reference includes a specific secret version

- A: Correct. Only references without a version resolve to the latest version. A versioned URI keeps returning that exact version.
- B: Read access to secrets isn't limited to one version. The identity can read whichever version the URI asks for.
- C: Slot settings control what moves during a swap. They don't affect how secrets refresh.
- D: App Service refreshes resolved values within 24 hours, and a restart forces a refetch, so references aren't fixed at creation.

References without a version resolve to the latest version, and App Service refreshes resolved values within 24 hours (a restart forces an immediate refetch). A version in the SecretUri pins the reference to that version.

📘 Source: [Configure application settings](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/4-configure-settings)

</details>

## 29. `lp1m2-029`

You want to confirm every environment variable the app receives, including system-provided ones. Where do you look?

- **A.** The log stream
- **B.** The Environment page of the Kudu (SCM) site
- **C.** The output of az webapp show --query defaultHostName
- **D.** The AppServiceHTTPLogs table

<details><summary>💡 Hint</summary>

Look in the advanced tools that run beside your app, not in the portal's configuration blade.

</details>

<details><summary>✅ Answer</summary>

**B.** The Environment page of the Kudu (SCM) site

- A: The log stream shows output, not the configured environment.
- B: Correct. /Env lists app settings and system variables.
- C: That returns the app's hostname only.
- D: That table holds request and response information.

/Env lists app settings and system variables.

📘 Source: [Configure application settings](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/4-configure-settings)

</details>

## 30. `lp1m2-030`

Match each log category to what it contains.

Choices: **AppServiceConsoleLogs** · **AppServiceHTTPLogs** · **AppServicePlatformLogs**

- Container stdout and stderr output
- HTTP request and response information
- Container lifecycle events and platform messages

<details><summary>💡 Hint</summary>

Each category name says where its data comes from: the console, HTTP traffic, or the platform.

</details>

<details><summary>✅ Answer</summary>

- Container stdout and stderr output → **AppServiceConsoleLogs**. Console logs capture the container's standard output and error streams.
- HTTP request and response information → **AppServiceHTTPLogs**. HTTP logs record requests and responses.
- Container lifecycle events and platform messages → **AppServicePlatformLogs**. Platform logs record lifecycle events.

Send these categories to Log Analytics with a diagnostic setting for long-term analysis and alerts.

📘 Source: [Observe and troubleshoot containerized apps](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/5-observe-troubleshoot)

</details>

## 31. `lp1m2-031`

While testing a fix, you want to watch container output from every instance as it happens. What should you use?

- **A.** The Kudu Environment page
- **B.** The diagnostic dump ZIP from the Kudu site
- **C.** A diagnostic setting that archives logs to a storage account
- **D.** The log stream, for example az webapp log tail

<details><summary>💡 Hint</summary>

You want output now, from every instance. Which feature streams logs live?

</details>

<details><summary>✅ Answer</summary>

**D.** The log stream, for example az webapp log tail

- A: That page shows environment variables, not log output.
- B: A dump is a snapshot for offline analysis, not a live view.
- C: That's for retention, not live watching.
- D: Correct. It shows new entries in real time from all instances, each tagged with its instance.

It shows new entries in real time from all instances, each tagged with its instance.

📘 Source: [Observe and troubleshoot containerized apps](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/5-observe-troubleshoot)

</details>

## 32. `lp1m2-032`

The container log says "Listening on `http://localhost:8000`" and WEBSITES_PORT is 8000, but every request returns 404. What is the most likely fix?

- **A.** Change WEBSITES_PORT to 80 so the default route is used
- **B.** Enable always-on so the container finishes starting up
- **C.** Bind the application to 0.0.0.0 instead of localhost
- **D.** Turn on persistent storage so the routes are kept

<details><summary>💡 Hint</summary>

The app listens, and the port matches, but nothing gets in. Which address accepts connections from outside the container?

</details>

<details><summary>✅ Answer</summary>

**C.** Bind the application to 0.0.0.0 instead of localhost

- A: The port already matches; changing it would create a mismatch.
- B: Always-on doesn't change which interface the app listens on.
- C: Correct. An app listening on localhost doesn't accept traffic from outside the container.
- D: Persistent storage doesn't affect routing.

For 404s after deployment, check that WEBSITES_PORT matches and that the app binds to 0.0.0.0 rather than localhost.

📘 Source: [Observe and troubleshoot containerized apps](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/5-observe-troubleshoot)

</details>

## 33. `lp1m2-033`

You need to inspect running processes inside the app container. You open the Kudu Debug console but can't find them. Why, and what should you use?

- **A.** Kudu lists Windows processes, so switch the plan to Windows
- **B.** Processes are listed in the diagnostic dump download
- **C.** The log stream hides processes; enable filesystem logging
- **D.** Kudu is a separate site, so use SSH enabled in the image

<details><summary>💡 Hint</summary>

Kudu runs beside your app, not inside it. How do you get a shell in the app container itself?

</details>

<details><summary>✅ Answer</summary>

**D.** Kudu is a separate site, so use SSH enabled in the image

- A: The plan OS isn't the reason; Kudu runs as a separate site.
- B: The dump contains logs and configuration, not a live process view.
- C: Logging settings don't expose processes.
- D: Correct. The SCM site isn't the app container. SSH (when enabled in the image) gives in-container inspection.

Kudu can browse /home and environment variables, but not the full container file system or processes. Use SSH for that.

📘 Source: [Observe and troubleshoot containerized apps](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/5-observe-troubleshoot)

</details>

## 34. `lp1m2-034`

You're adding SSH support to a custom container for App Service. Which three requirements must the image meet? (Select three.)

- **A.** Store the SSH password as a Key Vault reference
- **B.** Expose SSH on port 22 through WEBSITES_PORT
- **C.** Set the root password to Docker!
- **D.** Configure SSH to listen on port 2222
- **E.** Install the openssh-server package

<details><summary>💡 Hint</summary>

SSH needs a server, a fixed port that App Service expects, and a known root password.

</details>

<details><summary>✅ Answer</summary>

**C.** Set the root password to Docker!  
**D.** Configure SSH to listen on port 2222  
**E.** Install the openssh-server package

- A: The root password is a fixed value App Service requires, not a stored secret.
- B: WEBSITES_PORT is for HTTP traffic, and SSH uses 2222, not 22.
- C: Correct. App Service requires the root password Docker!.
- D: Correct. App Service expects SSH on port 2222.
- E: Correct. The image must include the OpenSSH server.

Install openssh-server, listen on 2222, set root:Docker!, and start sshd alongside the app.

📘 Source: [Observe and troubleshoot containerized apps](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/5-observe-troubleshoot)

</details>

## 35. `lp1m2-035`

Ops wants to query the last hour of container errors with KQL and keep the logs long-term. What should you configure?

- **A.** The log stream in the portal
- **B.** Send AppServiceConsoleLogs to Log Analytics
- **C.** Enable container logging to the App Service filesystem
- **D.** The Kudu diagnostic dump

<details><summary>💡 Hint</summary>

KQL queries and long-term retention point to one Azure Monitor destination.

</details>

<details><summary>✅ Answer</summary>

**B.** Send AppServiceConsoleLogs to Log Analytics

- A: The log stream is live viewing, not something you can query.
- B: Correct. Log Analytics supports KQL queries, alerts and long retention.
- C: This stores logs in /home/LogFiles. It doesn't support KQL queries or long retention.
- D: A dump is a one-off ZIP for offline analysis.

Log Analytics supports KQL queries, alerts and long retention.

📘 Source: [Observe and troubleshoot containerized apps](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/5-observe-troubleshoot)

</details>

## 36. `lp1m2-036`

You suspect the platform restarted the container overnight. Which log category records container lifecycle events?

- **A.** AppServicePlatformLogs
- **B.** AppServiceAppLogs
- **C.** AppServiceHTTPLogs
- **D.** AppServiceConsoleLogs

<details><summary>💡 Hint</summary>

Restarts are platform events, not app output. Which category records the platform's actions?

</details>

<details><summary>✅ Answer</summary>

**A.** AppServicePlatformLogs

- A: Correct. It records container lifecycle events and platform messages.
- B: This holds application-level logs, when configured.
- C: This holds HTTP request and response information.
- D: This holds the container's own stdout and stderr.

It records container lifecycle events and platform messages.

📘 Source: [Observe and troubleshoot containerized apps](https://learn.microsoft.com/en-us/training/modules/deploy-containers-azure-app-service/5-observe-troubleshoot)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
