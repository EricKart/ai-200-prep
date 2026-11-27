# LP3 · M2: Configure applications on Azure Kubernetes Service

> **Learning path 3:** Deploy and monitor applications on Azure Kubernetes Service · **Skill area 1:** Develop and deploy containerized solutions · about 72 min on Microsoft Learn  
> Study it interactively at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-3/configure-apps-azure-kubernetes-service)

Applications need settings, secrets and sometimes durable storage. You'll learn ConfigMaps, Secrets (and their Azure integrations), and persistent volumes on AKS.

**In this lesson**

1. [Define ConfigMaps for application settings](#define-configmaps-for-application-settings)
2. [Implement secrets for sensitive data](#implement-secrets-for-sensitive-data)
3. [Attach persistent storage to an app](#attach-persistent-storage-to-an-app)

## Define ConfigMaps for application settings

📘 Microsoft Learn: [Define ConfigMaps for application settings](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/2-define-configmaps)

A ConfigMap is a **settings sheet** kept outside the image. Pods can read it as environment variables (read once at start) or as **files** on disk (which refresh when the sheet changes). An **immutable** ConfigMap is a sheet that's been laminated: to change it, make a new one.

**Key facts**

- **ConfigMaps** store **non-sensitive** configuration (feature flags, endpoints) as key-value pairs in `data`; `binaryData` holds base64 binary values.
- Limit: **1 MiB per ConfigMap**. Keys: alphanumerics, dashes, underscores or dots. Larger data → persistent volumes or external configuration services.
- Environment variables: `valueFrom.configMapKeyRef` for one key, or `envFrom.configMapRef` to load **all keys** at once.
- Files: a volume backed by the ConfigMap plus a `volumeMount`; each key becomes a file. Mounted files **update automatically** (kubelet sync), except with **subPath** mounts.
- Environment variables from a ConfigMap **don't update**; Pods need a **restart**.
- **Immutable** ConfigMaps protect against accidental changes and reduce API server load (Kubernetes can close watches). You can't change the data or undo immutability; **delete and recreate** (e.g. app-settings-v2). Existing Pods keep the old mount until restart.
- The **Azure App Configuration Kubernetes Provider** runs in the cluster and generates ConfigMaps from App Configuration, syncing changes, and gives a central view across AKS clusters.
- Verify with `kubectl describe configmap`, `describe deployment`, `describe pod` and logs.

| Consume as | Updates when the ConfigMap changes? |
|---|---|
| Environment variables (configMapKeyRef / envFrom) | No, restart the Pods |
| Mounted files (volume) | Yes, automatically on kubelet sync |
| Mounted with subPath | No |

> [!WARNING]
> **Exam traps**
>
> - 1 MiB maximum per ConfigMap.
> - Immutable ConfigMaps can't be edited or made mutable again.

## Implement secrets for sensitive data

📘 Microsoft Learn: [Implement secrets for sensitive data](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/3-implement-secrets)

Kubernetes Secrets are the cluster's **small safe** for API keys and passwords. For stricter rules (audit trails, automatic rotation), keep the secrets in **Key Vault** and let the CSI driver bring them into Pods as files, or let **App Configuration** decide which secrets each app gets.

**Key facts**

- Secrets hold sensitive values (connection strings, API keys) out of source control and images. `kubectl create secret generic app-secrets --from-literal=…`; also from files or YAML (GitOps).
- Types: **Opaque** for most strings; **kubernetes.io/dockerconfigjson** for registry credentials; **kubernetes.io/tls** for TLS certificates and keys.
- Reference with `valueFrom.secretKeyRef`; values are injected as environment variables and stay in memory, not written to disk by default. Restrict access with **RBAC**.
- `kubectl describe secret` shows keys but **masks values**; `kubectl get secrets` lists name, type, data count and age.
- **Key Vault + Secrets Store CSI Driver**: mounts secrets as **files**; secrets stay in Key Vault; the driver **polls and updates** without Pod restarts; rotation, audit logging, private endpoints.
- **App Configuration + Key Vault references**: the App Configuration Kubernetes Provider resolves references and creates **native Kubernetes Secrets**; apps don't authenticate to Key Vault themselves.
- Choose direct Key Vault for fine-grained audit of each secret access; choose App Configuration for central management of which secrets each app uses.
- Practices: RBAC, never commit Secret manifests with literal values, rotate and **trigger a rollout** so Pods get new values, enable **etcd encryption at rest**.

| Option | Secrets live in | Pods receive |
|---|---|---|
| Kubernetes Secret | The cluster | Env vars (or files) |
| Key Vault + CSI driver | Key Vault | Mounted files, auto-updated |
| App Configuration provider | Key Vault (referenced from App Configuration) | Generated Kubernetes Secrets |

> [!WARNING]
> **Exam traps**
>
> - Registry credentials use **kubernetes.io/dockerconfigjson**; TLS uses **kubernetes.io/tls**.
> - After rotating a plain Kubernetes Secret used as env vars, trigger a rollout.

## Attach persistent storage to an app

📘 Microsoft Learn: [Attach persistent storage to an app](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/4-persistent-storage)

A Pod's own disk is **wiped** when it restarts. A **PersistentVolumeClaim** is a request slip: "I need 10 GiB of this kind of storage". Azure Disk is a **personal drive** (one node at a time); Azure Files is a **shared drive** many Pods can use at once.

**Key facts**

- Container file systems are **ephemeral**. **PersistentVolume** (PV) and **PersistentVolumeClaim** (PVC) give storage that survives restarts and rescheduling.
- **CSI drivers** integrate Azure Disk (single-node block), Azure Files (shared across Pods) and Azure Blob (large unstructured data) through StorageClasses.
- **Azure Container Storage**: fully managed, container-native; uses NVMe-oF for fast attach/detach and quicker failover; for I/O-intensive or rapidly scaling stateful workloads.
- A PVC sets capacity, **access mode** and **storageClassName**. **ReadWriteOnce** = single node; **ReadWriteMany** = shared across nodes.
- Built-in classes: **managed-csi** (default; Azure Disk; RWO), **managed-csi-premium** (Premium SSD; RWO), **azurefile-csi** (Azure Files; RWX), **azurefile-csi-premium** (Premium; RWX).
- Disk = RWO because the disk attaches to one node. Files = RWX because the SMB share mounts on many nodes.
- Mount: a `volumes` entry referencing the claim + a `volumeMount` with `mountPath`. Check container permissions on the path.
- Verify: `kubectl describe pvc` shows it's **bound**; write a file, delete the Pod, check the file exists in the replacement; run small load tests.

| StorageClass | Backing | Access mode | Use |
|---|---|---|---|
| managed-csi (default) | Azure Disk | ReadWriteOnce | Single-Pod databases, stateful apps |
| managed-csi-premium | Azure Disk Premium SSD | ReadWriteOnce | Low-latency single-Pod I/O |
| azurefile-csi | Azure Files | ReadWriteMany | Shared files, logs, content |
| azurefile-csi-premium | Azure Files Premium | ReadWriteMany | High-performance shared access |

> [!WARNING]
> **Exam traps**
>
> - Several Pods on different nodes writing the same volume → **Azure Files (RWX)**.
> - managed-csi is the **default** class.

## Check yourself

- **Practice questions:** [lp3m2 on GitHub](../../practice/lp3m2.md), or [on the site](https://aryantripathi.dev/ai-200/lp-3/configure-apps-azure-kubernetes-service) with hints and saved progress
- **Cheat sheet:** [Learning path 3](../cheatsheets/lp3.md)
- **Microsoft Learn exercise:** [Configure apps on Azure Kubernetes Service](https://learn.microsoft.com/en-us/training/modules/configure-apps-azure-kubernetes-service/5-exercise-configure-apps)
- **Hands-on lab:** [labs/](../../labs/README.md) has a lab for this learning path

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
