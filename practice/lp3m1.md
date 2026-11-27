# Practice: LP3 · M1 Deploy applications to Azure Kubernetes Service

> 23 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp3m1.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-3/deploy-apps-azure-kubernetes-service)

## 1. `lp3m1-001`

In a Deployment manifest, which field sets how many copies of the Pod run at the same time?

- **A.** replicas
- **B.** selector
- **C.** resources
- **D.** containers

<details><summary>💡 Hint</summary>

One field in the Deployment spec says how many copies of the Pod should run at the same time.

</details>

<details><summary>✅ Answer</summary>

**A.** replicas

- A: Correct. replicas determines how many copies run simultaneously.
- B: selector matches Pods by label; it doesn't set a count.
- C: resources sets CPU and memory per container.
- D: containers lists the containers in each Pod.

spec.replicas sets the number of Pods the Deployment maintains.

📘 Source: [Create Kubernetes deployment manifests](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/2-create-deployment-manifests)

</details>

## 2. `lp3m1-002`

How many replicas does Learn recommend for a production AI inference API that serves external users?

- **A.** 1
- **B.** 2
- **C.** 10
- **D.** 3

<details><summary>💡 Hint</summary>

Learn gives 2 for basic resilience and a higher number for production APIs with external users.

</details>

<details><summary>✅ Answer</summary>

**D.** 3

- A: One Pod means downtime whenever it crashes.
- B: Two give basic resilience, suited to development and noncritical services.
- C: Learn suggests 4+ only for high traffic, balancing resilience with cost.
- D: Correct. Three replicas are recommended for production APIs.

2 replicas = basic resilience; 3 = recommended for production; 4+ only for high traffic.

📘 Source: [Create Kubernetes deployment manifests](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/2-create-deployment-manifests)

</details>

## 3. `lp3m1-003`

A model's documentation says it needs 4 GB of memory. Following Learn's guidance, roughly what memory should you start with for the Pod?

- **A.** About 4.8 GB, the documented 4 GB plus 20%
- **B.** About 16 GB, to be safe from OOMKill
- **C.** About 2 GB, then raise it if needed
- **D.** Exactly 4 GB, with no overhead

<details><summary>💡 Hint</summary>

Start from the documented need, then add a fixed percentage for overhead.

</details>

<details><summary>✅ Answer</summary>

**A.** About 4.8 GB, the documented 4 GB plus 20%

- A: Correct. Start with the documented requirement plus 20% for overhead.
- B: Over-allocating wastes cluster resources and money.
- C: Starting below the documented need invites OOMKills.
- D: Learn adds overhead on top of the documented requirement.

Start with the model's documented requirement plus 20%, then refine from observed usage.

📘 Source: [Create Kubernetes deployment manifests](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/2-create-deployment-manifests)

</details>

## 4. `lp3m1-004`

For each statement, select Yes if the statement is true. Otherwise, select No. A Pod spec has `requests: memory 2Gi` and `limits: memory 4Gi`.

| Statement | Yes / No |
|---|---|
| Kubernetes uses the 2Gi request to decide which node can run the Pod. | ☐ |
| If every node has only 1Gi free, the Pod stays Pending. | ☐ |
| If the container uses 5Gi, it keeps running but is slowed down. | ☐ |

<details><summary>💡 Hint</summary>

Requests decide scheduling. Going over the memory limit doesn't just slow a container down.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Kubernetes uses the 2Gi request to decide which node can run the Pod. | Yes | Requests are used for scheduling. |
| If every node has only 1Gi free, the Pod stays Pending. | Yes | A Pod requesting more than any node has free stays Pending. |
| If the container uses 5Gi, it keeps running but is slowed down. | No | Exceeding the memory limit gets the container terminated and restarted (OOMKill). |

Requests drive scheduling; limits are the ceiling, and going over the memory limit means OOMKill.

📘 Source: [Create Kubernetes deployment manifests](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/2-create-deployment-manifests)

</details>

## 5. `lp3m1-005`

A manifest stored in Git sets `env: - name: API_KEY value: "sk-123…"`. What should you do?

