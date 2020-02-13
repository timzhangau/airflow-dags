data "template_file" "news-feed-s3-to-neo4j-definition" {
  template = file("task-definition.json")
  vars = {
    container_name   = "news-feed-s3-to-neo4j"
    container_cpu    = 1024
    container_memory = 2048
    image_url        = "timzhangau/pipeline"
    env              = "airflow"
    log_group_name   = aws_cloudwatch_log_group.airflow-news-feed-s3-to-neo4j.name
    log_group_region = "ap-southeast-2"
  }
}


resource "aws_cloudwatch_log_group" "airflow-news-feed-s3-to-neo4j" {
  name              = "airflow/news-feed-s3-to-neo4j"
  retention_in_days = 30  # use 30 days as retention, the log will be retrieved and saved by airflow to s3
}

resource "aws_ecs_task_definition" "news-feed-s3-to-neo4j" {
  family                   = "news-feed-s3-to-neo4j"
  requires_compatibilities = ["FARGATE"]
  //  within container definitions, repositoryCredentials specifies the secrect manager to access private registry
  container_definitions = data.template_file.news-feed-s3-to-neo4j-definition.rendered
  task_role_arn         = aws_iam_role.airflow-ecs-role.arn
  execution_role_arn    = aws_iam_role.airflow-ecs-role.arn
  network_mode          = "awsvpc"
  cpu                   = 1024
  memory                = 2048
}