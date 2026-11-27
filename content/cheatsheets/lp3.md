# LP3 cheat sheet: Deploy and monitor applications on Azure Kubernetes Service

> Skill area 1 · one page to review before the exam · full lessons in [content/lessons](../lessons/) · practise at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-3)

## Which one?

| You need… | Answer | Don't confuse with |
|---|---|---|
| Stable internal name for Pods | ClusterIP Service | LoadBalancer = public IP |
| Public production API | LoadBalancer Service (or ingress controller) | NodePort is for testing |
| Pod stuck Pending: insufficient memory | Lower requests or add nodes | Not an image or app problem |
| Service has no endpoints | Fix Pod labels / Service selector | Changing Service type won't help |
| Config file updates without Pod restart | ConfigMap mounted as a volume (no subPath) | Env vars need a restart |
| Secrets stay in a vault, audited, rotated | Key Vault + Secrets Store CSI Driver | Plain Kubernetes Secrets |
| Pods on many nodes share one volume | azurefile-csi (ReadWriteMany) | managed-csi disks are ReadWriteOnce |
| Test a Service from your laptop | kubectl port-forward | kubectl top shows usage |

## Must remember

### M1: Deploy applications to Azure Kubernetes Service

- Requests drive **scheduling**; limits cap usage.
- Learn recommends **3** replicas for production APIs.
- ClusterIP is the **default** type.
- port ≠ targetPort: clients use port; the container listens on targetPort.
- EXTERNAL-IP `<pending>` = load balancer still provisioning; wait.
- kubectl apply returns before the Pods are ready.

Lesson: [lp3m1](../lessons/lp3m1.md) · Practice: [lp3m1](../../practice/lp3m1.md)

### M2: Configure applications on Azure Kubernetes Service

- 1 MiB maximum per ConfigMap.
- Immutable ConfigMaps can't be edited or made mutable again.
- Registry credentials use **kubernetes.io/dockerconfigjson**; TLS uses **kubernetes.io/tls**.
- After rotating a plain Kubernetes Secret used as env vars, trigger a rollout.
- Several Pods on different nodes writing the same volume → **Azure Files (RWX)**.
- managed-csi is the **default** class.

Lesson: [lp3m2](../lessons/lp3m2.md) · Practice: [lp3m2](../../practice/lp3m2.md)

### M3: Monitor and troubleshoot applications on Azure Kubernetes Service

- kubectl top needs the **metrics server**.
- Use **-c** to pick a container in a multi-container Pod.
- Healthy Pods + no EndpointSlices = Service selector or port problem.
- Don't patch running containers by hand; change the manifest.
- port-forward `8080:80` = local 8080 → Service port 80.
- Ingress external address appears in the **Address** column.

Lesson: [lp3m3](../lessons/lp3m3.md) · Practice: [lp3m3](../../practice/lp3m3.md)

## Commands and syntax you'll see

```text
kubectl create secret generic api-secrets --from-literal=api-key=…
kubectl get svc
kubectl apply -f deployment.yaml
kubectl get pods
kubectl logs <pod>
kubectl run -it --rm debug --image=alpine:latest --restart=Never -- sh
az acr repository list
kubectl describe pod
kubectl top nodes
az aks scale --node-count 3
kubectl get pods --show-labels
kubectl describe configmap
kubectl create secret generic app-secrets --from-literal=…
kubectl describe secret
kubectl get secrets
kubectl describe pvc
kubectl get pods -n ai-workloads
kubectl logs <pod> -n ai-workloads
kubectl top pods
kubectl get events -n …
kubectl exec -it <pod> -- /bin/sh
curl http://localhost:8080/health
kubectl describe service
kubectl get endpointslices -l kubernetes.io/service-name=<name>
kubectl get endpointslices -l kubernetes.io/service-name=inference-api
kubectl port-forward service/inference-api 8080:80 -n ai-workloads
curl http://localhost:8080/api/inference
kubectl get service inference-api
kubectl get ingress
```

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
