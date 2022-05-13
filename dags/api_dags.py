import http
import json
from datetime import datetime
from urllib import response
from numpy import False_
from airflow.models  import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator


def save_posts(task_instance) -> None:
    ti = task_instance
    posts = ti.xcom_pull(task_ids=['get_posts']) #xcom_pull dari airflow 
    with open('/home/fadilardhi/airflow/data/posts.json', 'w') as f:
        json.dump(posts[0], f)
    return posts

with DAG(
    dag_id='api_dag',
    schedule_interval='@once',
    start_date=datetime(2022, 5, 10),
    catchup=False
) as dag:
    
    task_is_api_active = HttpSensor( #checking koneksi
        task_id = 'is_api_active',
        http_conn_id = 'api_post',
        endpoint = 'posts/'
    )

    task_get_posts = SimpleHttpOperator( #Http operator untul ambil data response
        task_id='get_posts',
        http_conn_id='api_post',
        endpoint='posts/',
        method='GET',
        response_filter=lambda response: json.loads(response.text), 
        log_response=True
    ) 
    
    task_save = PythonOperator( #deklarasi fungsi python
        task_id='save_posts',
        python_callable=save_posts
    )
    task_is_api_active >> task_get_posts >> task_save