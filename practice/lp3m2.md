# Practice: LP3 · M2 Configure applications on Azure Kubernetes Service

> 24 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp3m2.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-3/configure-apps-azure-kubernetes-service)

## 1. `lp3m2-001`

What is the maximum total size of a single ConfigMap?

- **A.** 64 KiB
- **B.** 10 MiB
- **C.** 128 MB
- **D.** 1 MiB

<details><summary>💡 Hint</summary>

ConfigMaps are meant for small settings, and the limit is measured in mebibytes.

</details>

<details><summary>✅ Answer</summary>

**D.** 1 MiB

- A: Learn gives a larger limit.
- B: Learn gives a smaller limit.
- C: 128 MB is the dynamic sessions upload limit, not a ConfigMap limit.
- D: Correct. ConfigMap data is limited to 1 MiB.

The 1 MiB limit keeps node synchronization fast and etcd storage efficient.

📘 Source: [Define ConfigMaps for application settings](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/2-define-configmaps)

</details>

## 2. `lp3m2-002`

An app has 25 settings in one ConfigMap and you want all of them as environment variables without listing each key. What should you use?

- **A.** valueFrom with configMapKeyRef
- **B.** valueFrom with secretKeyRef
- **C.** envFrom with configMapRef
- **D.** A PersistentVolumeClaim

<details><summary>💡 Hint</summary>

One field loads every key at once instead of naming each one.

</details>

<details><summary>✅ Answer</summary>

**C.** envFrom with configMapRef

- A: configMapKeyRef references one key at a time.
- B: secretKeyRef reads from a Secret.
- C: Correct. envFrom loads all keys as environment variables in one declaration.
- D: A PVC is storage, not configuration injection.

Bulk-load with envFrom/configMapRef; pick single keys with valueFrom/configMapKeyRef.

📘 Source: [Define ConfigMaps for application settings](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/2-define-configmaps)

</details>

## 3. `lp3m2-003`

You change a feature flag in a ConfigMap. Pods that read it as an environment variable still show the old value. What should you do?

- **A.** Wait for the kubelet's next sync period
- **B.** Raise the ConfigMap size limit
- **C.** Restart the Pods so they read the new value
- **D.** Mark the ConfigMap as immutable

<details><summary>💡 Hint</summary>

Environment variables are read when the container starts.

</details>

<details><summary>✅ Answer</summary>

**C.** Restart the Pods so they read the new value

- A: Kubelet sync updates mounted files, not environment variables.
- B: Size has nothing to do with it.
- C: Correct. Environment variables from ConfigMaps need a Pod restart.
- D: Immutability prevents changes; it doesn't apply them.

Mounted ConfigMap files update automatically; environment variables don't.

📘 Source: [Define ConfigMaps for application settings](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/2-define-configmaps)

</details>

## 4. `lp3m2-004`

For each statement, select Yes if the statement is true. Otherwise, select No. A ConfigMap named `app-settings` is marked `immutable: true`.

| Statement | Yes / No |
|---|---|
| You can edit its data later with kubectl apply. | ☐ |
| You can set immutable back to false if you need to change it. | ☐ |
| To change settings, you create a new ConfigMap such as app-settings-v2. | ☐ |
| Immutable ConfigMaps can reduce load on the API server in large clusters. | ☐ |

<details><summary>💡 Hint</summary>

Immutable means you can't edit it or undo the flag. You replace it with a new one.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| You can edit its data later with kubectl apply. | No | You can't change an immutable ConfigMap's data. |
| You can set immutable back to false if you need to change it. | No | You can't revert the immutable setting. |
| To change settings, you create a new ConfigMap such as app-settings-v2. | Yes | Delete and recreate, often with a new name. |
| Immutable ConfigMaps can reduce load on the API server in large clusters. | Yes | Kubernetes can close watches on immutable ConfigMaps. |

Use immutable ConfigMaps for configuration tied to specific app versions.

📘 Source: [Define ConfigMaps for application settings](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/2-define-configmaps)

</details>

## 5. `lp3m2-005`

A config file is mounted from a ConfigMap with a **subPath** mount. After the ConfigMap changes, the file in the container never updates. Why?

