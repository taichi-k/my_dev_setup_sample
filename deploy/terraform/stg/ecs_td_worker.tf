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
      image             = "${data.aws_ecr_repository.worker.repository_url}:${var.image_tag}"
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
