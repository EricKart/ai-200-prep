# Practice: LP9 · M2 Analyze app telemetry with logs and metrics

> 26 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp9m2.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-9/analyze-telemetry-logs-metrics)

## 1. `lp9m2-001`

Which KQL operator selects specific columns for the output?

- **A.** render
- **B.** where
- **C.** project
- **D.** summarize

<details><summary>💡 Hint</summary>

One operator chooses which columns appear in the output.

</details>

<details><summary>✅ Answer</summary>

**C.** project

- A: render draws a chart.
- B: where filters rows.
- C: Correct. project picks, renames or computes columns.
- D: summarize aggregates rows into groups.

Filter with where, shape with project.

📘 Source: [Write basic KQL queries](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/2-write-basic-kql-queries)

</details>

## 2. `lp9m2-002`

You open Logs from a Log Analytics workspace rather than from the Application Insights resource. Which table holds incoming requests?

- **A.** requests
- **B.** Requests_CL
- **C.** AzureDiagnostics
- **D.** AppRequests

<details><summary>💡 Hint</summary>

Workspace-based tables have App-prefixed names.

</details>

<details><summary>✅ Answer</summary>

**D.** AppRequests

- A: requests is the name in Application Insights scope.
- B: That's a custom log table naming pattern, not this table.
- C: That's a different diagnostics table.
- D: Correct. Workspace scope uses AppRequests, AppExceptions, AppDependencies.

Query scope decides table and column names.

📘 Source: [Write basic KQL queries](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/2-write-basic-kql-queries)

</details>

## 3. `lp9m2-003`

Which function groups timestamps into fixed hourly intervals for trend analysis?

- **A.** bin(timestamp, 1h)
- **B.** dcount(timestamp)
- **C.** ago(1h)
- **D.** percentile(duration, 95)

<details><summary>💡 Hint</summary>

One function rounds timestamps down into fixed-size buckets.

</details>

<details><summary>✅ Answer</summary>

**A.** bin(timestamp, 1h)

- A: Correct. bin rounds each timestamp down into 1-hour buckets.
- B: dcount estimates distinct values.
- C: ago(1h) is a point in time used for filtering.
- D: percentile calculates a latency percentile.

Without bin(), each unique timestamp would form its own group.

📘 Source: [Write basic KQL queries](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/2-write-basic-kql-queries)

</details>

## 4. `lp9m2-004`

You want the 20 slowest failed requests from the last hour, sorted by duration. Which operator should end the query?

- **A.** take 20
- **B.** project 20
- **C.** top 20 by duration desc
- **D.** summarize count() by duration

<details><summary>💡 Hint</summary>

One operator sorts and limits in a single step.

</details>

<details><summary>✅ Answer</summary>

**C.** top 20 by duration desc

- A: take returns an arbitrary 20 rows, not the slowest.
- B: project selects columns; it doesn't limit rows.
- C: Correct. top returns the first N rows sorted by a column.
- D: That groups by duration rather than listing requests.

take for a quick look; top for the highest or lowest values.

📘 Source: [Write basic KQL queries](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/2-write-basic-kql-queries)

</details>

## 5. `lp9m2-005`

For each statement, select Yes if the statement is true. Otherwise, select No. A query searches a large traces table for the word timeout in the message column.

| Statement | Yes / No |
|---|---|
| The has operator uses the term index and is usually faster than contains. | ☐ |
| dcount() returns an exact distinct count in every case. | ☐ |
| Adding render timechart needs a datetime column in the results. | ☐ |
| The take operator returns rows sorted by the column you name. | ☐ |

<details><summary>💡 Hint</summary>

Think about term-indexed search, approximate distinct counts, charts needing time, and whether take sorts.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The has operator uses the term index and is usually faster than contains. | Yes | has uses term indexing; contains doesn't. |
| dcount() returns an exact distinct count in every case. | No | dcount() estimates; count_distinct() is exact but heavier. |
| Adding render timechart needs a datetime column in the results. | Yes | timechart requires a datetime column and numeric columns. |
| The take operator returns rows sorted by the column you name. | No | take returns arbitrary rows; top sorts. |