- **A.** The file exceeds the 1 MiB ConfigMap size limit
- **B.** The ConfigMap has to be marked immutable first
- **C.** Mounted files update after you run kubectl describe
- **D.** Automatic updates don't apply to subPath mounts

<details><summary>💡 Hint</summary>

Mounted ConfigMaps update by themselves, with one exception for how the file is mounted.

</details>

<details><summary>✅ Answer</summary>

**D.** Automatic updates don't apply to subPath mounts

- A: An oversized ConfigMap wouldn't have been accepted in the first place.
- B: Immutable ConfigMaps can't change at all.
- C: describe only reads state; it doesn't trigger updates.
- D: Correct. Learn says automatic updates don't apply when you use subPath mounts.

Volume-mounted ConfigMap files update on kubelet sync, except with subPath.

📘 Source: [Define ConfigMaps for application settings](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/2-define-configmaps)

</details>

## 6. `lp3m2-006`

An inference API needs only SERVICE_ENDPOINT from a ConfigMap that holds 20 keys, and you want the container's environment to stay small. How should the Deployment reference it?

- **A.** An env entry with valueFrom.secretKeyRef pointing at the ConfigMap
- **B.** envFrom with configMapRef, so that every key is loaded
- **C.** valueFrom.configMapKeyRef for that one key
- **D.** A volume mount of the whole ConfigMap at /etc/config

<details><summary>💡 Hint</summary>

One option picks a single key. Another loads the whole ConfigMap.

</details>

<details><summary>✅ Answer</summary>

**C.** valueFrom.configMapKeyRef for that one key

- A: secretKeyRef reads Secrets, not ConfigMaps.
- B: envFrom loads all 20 keys, which is the opposite of what you want.
- C: Correct. configMapKeyRef injects one specific key as an environment variable.
- D: That exposes all keys as files rather than one environment variable.

Use valueFrom with configMapKeyRef to reference specific keys. envFrom with configMapRef loads every key as an environment variable.

📘 Source: [Define ConfigMaps for application settings](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/2-define-configmaps)

</details>

## 7. `lp3m2-007`

A legacy model server reads its settings from files in /etc/model rather than from environment variables. You mount a ConfigMap with keys log_level and timeout_seconds as a volume at /etc/model. What does the container see?

- **A.** One file per key, such as /etc/model/log_level
- **B.** One file, /etc/model/configmap.yaml, with the whole manifest
- **C.** Environment variables named LOG_LEVEL and TIMEOUT_SECONDS
- **D.** An empty folder until you run kubectl apply again

<details><summary>💡 Hint</summary>

With a volume, keys become something on disk. One per key.

</details>

<details><summary>✅ Answer</summary>

**A.** One file per key, such as /etc/model/log_level

- A: Correct. Each key in a mounted ConfigMap becomes a file whose content is the value.
- B: Kubernetes projects keys as files. It doesn't copy the manifest.
- C: A volume mount creates files, not environment variables.
- D: The files appear when the Pod starts with the volume mounted.

Mount a ConfigMap as a volume and add a volumeMount; each key becomes a file under the mount path, and the file's content is the value.

📘 Source: [Define ConfigMaps for application settings](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/2-define-configmaps)

</details>

## 8. `lp3m2-008`

Twelve services across three clusters must share feature flags managed in one central place, and the apps should keep reading standard ConfigMaps. What does Learn suggest?

- **A.** Store the flags in a Kubernetes Secret, because Secrets sync across clusters
- **B.** Bake the flags into each image so that every cluster gets the same values
- **C.** App Configuration and its Kubernetes Provider
- **D.** Copy one configmap.yaml into each cluster with a script

<details><summary>💡 Hint</summary>

You want one central store, while the apps keep using normal Kubernetes resources.

</details>

<details><summary>✅ Answer</summary>

**C.** App Configuration and its Kubernetes Provider

- A: Secrets don't sync across clusters, and flags aren't sensitive.
- B: That ties configuration to images, which ConfigMaps exist to avoid.
- C: Correct. The provider runs in the cluster and creates standard ConfigMaps from App Configuration data.
- D: Copies drift apart. That isn't central management.

