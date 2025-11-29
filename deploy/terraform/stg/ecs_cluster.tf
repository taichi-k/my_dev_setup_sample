resource "aws_ecs_cluster" "this" {
  name = "test-cluster-kosugi"
  configuration {
    execute_command_configuration {
      logging = "DEFAULT"
    }
  }
}