Pick fast operators and remember sampling when counting.

📘 Source: [Write basic KQL queries](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/2-write-basic-kql-queries)

</details>

## 6. `lp9m2-006`

Each option starts with `requests | where timestamp > ago(24h)`. Which one gives request count and average duration per hour for each service?

- **A.** … | project timestamp, duration, cloud_RoleName | render timechart
- **B.** … | summarize count(), avg(duration) by bin(timestamp, 1h), cloud_RoleName
- **C.** … | take 24 | summarize count(), avg(duration) by cloud_RoleName
- **D.** … | summarize count(), avg(duration) by timestamp, cloud_RoleName

<details><summary>💡 Hint</summary>

Count and average per hour and per service: group by both the time bucket and the role name.

</details>

<details><summary>✅ Answer</summary>

**B.** … | summarize count(), avg(duration) by bin(timestamp, 1h), cloud_RoleName

- A: render doesn't aggregate data.
- B: Correct. bin buckets the time and the by clause groups per service.
- C: take 24 returns 24 arbitrary rows, not 24 hours.
- D: Grouping by raw timestamp creates one group per unique time.

summarize … by bin(timestamp, 1h), cloud_RoleName is the standard trend pattern.

📘 Source: [Write basic KQL queries](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/2-write-basic-kql-queries)

</details>

## 7. `lp9m2-007`

Your code tracks a custom event, "document classified", each time the classifier finishes. In which Application Insights table do these rows appear?

- **A.** customMetrics
- **B.** requests
- **C.** customEvents
- **D.** traces

<details><summary>💡 Hint</summary>

Business events you track yourself have their own table, separate from logs and numbers.

</details>

<details><summary>✅ Answer</summary>

**C.** customEvents

- A: customMetrics holds numeric measurements such as queue depth.
- B: requests holds incoming HTTP requests.
- C: Correct. customEvents stores custom business events that developers track explicitly.
- D: traces holds application log messages.

Application Insights tables: requests, dependencies, exceptions, traces (logs), customEvents (business events), customMetrics (numeric measures) and performanceCounters (system metrics).

📘 Source: [Write basic KQL queries](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/2-write-basic-kql-queries)

</details>

## 8. `lp9m2-008`

Sampling is enabled in Application Insights. Which aggregation gives an accurate exception total?

- **A.** sum(itemCount)
- **B.** count()
- **C.** dcount(type)
- **D.** avg(itemCount)

<details><summary>💡 Hint</summary>

With sampling, each row may stand for several items. Add up the weights.

</details>

<details><summary>✅ Answer</summary>

**A.** sum(itemCount)

- A: Correct. Each sampled record represents itemCount real events.
- B: count() returns only the number of sampled records.
- C: dcount counts distinct exception types.
- D: An average doesn't give a total.

Use sum(itemCount) whenever sampling may be active.

📘 Source: [Explore logs for errors and performance](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/3-explore-logs-errors-performance)

</details>

## 9. `lp9m2-009`

A failed dependency call to a model inference endpoint shows resultCode 429. What does it indicate?

- **A.** Rate limiting
- **B.** A network timeout
- **C.** A server-side crash
- **D.** An invalid query

<details><summary>💡 Hint</summary>

429 is the HTTP code for too many requests.

</details>

<details><summary>✅ Answer</summary>

**A.** Rate limiting

- A: Correct. 429 means the endpoint is rate limiting; adjust throughput or retry policies.
- B: Timeouts often have no result code.
- C: That's typically a 500.
- D: KQL query errors don't produce dependency result codes.

429 = throttled, 500 = server failure, no code = timeout or network.

📘 Source: [Explore logs for errors and performance](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/3-explore-logs-errors-performance)

</details>

## 10. `lp9m2-010`

After joining exceptions with requests, you see columns named cloud_RoleName and cloud_RoleName1. What does Learn recommend?