The Azure App Configuration Kubernetes Provider runs in your cluster and generates standard ConfigMaps from data stored in App Configuration, for centralized configuration across apps and environments.

📘 Source: [Define ConfigMaps for application settings](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/2-define-configmaps)

</details>

## 9. `lp3m2-009`

After you apply a new ConfigMap and Deployment, you want to confirm FEATURE_X_ENABLED reached the running container. Which command checks it directly?

- **A.** kubectl exec <pod> -- printenv
- **B.** kubectl describe configmap app-settings
- **C.** kubectl get deployment web-api
- **D.** kubectl logs <pod-name> --previous

<details><summary>💡 Hint</summary>

Look inside the running container instead of at the source object.

</details>

<details><summary>✅ Answer</summary>

**A.** kubectl exec <pod> -- printenv

- A: Correct. This prints the container's actual environment.
- B: This shows the ConfigMap, not whether a running container received it.
- C: This shows replica counts, not environment variables.
- D: Logs show program output, not the environment it received.

kubectl describe configmap shows the source data; kubectl exec <pod> -- printenv confirms what the container actually received.

📘 Source: [Define ConfigMaps for application settings](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/2-define-configmaps)

</details>

## 10. `lp3m2-010`

Which Kubernetes Secret type does Learn recommend for container registry credentials?

- **A.** kubernetes.io/basic-auth
- **B.** Opaque
- **C.** kubernetes.io/tls
- **D.** kubernetes.io/dockerconfigjson

<details><summary>💡 Hint</summary>

Registry credentials have their own Secret type, named after a Docker config file.

</details>

<details><summary>✅ Answer</summary>

**D.** kubernetes.io/dockerconfigjson

- A: Learn doesn't list this type.
- B: Opaque suits most string values such as API keys.
- C: tls is for certificates and keys.
- D: Correct. Use kubernetes.io/dockerconfigjson for registry credentials.

Opaque for general strings, dockerconfigjson for registries, tls for certificates.

📘 Source: [Implement secrets for sensitive data](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/3-implement-secrets)

</details>

## 11. `lp3m2-011`

Compliance requires a detailed audit trail of each secret access, automatic rotation, and secrets that never leave a dedicated vault. Which approach fits?

- **A.** ConfigMaps mounted as immutable files
- **B.** Azure Key Vault with the Secrets Store CSI Driver
- **C.** Opaque Kubernetes Secrets with etcd encryption
- **D.** Secret values stored in the Deployment manifest

<details><summary>💡 Hint</summary>

Which integration keeps secrets in their dedicated store and mounts them into Pods?

</details>

<details><summary>✅ Answer</summary>

**B.** Azure Key Vault with the Secrets Store CSI Driver

- A: ConfigMaps are for non-sensitive data.
- B: Correct. Secrets stay in Key Vault, mounted as files, with rotation and audit logging.
- C: Encryption at rest helps, but it doesn't give vault audit trails or rotation.
- D: Never put secret values in manifests.

Choose direct Key Vault integration for fine-grained audit and secrets that stay in the vault.

📘 Source: [Implement secrets for sensitive data](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/3-implement-secrets)

</details>

## 12. `lp3m2-012`

For each statement, select Yes if the statement is true. Otherwise, select No. A team uses the Azure App Configuration Kubernetes Provider with Key Vault references.

| Statement | Yes / No |
|---|---|
| App Configuration stores the actual secret values. | ☐ |
| The provider creates native Kubernetes Secret resources with the resolved values. | ☐ |
| Each application must authenticate to Key Vault itself to read its secrets. | ☐ |

<details><summary>💡 Hint</summary>

App Configuration holds references, not values. The provider resolves them into Kubernetes resources.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| App Configuration stores the actual secret values. | No | It stores references; the values stay in Key Vault. |
| The provider creates native Kubernetes Secret resources with the resolved values. | Yes | The provider resolves references and generates Kubernetes Secrets. |
| Each application must authenticate to Key Vault itself to read its secrets. | No | Apps receive standard Kubernetes resources without authenticating to Key Vault. |

App Configuration centralizes which secrets each app uses; Key Vault keeps the values.

