# Practice: LP1 · M1 Store and manage containers in Azure Container Registry

> 33 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp1m1.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-1/store-manage-containers-azure-container-registry)

## 1. `lp1m1-001`

Your team creates a registry named `contosoinference`. Which login server do developers use to push images to it?

- **A.** contosoinference.registry.azure.com
- **B.** contosoinference.azurewebsites.net
- **C.** contosoinference.azurecr.io
- **D.** azurecr.io/contosoinference

<details><summary>💡 Hint</summary>

Every registry gets its own login server. Think about which Azure domain is reserved for container registries.

</details>

<details><summary>✅ Answer</summary>

**C.** contosoinference.azurecr.io

- A: ACR login servers use the azurecr.io domain.
- B: azurewebsites.net is the App Service domain, not a registry login server.
- C: Correct. Each registry has a login server in the format `<registry-name>`.azurecr.io.
- D: The registry name comes first, as a subdomain, not as a path.

The registry name becomes part of its unique login server URL: `<registry-name>`.azurecr.io.

📘 Source: [Registries, repositories, and artifacts](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/2-image-storage)

</details>

## 2. `lp1m1-002`

In Azure Container Registry, what is a repository?

- **A.** A collection of images with the same name but different tags
- **B.** A single image layer created by one Dockerfile instruction
- **C.** The SHA-256 manifest that lists an image's layers
- **D.** The top-level resource that hosts all of the registry content

<details><summary>💡 Hint</summary>

Picture the three levels: registry, then repository, then artifact. Which level holds every tag of one image name?

</details>

<details><summary>✅ Answer</summary>

**A.** A collection of images with the same name but different tags

- A: Correct. A repository such as inference-api holds every version (tag) of that image.
- B: That is a layer, which is part of an artifact.
- C: That is the manifest, identified by a digest.
- D: That describes the registry, the top level of the hierarchy.

Registry → repository → artifact. A repository groups all tagged versions of one image name.

📘 Source: [Registries, repositories, and artifacts](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/2-image-storage)

</details>

## 3. `lp1m1-003`

The ML team must be able to push images to their own area of the registry, but must not push to the production images. How should you organize the repositories?

- **A.** Create a second registry for the ML team in the Basic tier
- **B.** Use namespaces such as ml-team/model-server and production/inference-api
- **C.** Give every ML image a tag starting with ml- inside the shared production repository
- **D.** Store the ML team's images as Helm charts instead of Docker images

<details><summary>💡 Hint</summary>

You can grant push rights to part of a registry. What groups repositories by a prefix with a forward slash?

</details>

<details><summary>✅ Answer</summary>

**B.** Use namespaces such as ml-team/model-server and production/inference-api

- A: Learn recommends namespaces inside a registry for this; a second registry isn't needed.
- B: Correct. Forward-slash namespaces group images, and you can grant a team push rights to only its namespace.
- C: Tags label versions; they don't separate permissions between teams.
- D: The artifact format doesn't control who can push.

Namespaces (team/image) help with access control: a team can push only to its namespace while production stays restricted.

📘 Source: [Registries, repositories, and artifacts](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/2-image-storage)

</details>

## 4. `lp1m1-004`

Inference nodes in five regions pull a 6 GB model-serving image, and pulls from far-away regions are slow. Which ACR capability addresses this, and which tier provides it?

- **A.** Content trust, in the Standard tier
- **B.** Layer sharing, in the Standard tier
- **C.** Geo-replication, in the Premium tier
- **D.** Private endpoints, in the Basic tier

<details><summary>💡 Hint</summary>

Slow pulls from far regions are a distance problem. Which feature puts copies of images near each region, and which tier has it?

</details>

<details><summary>✅ Answer</summary>

**C.** Geo-replication, in the Premium tier

- A: Content trust is about image signing, not pull latency, and it's a Premium feature.
- B: Layer sharing saves storage in every tier; it doesn't move images closer to regions.
- C: Correct. Geo-replication puts images close to deployment regions, and it's a Premium feature.
- D: Private endpoints control network access, and they need Premium.

Geo-replication distributes images close to deployment regions for faster pulls; it's part of the Premium tier.

📘 Source: [Registries, repositories, and artifacts](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/2-image-storage)

</details>

## 5. `lp1m1-005`

Production pods pulled `inference-api:stable` at different times and now run two different images. You need every node to run exactly the image that passed testing, even if someone pushes to that tag again. What should the deployment reference?

