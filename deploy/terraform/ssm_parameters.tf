# ========================================
# App Service Parameters
# ========================================

resource "aws_ssm_parameter" "app_secret_key_for_session_middleware" {
  name  = "/${var.project_name}/${var.environment}/app/SECRET_KEY_FOR_SESSION_MIDDLEWARE"
  type  = "SecureString"
  value = var.app_secret_key_for_session_middleware

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_google_client_id" {
  name  = "/${var.project_name}/${var.environment}/app/GOOGLE_CLIENT_ID"
  type  = "SecureString"
  value = var.app_google_client_id

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_google_client_secret" {
  name  = "/${var.project_name}/${var.environment}/app/GOOGLE_CLIENT_SECRET"
  type  = "SecureString"
  value = var.app_google_client_secret

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_google_auth_redirect_url" {
  name  = "/${var.project_name}/${var.environment}/app/GOOGLE_AUTH_REDIRECT_URL"
  type  = "String"
  value = var.app_google_auth_redirect_url

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_database_url" {
  name  = "/${var.project_name}/${var.environment}/app/DATABASE_URL"
  type  = "SecureString"
  value = var.app_database_url

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_database_url_sync" {
  name  = "/${var.project_name}/${var.environment}/app/DATABASE_URL_SYNC"
  type  = "SecureString"
  value = var.app_database_url_sync

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_otel_exporter_otlp_endpoint" {
  name  = "/${var.project_name}/${var.environment}/app/OTEL_EXPORTER_OTLP_ENDPOINT"
  type  = "String"
  value = var.app_otel_exporter_otlp_endpoint

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_otel_service_name" {
  name  = "/${var.project_name}/${var.environment}/app/OTEL_SERVICE_NAME"
  type  = "String"
  value = var.app_otel_service_name

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_otel_service_version" {
  name  = "/${var.project_name}/${var.environment}/app/OTEL_SERVICE_VERSION"
  type  = "String"
  value = var.app_otel_service_version

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_otel_service_namespace" {
  name  = "/${var.project_name}/${var.environment}/app/OTEL_SERVICE_NAMESPACE"
  type  = "String"
  value = var.app_otel_service_namespace

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_otel_deployment_environment" {
  name  = "/${var.project_name}/${var.environment}/app/OTEL_DEPLOYMENT_ENVIRONMENT"
  type  = "String"
  value = var.app_otel_deployment_environment

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_otel_logs_exporter" {
  name  = "/${var.project_name}/${var.environment}/app/OTEL_LOGS_EXPORTER"
  type  = "String"
  value = var.app_otel_logs_exporter

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_otel_exporter_otlp_protocol" {
  name  = "/${var.project_name}/${var.environment}/app/OTEL_EXPORTER_OTLP_PROTOCOL"
  type  = "String"
  value = var.app_otel_exporter_otlp_protocol

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_sentry_dsn" {
  name  = "/${var.project_name}/${var.environment}/app/SENTRY_DSN"
  type  = "SecureString"
  value = var.app_sentry_dsn

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_aws_region" {
  name  = "/${var.project_name}/${var.environment}/app/AWS_REGION"
  type  = "String"
  value = var.app_aws_region

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_sqs_queue_name" {
  name  = "/${var.project_name}/${var.environment}/app/SQS_QUEUE_NAME"
  type  = "String"
  value = var.app_sqs_queue_name

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_sqs_dlq_name" {
  name  = "/${var.project_name}/${var.environment}/app/SQS_DLQ_NAME"
  type  = "String"
  value = var.app_sqs_dlq_name

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_sqs_queue_url" {
  name  = "/${var.project_name}/${var.environment}/app/SQS_QUEUE_URL"
  type  = "String"
  value = var.app_sqs_queue_url

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_sqs_dlq_url" {
  name  = "/${var.project_name}/${var.environment}/app/SQS_DLQ_URL"
  type  = "String"
  value = var.app_sqs_dlq_url

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_redis_host" {
  name  = "/${var.project_name}/${var.environment}/app/REDIS_HOST"
  type  = "String"
  value = var.app_redis_host

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "app_redis_port" {
  name  = "/${var.project_name}/${var.environment}/app/REDIS_PORT"
  type  = "String"
  value = var.app_redis_port

  tags = {
    Service     = "app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# ========================================
# Worker Service Parameters
# ========================================

resource "aws_ssm_parameter" "worker_database_url" {
  name  = "/${var.project_name}/${var.environment}/worker/DATABASE_URL"
  type  = "SecureString"
  value = var.worker_database_url

  tags = {
    Service     = "worker"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "worker_database_url_sync" {
  name  = "/${var.project_name}/${var.environment}/worker/DATABASE_URL_SYNC"
  type  = "SecureString"
  value = var.worker_database_url_sync

  tags = {
    Service     = "worker"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "worker_aws_region" {
  name  = "/${var.project_name}/${var.environment}/worker/AWS_REGION"
  type  = "String"
  value = var.worker_aws_region

  tags = {
    Service     = "worker"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "worker_sqs_queue_name" {
  name  = "/${var.project_name}/${var.environment}/worker/SQS_QUEUE_NAME"
  type  = "String"
  value = var.worker_sqs_queue_name

  tags = {
    Service     = "worker"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "worker_sqs_dlq_name" {
  name  = "/${var.project_name}/${var.environment}/worker/SQS_DLQ_NAME"
  type  = "String"
  value = var.worker_sqs_dlq_name

  tags = {
    Service     = "worker"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "worker_sqs_queue_url" {
  name  = "/${var.project_name}/${var.environment}/worker/SQS_QUEUE_URL"
  type  = "String"
  value = var.worker_sqs_queue_url

  tags = {
    Service     = "worker"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "worker_sqs_dlq_url" {
  name  = "/${var.project_name}/${var.environment}/worker/SQS_DLQ_URL"
  type  = "String"
  value = var.worker_sqs_dlq_url

  tags = {
    Service     = "worker"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# ========================================
# OTEL Collector Parameters
# ========================================

resource "aws_ssm_parameter" "otel_collector_loki_host" {
  name  = "/${var.project_name}/${var.environment}/otel-collector/LOKI_HOST"
  type  = "String"
  value = var.otel_collector_loki_host

  tags = {
    Service     = "otel-collector"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ssm_parameter" "otel_collector_loki_port" {
  name  = "/${var.project_name}/${var.environment}/otel-collector/LOKI_PORT"
  type  = "String"
  value = var.otel_collector_loki_port

  tags = {
    Service     = "otel-collector"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}
