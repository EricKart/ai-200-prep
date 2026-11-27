# LP3 · M3: Monitor and troubleshoot applications on Azure Kubernetes Service

> **Learning path 3:** Deploy and monitor applications on Azure Kubernetes Service · **Skill area 1:** Develop and deploy containerized solutions · about 65 min on Microsoft Learn  
> Study it interactively at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-3/monitor-apps-azure-kubernetes-service)

When something breaks on AKS, you need to know where to look. This module covers logs and metrics, troubleshooting Pods and Services, and checking connectivity end to end.

**In this lesson**

1. [Monitor application logs and metrics](#monitor-application-logs-and-metrics)
2. [Troubleshoot pods and services](#troubleshoot-pods-and-services)
3. [Verify service connectivity and endpoints](#verify-service-connectivity-and-endpoints)

## Monitor application logs and metrics

📘 Microsoft Learn: [Monitor application logs and metrics](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/2-monitor-logs-metrics)

Use the **portal for the big picture** (Monitoring tab, Container insights, Live Logs) and **kubectl for the close-up** (logs of one Pod, `kubectl top` for a quick usage snapshot). Compare usage with the requests and limits you set.

**Key facts**

- Key signals for AI workloads: **latency and throughput**, **error rates** (HTTP 5xx, timeouts), **Pod restarts and exit codes**, **CPU and memory vs requests and limits**.
- Portal logs: AKS → Kubernetes resources → **Workloads** → select a workload → **Live Logs** (stdout/stderr in real time; pause, search, switch containers). **Container insights** under Monitoring → Insights gives a cluster-wide view filtered by namespace, Pod and container.
- kubectl: `kubectl get pods -n ai-workloads`, `kubectl logs <pod> -n ai-workloads`, `-f` to stream, `-c inference-api` for one container in a multi-container Pod.
- **Namespaces** separate environments and control access and quotas; **labels** select specific Pods within a namespace.
- Portal metrics: **Monitoring tab** on the Overview page (CPU and memory per node pool, open in metrics explorer); Insights → Nodes/Controllers/Containers; **Live Metrics** for a Pod.
- `kubectl top nodes` and `kubectl top pods` need the **metrics server**. A Pod constantly at its CPU limit can be **throttled**, raising inference latency.
- Workflow: Monitoring tab for health → Live Logs while investigating → kubectl logs to filter or pipe → kubectl top for a snapshot → Container insights for history and cross-Pod analysis.
- Practices: include request ids, model names and versions in logs; prefer **structured logging**; measure against latency and error-budget targets.

| Need | Tool |
|---|---|
| Quick health overview | Portal Monitoring tab |
| Watch output live in a browser | Live Logs (Workloads) |
| Historical trends across Pods | Container insights |
| Filter or pipe one Pod's logs | kubectl logs |
| Current CPU and memory snapshot | kubectl top (metrics server) |

> [!WARNING]
> **Exam traps**
>
> - kubectl top needs the **metrics server**.
> - Use **-c** to pick a container in a multi-container Pod.

## Troubleshoot pods and services

📘 Microsoft Learn: [Troubleshoot pods and services](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/3-troubleshoot-pods-services)

Go from symptom to cause: read the **Pod status**, then **describe** the Pod to read its events, peek **inside** the container if needed, and check the **Service** really points at the Pods. Fix it in the manifest, not by hand inside the container.

**Key facts**

- Pod problems: **ImagePullBackOff** (wrong image reference or registry credentials), **CrashLoopBackOff** (starts and exits with an error), **Pending** (resource constraints), frequent restarts (memory leaks, unhandled exceptions).
- Portal: **Workloads** shows status, restart counts and age; **Live Logs**; **Diagnose and solve problems** runs guided diagnostics (connectivity, node health, configuration) and suggests fixes.
- `kubectl describe pod`: probes, environment variables and mounted Secrets, volume mounts, and **events** (failed pulls, scheduling, probe failures). `kubectl get events -n …` shows recent events cluster-wide.
- Inside the container: portal **Console** tab, or `kubectl exec -it <pod> -- /bin/sh`. List model files, check env vars, `curl http://localhost:8080/health`.
- Make permanent fixes in **manifests and source**, not manual changes inside containers.
- Services: portal **Services and ingresses**; `kubectl describe service`; `kubectl get endpointslices -l kubernetes.io/service-name=<name>`. Check selector, ports/targetPorts and EndpointSlices. No EndpointSlices = no traffic even if Pods are healthy.

| Tool | Shows |
|---|---|
| Workloads (portal) | Status, restarts, age |
| Diagnose and solve problems | Guided diagnostics with suggested fixes |
| kubectl describe pod | Probes, env, mounts, events |
| Console / kubectl exec | Shell inside the container |
| kubectl get endpointslices | Pod IPs that actually receive traffic |

> [!WARNING]
> **Exam traps**
>
> - Healthy Pods + no EndpointSlices = Service selector or port problem.
> - Don't patch running containers by hand; change the manifest.

## Verify service connectivity and endpoints

📘 Microsoft Learn: [Verify service connectivity and endpoints](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/4-verify-connectivity)

Test the path a request takes: from your laptop straight into the Service (**port-forward**), then from the internet through the **load balancer or ingress**. If the Service has no endpoints, fix the labels first.

**Key facts**

- Service types: **ClusterIP** (inside only), **LoadBalancer** (external through Azure Load Balancer), **NodePort** (port on each node). Client-facing AI APIs usually use a LoadBalancer Service or an **ingress controller**.
- Portal **Services and ingresses**: type, cluster IP, external IP, ports, selector labels and **Endpoints**; for ingress, host rules, paths, backends and the **Address** column.
- kubectl: `kubectl describe service` and `kubectl get endpointslices -l kubernetes.io/service-name=inference-api`. Empty EndpointSlices → fix Pod labels or the Service selector, then confirm they appear.
- `kubectl port-forward service/inference-api 8080:80 -n ai-workloads` forwards local port 8080 to Service port 80; then `curl http://localhost:8080/api/inference`. Useful before ingress exists.
- External addresses: `kubectl get service inference-api` (EXTERNAL-IP) and `kubectl get ingress` (ADDRESS).
- Practices: start with the portal, standardize labels, **test before exposing** (port-forward), combine portal and kubectl, pair connectivity checks with logs and metrics.

> [!WARNING]
> **Exam traps**
>
> - port-forward `8080:80` = local 8080 → Service port 80.
> - Ingress external address appears in the **Address** column.

## Check yourself

- **Practice questions:** [lp3m3 on GitHub](../../practice/lp3m3.md), or [on the site](https://aryantripathi.dev/ai-200/lp-3/monitor-apps-azure-kubernetes-service) with hints and saved progress
- **Cheat sheet:** [Learning path 3](../cheatsheets/lp3.md)
- **Microsoft Learn exercise:** [Troubleshoot apps on Azure Kubernetes Service](https://learn.microsoft.com/en-us/training/modules/monitor-apps-azure-kubernetes-service/5-exercise-troubleshoot-apps)
- **Hands-on lab:** [labs/](../../labs/README.md) has a lab for this learning path

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