- **A.** Move the value to a second env entry named API_KEY_B64
- **B.** Keep it, because env values are encrypted by Kubernetes
- **C.** Put the key in the image tag so it stays out of the manifest
- **D.** Create a Secret with kubectl and reference it with valueFrom

<details><summary>💡 Hint</summary>

Never keep a secret value in a manifest that's in source control.

</details>

<details><summary>✅ Answer</summary>

**D.** Create a Secret with kubectl and reference it with valueFrom

- A: Encoding the value in another env entry still puts it in Git.
- B: Learn says never hardcode secrets in manifests.
- C: Image tags are visible and aren't a place for secrets.
- D: Correct. Create the Secret separately and reference it, so the key stays out of source control.

Use env for non-sensitive values and Secrets (valueFrom) for API keys and credentials.

📘 Source: [Create Kubernetes deployment manifests](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/2-create-deployment-manifests)

</details>

## 6. `lp3m1-006`

A Deployment sets replicas: 3. One of the three inference Pods crashes with an out-of-memory error. You don't run any command. What happens?

- **A.** The controller replaces it to get back to 3
- **B.** The other two Pods also restart so that all replicas run the same version
- **C.** The Deployment stays at 2 Pods until someone runs kubectl apply again
- **D.** AKS removes the Deployment because one of its Pods failed

<details><summary>💡 Hint</summary>

A manifest describes the state you want. Who keeps the cluster in that state?

</details>

<details><summary>✅ Answer</summary>

**A.** The controller replaces it to get back to 3

- A: Correct. A manifest declares desired state, and the controller keeps working toward it.
- B: Healthy replicas keep serving. Only the failed Pod is replaced.
- C: You don't need to reapply. The controller reconciles toward the declared state on its own.
- D: One failed Pod doesn't remove a Deployment. Its controller replaces the Pod.

You describe desired state in the manifest. The Deployment controller monitors Pod health and restarts crashed Pods so that the running replicas match the replicas field.

📘 Source: [Create Kubernetes deployment manifests](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/2-create-deployment-manifests)

</details>

## 7. `lp3m1-007`

A Deployment's spec.selector.matchLabels is app: inference-api, but its Pod template's labels say app: inference. What's wrong?

- **A.** Nothing, because the Deployment manages Pods by their image name
- **B.** The labels can differ until the first Pod has started
- **C.** The selector doesn't match the template labels
- **D.** Nothing, because label selectors are a Service feature

<details><summary>💡 Hint</summary>

matchLabels says which Pods the Deployment manages. Where do those Pods get their labels from?

</details>

<details><summary>✅ Answer</summary>

**C.** The selector doesn't match the template labels

- A: Deployments find their Pods by label, not by image.
- B: The selector has to match the template's labels from the start.
- C: Correct. The selector tells the Deployment which Pods it manages, so it has to match the template labels.
- D: Deployments use a label selector too (spec.selector.matchLabels).

spec.selector.matchLabels must match spec.template.metadata.labels. The Deployment manages the Pods that carry those labels.

📘 Source: [Create Kubernetes deployment manifests](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/2-create-deployment-manifests)

</details>

## 8. `lp3m1-008`

You're sizing CPU for a Pod that serves inference from a small language model. Which starting point does Learn give?

- **A.** 0.1 CPU cores, because inference is mostly memory-bound
- **B.** 8 CPU cores per Pod so that requests don't queue
- **C.** No CPU request, so that Kubernetes decides at run time
- **D.** 1–2 cores per Pod, adjusted for throughput

<details><summary>💡 Hint</summary>

Learn gives a small range of cores for inference, then says to tune it.

</details>

<details><summary>✅ Answer</summary>

**D.** 1–2 cores per Pod, adjusted for throughput

- A: Inference uses CPU too. Too little causes slow responses.
- B: Over-sizing wastes cluster resources and money. Learn suggests starting smaller and adjusting.
- C: Without a request, the scheduler can't place the Pod based on what it needs.
- D: Correct. For inference, 1–2 cores per Pod is typically enough, then you adjust for throughput.

For an AI inference Pod, typically 1–2 CPU cores per Pod is sufficient. Adjust based on expected throughput and observed usage.

