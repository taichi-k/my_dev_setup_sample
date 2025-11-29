resource "aws_ecs_task_definition" "migration" {
  family                   = "test-migration-td"
  task_role_arn            = "arn:aws:iam::771623671665:role/test-task-role"
  execution_role_arn       = "arn:aws:iam::771623671665:role/test-task-execution-role"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"

  runtime_platform {
    cpu_architecture        = "ARM64"
    operating_system_family = "LINUX"
  }

  container_definitions = jsonencode([
    {
      name              = "app"
      image             = "${data.aws_ecr_repository.app.repository_url}:${var.image_tag}"
      cpu               = 512
      memory            = 1024
      memoryReservation = 1024
      essential         = true
      command = [
        "uv",
        "run",
        "alembic",
        "upgrade",
        "head"
      ]
      portMappings = []
      environment  = []
      mountPoints  = []
      volumesFrom  = []
      secrets = [
        {
          name      = "AWS_REGION"
          valueFrom = "/test/dev/app/AWS_REGION"
        },
        {
          name      = "DATABASE_URL"
          valueFrom = "/test/dev/app/DATABASE_URL"
        },
        {
          name      = "DATABASE_URL_SYNC"
          valueFrom = "/test/dev/app/DATABASE_URL_SYNC"
        },
        {
          name      = "GOOGLE_CLIENT_ID"
          valueFrom = "/test/dev/app/GOOGLE_CLIENT_ID"
        },
        {
          name      = "GOOGLE_CLIENT_SECRET"
          valueFrom = "/test/dev/app/GOOGLE_CLIENT_SECRET"
        },
        {
          name      = "OTEL_DEPLOYMENT_ENVIRONMENT"
          valueFrom = "/test/dev/app/OTEL_DEPLOYMENT_ENVIRONMENT"
        },
        {
          name      = "OTEL_EXPORTER_OTLP_ENDPOINT"
          valueFrom = "/test/dev/app/OTEL_EXPORTER_OTLP_ENDPOINT"
        },
        {
          name      = "OTEL_EXPORTER_OTLP_PROTOCOL"
          valueFrom = "/test/dev/app/OTEL_EXPORTER_OTLP_PROTOCOL"
        },
        {
          name      = "OTEL_LOGS_EXPORTER"
          valueFrom = "/test/dev/app/OTEL_LOGS_EXPORTER"
        },
        {
          name      = "OTEL_SERVICE_NAME"
          valueFrom = "/test/dev/app/OTEL_SERVICE_NAME"
        },
        {
          name      = "OTEL_SERVICE_NAMESPACE"
          valueFrom = "/test/dev/app/OTEL_SERVICE_NAMESPACE"
        },
        {
          name      = "OTEL_SERVICE_VERSION"
          valueFrom = "/test/dev/app/OTEL_SERVICE_VERSION"
        },
        {
          name      = "REDIS_HOST"
          valueFrom = "/test/dev/app/REDIS_HOST"
        },
        {
          name      = "REDIS_PORT"
          valueFrom = "/test/dev/app/REDIS_PORT"
        },
        {
          name      = "SECRET_KEY_FOR_SESSION_MIDDLEWARE"
          valueFrom = "/test/dev/app/SECRET_KEY_FOR_SESSION_MIDDLEWARE"
        },
        {
          name      = "SENTRY_DSN"
          valueFrom = "/test/dev/app/SENTRY_DSN"
        },
        {
          name      = "SQS_DLQ_NAME"
          valueFrom = "/test/dev/app/SQS_DLQ_NAME"
        },
        {
          name      = "SQS_DLQ_URL"
          valueFrom = "/test/dev/app/SQS_DLQ_URL"
        },
        {
          name      = "SQS_QUEUE_NAME"
          valueFrom = "/test/dev/app/SQS_QUEUE_NAME"
        },
        {
          name      = "SQS_QUEUE_URL"
          valueFrom = "/test/dev/app/SQS_QUEUE_URL"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/test-migration-td"
          "awslogs-create-group"  = "true"
          "awslogs-region"        = "ap-northeast-1"
          "awslogs-stream-prefix" = "ecs"
        }
        secretOptions = []
      }
      systemControls = []
    }
  ])
}
