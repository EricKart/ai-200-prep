# Practice: LP3 · M3 Monitor and troubleshoot applications on Azure Kubernetes Service

> 23 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp3m3.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-3/monitor-apps-azure-kubernetes-service)

## 1. `lp3m3-001`

A Pod runs an inference-api container and a logging sidecar. Which command shows only the inference-api container's logs?

- **A.** kubectl top pods -n ai-workloads
- **B.** kubectl logs <pod> -f
- **C.** kubectl logs <pod> -c inference-api
- **D.** kubectl describe pod <pod> -n ai-workloads

<details><summary>💡 Hint</summary>

The Pod has two containers. Tell kubectl which one you mean.

</details>

<details><summary>✅ Answer</summary>

**C.** kubectl logs <pod> -c inference-api

- A: top shows resource usage, not logs.
- B: -f streams logs, but doesn't choose the container.
- C: Correct. -c selects the container in a multi-container Pod.
- D: describe shows configuration and events, not container logs.

Specify -c <container> when a Pod has several containers.

📘 Source: [Monitor application logs and metrics](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/2-monitor-logs-metrics)

</details>

## 2. `lp3m3-002`

What must be installed in the cluster for kubectl top nodes to work?

- **A.** Container insights
- **B.** The Key Vault CSI driver
- **C.** An ingress controller
- **D.** The metrics server

<details><summary>💡 Hint</summary>

kubectl top reads data that a cluster add-on collects.

</details>

<details><summary>✅ Answer</summary>

**D.** The metrics server

- A: Container insights is a portal monitoring feature, not what kubectl top needs.
- B: The CSI driver mounts secrets.
- C: Ingress controllers route traffic.
- D: Correct. kubectl top requires the metrics server.

kubectl top nodes and kubectl top pods need the metrics server.

📘 Source: [Monitor application logs and metrics](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/2-monitor-logs-metrics)

</details>

## 3. `lp3m3-003`

You need historical CPU trends across many Pods to see which inference workloads were resource-constrained last week. Which tool fits best?

- **A.** kubectl top pods
- **B.** Live Logs in the portal
- **C.** kubectl logs -f
- **D.** Container insights dashboards

<details><summary>💡 Hint</summary>

Last week, across many Pods: you need history, not a snapshot.

</details>

<details><summary>✅ Answer</summary>

**D.** Container insights dashboards

- A: kubectl top gives a current snapshot only.
- B: Live Logs streams output; it doesn't chart resource history.
- C: Streaming logs shows current output, not resource trends.
- D: Correct. Container insights gives historical trends and cross-Pod analysis.

Use Container insights for history and cross-Pod analysis; kubectl top for a quick snapshot.

📘 Source: [Monitor application logs and metrics](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/2-monitor-logs-metrics)

</details>

## 4. `lp3m3-004`

For each statement, select Yes if the statement is true. Otherwise, select No. An inference Pod has a CPU limit of 2, and kubectl top shows it at 2 cores all the time while latency is rising.

| Statement | Yes / No |
|---|---|
| The Pod may be throttled at its CPU limit, which can increase inference latency. | ☐ |
| Exceeding the CPU limit makes Kubernetes kill the container immediately. | ☐ |
| Scaling out replicas or giving the model more CPU are both options Learn mentions. | ☐ |

<details><summary>💡 Hint</summary>

A container held at its CPU limit gets throttled, not killed.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The Pod may be throttled at its CPU limit, which can increase inference latency. | Yes | A Pod constantly at its CPU limit can be throttled. |
| Exceeding the CPU limit makes Kubernetes kill the container immediately. | No | CPU over-use is throttled; OOMKill is the memory behavior. |
| Scaling out replicas or giving the model more CPU are both options Learn mentions. | Yes | High CPU can indicate a need for more resources or more replicas. |

Compare usage with requests and limits; CPU pressure shows up as throttling and latency.

📘 Source: [Monitor application logs and metrics](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/2-monitor-logs-metrics)

</details>

## 5. `lp3m3-005`

CPU is spiking on the inference cluster. Put Learn's example investigation in order.

- Drill into Container insights to find the affected Pods
- Notice high CPU on the portal's Monitoring tab
- Use kubectl logs to inspect app behavior during the spike

<details><summary>💡 Hint</summary>

Start broad in the portal, narrow down to Pods, then read the logs.

</details>

<details><summary>✅ Answer</summary>

1. Notice high CPU on the portal's Monitoring tab
2. Drill into Container insights to find the affected Pods
3. Use kubectl logs to inspect app behavior during the spike