📘 Source: [Create Kubernetes deployment manifests](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/2-create-deployment-manifests)

</details>

## 9. `lp3m1-009`

Which image reference follows the format Learn uses for a Deployment that pulls from Azure Container Registry?

- **A.** myregistry.azurecr.io/inference-api:v1.0
- **B.** myregistry/inference-api.azurecr.io:v1.0
- **C.** azurecr.io/myregistry/inference-api:v1.0
- **D.** myregistry.azurecr.io:v1.0/inference-api

<details><summary>💡 Hint</summary>

Registry host first, then a slash, the image name, a colon, and the tag.

</details>

<details><summary>✅ Answer</summary>

**A.** myregistry.azurecr.io/inference-api:v1.0

- A: Correct. registryname.azurecr.io/imagename:tag.
- B: The host is myregistry.azurecr.io, and the image name follows the slash.
- C: The registry name is a subdomain of azurecr.io, not a path.
- D: The tag goes after the image name, not after the registry host.

The image path format is registryname.azurecr.io/imagename:tag, for example myregistry.azurecr.io/inference-api:v1.0.

📘 Source: [Create Kubernetes deployment manifests](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/2-create-deployment-manifests)

</details>

## 10. `lp3m1-010`

Match each need to the Kubernetes Service type.

Choices: **ClusterIP** · **NodePort** · **LoadBalancer** · **ExternalName**

- A vector search service called only by other Pods
- Quick external access during development through a node's IP
- A production AI API that internet users call
- Represent a service outside the cluster by its DNS name

<details><summary>💡 Hint</summary>

Internal only, node IP for dev, managed public IP, or a name for something outside the cluster.

</details>

<details><summary>✅ Answer</summary>

- A vector search service called only by other Pods → **ClusterIP**. ClusterIP is internal to the cluster.
- Quick external access during development through a node's IP → **NodePort**. NodePort exposes a port on every node.
- A production AI API that internet users call → **LoadBalancer**. LoadBalancer creates an Azure Load Balancer with a public IP.
- Represent a service outside the cluster by its DNS name → **ExternalName**. ExternalName maps to an external DNS name.

Choose the Service type by who needs to reach the application.

📘 Source: [Expose applications in Azure Kubernetes Services](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/3-expose-applications)

</details>

## 11. `lp3m1-011`

Clients connect to the Service on port 80, and the FastAPI container listens on 8080. How should the Service ports be set?

- **A.** port: 80, targetPort: 8080
- **B.** port: 80, nodePort: 8080
- **C.** port: 8080, targetPort: 8080
- **D.** port: 8080, targetPort: 80

<details><summary>💡 Hint</summary>

port is what clients use. targetPort is where the app listens.

</details>

<details><summary>✅ Answer</summary>

**A.** port: 80, targetPort: 8080

- A: Correct. port is what clients use; targetPort is where the container listens.
- B: nodePort is for NodePort services, not the container port.
- C: Clients would then have to connect on 8080.
- D: That's reversed: clients would need port 8080.

The Service forwards connections from its port to the Pod's targetPort.

📘 Source: [Expose applications in Azure Kubernetes Services](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/3-expose-applications)

</details>

## 12. `lp3m1-012`

Another Pod in the default namespace must call inference-api-service on port 8080. Which address should it use?

- **A.** `http://inference-api-service.azurecr.io:8080`
- **B.** `http://inference-api-service.default.svc.cluster.local:8080`
- **C.** The EXTERNAL-IP shown for the Service
- **D.** `http://localhost:8080`

<details><summary>💡 Hint</summary>

Service DNS names follow service.namespace.svc.cluster.local.

</details>

<details><summary>✅ Answer</summary>

**B.** `http://inference-api-service.default.svc.cluster.local:8080`

- A: azurecr.io is the registry domain.
- B: Correct. ClusterIP services use servicename.namespace.svc.cluster.local.
- C: A ClusterIP service has no external IP.
- D: localhost reaches the calling Pod itself.

Inside the cluster, call the Service by its DNS name.

📘 Source: [Expose applications in Azure Kubernetes Services](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/3-expose-applications)

</details>

## 13. `lp3m1-013`