- **A.** Its digest: inference-api@sha256:`<hash>`
- **B.** inference-api:latest, because it resolves to a single image
- **C.** The repository name alone, so ACR picks the newest manifest
- **D.** The same tag, with the image locked by write-enabled false

<details><summary>💡 Hint</summary>

Tags can move after a push. Which way of naming an image can never change?

</details>

<details><summary>✅ Answer</summary>

**A.** Its digest: inference-api@sha256:`<hash>`

- A: Correct. Digests are immutable, so pulling by digest always returns the same image.
- B: latest is a mutable tag and is the default; it causes this exact problem.
- C: Without a tag, Docker uses latest, which is still a moving tag.
- D: Locking stops overwrites from now on, but Learn's answer for guaranteed reproducibility is the digest.

Tags are mutable and can move; a SHA-256 digest never changes. Pull by digest when consistency across nodes is critical.

📘 Source: [Registries, repositories, and artifacts](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/2-image-storage)

</details>

## 6. `lp1m1-006`

For each statement, select Yes if the statement is true. Otherwise, select No. Your registry holds `inference-api:v1.2.0`, which is also tagged `inference-api:stable`.

| Statement | Yes / No |
|---|---|
| Both tags reference the same underlying image. | ☐ |
| Pushing a new image as inference-api:stable moves that tag to the new image. | ☐ |
| Pushing a new image as inference-api:stable changes the digest of the v1.2.0 image. | ☐ |
| Running docker pull without a tag pulls inference-api:stable. | ☐ |

<details><summary>💡 Hint</summary>

Two tags can point to the same image. Pushing to a tag moves only that tag, and a digest never changes.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Both tags reference the same underlying image. | Yes | A single artifact can have multiple tags pointing to it. |
| Pushing a new image as inference-api:stable moves that tag to the new image. | Yes | Tags are mutable: pushing an existing tag moves it. |
| Pushing a new image as inference-api:stable changes the digest of the v1.2.0 image. | No | Digests are immutable; the v1.2.0 image keeps its digest. |
| Running docker pull without a tag pulls inference-api:stable. | No | With no tag, Docker uses latest by default. |

Several tags can point at one artifact. Tags move when you push; digests never change; the default tag is latest.

📘 Source: [Registries, repositories, and artifacts](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/2-image-storage)

</details>

## 7. `lp1m1-007`

Your inference images must be replicated to the regions where you deploy, and the registry must be reachable only through a private endpoint. Which ACR tier do you need?

- **A.** Basic
- **B.** Any tier, because all features are shared
- **C.** Premium
- **D.** Standard

<details><summary>💡 Hint</summary>

You need copies in several regions and private network access. Both features sit in the same tier.

</details>

<details><summary>✅ Answer</summary>

**C.** Premium

- A: Basic is meant for development and learning. It has no geo-replication or private endpoints.
- B: Most developer workflows are the same on every tier, but these features are Premium-only.
- C: Correct. Premium adds geo-replication, private endpoints and content trust.
- D: Standard adds storage and throughput for production, but not geo-replication or private endpoints.

Premium adds geo-replication, private endpoints and content trust.

📘 Source: [Registries, repositories, and artifacts](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/2-image-storage)

</details>

## 8. `lp1m1-008`

For each statement about ACR artifacts, select Yes if it's true. Otherwise, select No.

| Statement | Yes / No |
|---|---|
| One artifact can have more than one tag pointing to it. | ☐ |
| Pushing an image with a tag that already exists fails by default. | ☐ |
| When several images share a base layer such as python:3.11, the registry keeps one copy of that layer. | ☐ |

<details><summary>💡 Hint</summary>

Think about tags as movable labels, and about how a registry stores layers that many images share.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| One artifact can have more than one tag pointing to it. | Yes | For example, inference-api:v1.2.0 and inference-api:stable can point to the same image. |
| Pushing an image with a tag that already exists fails by default. | No | Tags are mutable. The push succeeds and the tag moves to the new image. Only a locked image rejects it. |
| When several images share a base layer such as python:3.11, the registry keeps one copy of that layer. | Yes | ACR shares common layers across images, which cuts storage and speeds up pulls. |

An artifact can carry many tags, tags are mutable (a push to an existing tag moves it), and shared layers are stored once.

📘 Source: [Registries, repositories, and artifacts](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/2-image-storage)