📘 Source: [Implement secrets for sensitive data](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/3-implement-secrets)

</details>

## 13. `lp3m2-013`

You rotated a database password in a plain Kubernetes Secret that Pods read through secretKeyRef environment variables. Pods still use the old password. What does Learn recommend?

- **A.** Mark the Secret immutable to force a refresh
- **B.** Wait, because the CSI driver polls and updates the variables
- **C.** Run kubectl describe secret to push the new value
- **D.** Trigger a Deployment rollout so Pods receive the new value

<details><summary>💡 Hint</summary>

Environment variables from Secrets don't change in running Pods.

</details>

<details><summary>✅ Answer</summary>

**D.** Trigger a Deployment rollout so Pods receive the new value

- A: Immutability prevents changes; it doesn't refresh Pods.
- B: There's no CSI driver here; that's the Key Vault option, and it updates files.
- C: describe only shows metadata and keys.
- D: Correct. After updates, trigger rollouts so Pods receive new values.

Rotate regularly and roll out Deployments so Pods pick up new Secret values.

📘 Source: [Implement secrets for sensitive data](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/3-implement-secrets)

</details>

## 14. `lp3m2-014`

A teammate asks you to prove the Secret app-secrets has the keys DB_CONNECTION and API_KEY, without printing their values. Which command does that?

- **A.** kubectl logs <pod-name>
- **B.** kubectl describe secret app-secrets
- **C.** kubectl exec <pod-name> -- printenv
- **D.** kubectl get secret app-secrets -o yaml

<details><summary>💡 Hint</summary>

One command lists keys and sizes but leaves the values out.

</details>

<details><summary>✅ Answer</summary>

**B.** kubectl describe secret app-secrets

- A: Logs don't list a Secret's keys.
- B: Correct. describe secret shows metadata and keys without showing the values.
- C: This prints the values inside the container.
- D: This prints the data field, which exposes the encoded values.

kubectl get secrets lists Secrets (name, type, data count, age); kubectl describe secret <name> shows metadata and keys without exposing values.

📘 Source: [Implement secrets for sensitive data](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/3-implement-secrets)

</details>

## 15. `lp3m2-015`

A GitOps repository manages every Kubernetes resource. A developer adds secret.yaml with the model API key written in it as a literal value. What does Learn's guidance say?

- **A.** It's fine, because Kubernetes encodes Secret values in base64
- **B.** It's fine if the repository is private
- **C.** Don't commit literal values; create Secrets in the cluster instead
- **D.** Convert it to a ConfigMap so that GitOps can manage it

<details><summary>💡 Hint</summary>

Think about where the value ends up once it's committed.

</details>

<details><summary>✅ Answer</summary>

**C.** Don't commit literal values; create Secrets in the cluster instead

- A: Encoding isn't protection. The value is still in source control.
- B: A private repository still keeps the secret in its history for everyone with access.
- C: Correct. Committing literal values exposes them in source control and history.
- D: ConfigMaps are for non-sensitive data, so that's worse.

Never commit Secret manifests with literal values. Create Secrets directly in the cluster, or use external secret management such as Key Vault with the CSI driver.

📘 Source: [Implement secrets for sensitive data](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/3-implement-secrets)

</details>

## 16. `lp3m2-016`

A platform team wants to manage, in one place, which Key Vault secrets each of 15 apps receives. The apps should read ordinary Kubernetes Secrets, and values must stay in Key Vault. Which option fits best?

- **A.** A ConfigMap that lists each app's secret names
- **B.** The Secrets Store CSI Driver, with secrets mounted as files in each Pod
- **C.** A Secret manifest per app in Git, applied by the pipeline
- **D.** App Configuration Key Vault references, via its Kubernetes Provider

<details><summary>💡 Hint</summary>

The key words are "manage the mappings centrally" and "ordinary Kubernetes Secrets".

</details>

<details><summary>✅ Answer</summary>

**D.** App Configuration Key Vault references, via its Kubernetes Provider

- A: A ConfigMap of names doesn't resolve or deliver secret values.
- B: The CSI driver keeps secrets in the vault but mounts them as files. It doesn't centralize the mappings.
- C: That puts secret values in source control.
- D: Correct. It centralizes secret mappings while values stay in Key Vault and arrive as Kubernetes Secrets.

