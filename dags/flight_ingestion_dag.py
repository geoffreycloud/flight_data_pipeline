from airflow.sdk import dag, task
from scripts.utils import extract, transform, load_to_postgres
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import os

url = 'https://www.goflightlabs.com/flights'
ACCESS_KEY = os.getenv('ACCESS_KEY')

# Creating connection to local flight data database
dbname=os.getenv('DB_NAME')
user=os.getenv('DB_USER')
password=os.getenv('DB_PASSWORD')
host=os.getenv('DB_HOST')
port=os.getenv('DB_PORT')

conn = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}')

# DAG default args
default_args = {
    'owner': 'Geoffrey Cloud',
    'email': 'gcloudio98@gmail.com',
    'start_date': datetime(2025, 12, 4),
    'retries': 3,
    'retry_delay': timedelta(minutes=3)
}

@dag(
    dag_id='flight_data_hourly_etl',
    start_date=datetime(2025, 12, 4),
    schedule='0 * * * *', # Every hour
    catchup=False
)
def flight_pipeline():

    @task
    def extract_flights():
        df_raw = extract(url, ACCESS_KEY)
        return df_raw

    @task
    def transform_flights(df_raw):
        df_clean = transform(df_raw)
        return df_clean
    
    @task
    def load_flights(df_raw, df_clean):
        load_to_postgres(df_raw, df_clean, conn)

    raw = extract_flights()
    clean = transform_flights(raw)
    load_flights(raw, clean)

# Instantiate DAG
flight_pipeline()


    


