variable "environment" {
  description = "Environment name (dev, stg, prd)"
  type        = string
}

variable "project_name" {
  description = "Project name for parameter path prefix"
  type        = string
}

variable "aws_region" {
  description = "AWS region for provider"
  type        = string
}

# ========================================
# App Service Variables
# ========================================

variable "app_secret_key_for_session_middleware" {
  description = "Secret key for session middleware"
  type        = string
  sensitive   = true
}

variable "app_google_client_id" {
  description = "Google OAuth client ID"
  type        = string
  sensitive   = true
}

variable "app_google_client_secret" {
  description = "Google OAuth client secret"
  type        = string
  sensitive   = true
}

variable "app_google_auth_redirect_url" {
  description = "Google OAuth redirect URL"
  type        = string
}

variable "app_database_url" {
  description = "Database URL for async connections"
  type        = string
  sensitive   = true
}

variable "app_database_url_sync" {
  description = "Database URL for sync connections"
  type        = string
  sensitive   = true
}

variable "app_otel_exporter_otlp_endpoint" {
  description = "OTEL OTLP endpoint"
  type        = string
}

variable "app_otel_service_name" {
  description = "OTEL service name"
  type        = string
}

variable "app_otel_service_version" {
  description = "OTEL service version"
  type        = string
}

variable "app_otel_service_namespace" {
  description = "OTEL service namespace"
  type        = string
}

variable "app_otel_deployment_environment" {
  description = "OTEL deployment environment"
  type        = string
}

variable "app_otel_logs_exporter" {
  description = "OTEL logs exporter"
  type        = string
}

variable "app_otel_exporter_otlp_protocol" {
  description = "OTEL OTLP protocol"
  type        = string
}

variable "app_sentry_dsn" {
  description = "Sentry DSN"
  type        = string
  sensitive   = true
}

variable "app_aws_region" {
  description = "AWS region"
  type        = string
}

variable "app_sqs_queue_name" {
  description = "SQS queue name"
  type        = string
}

variable "app_sqs_dlq_name" {
  description = "SQS DLQ name"
  type        = string
}

variable "app_sqs_queue_url" {
  description = "SQS queue URL"
  type        = string
}

variable "app_sqs_dlq_url" {
  description = "SQS DLQ URL"
  type        = string
}

variable "app_redis_host" {
  description = "Redis host"
  type        = string
}

variable "app_redis_port" {
  description = "Redis port"
  type        = string
}

variable "app_redis_use_tls" {
  description = "Whether to use TLS for Redis connection"
  type        = string
}

# ========================================
# Worker Service Variables
# ========================================

variable "worker_database_url" {
  description = "Worker database URL for async connections"
  type        = string
  sensitive   = true
}

variable "worker_database_url_sync" {
  description = "Worker database URL for sync connections"
  type        = string
  sensitive   = true
}

variable "worker_aws_region" {
  description = "Worker AWS region"
  type        = string
}

variable "worker_sqs_queue_name" {
  description = "Worker SQS queue name"
  type        = string
}

variable "worker_sqs_dlq_name" {
  description = "Worker SQS DLQ name"
  type        = string
}

variable "worker_sqs_queue_url" {
  description = "Worker SQS queue URL"
  type        = string
}

variable "worker_sqs_dlq_url" {
  description = "Worker SQS DLQ URL"
  type        = string
}

# ========================================
# OTEL Collector Variables
# ========================================

variable "otel_collector_loki_host" {
  description = "Loki host for OTEL collector"
  type        = string
}

variable "otel_collector_loki_port" {
  description = "Loki port for OTEL collector"
  type        = string
}