Choose App Configuration with Key Vault references to manage secret mappings centrally and provide secrets as standard Kubernetes resources. Choose the Key Vault CSI driver for fine-grained per-access audit with secrets kept only in the vault.

📘 Source: [Implement secrets for sensitive data](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/3-implement-secrets)

</details>

## 17. `lp3m2-017`

You're creating a new AKS cluster for an AI service and want an extra layer of protection for Secrets stored in the cluster itself. What does Learn recommend configuring at creation time?

- **A.** A larger node size for the system pool
- **B.** Public network access to the API server
- **C.** Immutable ConfigMaps for every Secret
- **D.** etcd encryption at rest

<details><summary>💡 Hint</summary>

Secrets are stored in the cluster's key-value store. How do you protect data at rest?

</details>

<details><summary>✅ Answer</summary>

**D.** etcd encryption at rest

- A: Node size doesn't protect stored Secrets.
- B: That widens access instead of protecting Secrets.
- C: ConfigMaps aren't Secrets, and immutability doesn't encrypt anything.
- D: Correct. Configure etcd encryption when you create the cluster, and combine it with Key Vault integration.

Enable encryption at rest by configuring etcd encryption when you create the cluster. Combine it with Key Vault integration for rotation and audit.

📘 Source: [Implement secrets for sensitive data](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/3-implement-secrets)

</details>

## 18. `lp3m2-018`

Which is the default CSI storage class in AKS?

- **A.** azurefile-csi-premium
- **B.** managed-csi
- **C.** azurefile-csi
- **D.** managed-csi-premium

<details><summary>💡 Hint</summary>

One storage class is the AKS default, and it's backed by Azure Disk.

</details>

<details><summary>✅ Answer</summary>

**B.** managed-csi

- A: That's the Premium Azure Files class.
- B: Correct. managed-csi (Azure Disk) is the default.
- C: azurefile-csi is a built-in class, but not the default.
- D: That's the Premium SSD disk class.

managed-csi uses Azure Disk with ReadWriteOnce.

📘 Source: [Attach persistent storage to an app](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/4-persistent-storage)

</details>

## 19. `lp3m2-019`

Five embedding-worker Pods on different nodes must read and write the same cache directory. Which storage class fits?

- **A.** An emptyDir in each Pod
- **B.** managed-csi
- **C.** managed-csi-premium
- **D.** azurefile-csi

<details><summary>💡 Hint</summary>

Pods on several nodes all need to write. Which backing service mounts on many nodes?

</details>

<details><summary>✅ Answer</summary>

**D.** azurefile-csi

- A: Each Pod's local directory isn't shared or persistent.
- B: Azure Disk is ReadWriteOnce, attached to one node.
- C: Premium disks are still ReadWriteOnce.
- D: Correct. Azure Files is ReadWriteMany across nodes.

Choose file-based storage when multiple Pods need concurrent access to shared data.

📘 Source: [Attach persistent storage to an app](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/4-persistent-storage)

</details>

## 20. `lp3m2-020`

Put the steps to give a Deployment durable storage, and prove it, in order.

- Add a volume that references the claim and a volumeMount with a mountPath
- Check with kubectl describe pvc that the claim is bound
- Create a PersistentVolumeClaim with size, access mode and storageClassName
- Write a file, delete the Pod and check the file in the replacement Pod

<details><summary>💡 Hint</summary>

Claim first, then mount it, then confirm it's bound, then test.

</details>

<details><summary>✅ Answer</summary>

1. Create a PersistentVolumeClaim with size, access mode and storageClassName
2. Add a volume that references the claim and a volumeMount with a mountPath
3. Check with kubectl describe pvc that the claim is bound
4. Write a file, delete the Pod and check the file in the replacement Pod

Claim → mount → confirm bound → prove persistence across a Pod restart.

📘 Source: [Attach persistent storage to an app](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/4-persistent-storage)

</details>

## 21. `lp3m2-021`

For each statement, select Yes if the statement is true. Otherwise, select No. A single-Pod vector database needs low-latency block storage on AKS.

