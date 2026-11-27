# Lab LP9: Observe and troubleshoot an AI pipeline

> Covers all of **Learning Path 9**: OpenTelemetry (M1) and logs, metrics and alerts (M2). About 2 hours.
> **Step-by-step guide with explanations and diagrams:** open [guide.html](guide.html) in your browser (works offline).
> Part of [AI-200 Prep](../../README.md) · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200)

## What you'll do

- Create Log Analytics and Application Insights.
- Run a small three-service RAG pipeline (gateway, orchestrator, LLM service) instrumented with the Azure Monitor OpenTelemetry Distro.
- Check that telemetry arrives, then find the bottleneck on the Application Map and in the end-to-end transaction view.
- Investigate with 21 ready-made KQL queries in [app/queries](app/queries/): slow requests, dependencies, cold starts, rate limits and exceptions.
- Run a sampling experiment, build a dashboard, deploy a workbook, and create log and metric alerts that really fire.

## Before you start

- An Azure subscription, Azure CLI signed in (`az login`), Python 3.10+, and a terminal (bash, zsh, Git Bash, Cloud Shell or PowerShell).
- Put the lab folder in your home folder (`~/ai200-lp9-lab`).

## Cost

Official pricing, November 2026.

| Resource | Price | This lab |
|---|---|---|
| Log Analytics / Application Insights | pay per GB ingested; first 5 GB per billing account per month free | a few MB |
| Log search alert rules | about $1.50 per rule per month, charged hourly while the rule exists | two rules for an afternoon: a few rupees |
| Metric alert | about $0.10 per month | |
| Action group email | first 1,000 free | |
| Workbooks and dashboards | free | |

Clean up the same day and the total is **a few rupees**.

## Run it

1. Open [guide.html](guide.html) and pick **Bash** or **PowerShell** once.
2. Commands are in [cmd/bash.sh](cmd/bash.sh) and [cmd/ps.ps1](cmd/ps.ps1) (`# @@ step-name` blocks). The pipeline and queries are in [app/](app/).
3. The launcher sets `OTEL_EXPERIMENTAL_RESOURCE_DETECTORS=otel` so that the Distro doesn't probe the Azure VM metadata endpoint on your laptop.

## Clean up

```bash
az group delete --name rg-ai200-lp9 --yes
```

This removes the workspace, Application Insights, alert rules and action group. Alert rules bill hourly, so don't leave them running.

## Tested

Tested live in Central India on 26–27 Nov 2026 with bash and zsh. The PowerShell blocks **haven't been run live yet**.
Please [report](../../CONTRIBUTING.md) anything that fails.

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200)
