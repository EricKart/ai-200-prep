"""One function every service calls FIRST, before importing Flask.

configure_azure_monitor() (the Azure Monitor OpenTelemetry Distro) sets up:
  - traces  -> requests / dependencies tables
  - logs    -> traces table (Python's logging module is hooked in automatically)
  - metrics -> customMetrics table
and auto-instruments Flask (incoming requests) and the requests library (outgoing calls).

Where does it get its settings? From environment variables, so the code has no secrets:
  APPLICATIONINSIGHTS_CONNECTION_STRING  where to send telemetry
  OTEL_SERVICE_NAME                      e.g. "api-gateway"
  OTEL_RESOURCE_ATTRIBUTES               e.g. "service.namespace=rag-pipeline,service.instance.id=gw-1"
  OTEL_TRACES_SAMPLER / _ARG             sampling (run_demo.py sets these)
Cloud role name on the Application Map = service.namespace + "." + service.name

The same thing in code (the other option shown in Learn) would be:
  from opentelemetry.sdk.resources import Resource
  configure_azure_monitor(resource=Resource.create({"service.name": "api-gateway",
                                                    "service.namespace": "rag-pipeline"}))
"""
import logging
import os
import sys

from azure.monitor.opentelemetry import configure_azure_monitor


def setup_telemetry():
    if not os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING"):
        print("[!] APPLICATIONINSIGHTS_CONNECTION_STRING is not set in this terminal. Paste the guide's 'New terminal' block.")
        sys.exit(1)
    configure_azure_monitor(
        logger_name="rag",                 # only loggers named "rag..." are sent (keeps Flask noise out)
        enable_live_metrics=True,          # on by default; written here so you can see it
    )
    logger = logging.getLogger("rag")
    logger.setLevel(logging.INFO)
    return logger


def flush_telemetry():
    """Push everything that's still buffered to Application Insights (used before shutdown)."""
    from opentelemetry import metrics, trace
    from opentelemetry._logs import get_logger_provider

    for provider in (trace.get_tracer_provider(), metrics.get_meter_provider(), get_logger_provider()):
        if hasattr(provider, "force_flush"):
            provider.force_flush()