| Statement | Yes / No |
|---|---|
| managed-csi-premium is a reasonable choice. | ☐ |
| Azure Disk volumes can be written by Pods on several nodes at once. | ☐ |
| Data written to the PVC mount path survives a Pod restart. | ☐ |

<details><summary>💡 Hint</summary>

Premium disks are fast, but a disk attaches to one node.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| managed-csi-premium is a reasonable choice. | Yes | Premium SSD disk with ReadWriteOnce suits low-latency single-Pod I/O. |
| Azure Disk volumes can be written by Pods on several nodes at once. | No | Disks attach to a single node (ReadWriteOnce). |
| Data written to the PVC mount path survives a Pod restart. | Yes | PVC data persists across Pod restarts. |

Disk classes are RWO and suit single-Pod stateful apps; files classes are RWX.

📘 Source: [Attach persistent storage to an app](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/4-persistent-storage)

</details>

## 22. `lp3m2-022`

A team asks why managed-csi only supports ReadWriteOnce while azurefile-csi supports ReadWriteMany. What does Learn give as the reason?

- **A.** ReadWriteMany needs a premium AKS tier that Azure Disk doesn't support
- **B.** Azure Disk is being retired, so it gets fewer features
- **C.** A disk attaches to one node; an SMB share mounts on many
- **D.** Kubernetes limits block storage to one Pod for consistency

<details><summary>💡 Hint</summary>

Think about how each kind of storage connects to the nodes.

</details>

<details><summary>✅ Answer</summary>

**C.** A disk attaches to one node; an SMB share mounts on many

- A: There's no such tier rule. The difference is how the storage attaches.
- B: Azure Disk is the default storage class, not a retired one.
- C: Correct. The access mode follows from how each kind of storage attaches.
- D: The reason Learn gives is that the disk attaches to a single node.

Azure Disk classes use ReadWriteOnce because the disk attaches to a single node. Azure Files classes use ReadWriteMany because the SMB share mounts across multiple nodes.

📘 Source: [Attach persistent storage to an app](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/4-persistent-storage)

</details>

## 23. `lp3m2-023`

Several Pods on different nodes collaborate on the same working files and need low latency for frequent reads and writes. Which storage class fits?

- **A.** managed-csi-premium
- **B.** azurefile-csi
- **C.** azurefile-csi-premium
- **D.** managed-csi

<details><summary>💡 Hint</summary>

You need sharing across nodes and premium performance at the same time.

</details>

<details><summary>✅ Answer</summary>

**C.** azurefile-csi-premium

- A: Premium disk is fast, but it's ReadWriteOnce and attaches to one node.
- B: This shares across nodes, but on standard storage rather than premium.
- C: Correct. It gives shared ReadWriteMany access on Premium SSD.
- D: This is a single-node disk class without premium performance.

azurefile-csi-premium (Azure Files Premium) gives ReadWriteMany shared access with Premium SSD performance for collaborative, low-latency workloads.

📘 Source: [Attach persistent storage to an app](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/4-persistent-storage)

</details>

## 24. `lp3m2-024`

A conversation-state service writes to /data inside its container. After every Pod restart, the state is gone. What should you add?

- **A.** A larger memory limit for the container
- **B.** An immutable ConfigMap mounted at /data
- **C.** A PersistentVolumeClaim mounted at /data
- **D.** A second replica so that one copy always survives

<details><summary>💡 Hint</summary>

Container file systems are temporary. Which Kubernetes object requests durable storage?

</details>

<details><summary>✅ Answer</summary>

**C.** A PersistentVolumeClaim mounted at /data

- A: Memory doesn't keep files across restarts.
- B: ConfigMaps are read-only configuration, not writable storage.
- C: Correct. Container file systems are ephemeral, and a PVC gives storage that survives restarts and rescheduling.
- D: Each replica has its own ephemeral file system, so nothing is shared or kept.

Container filesystems are ephemeral. A PersistentVolumeClaim, mounted with a volume and volumeMount, provides storage that survives Pod restarts and rescheduling.

📘 Source: [Attach persistent storage to an app](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/4-persistent-storage)

</details>


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
