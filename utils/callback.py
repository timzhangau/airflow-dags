from airflow.models import Variable
import requests

# get environment variable for slack callback functions
BASE_URL = Variable.get('BASE_URL', 'http://localhost:8080')
SLACK_WEBHOOK_URL = Variable.get('SLACK_WEBHOOK_URL')
DEFAULT_SLACK_CHANNEL = Variable.get('DEFAULT_SLACK_CHANNEL')


def slack_callback(context, type):
    """
    slack callback method
    :param context:
    :param type:
    :return:
    """
    dag_id = context['dag'].dag_id
    task_id = context['task'].task_id
    author = context['dag'].owner
    execution_date_pendulum = context["execution_date"]
    if execution_date_pendulum.microsecond == 0:
        execution_date = execution_date_pendulum.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        execution_date = execution_date_pendulum.strftime("%Y-%m-%dT%H:%M:%S.%f")
    log_url = f"{BASE_URL}/admin/airflow/log?task_id={task_id}&dag_id={dag_id}&execution_date={execution_date}"

    if type == 'success':
        attachment = {
            "fallback": f"<{log_url}|View completion log>",
            "color": "good",
            "pretext": f"<{log_url}|View completion log>",
            "author_name": author,
            "fields": [
                {
                    "title": "Completed task",
                    "value": f"{dag_id}.{task_id}",
                    "short": False,
                }
            ]
        }
    elif type == 'failure':
        attachment = {
            "fallback": f"<{log_url}|View failure log>",
            "color": "danger",
            "pretext": f"<{log_url}|View failure log>",
            "author_name": author,
            "fields": [
                {
                    "title": "Failed task",
                    "value": f"{dag_id}.{task_id}",
                    "short": False,
                }
            ]
        }

    payload = {"text": "", "attachments": [attachment], "channel": DEFAULT_SLACK_CHANNEL}
    requests.post(SLACK_WEBHOOK_URL, json=payload)
    return


def slack_success_callback(context):
    slack_callback(context, type='success')
    return


def slack_failure_callback(context):
    slack_callback(context, type='failure')
    return