</details>

## 9. `lp1m1-009`

Your AI platform ships both Docker images and Helm charts. You want them in one private registry. What does ACR support?

- **A.** Docker images, Helm charts and OCI artifacts in one registry
- **B.** Docker images; Helm charts need a separate storage account
- **C.** Helm charts on the Premium tier but not on Basic
- **D.** Helm charts if they're pushed with az acr build

<details><summary>💡 Hint</summary>

ACR stores more than Docker images. Think about the OCI standard.

</details>

<details><summary>✅ Answer</summary>

**A.** Docker images, Helm charts and OCI artifacts in one registry

- A: Correct. One registry can hold all three content formats.
- B: ACR also stores Helm charts and other OCI artifacts.
- C: Content formats don't depend on the tier. The Premium-only features are geo-replication, private endpoints and content trust.
- D: How content is pushed doesn't limit what ACR can store.

One registry can hold all three content formats.

📘 Source: [Registries, repositories, and artifacts](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/2-image-storage)

</details>

## 10. `lp1m1-010`

One image is tagged both inference-api:v1.2.0 and inference-api:stable. A colleague then pushes a new image tagged stable. What does each tag point to now?

- **A.** The original image is deleted and v1.2.0 is removed
- **B.** Only stable moves; v1.2.0 keeps the original
- **C.** Both tags point to the new image
- **D.** The push fails because stable is already in use

<details><summary>💡 Hint</summary>

A push moves only the tag it names. What happens to the other tag?

</details>

<details><summary>✅ Answer</summary>

**B.** Only stable moves; v1.2.0 keeps the original

- A: The previous image stays in the registry. Nothing is deleted by a push.
- B: Correct. Tags are mutable: stable moves, and v1.2.0 keeps referencing the original.
- C: Only the tag that was pushed moves. v1.2.0 wasn't part of the new push.
- D: Pushing an existing tag succeeds unless the image is locked. The tag simply moves.

Tags are mutable: stable moves, and v1.2.0 keeps referencing the original.

📘 Source: [Registries, repositories, and artifacts](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/2-image-storage)

</details>

## 11. `lp1m1-011`

Which statement correctly describes a manifest digest in ACR?

- **A.** An identifier for one layer rather than for the whole artifact
- **B.** A human-readable name that can be moved to a newer image
- **C.** An immutable SHA-256 identifier for the whole image
- **D.** A value generated again each time the image is pulled

<details><summary>💡 Hint</summary>

A digest is a hash of the manifest. Can a hash of fixed content change?

</details>

<details><summary>✅ Answer</summary>

**C.** An immutable SHA-256 identifier for the whole image

- A: The manifest lists the artifact's layers and configuration. Its digest identifies the whole artifact.
- B: That describes a tag, not a digest.
- C: Correct. Digests are immutable, unlike tags.
- D: The digest identifies the content and stays the same on every pull.

Digests are immutable, unlike tags.

📘 Source: [Registries, repositories, and artifacts](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/2-image-storage)

</details>

## 12. `lp1m1-012`

A data scientist needs to build an image from the Dockerfile in the current folder and push it to the registry, but Docker isn't installed on their laptop. Which command should they run?

- **A.** az acr run --registry myregistry --cmd 'inference-api:v1.0.0' /dev/null
- **B.** az acr repository update --name myregistry --image inference-api:v1.0.0
- **C.** az acr build --registry myregistry --image inference-api:v1.0.0 .
- **D.** docker push myregistry.azurecr.io/inference-api:v1.0.0

<details><summary>💡 Hint</summary>

There's no local Docker, so the build has to happen in Azure. Which az acr command sends the build context to the registry?

</details>

<details><summary>✅ Answer</summary>

**C.** az acr build --registry myregistry --image inference-api:v1.0.0 .

- A: az acr run runs a command in an existing image; it doesn't build from source.
- B: repository update changes attributes such as write-enabled; it doesn't build.
- C: Correct. A quick task uploads the context (.), builds in Azure and pushes the image.
- D: docker push needs a locally built image and Docker installed.

az acr build is a quick task: like docker build + docker push, but done in Azure.

📘 Source: [Build and run images with ACR Tasks](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/3-build-run-acr-tasks)

</details>

## 13. `lp1m1-013`

Every commit to the main branch of a GitHub repo must produce a new image with a tag no previous build has used. Which tag value should the task use?

