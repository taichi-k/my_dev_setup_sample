data "aws_ecr_repository" "app" {
  name = "test/app"
}

data "aws_ecr_repository" "otel_collector" {
  name = "test/otel_collector"
}

data "aws_ecr_repository" "worker" {
  name = "test/worker"
}