For each statement, select Yes if the statement is true. Otherwise, select No. A Service has `selector: app: inference-api`, and the Deployment's Pod template uses the label `app: inference`.

| Statement | Yes / No |
|---|---|
| The Service routes traffic to the Deployment's Pods. | ☐ |
| kubectl describe svc shows Endpoints: `<none>`. | ☐ |
| Changing the Service type to LoadBalancer fixes the problem. | ☐ |

<details><summary>💡 Hint</summary>

The selector must match the Pod labels exactly. Changing the Service type doesn't change matching.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The Service routes traffic to the Deployment's Pods. | No | The labels don't match, so the Service has no Pods to route to. |
| kubectl describe svc shows Endpoints: `<none>`. | Yes | No matching Pods means no endpoints. |
| Changing the Service type to LoadBalancer fixes the problem. | No | The type doesn't matter if the selector matches no Pods. |

Selectors connect Services to Pods; a mismatch leaves the Service without endpoints.

📘 Source: [Expose applications in Azure Kubernetes Services](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/3-expose-applications)

</details>

## 14. `lp3m1-014`

A worker calls an inference Pod directly by its IP address. Every time the Pod restarts, the worker breaks. What should the worker call instead?

- **A.** A second Pod that records the first Pod's IP address
- **B.** A Service, which has a stable IP and DNS name
- **C.** The Deployment's name, which Kubernetes resolves to the newest Pod
- **D.** The node's IP address, because nodes don't restart

<details><summary>💡 Hint</summary>

Pod IPs change on restart. Which Kubernetes object gives you an address that doesn't?

</details>

<details><summary>✅ Answer</summary>

**B.** A Service, which has a stable IP and DNS name

- A: That just moves the problem. A Service is the built-in stable endpoint.
- B: Correct. A Service abstracts the changing Pod IPs behind a persistent endpoint.
- C: Deployments don't provide DNS names for routing traffic. Services do.
- D: Pods can move between nodes, so a node IP isn't a stable way to reach one app.

Pods get new internal IPs when they restart. A Service gives a persistent IP and DNS name and routes traffic to Pods whose labels match its selector.

📘 Source: [Expose applications in Azure Kubernetes Services](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/3-expose-applications)

</details>

## 15. `lp3m1-015`

You apply a Service manifest that has no type field. Other Pods can reach it, but nothing outside the cluster can. Which type did Kubernetes use?

- **A.** LoadBalancer
- **B.** NodePort
- **C.** ClusterIP
- **D.** ExternalName

<details><summary>💡 Hint</summary>

The default type keeps the Service internal to the cluster.

</details>

<details><summary>✅ Answer</summary>

**C.** ClusterIP

- A: LoadBalancer isn't the default. It provisions a public IP.
- B: NodePort isn't the default. It opens a port on each node.
- C: Correct. ClusterIP is the default type: an internal IP reachable only from within the cluster.
- D: ExternalName isn't the default. It maps the Service to an outside DNS name.

ClusterIP is the default Service type. It gives an internal IP that Pods can reach by the Service's DNS name, with no external access.

📘 Source: [Expose applications in Azure Kubernetes Services](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/3-expose-applications)

</details>

## 16. `lp3m1-016`

A Pod shows STATUS CrashLoopBackOff. Which command should you run first to see why?

- **A.** `kubectl get svc`
- **B.** `kubectl logs <pod-name>`
- **C.** `az acr repository list`
- **D.** `az aks scale --node-count 3`

<details><summary>💡 Hint</summary>

The Pod keeps restarting. What the app printed before it exited is the quickest clue.

</details>

<details><summary>✅ Answer</summary>

**B.** `kubectl logs <pod-name>`

- A: Service status doesn't explain an application crash.
- B: Correct. The application's logs show why it crashes on startup.
- C: That checks images exist, which matters for ImagePullBackOff.
- D: Adding nodes fixes Pending Pods, not crashing apps.

CrashLoopBackOff means the app keeps exiting; read its logs (use --previous for earlier crashes).

📘 Source: [Deploy applications to Azure Kubernetes Services](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/4-deploy-verify-results)

</details>

## 17. `lp3m1-017`