- **A.** inference-api:stable
- **B.** inference-api:latest
- **C.** inference-api:{{.Run.ID}}
- **D.** inference-api:main-branch

<details><summary>💡 Hint</summary>

The tag must be different for every run. Which built-in task variable changes on every run?

</details>

<details><summary>✅ Answer</summary>

**C.** inference-api:{{.Run.ID}}

- A: stable is reused, so it moves each time.
- B: latest is reused on every push, so each build overwrites the last.
- C: Correct. {{.Run.ID}} is the task run id, so each triggered build gets a distinct tag.
- D: A branch-name tag is reused by every build, so it moves.

Run variables such as {{.Run.ID}} and {{.Run.Date}} create unique, traceable tags per build.

📘 Source: [Build and run images with ACR Tasks](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/3-build-run-acr-tasks)

</details>

## 14. `lp1m1-014`

Your app images use a custom PyTorch base image. When the base image is patched, every app image must rebuild automatically. Where should the base image be stored so ACR detects the update?

- **A.** In Docker Hub, as a private repository
- **B.** In a separate registry in another region
- **C.** In a remote tarball referenced by URL
- **D.** In the same registry as the app images

<details><summary>💡 Hint</summary>

Automatic rebuilds after a base-image update need ACR to see that update. Where can it see a private base image?

</details>

<details><summary>✅ Answer</summary>

**D.** In the same registry as the app images

- A: Learn says private base images should be in the same registry as the app images.
- B: A separate registry breaks automatic detection for private base images.
- C: A tarball is a build context location, not a base image store.
- D: Correct. For private base images, keep the base and the app images in the same registry.

Base image triggers work for base images in the same registry, or public ones such as Docker Hub. Private base images belong in the same registry as the app images.

📘 Source: [Build and run images with ACR Tasks](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/3-build-run-acr-tasks)

</details>

## 15. `lp1m1-015`

A multi-step task must build the image, store it in the registry, and then run the test suite inside it. Put the YAML steps in order.

- build: -t {{.Run.Registry}}/inference-api:{{.Run.ID}} .
- cmd: {{.Run.Registry}}/inference-api:{{.Run.ID}} python -m pytest tests/
- push: {{.Run.Registry}}/inference-api:{{.Run.ID}}

<details><summary>💡 Hint</summary>

You can't test an image that doesn't exist yet, and the test step runs the image from the registry.

</details>

<details><summary>✅ Answer</summary>

1. build: -t {{.Run.Registry}}/inference-api:{{.Run.ID}} .
2. push: {{.Run.Registry}}/inference-api:{{.Run.ID}}
3. cmd: {{.Run.Registry}}/inference-api:{{.Run.ID}} python -m pytest tests/

The Learn example builds, pushes, then runs the container with cmd to execute pytest. If tests fail, you know before deployment.

📘 Source: [Build and run images with ACR Tasks](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/3-build-run-acr-tasks)

</details>

## 16. `lp1m1-016`

Builds of your inference image are slow because the context upload is large and every build reinstalls all packages. Which two changes does Learn recommend? (Select two.)

- **A.** Move the registry from Standard to the Premium tier
- **B.** Add a .dockerignore file to exclude unneeded files
- **C.** Build from a remote tarball instead of a Git repository
- **D.** Put frequently changing instructions late in the Dockerfile

<details><summary>💡 Hint</summary>

One fix shrinks what gets uploaded. The other keeps more Dockerfile layers cached between builds.

</details>

<details><summary>✅ Answer</summary>

**B.** Add a .dockerignore file to exclude unneeded files  
**D.** Put frequently changing instructions late in the Dockerfile

- A: The tier doesn't change context size or layer caching.
- B: Correct. .dockerignore keeps the context small, which speeds the upload.
- C: Changing the context location doesn't shrink it or improve caching.
- D: Correct. ACR Tasks caches layers, and late changing instructions keep earlier layers cached.

Optimize the build context with .dockerignore, and order Dockerfile instructions to maximize layer cache hits.

📘 Source: [Build and run images with ACR Tasks](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/3-build-run-acr-tasks)

</details>

## 17. `lp1m1-017`

One teammate builds from a folder on their laptop. A legacy pipeline drops a compressed source archive on an internal web server reachable by URL. Which two can ACR Tasks use directly as a build context? Each correct answer is a complete solution.

