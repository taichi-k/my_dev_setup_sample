resource "aws_ecs_service" "app" {
  name                          = "test-app-td-service-1tlr13r8"
  cluster                       = aws_ecs_cluster.this.id
  task_definition               = aws_ecs_task_definition.app.arn
  desired_count                 = 0
  availability_zone_rebalancing = "ENABLED"
  wait_for_steady_state         = false

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

  load_balancer {
    target_group_arn = "arn:aws:elasticloadbalancing:ap-northeast-1:771623671665:targetgroup/test-ecs-tg/ad645089803a3a56"
    container_name   = "app"
    container_port   = 8000
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  health_check_grace_period_seconds = 0
  enable_execute_command            = true
  enable_ecs_managed_tags           = true
  propagate_tags                    = "NONE"

  platform_version = "LATEST"

  depends_on = [aws_ecs_cluster.this]
}

import {
  to = aws_ecs_service.app
  id = "test-cluster-kosugi/test-app-td-service-1tlr13r8"
}