Overview in the portal → identify Pods in Container insights → targeted kubectl investigation.

📘 Source: [Monitor application logs and metrics](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/2-monitor-logs-metrics)

</details>

## 6. `lp3m3-006`

During an incident, you want to watch an inference container's stdout and stderr as it's written, from the Azure portal and without kubectl. Which feature do you use?

- **A.** Live Logs
- **B.** Diagnose and solve problems
- **C.** Container insights
- **D.** Metrics explorer

<details><summary>💡 Hint</summary>

You want the real-time stream of what the container prints.

</details>

<details><summary>✅ Answer</summary>

**A.** Live Logs

- A: Correct. Live Logs streams container stdout and stderr in real time in the portal.
- B: This runs guided diagnostics. It doesn't stream container output.
- C: Container insights is for dashboards and historical trends, not a live text stream.
- D: Metrics explorer charts numbers. It doesn't show log lines.

Live Logs streams container output in the browser; you can pause, search and switch containers in multi-container Pods.

📘 Source: [Monitor application logs and metrics](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/2-monitor-logs-metrics)

</details>

## 7. `lp3m3-007`

You want the terminal to keep printing new log lines from an inference Pod while you send test requests. Which command does that?

- **A.** kubectl logs -f <pod-name> -n ai-workloads
- **B.** kubectl top pods -n ai-workloads
- **C.** kubectl describe pod <pod-name>
- **D.** kubectl get pods -n ai-workloads -w

<details><summary>💡 Hint</summary>

One command prints container output, and a flag keeps it streaming.

</details>

<details><summary>✅ Answer</summary>

**A.** kubectl logs -f <pod-name> -n ai-workloads

- A: Correct. -f follows the log and prints new output as it arrives.
- B: This shows CPU and memory, not logs.
- C: describe shows configuration and events once. It doesn't stream logs.
- D: -w watches Pod status changes, not log output.

kubectl logs -f <pod> follows the container's output as new lines arrive. Add -c <container> for multi-container Pods.

📘 Source: [Monitor application logs and metrics](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/2-monitor-logs-metrics)

</details>

## 8. `lp3m3-008`

A worker Pod's memory use climbs slowly for hours before it's OOM-killed. Which view would have shown the problem earliest?

- **A.** The Pod's restart count
- **B.** The ingress 5xx error rate
- **C.** A single kubectl top snapshot after the restart
- **D.** Container insights memory trends over time

<details><summary>💡 Hint</summary>

A slow leak is a trend over time. Which tool keeps history?

</details>

<details><summary>✅ Answer</summary>

**D.** Container insights memory trends over time

- A: The restart count changes only after the kill has already happened.
- B: Errors may appear late, and they don't show memory growth.
- C: A snapshot after the restart shows the new, low usage, not the trend.
- D: Correct. Historical trends show a steady climb long before the kill.

Use Container insights dashboards for historical trends and cross-Pod analysis, and kubectl top for a quick point-in-time snapshot.

📘 Source: [Monitor application logs and metrics](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/2-monitor-logs-metrics)

</details>

## 9. `lp3m3-009`

Your team keeps dev and prod AI services in the same cluster. You need to filter logs for one AI service within prod. How do namespaces and labels split this job?

- **A.** Either one works, because they're interchangeable
- **B.** Namespaces apply to Services only, so labels do both jobs
- **C.** Labels separate the environments; namespaces select the service's Pods
- **D.** Namespaces separate the environments; labels select the service's Pods

<details><summary>💡 Hint</summary>

One is a boundary you pass with -n. The other is a tag you select with -l.

</details>

<details><summary>✅ Answer</summary>

**D.** Namespaces separate the environments; labels select the service's Pods

- A: They do different jobs: one scopes, and the other selects.
- B: Namespaces contain Pods too, and kubectl -n targets them.
- C: That's the other way round.
- D: Correct. Namespaces separate environments, access and quotas; labels select specific Pods inside a namespace.

Namespaces help you separate environments and control access and quotas, while labels select specific Pods inside a namespace when you scale, roll out or filter logs.

📘 Source: [Monitor application logs and metrics](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/2-monitor-logs-metrics)

</details>

## 10. `lp3m3-010`

You don't have kubectl configured, but you need a shell inside a running container from your browser. What should you use?

- **A.** The Monitoring tab on the Overview page
- **B.** Diagnose and solve problems in the AKS resource menu
- **C.** The Console tab for the Pod in the Azure portal
- **D.** Container insights Live Metrics

<details><summary>💡 Hint</summary>

Without kubectl, the portal can open a shell into a Pod.

