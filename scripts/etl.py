import os
from dotenv import load_dotenv
import psycopg2
from utils import extract, transform, load

load_dotenv()

# Define API endpoint
url = 'https://www.goflightlabs.com/flights'

if __name__ == "__main__":

    # Extracting raw flight data from flight labs API
    access_key = os.getenv('ACCESS_KEY')
    flight_data_raw = extract(url, access_key)

    # Transforming raw flight data
    flight_data_clean = transform(flight_data_raw)

    # Connecting to local flight data database
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

    # Loading raw and clean data to Flight Data Database
    load(flight_data_raw, flight_data_clean, conn)

