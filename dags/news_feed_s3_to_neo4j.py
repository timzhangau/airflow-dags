from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.ecs_operator import ECSOperator
from utils.callback import slack_failure_callback, slack_success_callback


default_args = {
    "owner": "timzhang",
    "depends_on_past": False,
    "start_date": datetime(2019, 1, 1),
    "email": ["tim.zhang@newsmartwealth.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

# run twice a day at minute 0 past hour 10 and 22
schedule = "15 10,22 * * *"

# vpc and security group setting
network_config = {
    "awsvpcConfiguration": {
        "subnets": ["subnet-ca3f40ae"],
        "assignPublicIp": "ENABLED",  # keep it enabled otherwise will fail to pull the image
        "securityGroups": ["sg-0b06af062af4bcd99"],
    }
}

overrides_config = {
    "containerOverrides": [
        {
            "name": "news-feed-s3-to-neo4j",
            "command": ["python", "newsroom/s3_json_to_neo4j.py",],
            # "environment": [{"name": "string", "value": "string"},],
        }
    ]
}

log_config = {
    "awslogs_group": "airflow/news-feed-s3-to-neo4j",
    "awslogs_region": "ap-southeast-2",
    "awslogs_stream_prefix": "ecs/news-feed-s3-to-neo4j",  # need to append the task container name here
}

dag = DAG(
    "news_feed_s3_to_neo4j",
    default_args=default_args,
    schedule_interval=schedule,
    catchup=False,
)

pipeline_task = ECSOperator(
    aws_conn_id="aws_default",
    task_id="s3_to_neo4j_ecs_operator",
    region_name="ap-southeast-2",
    cluster="airflow",
    launch_type="FARGATE",
    task_definition="news-feed-s3-to-neo4j:1",
    platform_version="LATEST",
    network_configuration=network_config,
    overrides=overrides_config,
    dag=dag,
    on_success_callback=slack_success_callback,
    on_failure_callback=slack_failure_callback,
    **log_config,
)