- **A.** Ignore it; the suffix disappears after render
- **B.** Drop the join and query each table separately
- **C.** Use union instead of join
- **D.** Rename the columns inside the subquery before the join

<details><summary>💡 Hint</summary>

A join adds a 1 to duplicate column names. Fix it before joining.

</details>

<details><summary>✅ Answer</summary>

**D.** Rename the columns inside the subquery before the join

- A: The suffix is part of the result columns.
- B: You'd lose the correlation.
- C: union stacks rows; it doesn't correlate them.
- D: Correct. Renaming first gives unambiguous names in the final project.

KQL adds a numeric suffix to duplicate column names after a join.

📘 Source: [Explore logs for errors and performance](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/3-explore-logs-errors-performance)

</details>

## 11. `lp9m2-011`

For each statement, select Yes if the statement is true. Otherwise, select No. A dependency has an average duration of 200 ms.

| Statement | Yes / No |
|---|---|
| This proves that nearly all calls finish in about 200 ms. | ☐ |
| Checking the 95th and 99th percentiles can reveal slow outliers. | ☐ |
| The Performance view's duration distribution can show a bimodal pattern. | ☐ |

<details><summary>💡 Hint</summary>

An average hides the spread. Look at percentiles and the distribution.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| This proves that nearly all calls finish in about 200 ms. | No | Averages can hide slow tails; check percentiles. |
| Checking the 95th and 99th percentiles can reveal slow outliers. | Yes | Percentiles show the tail behavior. |
| The Performance view's duration distribution can show a bimodal pattern. | Yes | It reveals mostly-fast with a slow subset. |

Use percentiles(duration, 50, 95, 99) for latency analysis.

📘 Source: [Explore logs for errors and performance](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/3-explore-logs-errors-performance)

</details>

## 12. `lp9m2-012`

An investigator wants the top response codes and exception types for a failing operation, then to open a sample request's full timeline. Where should they start?

- **A.** A pinned dashboard tile
- **B.** The Performance view's duration chart
- **C.** The Failures view under Investigate
- **D.** Live Metrics

<details><summary>💡 Hint</summary>

The portal has a view built for exactly this, with drill-down to samples.

</details>

<details><summary>✅ Answer</summary>

**C.** The Failures view under Investigate

- A: Dashboard tiles summarize; they aren't the drill-down tool.
- B: Performance shows durations, not failure breakdowns.
- C: Correct. It shows top codes, exceptions and failed dependencies, with drill-down to samples.
- D: Live Metrics is real-time, not a failure breakdown.

Built-in views first, then KQL for deeper questions.

📘 Source: [Explore logs for errors and performance](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/3-explore-logs-errors-performance)

</details>

## 13. `lp9m2-013`

A classifier catches an exception, logs it and returns a fallback label. Will the exception appear in the Application Insights exceptions table?

- **A.** No, only unhandled exceptions are stored
- **B.** Yes, but only in the dependencies table
- **C.** No, exceptions go to the traces table with the logs
- **D.** Yes, if it's recorded; handled ones appear too

<details><summary>💡 Hint</summary>

The exceptions table isn't only for crashes.

</details>

<details><summary>✅ Answer</summary>

**D.** Yes, if it's recorded; handled ones appear too

- A: Handled exceptions can be recorded too.
- B: Dependencies are outgoing calls, not exceptions.
- C: traces holds log messages. Exceptions have their own table.
- D: Correct. The exceptions table records both handled and unhandled exceptions with stack traces.

The exceptions table records errors with stack traces and severity, and both handled and unhandled exceptions appear there when they're recorded.

📘 Source: [Explore logs for errors and performance](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/3-explore-logs-errors-performance)

</details>

## 14. `lp9m2-014`

A metrics chart should reveal rare worst-case latency spikes that averages hide. Which aggregation fits?

- **A.** Count
- **B.** Average
- **C.** Sum
- **D.** Max

<details><summary>💡 Hint</summary>

Rare spikes disappear in an average. Which aggregation keeps the worst value?

</details>

<details><summary>✅ Answer</summary>

