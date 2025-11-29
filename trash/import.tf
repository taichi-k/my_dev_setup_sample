import {
  to = module.network.aws_vpc.this
  id = "vpc-0ffbb018b6691139b"
}

import {
  to = module.network.aws_internet_gateway.main
  id = "igw-08e56cecb6cbd1cb6"
}

import {
  to = module.network.aws_subnet.public1
  id = "subnet-042e7397365a82c5f"
}

import {
  to = module.network.aws_subnet.public2
  id = "subnet-01a269fcba0d61dc7"
}

import {
  to = module.network.aws_subnet.private1
  id = "subnet-00a61ab5040f1a9d8"
}

import {
  to = module.network.aws_subnet.private2
  id = "subnet-01203211c2b3d75af"
}

import {
  to = module.network.aws_subnet.private3
  id = "subnet-0a63623d055a54468"
}

import {
  to = module.network.aws_subnet.private4
  id = "subnet-04946856519c98821"
}

# ========================================
# App Service SSM Parameters
# ========================================

import {
  to = aws_ssm_parameter.app_secret_key_for_session_middleware
  id = "/${var.project_name}/${var.environment}/app/SECRET_KEY_FOR_SESSION_MIDDLEWARE"
}

import {
  to = aws_ssm_parameter.app_google_client_id
  id = "/${var.project_name}/${var.environment}/app/GOOGLE_CLIENT_ID"
}

import {
  to = aws_ssm_parameter.app_google_client_secret
  id = "/${var.project_name}/${var.environment}/app/GOOGLE_CLIENT_SECRET"
}

import {
  to = aws_ssm_parameter.app_google_auth_redirect_url
  id = "/${var.project_name}/${var.environment}/app/GOOGLE_AUTH_REDIRECT_URL"
}

import {
  to = aws_ssm_parameter.app_database_url
  id = "/${var.project_name}/${var.environment}/app/DATABASE_URL"
}

import {
  to = aws_ssm_parameter.app_database_url_sync
  id = "/${var.project_name}/${var.environment}/app/DATABASE_URL_SYNC"
}

import {
  to = aws_ssm_parameter.app_otel_exporter_otlp_endpoint
  id = "/${var.project_name}/${var.environment}/app/OTEL_EXPORTER_OTLP_ENDPOINT"
}

import {
  to = aws_ssm_parameter.app_otel_service_name
  id = "/${var.project_name}/${var.environment}/app/OTEL_SERVICE_NAME"
}

import {
  to = aws_ssm_parameter.app_otel_service_version
  id = "/${var.project_name}/${var.environment}/app/OTEL_SERVICE_VERSION"
}

import {
  to = aws_ssm_parameter.app_otel_service_namespace
  id = "/${var.project_name}/${var.environment}/app/OTEL_SERVICE_NAMESPACE"
}

import {
  to = aws_ssm_parameter.app_otel_deployment_environment
  id = "/${var.project_name}/${var.environment}/app/OTEL_DEPLOYMENT_ENVIRONMENT"
}

import {
  to = aws_ssm_parameter.app_otel_logs_exporter
  id = "/${var.project_name}/${var.environment}/app/OTEL_LOGS_EXPORTER"
}

import {
  to = aws_ssm_parameter.app_otel_exporter_otlp_protocol
  id = "/${var.project_name}/${var.environment}/app/OTEL_EXPORTER_OTLP_PROTOCOL"
}

import {
  to = aws_ssm_parameter.app_sentry_dsn
  id = "/${var.project_name}/${var.environment}/app/SENTRY_DSN"
}

import {
  to = aws_ssm_parameter.app_aws_region
  id = "/${var.project_name}/${var.environment}/app/AWS_REGION"
}

import {
  to = aws_ssm_parameter.app_sqs_queue_name
  id = "/${var.project_name}/${var.environment}/app/SQS_QUEUE_NAME"
}

import {
  to = aws_ssm_parameter.app_sqs_dlq_name
  id = "/${var.project_name}/${var.environment}/app/SQS_DLQ_NAME"
}

import {
  to = aws_ssm_parameter.app_sqs_queue_url
  id = "/${var.project_name}/${var.environment}/app/SQS_QUEUE_URL"
}

import {
  to = aws_ssm_parameter.app_sqs_dlq_url
  id = "/${var.project_name}/${var.environment}/app/SQS_DLQ_URL"
}

import {
  to = aws_ssm_parameter.app_redis_host
  id = "/${var.project_name}/${var.environment}/app/REDIS_HOST"
}

import {
  to = aws_ssm_parameter.app_redis_port
  id = "/${var.project_name}/${var.environment}/app/REDIS_PORT"
}

import {
  to = aws_ssm_parameter.app_redis_use_tls
  id = "/${var.project_name}/${var.environment}/app/REDIS_USE_TLS"
}

# ========================================
# Worker Service SSM Parameters
# ========================================

import {
  to = aws_ssm_parameter.worker_database_url
  id = "/${var.project_name}/${var.environment}/worker/DATABASE_URL"
}

import {
  to = aws_ssm_parameter.worker_database_url_sync
  id = "/${var.project_name}/${var.environment}/worker/DATABASE_URL_SYNC"
}

import {
  to = aws_ssm_parameter.worker_aws_region
  id = "/${var.project_name}/${var.environment}/worker/AWS_REGION"
}

import {
  to = aws_ssm_parameter.worker_sqs_queue_name
  id = "/${var.project_name}/${var.environment}/worker/SQS_QUEUE_NAME"
}

import {
  to = aws_ssm_parameter.worker_sqs_dlq_name
  id = "/${var.project_name}/${var.environment}/worker/SQS_DLQ_NAME"
}

import {
  to = aws_ssm_parameter.worker_sqs_queue_url
  id = "/${var.project_name}/${var.environment}/worker/SQS_QUEUE_URL"
}

import {
  to = aws_ssm_parameter.worker_sqs_dlq_url
  id = "/${var.project_name}/${var.environment}/worker/SQS_DLQ_URL"
}

# ========================================
# OTEL Collector SSM Parameters
# ========================================

import {
  to = aws_ssm_parameter.otel_collector_loki_host
  id = "/${var.project_name}/${var.environment}/otel-collector/LOKI_HOST"
}

import {
  to = aws_ssm_parameter.otel_collector_loki_port
  id = "/${var.project_name}/${var.environment}/otel-collector/LOKI_PORT"
}
