FROM otel/opentelemetry-collector-contrib:0.89.0

COPY infra/observability/otel/otel-collector.yaml /etc/otelcol-contrib/otel-collector.yaml

CMD ["--config=/etc/otelcol-contrib/otel-collector.yaml"]