**D.** Max

- A: Count gives a number of samples, not latency.
- B: Average shows typical behavior and smooths spikes.
- C: Sum totals events over a period.
- D: Correct. Max shows worst-case values.

Average for typical latency, sum for totals, max for spikes.

📘 Source: [Build dashboards for app telemetry](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/4-build-dashboards-app-telemetry)

</details>

## 15. `lp9m2-015`

For each statement, select Yes if the statement is true. Otherwise, select No. A team publishes an operations dashboard with tiles from Application Insights.

| Statement | Yes / No |
|---|---|
| The tiles show live, real-time data at every moment. | ☐ |
| A teammate with dashboard access but no access to Application Insights sees access errors on those tiles. | ☐ |
| Learn suggests keeping a dashboard to about 5–10 tiles. | ☐ |

<details><summary>💡 Hint</summary>

Dashboard tiles refresh periodically, follow the viewer's own access, and work best in small numbers.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The tiles show live, real-time data at every moment. | No | Tiles refresh on a schedule; use Live Metrics for real time. |
| A teammate with dashboard access but no access to Application Insights sees access errors on those tiles. | Yes | Viewers need read access to data sources too. |
| Learn suggests keeping a dashboard to about 5–10 tiles. | Yes | Too many tiles dilute attention. |

Dashboards are for at-a-glance health; scope access to data as well.

📘 Source: [Build dashboards for app telemetry](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/4-build-dashboards-app-telemetry)

</details>

## 16. `lp9m2-016`

A latency tile shows p50 flat at 300 ms while p95 climbs from 1 s to 4 s over a week. What does this indicate?

- **A.** All requests are getting four times slower
- **B.** Sampling is removing slow requests
- **C.** Most stay fast; a growing subset degrades
- **D.** The dashboard's refresh schedule is broken

<details><summary>💡 Hint</summary>

The median is steady while the tail grows. What does that say about most requests?

</details>

<details><summary>✅ Answer</summary>

**C.** Most stay fast; a growing subset degrades

- A: p50 is flat, so typical requests aren't slower.
- B: Sampling doesn't selectively drop slow requests.
- C: Correct. A widening p50–p95 gap points to a slow subset, such as one document type.
- D: The trend is consistent, not a refresh glitch.

Watch percentile gaps, not just averages.

📘 Source: [Build dashboards for app telemetry](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/4-build-dashboards-app-telemetry)

</details>

## 17. `lp9m2-017`

New team members open the operations dashboard and don't know what the application does or where the runbooks are. Which best practice addresses this?

- **A.** Merge the business and pipeline dashboards into one
- **B.** Add more tiles so that every metric is visible
- **C.** Name tiles Query 1, Query 2 and so on to keep them short
- **D.** Add a Markdown tile at the top with context, runbook links and on-call contacts

<details><summary>💡 Hint</summary>

One tile type is just text.

</details>

<details><summary>✅ Answer</summary>

**D.** Add a Markdown tile at the top with context, runbook links and on-call contacts

- A: Learn suggests separating concerns into different dashboards.
- B: Learn suggests 5–10 focused tiles; more tiles add clutter.
- C: Descriptive tile titles are the recommendation.
- D: Correct. A Markdown tile gives viewers the context they need.

Dashboard best practices: separate concerns, keep 5–10 tiles, use descriptive tile titles, and include a Markdown tile with context, runbook links and on-call information.

📘 Source: [Build dashboards for app telemetry](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/4-build-dashboards-app-telemetry)

</details>

## 18. `lp9m2-018`

During an incident, an engineer wants to pick a service and time range and have all charts update together. Which tool fits?

- **A.** Smart detection on the resource
- **B.** A workbook with parameters
- **C.** A dashboard with pinned tiles
- **D.** An action group for the team

<details><summary>💡 Hint</summary>

Interactive charts that all respond to the same choices need a tool with parameters.

</details>

<details><summary>✅ Answer</summary>

**B.** A workbook with parameters

