import pandas as pd
import numpy as np
import requests
from requests.exceptions import HTTPError
import os
from dotenv import load_dotenv
import datetime

load_dotenv()
access_key = os.getenv('ACCESS_KEY')

# Define API endpoint
url = 'https://www.goflightlabs.com/flights'

def extract(url, access_key):
    params = {'access_key': access_key,
              'limit': 1000}

    try:
        # Send a GET request to the API endpoint
        r = requests.get(url, params=params)
        r.raise_for_status()

        print(f'Returned status code: {r.status_code}')

    except HTTPError as http_err:
        # Error occured on GET request
        print(f'Connection error {http_err}')
    
    # Parse response content as JSON
    data = r.json()
    df = pd.json_normalize(data['data'])
    
    return df

def transform(df):
    # Copying raw flight data
    df_copy = df.copy()

    # Replacing missing values with default values
    default_vals = {'squawk': 'Unknown', 'alt': 0, 'speed': 0, 'v_speed': 0.0}
    df_copy = df_copy.fillna(default_vals)


    # Converting 'updated' values from timestamp to datetime
    df_copy['updated'] = df_copy['updated'].apply(lambda x: datetime.datetime.fromtimestamp(x))

    return df_copy

flight_data_raw = extract(url, access_key)
flight_data_clean = transform(flight_data_raw)