- **A.** The remote tarball, by its URL
- **B.** The file system of a running App Service container
- **C.** A file share mounted only inside another container
- **D.** The local directory on the laptop

<details><summary>💡 Hint</summary>

ACR Tasks accepts several kinds of build context. Which of these can it reach without your help?

</details>

<details><summary>✅ Answer</summary>

**A.** The remote tarball, by its URL  
**D.** The local directory on the laptop

- A: Correct. A compressed archive on a reachable web server is a supported context.
- B: A running container isn't a supported build context.
- C: That isn't one of the supported context locations (local directory, Git repository, remote tarball).
- D: Correct. ACR compresses and uploads a local directory.

ACR compresses and uploads a local directory.

📘 Source: [Build and run images with ACR Tasks](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/3-build-run-acr-tasks)

</details>

## 18. `lp1m1-018`

You want ACR to build an image, push it, then run the test suite inside it with pytest, all as one workflow in the registry. What should you use?

- **A.** A quick task started with az acr build
- **B.** A base image trigger on the python:3.11 image
- **C.** A source code trigger on the main branch
- **D.** A multi-step task defined in a YAML file

<details><summary>💡 Hint</summary>

Build, push and test as one workflow means several steps. Which ACR Tasks feature runs steps in sequence?

</details>

<details><summary>✅ Answer</summary>

**D.** A multi-step task defined in a YAML file

- A: A quick task builds and pushes one image. It doesn't chain a test step after the push.
- B: This decides when a rebuild happens. It doesn't define build, push and test steps.
- C: This starts builds on commits, but on its own it doesn't run tests.
- D: Correct. YAML steps can build, push and then cmd to run tests in the new image.

YAML steps can build, push and then cmd to run tests in the new image.

📘 Source: [Build and run images with ACR Tasks](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/3-build-run-acr-tasks)

</details>

## 19. `lp1m1-019`

In the command below, what does /dev/null tell ACR?

```text
az acr run --registry myregistry \
  --cmd 'inference-api:v1.0.0 python --version' /dev/null
```

- **A.** Nothing needs uploading, because only an existing image runs
- **B.** The command output should be thrown away rather than logged
- **C.** The run should use a Linux image rather than a Windows one
- **D.** The image should be deleted after the run completes

<details><summary>💡 Hint</summary>

az acr run can run an image that already exists. What would it need to upload in that case?

</details>

<details><summary>✅ Answer</summary>

**A.** Nothing needs uploading, because only an existing image runs

- A: Correct. /dev/null is the context: nothing to upload when you only run an image.
- B: /dev/null sits in the context position here. Task logs are still kept.
- C: /dev/null has nothing to do with the target platform.
- D: az acr run doesn't delete images. Cleanup is done with acr purge.

/dev/null is the context: nothing to upload when you only run an image.

📘 Source: [Build and run images with ACR Tasks](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/3-build-run-acr-tasks)

</details>

## 20. `lp1m1-020`

You create an ACR task with a GitHub context and a personal access token so that commits to main start a build. What does ACR set up in the GitHub repository to make this work?

- **A.** A repository webhook that fires on commits and pull requests
- **B.** A GitHub Actions workflow file that calls az acr build
- **C.** A scheduled job that polls the repository every hour
- **D.** A branch protection rule that blocks unbuilt commits

<details><summary>💡 Hint</summary>

Commits must start builds automatically. What does GitHub send to another service when something changes?

</details>

<details><summary>✅ Answer</summary>

**A.** A repository webhook that fires on commits and pull requests

- A: Correct. The PAT lets ACR create a webhook that triggers a build on each commit.
- B: ACR doesn't add workflow files. It uses a webhook.
- C: Source code triggers are event-driven through a webhook, not polling.
- D: ACR doesn't change branch protection.

The PAT lets ACR create a webhook that triggers a build on each commit.

📘 Source: [Build and run images with ACR Tasks](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/3-build-run-acr-tasks)

</details>

## 21. `lp1m1-021`

You want a build every night that picks up the latest dependencies, even when no code has changed. Which ACR Tasks trigger fits?

- **A.** Scheduled trigger
- **B.** Base image trigger
- **C.** Quick task with az acr build
- **D.** Source code trigger

<details><summary>💡 Hint</summary>

Nothing in the code changes, but you still want a build every night. Which trigger runs on the clock?

</details>

<details><summary>✅ Answer</summary>

