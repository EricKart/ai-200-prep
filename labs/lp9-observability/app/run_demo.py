"""Starts the 3 services, sends traffic, flushes telemetry, and stops them.

  python run_demo.py                     normal mix: ~40 requests incl. slow, 429, overflow, cold start
  python run_demo.py --failures 15       also send 15 failing requests (to trip the alert in Part 9)
  python run_demo.py --sampling 0.25     keep only ~25% of traces (Part 5 experiment)
  python run_demo.py --serve             start services and keep them running (Ctrl+C to stop);
                                         open http://127.0.0.1:5001/ask in a browser

Each service is a separate process with its own OTEL_SERVICE_NAME, exactly like 3 microservices.
Service logs go to the logs/ folder.
"""
import lab_env  # noqa: F401  first import: stops with a clear message if the venv isn't active
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
SERVICES = [  # (file, service.name, port)
    ("llm_service.py", "llm-service", 5003),
    ("orchestrator.py", "llm-orchestrator", 5002),
    ("gateway.py", "api-gateway", 5001),
]
GATEWAY = "http://127.0.0.1:5001"


def start_services(sampling):
    if not os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING"):
        sys.exit("[!] APPLICATIONINSIGHTS_CONNECTION_STRING is not set in this terminal. Paste the guide's 'New terminal' block.")
    (HERE / "logs").mkdir(exist_ok=True)
    procs = []
    for file, name, port in SERVICES:
        env = dict(os.environ)
        env.update(
            PORT=str(port),
            OTEL_SERVICE_NAME=name,
            OTEL_RESOURCE_ATTRIBUTES=f"service.namespace=rag-pipeline,service.instance.id={name}-1",
            OTEL_TRACES_SAMPLER="microsoft.fixed_percentage",
            OTEL_TRACES_SAMPLER_ARG=str(sampling),
            PYTHONUNBUFFERED="1",
            # Keep the data clean: don't record the /flush helper or the SDK's own calls...
            OTEL_PYTHON_EXCLUDED_URLS="flush,settings.sdk.monitor.azure.com,169.254.169.254",
            # ...and skip the Azure VM / App Service detectors (they probe 169.254.169.254,
            # which times out on a laptop and shows up as fake ConnectTimeout exceptions).
            OTEL_EXPERIMENTAL_RESOURCE_DETECTORS="otel",
        )
        out = open(HERE / "logs" / f"{name}.log", "w")
        procs.append(subprocess.Popen([sys.executable, str(HERE / "services" / file)], env=env,
                                      stdout=out, stderr=subprocess.STDOUT))
    for _, name, port in SERVICES:                       # wait until each one answers
        for _ in range(60):
            try:
                requests.post(f"http://127.0.0.1:{port}/flush", timeout=2)
                break
            except requests.ConnectionError:
                time.sleep(0.5)
        else:
            stop(procs)
            sys.exit(f"[!] {name} did not start. Look at logs/{name}.log")
    print(f"3 services running (sampling = {sampling}).")
    return procs


def stop(procs):
    for _, _, port in SERVICES:
        try:
            requests.post(f"http://127.0.0.1:{port}/flush", timeout=15)   # send buffered telemetry
        except requests.RequestException:
            pass
    for p in procs:
        p.terminate()
    for p in procs:
        p.wait(timeout=10)


def call(scenario, q="How do I reset my password?"):
    start = time.perf_counter()
    try:
        r = requests.get(f"{GATEWAY}/ask", params={"q": q, "scenario": scenario}, timeout=40)
        status, trace_id = r.status_code, r.json().get("trace_id", "")
    except requests.RequestException as e:
        status, trace_id = f"ERR {type(e).__name__}", ""
    ms = (time.perf_counter() - start) * 1000
    print(f"  {scenario:<11} -> HTTP {status}  {ms:6.0f} ms  operation_Id={trace_id}")


def traffic(failures):
    print("\nRound 1 (first search is a COLD START):")
    for s in ["normal"] * 8 + ["slow-llm", "normal", "rate-limit", "normal", "overflow", "normal", "slow-llm"]:
        call(s)
    print("\nIdle 25 s so the vector index goes cold again...")
    time.sleep(25)
    print("Round 2:")
    for s in ["normal"] * 10 + ["rate-limit", "slow-llm", "overflow", "rate-limit", "normal", "overflow"] + ["normal"] * 8:
        call(s)
    if failures:
        print(f"\nFailure burst: {failures} requests that overflow the context window:")
        for _ in range(failures):
            call("overflow")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sampling", type=float, default=1.0, help="0.0-1.0, share of traces kept")
    ap.add_argument("--failures", type=int, default=0, help="extra failing requests to send")
    ap.add_argument("--serve", action="store_true", help="keep services running until Ctrl+C")
    args = ap.parse_args()

    procs = start_services(args.sampling)
    try:
        if args.serve:
            print(f"Open {GATEWAY}/ask  or  {GATEWAY}/ask?scenario=slow-llm  (also: rate-limit, overflow)")
            print("Press Ctrl+C to stop.")
            while True:
                time.sleep(1)
        traffic(args.failures)
    except KeyboardInterrupt:
        pass
    finally:
        print("\nFlushing telemetry and stopping services...")
        stop(procs)
    print("Done. Data appears in Application Insights in about 2-5 minutes.")


if __name__ == "__main__":
    main()
