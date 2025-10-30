# Flight Data ETL Pipeline - Flightlabs API

* Brief overview:
    * This project extracts real-time flight data from the FlightLabs API, transforms it for analytics, and loads it into a PostgreSQL database. The pipeline is structured into raw and clean tables to follow a medallion architecture (bronze → silver). The clean data is then analyzed and visualized in Tableau, enabling insights such as flight trends, airport traffic, and airline performance.

* Technology used: _Python, pandas, psycopg2, PostgreSQL, Apache Airflow, Tableau_

* Final results:
    * Fully functioning ETL pipeline that ingests, cleans, and stores flight data
    * Raw flight table preserving API structure
    * Clean flight table with normalized column names and transformations
    * Interactive Tableau dashboards visualizing flight activity, airport traffic, and airline trends