</details>

<details><summary>✅ Answer</summary>

**C.** The Console tab for the Pod in the Azure portal

- A: The Monitoring tab shows metric graphs.
- B: That runs guided diagnostics, not an interactive shell.
- C: Correct. The Console tab opens an interactive terminal session in the browser.
- D: Live Metrics shows CPU, memory and network data.

Use the portal Console tab or kubectl exec -it … -- /bin/sh.

📘 Source: [Troubleshoot pods and services](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/3-troubleshoot-pods-services)

</details>

## 11. `lp3m3-011`

Inside a container you discover the MODEL_ENDPOINT variable is wrong. How should you fix it?

- **A.** Export the right value in the shell and leave it running
- **B.** Edit /etc/environment inside the container
- **C.** Restart the node so the container reloads
- **D.** Update the manifest or configuration and redeploy

<details><summary>💡 Hint</summary>

Changes made inside a running container disappear and can't be reproduced.

</details>

<details><summary>✅ Answer</summary>

**D.** Update the manifest or configuration and redeploy

- A: Manual changes inside a container are lost and aren't reproducible.
- B: Ad hoc edits inside containers break reproducibility.
- C: A node restart doesn't change the configured value.
- D: Correct. Make permanent changes through manifests and configuration.

Avoid ad hoc fixes inside containers; keep the environment reproducible.

📘 Source: [Troubleshoot pods and services](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/3-troubleshoot-pods-services)

</details>

## 12. `lp3m3-012`

A Pod keeps failing its readiness probe. In kubectl describe pod output, which two areas should you check? (Select two.)

- **A.** The node pool's billing tier and pricing details
- **B.** The registry's geo-replication settings for the image
- **C.** The Events section for probe failures
- **D.** The readiness probe definition for the AI endpoint

<details><summary>💡 Hint</summary>

describe shows both the probe's configuration and what happened to it.

</details>

<details><summary>✅ Answer</summary>

**C.** The Events section for probe failures  
**D.** The readiness probe definition for the AI endpoint

- A: Billing isn't in describe output and doesn't cause probe failures.
- B: Geo-replication doesn't affect readiness probes.
- C: Correct. Events record probe failures, failed pulls and scheduling issues.
- D: Correct. Describe shows the probe configuration.

Describe output shows probes, environment, mounts and events.

📘 Source: [Troubleshoot pods and services](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/3-troubleshoot-pods-services)

</details>

## 13. `lp3m3-013`

For each statement, select Yes if the statement is true. Otherwise, select No. All inference Pods are Running and Ready, but requests to the Service time out.

| Statement | Yes / No |
|---|---|
| Checking kubectl get endpointslices for the Service is a good next step. | ☐ |
| If no EndpointSlices exist, the Service can't route traffic even though the Pods are healthy. | ☐ |
| Healthy Pods prove that the Service's targetPort matches the container port. | ☐ |
| EndpointSlices list the node IPs, not Pod IPs, that receive the traffic. | ☐ |

<details><summary>💡 Hint</summary>

Healthy Pods don't prove routing works. Check what the Service actually routes to.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Checking kubectl get endpointslices for the Service is a good next step. | Yes | EndpointSlices list the Pod IPs that receive traffic. |
| If no EndpointSlices exist, the Service can't route traffic even though the Pods are healthy. | Yes | Without endpoints, the API can't receive traffic. |
| Healthy Pods prove that the Service's targetPort matches the container port. | No | Pod health doesn't validate the Service's port mapping. |
| EndpointSlices list the node IPs, not Pod IPs, that receive the traffic. | No | EndpointSlices list the actual Pod IPs that receive traffic. |

Check selectors, ports and EndpointSlices when Pods are healthy but unreachable.

📘 Source: [Troubleshoot pods and services](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/3-troubleshoot-pods-services)

</details>

## 14. `lp3m3-014`

Several Pods across the namespace failed in the last ten minutes for different reasons. Which command gives one view of recent events across Pods and controllers?

- **A.** kubectl get events -n ai-workloads
- **B.** kubectl exec -it <pod> -- /bin/sh
- **C.** kubectl logs -f <pod> -n ai-workloads
- **D.** kubectl top pods -n ai-workloads

<details><summary>💡 Hint</summary>

describe pod is for one Pod. You want events across the whole namespace.

</details>

<details><summary>✅ Answer</summary>

**A.** kubectl get events -n ai-workloads

- A: Correct. get events reviews recent cluster events across Pods and controllers.
- B: That opens a shell in one container.
- C: That streams one Pod's application output.
- D: That shows resource usage only.

