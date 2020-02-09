provider "aws" {
  profile = "default"
  region  = "ap-southeast-2"
}

terraform {
  backend "s3" {
    region         = "ap-southeast-2"
    bucket         = "timzhang-terraform-state"
    key            = "airflow-dags.tfstate"
    encrypt        = true #AES-256 encryption
    dynamodb_table = "terraform-state-lock"
  }
}

resource "aws_security_group" "airflow-ecs-sg" {
  name = "airflow-ecs-allowall"

  ingress {
    from_port   = "0"
    to_port     = "0"
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = "0"
    to_port     = "0"
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ecs cluster for airflow tasks
resource "aws_ecs_cluster" "airflow" {
  name = "airflow"
}
