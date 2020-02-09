import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from dags.utils.callback import slack_failure_callback

default_args = {
    'owner': 'timzhang',
    'start_date': datetime.datetime(2018, 11, 27),
    'retries': 0,
    'email': ['tim.zhang@newsmartwealth.com'],
    'email_on_failure': False,
    'depends_on_past': False,
    'retry_delay': datetime.timedelta(seconds=30),
}


# run every minute
schedule = '*/5 * * * *'

dag = DAG(
    dag_id='test_failure_notification',
    schedule_interval=schedule,
    default_args=default_args,
    catchup=False,
)

t1 = BashOperator(
    task_id='test_failure_notification_task',
    bash_command="echo.py",
    on_failure_callback=slack_failure_callback,
    dag=dag
)