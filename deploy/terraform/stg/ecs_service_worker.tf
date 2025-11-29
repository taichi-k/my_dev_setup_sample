resource "aws_ecs_service" "worker" {
  name            = "test-worker-td-service-6ku34fxr"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.worker.arn
  desired_count   = 0

  capacity_provider_strategy {
    capacity_provider = "FARGATE"
    weight            = 1
    base              = 0
  }

  network_configuration {
    subnets          = ["subnet-01203211c2b3d75af", "subnet-00a61ab5040f1a9d8"]
    security_groups  = ["sg-0a53a2fd3a34354e7"]
    assign_public_ip = false
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  deployment_maximum_percent         = 200
  deployment_minimum_healthy_percent = 100

  health_check_grace_period_seconds = 0
  enable_execute_command            = false
  enable_ecs_managed_tags           = true
  propagate_tags                    = "NONE"

  platform_version = "LATEST"

  depends_on = [aws_ecs_cluster.this]
}

import {
  to = aws_ecs_service.worker
  id = "test-cluster-kosugi/test-worker-td-service-6ku34fxr"
}
