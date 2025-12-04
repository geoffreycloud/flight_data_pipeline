# Flight Data ETL Pipeline - Flightlabs API
Technology used: _Python, pandas, psycopg2, PostgreSQL, Apache Airflow, Docker Desktop, Tableau_  

This project extracts real-time flight data from the FlightLabs API, transforms it for analytics, and loads it into a PostgreSQL database. The clean data is analyzed and visualized in Tableau, enabling insights such as flight trends, airport traffic, and airline performance.
Final results:
   * Fully functioning ETL pipeline that ingests, cleans, and stores flight data
   * Raw flight table preserving API structure
   * Clean flight table with normalized column names and transformations
   * Interactive Tableau dashboards visualizing flight activity, airport traffic, and airline trends  

## Python File
The automated ETL process was built using an Airflow DAG and tasks [flight_ingestion_dag.py](./dags/flight_ingestion_dag.py).  

Each task within the DAG is defined in [utils.py](./scripts/utils.py).

The process is also included in the jupyter notebook file [etl.py](./scripts/etl.ipynb)

## Output
[Raw Flight Data Sample](./data/flights_data_raw.csv)  

[Clean Flight Data Sample](./data/flights_data_clean.csv)  


## Visuals
Sample DAG Stages Ran Successfully
<img width="1905" height="725" alt="image" src="https://github.com/user-attachments/assets/e6480ca5-dfae-4bb9-bdb7-a154afe3fade" />