Use kubectl describe pod for one Pod's events and kubectl get events for a wider view.

📘 Source: [Troubleshoot pods and services](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/3-troubleshoot-pods-services)

</details>

## 15. `lp3m3-015`

You need one view of a Pod's events, environment variables and mounted volumes, including Secrets. Which command gives you all of that?

- **A.** kubectl logs <pod-name>
- **B.** kubectl top pod <pod-name>
- **C.** kubectl get pod <pod-name> -o name
- **D.** kubectl describe pod <pod-name>

<details><summary>💡 Hint</summary>

You want a detailed description of one Pod, not its output.

</details>

<details><summary>✅ Answer</summary>

**D.** kubectl describe pod <pod-name>

- A: Logs show application output, not configuration or events.
- B: top shows resource usage only.
- C: This prints only the Pod's name.
- D: Correct. describe pod shows probes, environment, mounts and events together.

kubectl describe pod shows the Pod's probes, environment, mounts and Events, which makes it the first stop for startup and probe problems.

📘 Source: [Troubleshoot pods and services](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/3-troubleshoot-pods-services)

</details>

## 16. `lp3m3-016`

You want to call a container's own health endpoint, http://localhost:8080/health, without changing or rebuilding the image. What do you do?

- **A.** Rebuild the image with an extra probe that logs the result
- **B.** Port-forward to the kubelet's port on the node
- **C.** SSH into the node and curl the Pod's localhost
- **D.** Exec into the container and run curl against localhost

<details><summary>💡 Hint</summary>

localhost means inside the container. How do you run a command in there?

</details>

<details><summary>✅ Answer</summary>

**D.** Exec into the container and run curl against localhost

- A: That changes the image, which you wanted to avoid.
- B: The kubelet isn't your app. Port-forward to the Service or Pod instead.
- C: localhost on the node isn't the container's localhost.
- D: Correct. kubectl exec (or the portal Console) lets you run simple HTTP checks from inside the container.

Use kubectl exec -it <pod> -- /bin/sh (or the portal Console tab) to inspect files, check variables and run commands such as curl http://localhost:8080/health.

📘 Source: [Troubleshoot pods and services](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/3-troubleshoot-pods-services)

</details>

## 17. `lp3m3-017`

Several services on the cluster have problems, and you suspect node health or cluster configuration. Why start with Diagnose and solve problems in the portal?

- **A.** It runs diagnostics for common issues automatically and suggests fixes
- **B.** It needs kubectl configured first, so it's more precise
- **C.** It shows more detail than kubectl describe for each Pod
- **D.** It edits the manifests to fix problems for you

<details><summary>💡 Hint</summary>

For cluster-wide symptoms, start with the tool that checks common problems for you.

</details>

<details><summary>✅ Answer</summary>

**A.** It runs diagnostics for common issues automatically and suggests fixes

- A: Correct. It gives guided troubleshooting for connectivity, node health and configuration.
- B: It's a portal tool, so you don't need kubectl at all.
- C: kubectl describe is still the detailed per-Pod view.
- D: It suggests fixes. It doesn't change your manifests.

Diagnose and solve problems gives guided troubleshooting for common issues such as connectivity, node health and cluster configuration, runs diagnostics automatically and suggests fixes.

📘 Source: [Troubleshoot pods and services](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/3-troubleshoot-pods-services)

</details>

## 18. `lp3m3-018`

Ingress isn't configured yet, and you want to test the inference Service from your laptop. Which command should you use?

- **A.** kubectl top pods -n ai-workloads to read Pod usage
- **B.** az aks scale --node-count 3 to add test capacity
- **C.** kubectl port-forward service/inference-api 8080:80
- **D.** kubectl get ingress -n ai-workloads to list ingress routes

<details><summary>💡 Hint</summary>

Test from your laptop without exposing the Service publicly.

</details>

<details><summary>✅ Answer</summary>

**C.** kubectl port-forward service/inference-api 8080:80

- A: top shows resource usage.
- B: Scaling nodes doesn't create a test path.
- C: Correct. Port-forwarding sends local traffic to the Service inside the cluster.
- D: Listing ingress shows nothing useful when none is configured.

Port-forwarding lets you test before exposing endpoints to users.

📘 Source: [Verify service connectivity and endpoints](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/4-verify-connectivity)

</details>

## 19. `lp3m3-019`

After `kubectl port-forward service/inference-api 8080:80`, which URL reaches the API from your laptop?

