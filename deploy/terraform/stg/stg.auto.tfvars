# Environment Configuration
environment  = "dev"
project_name = "test"
aws_region   = "ap-northeast-1"

# ========================================
# App Service Variables
# ========================================

app_google_auth_redirect_url          = "http://test-alb-1982208238.ap-northeast-1.elb.amazonaws.com/auth/callback"
app_otel_exporter_otlp_endpoint       = "otel-collector:4317"
app_otel_service_name                 = "app"
app_otel_service_version              = "1.0.0"
app_otel_service_namespace            = "myproj"
app_otel_deployment_environment       = "dev"
app_otel_logs_exporter                = "otlp"
app_otel_exporter_otlp_protocol       = "http/protobuf"
app_aws_region                        = "ap-northeast-1"
app_sqs_queue_name                    = "test-queue"
app_sqs_dlq_name                      = "test-queue-dlq"
app_sqs_queue_url                     = "https://sqs.ap-northeast-1.amazonaws.com/771623671665/test-queue"
app_sqs_dlq_url                       = "https://sqs.ap-northeast-1.amazonaws.com/771623671665/test-queue-dlq"
app_redis_host                        = "test-valkey-w1wf5a.serverless.apne1.cache.amazonaws.com"
app_redis_port                        = "6379"
app_redis_use_tls                     = "true"

# ========================================
# Worker Service Variables
# ========================================

worker_aws_region        = "ap-northeast-1"
worker_sqs_queue_name    = "test-queue"
worker_sqs_dlq_name      = "test-queue-dlq"
worker_sqs_queue_url     = "https://sqs.ap-northeast-1.amazonaws.com/771623671665/test-queue"
worker_sqs_dlq_url       = "https://sqs.ap-northeast-1.amazonaws.com/771623671665/test-queue-dlq"

# ========================================
# OTEL Collector Variables
# ========================================

otel_collector_loki_host = "loki"
otel_collector_loki_port = "3100"
