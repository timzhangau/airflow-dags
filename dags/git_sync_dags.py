from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from .utils.callback import slack_failure_callback, slack_success_callback



default_args = {
    'owner': 'airflow@spitfire',
    'start_date': datetime(2018, 11, 23),
    'retries': 1,
    'email': ['tim@spitfire.io'],
    'email_on_failure': False,
    'depends_on_past': False,
}


# run every minute
schedule = '*/15 * * * *'

dag = DAG(
    dag_id='git_sync_dags',
    schedule_interval=schedule,
    default_args=default_args,
    catchup=False,
)

git_sync_bash = """
    cd /usr/local/airflow/dags && git fetch origin && git reset --hard origin/master && git clean -f -d
"""

t1 = BashOperator(
    task_id='git_fetch_and_reset',
    bash_command=git_sync_bash,
    on_success_callback=slack_success_callback,
    on_failure_callback=slack_failure_callback,
    dag=dag
)