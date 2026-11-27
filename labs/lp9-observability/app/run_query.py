"""Run the KQL files in queries/ against your Application Insights resource.

  python run_query.py              list the queries
  python run_query.py 07           run queries/07_*.kql
  python run_query.py 21 --op <operation_Id>
  python run_query.py all          run every query

You can paste the same .kql text into the portal: Application Insights > Logs (switch to KQL mode).
`render` lines only matter in the portal (they draw a chart); here you get the table.
Needs: APPINSIGHTS_RESOURCE_ID, and `az login` (DefaultAzureCredential).
"""
import lab_env  # noqa: F401  first import: stops with a clear message if the venv isn't active
import argparse
import os
import sys
from datetime import timedelta
from pathlib import Path

import time

from azure.core.exceptions import HttpResponseError, ServiceRequestError, ServiceResponseError
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus

QDIR = Path(__file__).resolve().parent / "queries"


def run(client, resource_id, path, op):
    text = path.read_text()
    title = text.splitlines()[0].lstrip("/ ")
    kql = "\n".join(line for line in text.splitlines() if not line.startswith("//"))
    if "{OperationId}" in kql and not op:
        print(f"\n### {path.stem}  -  skipped: add --op <operation_Id> (copy one from run_demo.py output)")
        return
    kql = kql.replace("{TimeRange}", "24h").replace("{OperationId}", op or "")
    print(f"\n### {path.stem}  -  {title}")
    for attempt in range(4):                       # retry short network blips
        try:
            resp = client.query_resource(resource_id, kql, timespan=timedelta(days=2))
            break
        except (ServiceRequestError, ServiceResponseError) as e:
            if attempt == 3:
                print(f"  network error, try again: {str(e)[:100]}")
                return
            time.sleep(2)
        except HttpResponseError as e:
            print(f"  query failed: HTTP {e.status_code} {e.message[:200]}")
            return
    if resp.status != LogsQueryStatus.SUCCESS:
        print("  query error:", getattr(resp, "partial_error", resp))
        return
    for table in resp.tables:
        cols = table.columns
        rows = [[("" if v is None else str(v))[:60] for v in r] for r in table.rows]
        if not rows:
            print("  (no rows yet - wait 2-5 minutes after sending traffic, then try again)")
            continue
        widths = [max(len(c), *(len(r[i]) for r in rows)) for i, c in enumerate(cols)]
        print("  " + "  ".join(c.ljust(w) for c, w in zip(cols, widths)))
        print("  " + "  ".join("-" * w for w in widths))
        for r in rows[:25]:
            print("  " + "  ".join(v.ljust(w) for v, w in zip(r, widths)))
        if len(rows) > 25:
            print(f"  ... {len(rows) - 25} more rows")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("which", nargs="?", help="query number like 07, or 'all'")
    ap.add_argument("--op", help="operation_Id for query 21")
    args = ap.parse_args()
    files = sorted(QDIR.glob("*.kql"))
    if not args.which:
        for f in files:
            print(f"  {f.stem:<36} {f.read_text().splitlines()[0].lstrip('/ ')}")
        return
    resource_id = os.environ.get("APPINSIGHTS_RESOURCE_ID")
    if not resource_id:
        sys.exit("[!] APPINSIGHTS_RESOURCE_ID is not set in this terminal. Paste the guide's 'New terminal' block.")
    picked = files if args.which == "all" else [f for f in files if f.stem.startswith(args.which.zfill(2))]
    if not picked:
        sys.exit(f"No query starts with {args.which}. Run `python run_query.py` to list them.")
    client = LogsQueryClient(DefaultAzureCredential())
    for f in picked:
        run(client, resource_id, f, args.op)


if __name__ == "__main__":
    main()
