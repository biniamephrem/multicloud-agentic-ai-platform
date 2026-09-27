"""OpenTelemetry bootstrap; becomes a no-op when OTEL packages are absent."""
def configure(service_name="multicloud-agentic-ai"):
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.resources import Resource
        trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": service_name})))
        return trace.get_tracer(service_name)
    except Exception:
        return None
