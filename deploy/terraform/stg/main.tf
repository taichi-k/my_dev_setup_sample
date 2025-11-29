
provider "aws" {
  profile = "dev-setup-sample"
  region  = "ap-northeast-1"
}

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "771623671665-stg-test-terraform-state"
    key    = "terraform.tfstate"
    region = "ap-northeast-1"
  }
}

module "network" {
  source = "../modules/network"
}

module "ssm_parameters" {
  source = "../modules/ssm_parameters"

  environment  = var.environment
  project_name = var.project_name
  aws_region   = var.aws_region

  # App Service Variables
  app_secret_key_for_session_middleware = var.app_secret_key_for_session_middleware
  app_google_client_id                  = var.app_google_client_id
  app_google_client_secret              = var.app_google_client_secret
  app_google_auth_redirect_url          = var.app_google_auth_redirect_url
  app_database_url                      = var.app_database_url
  app_database_url_sync                 = var.app_database_url_sync
  app_otel_exporter_otlp_endpoint       = var.app_otel_exporter_otlp_endpoint
  app_otel_service_name                 = var.app_otel_service_name
  app_otel_service_version              = var.app_otel_service_version
  app_otel_service_namespace            = var.app_otel_service_namespace
  app_otel_deployment_environment       = var.app_otel_deployment_environment
  app_otel_logs_exporter                = var.app_otel_logs_exporter
  app_otel_exporter_otlp_protocol       = var.app_otel_exporter_otlp_protocol
  app_sentry_dsn                        = var.app_sentry_dsn
  app_aws_region                        = var.app_aws_region
  app_sqs_queue_name                    = var.app_sqs_queue_name
  app_sqs_dlq_name                      = var.app_sqs_dlq_name
  app_sqs_queue_url                     = var.app_sqs_queue_url
  app_sqs_dlq_url                       = var.app_sqs_dlq_url
  app_redis_host                        = var.app_redis_host
  app_redis_port                        = var.app_redis_port
  app_redis_use_tls                     = var.app_redis_use_tls

  # Worker Service Variables
  worker_database_url      = var.worker_database_url
  worker_database_url_sync = var.worker_database_url_sync
  worker_aws_region        = var.worker_aws_region
  worker_sqs_queue_name    = var.worker_sqs_queue_name
  worker_sqs_dlq_name      = var.worker_sqs_dlq_name
  worker_sqs_queue_url     = var.worker_sqs_queue_url
  worker_sqs_dlq_url       = var.worker_sqs_dlq_url

  # OTEL Collector Variables
  otel_collector_loki_host = var.otel_collector_loki_host
  otel_collector_loki_port = var.otel_collector_loki_port
}