**A.** Scheduled trigger

- A: Correct. A schedule such as "`0 0 * * *`" runs the task nightly.
- B: This fires only when the base image changes.
- C: A quick task runs once, when you start it.
- D: This needs a commit or pull request. Nights without commits wouldn't build.

A schedule such as "`0 0 * * *`" runs the task nightly.

📘 Source: [Build and run images with ACR Tasks](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/3-build-run-acr-tasks)

</details>

## 22. `lp1m1-022`

A source-triggered ACR task needs a GitHub personal access token. Where does the guidance say to keep the token?

- **A.** In the Dockerfile as a build argument
- **B.** In a .env file committed with the code
- **C.** Hardcoded in the az acr task create script
- **D.** In Azure Key Vault, not in scripts or repositories

<details><summary>💡 Hint</summary>

A personal access token is a secret. Where do Azure apps keep secrets?

</details>

<details><summary>✅ Answer</summary>

**D.** In Azure Key Vault, not in scripts or repositories

- A: That would place the secret in build files and possibly in image history.
- B: Committing tokens to repositories is exactly what the guidance warns against.
- C: The guidance says not to hardcode tokens in scripts.
- D: Correct. Store tokens in Key Vault rather than in scripts or repositories.

Store tokens in Key Vault rather than in scripts or repositories.

📘 Source: [Build and run images with ACR Tasks](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/3-build-run-acr-tasks)

</details>

## 23. `lp1m1-023`

Two developers build the same Dockerfile on their laptops and get images that behave differently in production. The team lead wants every build to run on the same infrastructure, whoever starts it. What should the team do?

- **A.** Pin every developer to the same Docker Desktop version and share one daemon.json
- **B.** Have developers push with the :latest tag so that production always pulls one image
- **C.** Move the registry to the Premium tier so that builds use dedicated agents
- **D.** Build with ACR Tasks so that every build runs in the registry's cloud environment

<details><summary>💡 Hint</summary>

The problem is the build machines, not the registry. Which ACR feature builds images in Azure instead of on laptops?

</details>

<details><summary>✅ Answer</summary>

**D.** Build with ACR Tasks so that every build runs in the registry's cloud environment

- A: Matching tool versions helps a little, but builds still run on different machines with different local state.
- B: A moving tag makes deployments less predictable. It does nothing to make builds consistent.
- C: The tier changes storage, geo-replication and network features. It doesn't change where builds run.
- D: Correct. ACR Tasks builds in a controlled cloud environment, so every build uses the same infrastructure. That removes "works on my machine" differences.

ACR Tasks builds images in a controlled cloud environment. Every build uses the same infrastructure regardless of which developer starts it, which removes "works on my machine" problems.

📘 Source: [Build and run images with ACR Tasks](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/3-build-run-acr-tasks)

</details>

## 24. `lp1m1-024`

For each statement, select Yes if the statement is true. Otherwise, select No. Your app images are built FROM a CUDA base image, and you configure ACR Tasks base image triggers.

| Statement | Yes / No |
|---|---|
| A base image trigger can detect updates to a base image pulled from Docker Hub. | ☐ |
| A private base image in a different registry from the app images is detected automatically. | ☐ |
| When the base image is patched, the trigger rebuilds the app image without anyone pushing code. | ☐ |

<details><summary>💡 Hint</summary>

Base image triggers can watch public registries. Private base images have one placement rule.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| A base image trigger can detect updates to a base image pulled from Docker Hub. | Yes | Base image triggers work for base images in the same registry, or in Docker Hub and other public registries. |
| A private base image in a different registry from the app images is detected automatically. | No | For private base images, both images should be in the same registry for automatic detection. |
| When the base image is patched, the trigger rebuilds the app image without anyone pushing code. | Yes | That's the purpose of the trigger: framework and driver patches flow into app images automatically. |

Base image triggers rebuild app images when the base updates. They work with base images in the same registry or in public registries such as Docker Hub. Private base images must be in the same registry as the app images.

📘 Source: [Build and run images with ACR Tasks](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/3-build-run-acr-tasks)

</details>

## 25. `lp1m1-025`

Match each version change of an inference API to the semantic version part you increment.

Choices: **MAJOR** · **MINOR** · **PATCH**

- A breaking change to the API request format
- A new model endpoint that is backward compatible
- A bug fix in preprocessing

<details><summary>💡 Hint</summary>