- **A.** http://inference-api:8080/api/inference
- **B.** The Service's cluster IP on port 8080
- **C.** http://localhost:8080/api/inference
- **D.** http://localhost:80/api/inference

<details><summary>💡 Hint</summary>

In local:remote, the first number is the port on your machine.

</details>

<details><summary>✅ Answer</summary>

**C.** http://localhost:8080/api/inference

- A: That DNS name isn't resolvable from your laptop.
- B: The cluster IP isn't reachable from your laptop.
- C: Correct. Local port 8080 forwards to Service port 80.
- D: The local side of the forward is 8080.

In 8080:80, the first number is the local port.

📘 Source: [Verify service connectivity and endpoints](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/4-verify-connectivity)

</details>

## 20. `lp3m3-020`

The portal shows the inference Service with an empty Endpoints list. Pods are running with the label `app: inference-api-v2`. What should you do?

- **A.** Run kubectl port-forward to create the missing endpoints
- **B.** Add more replicas so the Service discovers them automatically
- **C.** Align Pod labels and the Service selector, then check EndpointSlices
- **D.** Switch the Service type from LoadBalancer to ClusterIP

<details><summary>💡 Hint</summary>

Running Pods but no endpoints: the Service isn't finding them. Why?

</details>

<details><summary>✅ Answer</summary>

**C.** Align Pod labels and the Service selector, then check EndpointSlices

- A: Port-forwarding tests a path; it doesn't create endpoints.
- B: More Pods with the same wrong label still won't match.
- C: Correct. Endpoints come from matching labels; fix the mismatch and verify.
- D: The type doesn't affect which Pods are selected.

Standardize labels so Services and ingress resources select the correct Pods.

📘 Source: [Verify service connectivity and endpoints](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/4-verify-connectivity)

</details>

## 21. `lp3m3-021`

Where do you find the external hostname or IP of an ingress resource with kubectl get ingress or in the portal?

- **A.** The targetPort field
- **B.** The CLUSTER-IP column
- **C.** The selector labels
- **D.** The ADDRESS column

<details><summary>💡 Hint</summary>

Services and ingresses report their public address in different columns.

</details>

<details><summary>✅ Answer</summary>

**D.** The ADDRESS column

- A: targetPort is the container port.
- B: Cluster IPs are internal addresses.
- C: Selectors choose Pods; they aren't addresses.
- D: Correct. Ingress resources show their external hostname or IP in the Address column.

LoadBalancer Services show EXTERNAL-IP; ingress resources show ADDRESS.

📘 Source: [Verify service connectivity and endpoints](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/4-verify-connectivity)

</details>

## 22. `lp3m3-022`

The Service's labels match the Pods, and its EndpointSlices list the Pod IPs, but clients get connection refused. What else should you check?

- **A.** Whether the namespace name matches the environment
- **B.** Whether targetPort matches the port the container listens on
- **C.** Whether the Pods' restart count is zero
- **D.** Whether the image came from a private registry

<details><summary>💡 Hint</summary>

Traffic reaches the right Pods but finds nothing listening. Which number tells the Service where to send it?

</details>

<details><summary>✅ Answer</summary>

**B.** Whether targetPort matches the port the container listens on

- A: Naming doesn't affect routing within a namespace.
- B: Correct. With endpoints in place, a wrong targetPort sends traffic to a port nobody listens on.
- C: A zero restart count is healthy and doesn't explain refused connections.
- D: The Pods are running, so the image pull already worked.

When Pods are healthy and endpoints exist but connections fail, check that the Service's targetPort matches the container port, and that ingress rules point to the right Service and port.

📘 Source: [Verify service connectivity and endpoints](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/4-verify-connectivity)

</details>

## 23. `lp3m3-023`

A LoadBalancer Service still has no external IP after several minutes. Where in the portal do you check first?

- **A.** The node pool scaling settings
- **B.** The Live Logs stream of an inference Pod
- **C.** The activity log, and nothing else
- **D.** Services and ingresses under Kubernetes resources

<details><summary>💡 Hint</summary>

Look in the portal section that lists Services and their addresses.

</details>

<details><summary>✅ Answer</summary>

**D.** Services and ingresses under Kubernetes resources

- A: Node scaling doesn't show Service addresses.
- B: Container output doesn't show the Service's address.
- C: The Services and ingresses view is the direct place to check a Service's address.
- D: Correct. It shows every Service with external IPs, selectors, ports and endpoints.

The Services and ingresses section shows all Services across namespaces, with external IPs, selector labels, ports and current endpoints.

📘 Source: [Verify service connectivity and endpoints](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/4-verify-connectivity)

</details>


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