Right after creating a LoadBalancer Service, `kubectl get svc` shows EXTERNAL-IP as `<pending>`. What does this mean?

- **A.** The Service selector doesn't match any Pods
- **B.** The Pods are waiting for more CPU on the nodes
- **C.** The image couldn't be pulled from the registry
- **D.** The load balancer is still being provisioned

<details><summary>💡 Hint</summary>

Azure is still creating something for this Service.

</details>

<details><summary>✅ Answer</summary>

**D.** The load balancer is still being provisioned

- A: That shows as no endpoints, not a pending external IP.
- B: Scheduling problems show up as Pending Pods.
- C: Image pull problems show up in the Pod status.
- D: Correct. Wait a moment and check again.

`<pending>` means Azure is still creating the load balancer and public IP.

📘 Source: [Deploy applications to Azure Kubernetes Services](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/4-deploy-verify-results)

</details>

## 18. `lp3m1-018`

Match each symptom to its most likely cause.

Choices: **Image path or tag is wrong** · **Nodes lack the requested memory** · **Pod labels don't match the selector** · **The app exits at startup**

- Events show: Failed to pull image … image not found
- Pods stay Pending; events show Insufficient memory
- The Service shows Endpoints: `<none>`
- CrashLoopBackOff with a missing environment variable error in the logs

<details><summary>💡 Hint</summary>

Each event points to a different layer: image, capacity, labels, or the app itself.

</details>

<details><summary>✅ Answer</summary>

- Events show: Failed to pull image … image not found → **Image path or tag is wrong**. ImagePullBackOff: verify image path, tag and that it was pushed.
- Pods stay Pending; events show Insufficient memory → **Nodes lack the requested memory**. Requests are too large for the free capacity on nodes.
- The Service shows Endpoints: `<none>` → **Pod labels don't match the selector**. No Pods match the Service selector.
- CrashLoopBackOff with a missing environment variable error in the logs → **The app exits at startup**. The application crashes on startup.

Each status points to a different layer: registry, scheduling, service routing or the app.

📘 Source: [Deploy applications to Azure Kubernetes Services](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/4-deploy-verify-results)

</details>

## 19. `lp3m1-019`

For each statement, select Yes if the statement is true. Otherwise, select No. Two Pods requesting 6Gi of memory each stay Pending, and the nodes have 4Gi free each.

| Statement | Yes / No |
|---|---|
| Running az aks scale with more nodes can let the Pods schedule. | ☐ |
| Reviewing whether the 6Gi request is larger than the app needs is a valid fix. | ☐ |
| kubectl apply failed, because it would have reported the scheduling error. | ☐ |
| Reading kubectl logs is the best way to see the cause, because the app has started. | ☐ |

<details><summary>💡 Hint</summary>

Pending with not enough memory is a scheduling problem. Add capacity or request less.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Running az aks scale with more nodes can let the Pods schedule. | Yes | Adding nodes adds capacity if it's exhausted. |
| Reviewing whether the 6Gi request is larger than the app needs is a valid fix. | Yes | Requests that are too large for nodes keep Pods Pending. |
| kubectl apply failed, because it would have reported the scheduling error. | No | kubectl apply is asynchronous and returns immediately. |
| Reading kubectl logs is the best way to see the cause, because the app has started. | No | A Pending Pod hasn't started; use kubectl describe pod for the events. |

Pending = can't schedule: describe the Pod, then lower requests or add nodes.

📘 Source: [Deploy applications to Azure Kubernetes Services](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/4-deploy-verify-results)

</details>

## 20. `lp3m1-020`

A new Pod shows STATUS ImagePullBackOff. Which check does Learn list first?

- **A.** Read kubectl logs for the application's stack trace
- **B.** Raise the memory limit so that the container can start
- **C.** Verify the image path, tag and registry in the manifest
- **D.** Change the Service selector to match the Pod's labels

<details><summary>💡 Hint</summary>

The container never started. What does Kubernetes need before it can start one?

</details>

<details><summary>✅ Answer</summary>

**C.** Verify the image path, tag and registry in the manifest