MAJOR.MINOR.PATCH: which part signals a breaking change, a new compatible feature, or a fix?

</details>

<details><summary>✅ Answer</summary>

- A breaking change to the API request format → **MAJOR**. Breaking changes that require consumer updates increment MAJOR.
- A new model endpoint that is backward compatible → **MINOR**. New backward-compatible features increment MINOR.
- A bug fix in preprocessing → **PATCH**. Bug fixes and security patches increment PATCH.

MAJOR.MINOR.PATCH communicates compatibility: breaking, feature, fix.

📘 Source: [Tag and version images](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/4-tag-version-images)

</details>

## 26. `lp1m1-026`

Which is an example of a unique tag?

- **A.** inference-api:latest
- **B.** inference-api:v1.2.0-build456
- **C.** inference-api:production-current
- **D.** inference-api:v1.2

<details><summary>💡 Hint</summary>

A unique tag is never reused for a different image. Which value is specific to one build?

</details>

<details><summary>✅ Answer</summary>

**B.** inference-api:v1.2.0-build456

- A: latest is the default stable tag and moves on every push.
- B: Correct. A build-specific tag is never reused.
- C: A 'current' tag is reused for each new image, so it moves.
- D: v1.2 is a stable tag that moves to each new 1.2.x image.

Unique tags such as v1.2.0-build456 or 20260102-abc123 are never reused.

📘 Source: [Tag and version images](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/4-tag-version-images)

</details>

## 27. `lp1m1-027`

During an incident, the on-call engineer must find the exact source code that produced the running image, without access to the CI/CD system. Which tag pattern helps most?

- **A.** A stable major version such as v1
- **B.** The Git commit SHA, such as abc123f
- **C.** A timestamp such as 20260102-143022
- **D.** A build ID such as build-4567

<details><summary>💡 Hint</summary>

The engineer has source-control access but no CI access. Which identifier lives in source control?

</details>

<details><summary>✅ Answer</summary>

**B.** The Git commit SHA, such as abc123f

- A: A stable tag moves and doesn't point to one code state.
- B: Correct. Anyone with repository access can look up the code state from the commit hash.
- C: A timestamp shows image age, not which code state built it.
- D: A build ID needs access to the CI/CD system to trace.

Git SHA tags link the image directly to its source code; build IDs link to the pipeline run instead.

📘 Source: [Tag and version images](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/4-tag-version-images)

</details>

## 28. `lp1m1-028`

For each statement, select Yes if the statement is true. Otherwise, select No. You run `az acr repository update --name myregistry --image inference-api:v1.2.0 --write-enabled false`.

| Statement | Yes / No |
|---|---|
| The image can no longer be deleted, even by an administrator. | ☐ |
| Pushing another image tagged inference-api:v1.2.0 now fails. | ☐ |
| A retention policy for untagged manifests can still remove this image. | ☐ |
| To unlock the image later, you must delete it and push it again. | ☐ |

<details><summary>💡 Hint</summary>

Locking makes an image read-only. Think about delete, overwrite, cleanup policies, and how to undo it.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The image can no longer be deleted, even by an administrator. | Yes | Locked images can't be deleted. |
| Pushing another image tagged inference-api:v1.2.0 now fails. | Yes | Locked images can't be overwritten. |
| A retention policy for untagged manifests can still remove this image. | No | Locked images survive retention policies. |
| To unlock the image later, you must delete it and push it again. | No | You unlock it by running the same command with --write-enabled true. |

Locking (write-enabled false) prevents deletion and overwrite and protects the image from cleanup rules.

📘 Source: [Tag and version images](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/4-tag-version-images)

</details>

## 29. `lp1m1-029`

A Standard-tier registry keeps growing because each push to `:stable` leaves the previous image untagged. You need untagged images older than seven days removed every week, across all repositories. What should you configure?

- **A.** A scheduled ACR task that runs acr purge --untagged --ago 7d
- **B.** A base image trigger that rebuilds the stable tag
- **C.** A lock on every production image using --write-enabled false
- **D.** A registry-level retention policy that deletes untagged manifests after seven days

<details><summary>💡 Hint</summary>

Untagged images pile up after pushes. Which ACR command deletes images by age, and how do you run it every week?

</details>

<details><summary>✅ Answer</summary>

**A.** A scheduled ACR task that runs acr purge --untagged --ago 7d