- A: Smart detection raises anomaly alerts.
- B: Correct. Parameters such as {TimeRange} and {ServiceName} drive every dependent query.
- C: Dashboard tiles are relatively static.
- D: Action groups send notifications.

Dashboards for at-a-glance health; workbooks for interactive investigation.

📘 Source: [Create workbooks for interactive analysis](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/5-create-workbooks-interactive-analysis)

</details>

## 19. `lp9m2-019`

A workbook dropdown {ServiceName} allows multi-select. How should a query filter on it?

- **A.** | where cloud_RoleName == {ServiceName}
- **B.** | project {ServiceName}
- **C.** | where cloud_RoleName in ({ServiceName})
- **D.** | where cloud_RoleName has {ServiceName}

<details><summary>💡 Hint</summary>

Multi-select values need a filter that accepts a list.

</details>

<details><summary>✅ Answer</summary>

**C.** | where cloud_RoleName in ({ServiceName})

- A: == compares to one value.
- B: project selects columns.
- C: Correct. Multi-select becomes a comma-separated list for the in operator.
- D: has is a term search, not a list match.

Multi-select parameters compare several services side by side.

📘 Source: [Create workbooks for interactive analysis](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/5-create-workbooks-interactive-analysis)

</details>

## 20. `lp9m2-020`

A workbook shows a summary grid of services with error counts. Clicking a service should filter the rest of the workbook to that service. What should you configure?

- **A.** A second dashboard for each service
- **B.** A resource picker parameter at the top
- **C.** A grid link that exports a parameter
- **D.** A log search alert for each service

<details><summary>💡 Hint</summary>

Clicking a grid row should set something the rest of the workbook reads.

</details>

<details><summary>✅ Answer</summary>

**C.** A grid link that exports a parameter

- A: Separate dashboards don't drill down from a click.
- B: A resource picker chooses resources, not a service from a grid row.
- C: Correct. The exported parameter filters the remaining steps.
- D: Alerts notify; they don't filter views.

Combine linked grids with conditional visibility for drill-down.

📘 Source: [Create workbooks for interactive analysis](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/5-create-workbooks-interactive-analysis)

</details>

## 21. `lp9m2-021`

Which Azure Monitor alert severity is the most urgent?

- **A.** Sev 3 (Informational)
- **B.** Sev 4 (Verbose)
- **C.** Sev 1 (Error)
- **D.** Sev 0 (Critical)

<details><summary>💡 Hint</summary>

Severities run from 0 to 4. Lower numbers are more urgent.

</details>

<details><summary>✅ Answer</summary>

**D.** Sev 0 (Critical)

- A: 3 is for notable events without urgency.
- B: 4 is verbose diagnostic detail.
- C: 1 is Error, one step lower.
- D: Correct. 0 is Critical, for production-impacting failures.

Severity runs from 0 (Critical) to 4 (Verbose).

📘 Source: [Set alerts for app failures and anomalies](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/6-set-alerts-app-failures-anomalies)

</details>

## 22. `lp9m2-022`

You need an alert when the 95th-percentile response time of any service exceeds 3 seconds, computed with KQL. Which alert type fits?

- **A.** A log search alert
- **B.** Smart detection by itself
- **C.** A dashboard tile
- **D.** A metric alert on CPU percentage

<details><summary>💡 Hint</summary>

The condition is computed with a KQL query.

</details>

<details><summary>✅ Answer</summary>

**A.** A log search alert

- A: Correct. Log search alerts run KQL queries, including percentiles per service.
- B: Smart detection learns baselines; it doesn't enforce your 3-second SLA.
- C: Tiles don't notify anyone.
- D: CPU isn't response-time percentile per service.

Log search alerts give the flexibility AI apps usually need.

📘 Source: [Set alerts for app failures and anomalies](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/6-set-alerts-app-failures-anomalies)

</details>

## 23. `lp9m2-023`

For each statement, select Yes if the statement is true. Otherwise, select No. A log search alert runs `requests | where success == false | summarize failedCount = count() by cloud_RoleName | where failedCount > 10` every 5 minutes over a 5-minute window, firing when rows > 0.

