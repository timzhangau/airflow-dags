data "aws_iam_policy_document" "airflow-ecs-policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs.amazonaws.com", "ecs-tasks.amazonaws.com"]
    }
  }
}

data "template_file" "task-role-policy" {
  template = file("task-role-policy.json")
}

resource "aws_iam_role" "airflow-ecs-role" {
  name               = "airflow-ecs-role"
  description        = "Permission for Airflow ECS task"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.airflow-ecs-policy.json
}

resource "aws_iam_role_policy" "airflow-task-role-policy" {
  name   = "airflow-task-role-policy"
  role   = aws_iam_role.airflow-ecs-role.id
  policy = data.template_file.task-role-policy.rendered
}