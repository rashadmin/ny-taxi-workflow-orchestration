from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import os
from ingest_data import ingest_callable


user = os.getenv('PG_USER')
password = os.getenv('PG_PASSWORD')
host = os.getenv('PG_HOST')
port = os.getenv('PG_PORT')
db = os.getenv('PG_DB')

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME")
URL_PREFIX = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow"
URL_SUFFIX = "/yellow_tripdata_{{execution_date.strftime(\'%Y-%m\')}}.csv.gz"
URL_TEMPLATE = URL_PREFIX+URL_SUFFIX
OUTPUT_TEMPLATE = AIRFLOW_HOME + '/output_{{execution_date.strftime(\'%Y_%m\')}}.csv.gz'
table = 'ny_taxi_{{execution_date.strftime(\'%Y%m\')}}'


workflow = DAG(dag_id = 'NY_TAXI',
               start_date = datetime(2021,1,1),
               end_date = datetime(2021,5,1),
               schedule_interval='@monthly')

with workflow:
    curl_task = BashOperator(task_id='download_data',
                             bash_command=f'curl -sSL {URL_TEMPLATE} > {OUTPUT_TEMPLATE}')
    ingest_task  = PythonOperator(task_id='ingest_data',
                                  python_callable=ingest_callable,
                                  op_kwargs=dict(user=user,
                                                 password=password,
                                                 host=host,
                                                 port=port,
                                                 db=db,
                                                 table=table,
                                                 csv_file=OUTPUT_TEMPLATE))
    

    curl_task >> ingest_task

    
    