| Statement | Yes / No |
|---|---|
| Each returned row identifies a service with more than 10 failures in the window. | ☐ |
| One alert rule can reference up to ten action groups. | ☐ |
| Requiring several violations before firing reduces noise from single spikes. | ☐ |
| Smart detection makes this manual rule unnecessary. | ☐ |

<details><summary>💡 Hint</summary>

Each result row can be its own alert. Several violations reduce noise.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Each returned row identifies a service with more than 10 failures in the window. | Yes | Rows represent services over the threshold. |
| One alert rule can reference up to ten action groups. | No | The limit is five action groups per rule. |
| Requiring several violations before firing reduces noise from single spikes. | Yes | You can configure the number of violations. |
| Smart detection makes this manual rule unnecessary. | No | Manual rules enforce known thresholds; smart detection finds novel anomalies. |

Manual log alerts plus smart detection give the widest coverage.

📘 Source: [Set alerts for app failures and anomalies](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/6-set-alerts-app-failures-anomalies)

</details>

## 24. `lp9m2-024`

When a critical alert fires, the team wants a ticket created in an external system automatically. Which action group action fits?

- **A.** An SMS notification
- **B.** A Severity 4 setting
- **C.** An Azure mobile app push
- **D.** A Logic App action

<details><summary>💡 Hint</summary>

Creating a ticket elsewhere calls for a workflow automation service.

</details>

<details><summary>✅ Answer</summary>

**D.** A Logic App action

- A: SMS notifies a person; it doesn't create tickets.
- B: Severity classifies urgency; it isn't an action.
- C: Push notifies devices only.
- D: Correct. Logic Apps can create a ticket in an external system.

Automated actions: Function, Logic App, webhook, Automation Runbook, Event Hub.

📘 Source: [Set alerts for app failures and anomalies](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/6-set-alerts-app-failures-anomalies)

</details>

## 25. `lp9m2-025`

A dependency has slowed gradually over three weeks, and no fixed threshold has fired. Which feature is designed to catch this?

- **A.** A dashboard p50 tile
- **B.** Smart detection performance anomalies
- **C.** A workbook time-range parameter
- **D.** A metric alert with a static threshold

<details><summary>💡 Hint</summary>

A slow drift doesn't cross a fixed line. A feature that learns normal behavior can catch it.

</details>

<details><summary>✅ Answer</summary>

**B.** Smart detection performance anomalies

- A: A tile shows data but doesn't alert.
- B: Correct. Smart detection compares against historical norms and spots gradual degradation.
- C: Parameters filter views; they don't alert.
- D: Static thresholds miss values that never cross the line.

Smart detection learns a baseline and alerts on deviations.

📘 Source: [Set alerts for app failures and anomalies](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/6-set-alerts-app-failures-anomalies)

</details>

## 26. `lp9m2-026`

Five alert rules for the RAG pipeline should all page the same on-call engineer and post to the same team channel. What's the most maintainable setup?

- **A.** Copy the same notifications into each rule's condition
- **B.** One action group with both notifications, referenced by all five rules
- **C.** Raise every rule to Sev 0 so that notifications go out automatically
- **D.** Five action groups, one per rule, each with the same settings

<details><summary>💡 Hint</summary>

Alert rules have a scope, a condition, a severity, and something reusable that decides who hears about it.

</details>

<details><summary>✅ Answer</summary>

**B.** One action group with both notifications, referenced by all five rules

- A: Conditions decide when an alert fires. Notifications belong in action groups.
- B: Correct. Action groups are reusable across alert rules.
- C: Severity labels urgency. It doesn't send notifications by itself.
- D: That duplicates configuration that one reusable action group can hold.

An alert rule has a scope, a condition, an action group and a severity (0 Critical to 4 Verbose). Action groups hold notifications and automated actions, and they're reusable across rules.

📘 Source: [Set alerts for app failures and anomalies](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/6-set-alerts-app-failures-anomalies)

</details>


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
