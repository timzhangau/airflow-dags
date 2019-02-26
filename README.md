# airflow-dags
airflow dags repo

# To run history jobs for dag using cmd
use backfill from https://airflow.apache.org/cli.html
- in under kubernetes setting, need to run the below command from airflow webserver pod, it won't work for scheduler and worker pods
- also need to use '-x' to disable pickling dag object
> example:
```bash
airflow backfill -s '2017-02-05' -e '2017-02-05' -x wsj_spider
```

