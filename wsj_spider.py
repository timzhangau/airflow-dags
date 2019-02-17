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

# run every day at midnight
schedule = "0 0 * * *"

resource = Resources(
    request_memory="100Mi", request_cpu="100m", limit_memory="1000Mi", limit_cpu="100m"
)

volume_mount = VolumeMount(
    "newsspider-vol", mount_path="/app", sub_path="newsspider", read_only=True
)

volume_config = {"persistentVolumeClaim": {"claimName": "newsspider-pvc"}}
volume = Volume(name="newsspider-vol", configs=volume_config)


dag = DAG(
    "wsj_spider", default_args=default_args, schedule_interval=schedule, catchup=False
)


# start = DummyOperator(task_id='run_this_first', dag=dag)

# kube operator name cannot contain '_'
passing = KubernetesPodOperator(
    namespace="scrapy",
    image="timzhangau/scrapy",
    cmds=[
        "scrapy",
        "crawl",
        "wsj_spider",
        "-a",
        "news_date={{ macros.ds_add(ds, -1) }}",
    ],
    resources=resource,
    volumes=[volume],
    volume_mounts=[volume_mount],
    name="wsj-spider-kube-operator",
    task_id="wsj_spider_kube_operator",
    config_file="/usr/local/airflow/.kube/config",
    get_logs=True,
    is_delete_operator_pod=True,
    dag=dag,
    on_success_callback=slack_success_callback,
    on_failure_callback=slack_failure_callback,
)
