"""
OpenTelemetry tracing for SwarmForge.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def setup_tracing(service_name: str = "swarmforge", endpoint: str = "http://localhost:4317"):
    """Initialize OpenTelemetry tracing."""
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        provider = TracerProvider()
        exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)

        logger.info(f"OpenTelemetry tracing enabled (endpoint={endpoint})")
    except ImportError:
        logger.warning("OpenTelemetry packages not installed. Tracing disabled.")
    except Exception as e:
        logger.warning(f"Failed to setup tracing: {e}")
