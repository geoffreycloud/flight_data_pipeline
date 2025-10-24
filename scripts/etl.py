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
    params = {'access_key': access_key}

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


flight_data_raw = extract(url, access_key)
print(flight_data_raw.head())
