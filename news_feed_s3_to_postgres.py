from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.pod import Resources
from airflow.contrib.kubernetes.volume_mount import VolumeMount
from airflow.contrib.kubernetes.volume import Volume
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

# run every day at 3am
schedule = "0 3 * * *"

resource = Resources(
    request_memory="100Mi", request_cpu="100m", limit_memory="500Mi", limit_cpu="500m"
)

# # no longer requires volume mount as source code now built in image using private repo
# volume_mount = VolumeMount(
#     "newsspider-vol", mount_path="/app", sub_path="newsspider", read_only=True
# )
#
# volume_config = {"persistentVolumeClaim": {"claimName": "newsspider-pvc"}}
# volume = Volume(name="newsspider-vol", configs=volume_config)


dag = DAG(
    "news_feed_s3_to_postgres",
    default_args=default_args,
    schedule_interval=schedule,
    catchup=False,
)


# kube operator name cannot contain '_'
pipeline_task = KubernetesPodOperator(
    namespace="scrapy",
    image="timzhangau/pipeline",
    image_pull_secrets="docker-hub-timzhangau-repo",
    cmds=["python", "newsroom/s3_json_to_postgres.py"],
    resources=resource,
    # volumes=[volume],
    # volume_mounts=[volume_mount],
    name="pipeline-s3-to-postgres",
    task_id="s3_to_postgres_kube_operator",
    config_file="/usr/local/airflow/.kube/config",
    get_logs=True,
    is_delete_operator_pod=True,
    dag=dag,
    on_success_callback=slack_success_callback,
    on_failure_callback=slack_failure_callback,
)
