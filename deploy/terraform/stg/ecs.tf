resource "aws_ecs_cluster" "this" {
  name = "test-cluster-kosugi"
  configuration {
    execute_command_configuration {
      logging = "DEFAULT"
    }
  }
}


resource "aws_ecs_task_definition" "app" {
  family                   = "test-app-td"
  task_role_arn            = "arn:aws:iam::771623671665:role/test-task-role"
  execution_role_arn       = "arn:aws:iam::771623671665:role/test-task-execution-role"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "3072"

  runtime_platform {
    cpu_architecture        = "ARM64"
    operating_system_family = "LINUX"
  }

  container_definitions = jsonencode([
    {
      name              = "app"
      image             = "771623671665.dkr.ecr.ap-northeast-1.amazonaws.com/test/app@sha256:04abf87d3d53c6c192daf7e4e13d93455936e7d02523d69779ffae7b86c6bed8"
      cpu               = 512
      memory            = 2048
      memoryReservation = 2048
      portMappings = [
        {
          appProtocol   = "http"
          containerPort = 8000
          hostPort      = 8000
          name          = "app-80-tcp"
          protocol      = "tcp"
        }
      ]
      essential   = true
      environment = []
      mountPoints = []
      volumesFrom = []
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
          name      = "GOOGLE_AUTH_REDIRECT_URL"
          valueFrom = "/test/dev/app/GOOGLE_AUTH_REDIRECT_URL"
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
          name      = "REDIS_USE_TLS"
          valueFrom = "/test/dev/app/REDIS_USE_TLS"
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
      dependsOn = [
        {
          containerName = "otel_collector"
          condition     = "START"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/test-app-td"
          "awslogs-create-group"  = "true"
          "awslogs-region"        = "ap-northeast-1"
          "awslogs-stream-prefix" = "ecs"
        }
        secretOptions = []
      }
      systemControls = []
    },
    {
      name              = "otel_collector"
      image             = "771623671665.dkr.ecr.ap-northeast-1.amazonaws.com/test/otel_collector@sha256:d68fc4a7cdfa01d7f373c692b060e922458f779aa3e44ac408890de0844dce90"
      cpu               = 512
      memory            = 1024
      memoryReservation = 1024
      portMappings = [
        {
          appProtocol   = "http"
          name          = "prometheus"
          containerPort = 8889
          hostPort      = 8889
          protocol      = "tcp"
        }
      ]
      essential   = false
      environment = []
      mountPoints = []
      volumesFrom = []
      secrets = [
        {
          name      = "LOKI_HOST"
          valueFrom = "/test/dev/otel-collector/LOKI_HOST"
        },
        {
          name      = "LOKI_PORT"
          valueFrom = "/test/dev/otel-collector/LOKI_PORT"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/test-app-td"
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
      image             = "771623671665.dkr.ecr.ap-northeast-1.amazonaws.com/test/app@sha256:10689530f19e0bd8bb56108f6400bcc7034b599f8b6886c3996e74216bfaa1ad"
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


resource "aws_ecs_task_definition" "worker" {
  family                   = "test-worker-td"
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
      name              = "worker"
      image             = "771623671665.dkr.ecr.ap-northeast-1.amazonaws.com/test/worker@sha256:acf6bc3850a4883682f0bfa22155b0741d43e7c33f02b09ea1d2990231a67a21"
      cpu               = 512
      memory            = 1024
      memoryReservation = 1024
      essential         = true
      portMappings      = []
      environment       = []
      environmentFiles  = []
      mountPoints       = []
      volumesFrom       = []
      secrets = [
        {
          name      = "AWS_REGION"
          valueFrom = "/test/dev/worker/AWS_REGION"
        },
        {
          name      = "DATABASE_URL"
          valueFrom = "/test/dev/worker/DATABASE_URL"
        },
        {
          name      = "DATABASE_URL_SYNC"
          valueFrom = "/test/dev/worker/DATABASE_URL_SYNC"
        },
        {
          name      = "SQS_DLQ_NAME"
          valueFrom = "/test/dev/worker/SQS_DLQ_NAME"
        },
        {
          name      = "SQS_QUEUE_NAME"
          valueFrom = "/test/dev/worker/SQS_QUEUE_NAME"
        },
        {
          name      = "SQS_DLQ_URL"
          valueFrom = "/test/dev/worker/SQS_DLQ_URL"
        },
        {
          name      = "SQS_QUEUE_URL"
          valueFrom = "/test/dev/worker/SQS_QUEUE_URL"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/test-worker-td"
          "awslogs-create-group"  = "true"
          "awslogs-region"        = "ap-northeast-1"
          "awslogs-stream-prefix" = "ecs"
        }
        secretOptions = []
      }
      systemControls = []
      ulimits        = []
    }
  ])
}


import {
  to = aws_ecs_task_definition.worker
  id = "arn:aws:ecs:ap-northeast-1:771623671665:task-definition/test-worker-td:3"
}