- A: No container started, so there are no application logs to read yet.
- B: Memory affects running containers. The image never got pulled.
- C: Correct. ImagePullBackOff means Kubernetes can't pull the image, so start with the image reference.
- D: Selectors affect routing to running Pods, not pulling images.

ImagePullBackOff means Kubernetes can't pull the image. Check the image path, tag and registry, confirm the image was pushed (az acr repository list), and check the cluster can pull from the registry.

📘 Source: [Deploy applications to Azure Kubernetes Services](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/4-deploy-verify-results)

</details>

## 21. `lp3m1-021`

A Pod is in CrashLoopBackOff, and the current container exits before writing anything useful. You want the output of the container instance that crashed just before. Which command shows it?

- **A.** kubectl describe svc `<service-name>`
- **B.** kubectl top pods
- **C.** kubectl logs `<pod-name>` --previous
- **D.** kubectl get pods -w

<details><summary>💡 Hint</summary>

By default you see the container that's running now. You want the one before it.

</details>

<details><summary>✅ Answer</summary>

**C.** kubectl logs `<pod-name>` --previous

- A: Services don't hold container output.
- B: This shows resource usage, not logs.
- C: Correct. --previous shows logs from the previous container instance, which is the one that crashed.
- D: This watches status changes. It doesn't show what the crashed container printed.

CrashLoopBackOff means the image pulled but the container keeps exiting. Use kubectl logs `<pod>` --previous to read the crashed instance's output, and kubectl describe pod for events.

📘 Source: [Deploy applications to Azure Kubernetes Services](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/4-deploy-verify-results)

</details>

## 22. `lp3m1-022`

The inference API's Service is ClusterIP. You want to check from inside the cluster that it answers on its DNS name. What does Learn suggest?

- **A.** Run kubectl logs -l app=inference-api
- **B.** Run curl against the Service's CLUSTER-IP from your laptop
- **C.** Change the Service to LoadBalancer and call EXTERNAL-IP
- **D.** Run a temporary debug Pod and wget the Service name

<details><summary>💡 Hint</summary>

ClusterIP is only reachable from inside the cluster. How can you get a shell in there briefly?

</details>

<details><summary>✅ Answer</summary>

**D.** Run a temporary debug Pod and wget the Service name

- A: Logs show what the app printed. They don't test whether the Service answers.
- B: A cluster IP is only reachable from inside the cluster.
- C: That exposes the API publicly just to test it, which isn't needed.
- D: Correct. A throwaway debug Pod can reach a ClusterIP Service by its DNS name.

For ClusterIP Services, run a test Pod (kubectl run -it --rm debug --image=alpine:latest --restart=Never -- sh) and call the Service's DNS name. For LoadBalancer Services, use the public IP from your machine.

📘 Source: [Deploy applications to Azure Kubernetes Services](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/4-deploy-verify-results)

</details>

## 23. `lp3m1-023`

For each statement, select Yes if the statement is true. Otherwise, select No. You run kubectl apply -f . in a folder that holds deployment.yaml and service.yaml.

| Statement | Yes / No |
|---|---|
| kubectl apply waits until every Pod is Running before it returns. | ☐ |
| kubectl logs -l app=inference-api shows logs from every Pod with that label. | ☐ |
| A READY value of 2/2 for the Deployment means both replicas are running. | ☐ |

<details><summary>💡 Hint</summary>

Think about whether apply is synchronous, how -l selects Pods, and what READY counts.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| kubectl apply waits until every Pod is Running before it returns. | No | Deployment is asynchronous: apply returns immediately while images pull and containers start. |
| kubectl logs -l app=inference-api shows logs from every Pod with that label. | Yes | The -l flag selects Pods by label, so you see all replicas. |
| A READY value of 2/2 for the Deployment means both replicas are running. | Yes | READY shows how many replicas are ready out of the desired count. |

kubectl apply returns immediately and Kubernetes reconciles in the background. kubectl get pods/deployment show READY and STATUS; kubectl logs -l `<label>` reads all matching Pods.

📘 Source: [Deploy applications to Azure Kubernetes Services](https://learn.microsoft.com/en-us/training/modules/deploy-apps-azure-kubernetes-service/4-deploy-verify-results)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
