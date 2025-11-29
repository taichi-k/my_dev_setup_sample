output "ssm_parameters_created" {
  description = "List of SSM parameter names created"
  value = [
    # App parameters
    aws_ssm_parameter.app_secret_key_for_session_middleware.name,
    aws_ssm_parameter.app_google_client_id.name,
    aws_ssm_parameter.app_google_client_secret.name,
    aws_ssm_parameter.app_database_url.name,
    aws_ssm_parameter.app_database_url_sync.name,
    aws_ssm_parameter.app_otel_exporter_otlp_endpoint.name,
    aws_ssm_parameter.app_otel_service_name.name,
    aws_ssm_parameter.app_otel_service_version.name,
    aws_ssm_parameter.app_otel_service_namespace.name,
    aws_ssm_parameter.app_otel_deployment_environment.name,
    aws_ssm_parameter.app_otel_logs_exporter.name,
    aws_ssm_parameter.app_otel_exporter_otlp_protocol.name,
    aws_ssm_parameter.app_sentry_dsn.name,
    aws_ssm_parameter.app_aws_region.name,
    aws_ssm_parameter.app_sqs_queue_name.name,
    aws_ssm_parameter.app_sqs_dlq_name.name,
    # Worker parameters
    aws_ssm_parameter.worker_database_url.name,
    aws_ssm_parameter.worker_database_url_sync.name,
    aws_ssm_parameter.worker_aws_region.name,
    aws_ssm_parameter.worker_sqs_queue_name.name,
    aws_ssm_parameter.worker_sqs_dlq_name.name,
    # OTEL Collector parameters
    aws_ssm_parameter.otel_collector_loki_host.name,
    aws_ssm_parameter.otel_collector_loki_port.name,
  ]
}