- A: Correct. A scheduled task (for example --schedule "`0 0 * * 0`") can run acr purge on all repositories.
- B: A rebuild would create even more untagged images.
- C: Locks stop deletion, which is the opposite of what you need.
- D: Retention policies are a Premium tier feature, so they aren't available here.

In Standard, schedule acr purge as an ACR task. Retention policies are the simpler Premium alternative.

📘 Source: [Tag and version images](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/4-tag-version-images)

</details>

## 30. `lp1m1-030`

Inference nodes pulled inference-api:1 at different times and ended up serving different model versions. What should production deployments reference instead?

- **A.** A unique, never-reused tag such as v1.2.0-build456
- **B.** The inference-api:1.1 tag, which narrows updates to one minor version
- **C.** A repository in the staging/ namespace
- **D.** The latest tag, so that every node follows the newest build

<details><summary>💡 Hint</summary>

A tag like :1 moves with every 1.x push. Which kind of tag never moves?

</details>

<details><summary>✅ Answer</summary>

**A.** A unique, never-reused tag such as v1.2.0-build456

- A: Correct. A unique tag is never reused, so every node pulls the same image.
- B: 1.1 is still a stable tag that moves with each 1.1.x patch.
- C: Namespaces organize repositories. They don't stop a tag from moving.
- D: latest is a stable tag too. Nodes that pull at different times can still get different images.

A unique tag is never reused, so every node pulls the same image.

📘 Source: [Tag and version images](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/4-tag-version-images)

</details>

## 31. `lp1m1-031`

The inference API is at version 1.1.0. You fix a preprocessing bug, and the API itself doesn't change. Following semantic versioning, what is the next version?

- **A.** 2.1.1
- **B.** 1.1.1
- **C.** 2.0.0
- **D.** 1.2.0

<details><summary>💡 Hint</summary>

A bug fix that doesn't change the API is the smallest kind of change. Which number goes up?

</details>

<details><summary>✅ Answer</summary>

**B.** 1.1.1

- A: This would also bump MAJOR, which is only for breaking changes.
- B: Correct. PATCH increments for bug fixes and security patches that don't change the API.
- C: MAJOR increments for breaking changes.
- D: MINOR increments for new backward-compatible features, not bug fixes.

PATCH increments for bug fixes and security patches that don't change the API.

📘 Source: [Tag and version images](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/4-tag-version-images)

</details>

## 32. `lp1m1-032`

Your team debates using the latest tag. For each statement, select Yes if it's true. Otherwise, select No.

| Statement | Yes / No |
|---|---|
| If you push or pull without naming a tag, Docker uses latest. | ☐ |
| Referencing :latest in Kubernetes manifests makes every node run the same image. | ☐ |
| The guidance suggests limiting latest to development environments. | ☐ |

<details><summary>💡 Hint</summary>

Think about what Docker does when you leave out the tag, and why a moving tag is risky across many nodes.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| If you push or pull without naming a tag, Docker uses latest. | Yes | latest is Docker's default tag. |
| Referencing :latest in Kubernetes manifests makes every node run the same image. | No | Nodes can pull latest at different times and get different images. |
| The guidance suggests limiting latest to development environments. | Yes | That's where convenience outweighs the need for consistency. |

Docker uses latest when no tag is given. Different nodes may pull latest at different times and get different images, so the guidance limits latest to development.

📘 Source: [Tag and version images](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/4-tag-version-images)

</details>

## 33. `lp1m1-033`

The platform team maintains a base image that receives regular security patches. Dependent images should pick up those patches automatically through base image triggers. Which tagging approach fits the base image?

- **A.** Stable tags
- **B.** Build ID tags
- **C.** A unique tag for each patch
- **D.** Digest references in FROM

<details><summary>💡 Hint</summary>

This image should pass patches on to the images built from it. Which kind of tag is meant to move?

</details>

<details><summary>✅ Answer</summary>

**A.** Stable tags

- A: Correct. Stable tags let security updates flow to dependent images automatically.
- B: Build IDs are unique tags for traceability, not for automatic updates.
- C: Unique tags are for production consistency. Dependents would need config changes to pick up each patch.
- D: A digest pins one exact image, so patches would never flow through.

Stable tags let security updates flow to dependent images automatically.

📘 Source: [Tag and version images](https://learn.microsoft.com/en-us/training/modules/store-manage-containers-azure-container-registry/4-tag-version-images)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
