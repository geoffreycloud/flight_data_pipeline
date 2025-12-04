import pandas as pd
import requests
from requests.exceptions import HTTPError
import datetime
import os
from pathlib import Path

def extract(url, access_key):
    params = {'access_key': access_key, 'limit': 100}

    try:
        # Send a GET request to the API endpoint
        r = requests.get(url, params=params)
        r.raise_for_status()

        print(f'Returned status code: {r.status_code}')

    except HTTPError as http_err:
        # Error occured on GET request
        print(f'HTTP error {http_err}')
    
    # Parse response content as JSON
    data = r.json()
    df = pd.json_normalize(data['data'])

    print('Extraction complete')
    
    return df

def transform(df):
    # Copying raw flight data
    df_copy = df.copy()

    # Adding squawk column if it's missing
    df_copy['squawk'] = df_copy.get('squawk', 'Unknown')

    # Replacing missing values with default values
    default_vals = {'squawk': 'Unknown', 'alt': 0, 'speed': 0, 'v_speed': 0.0}
    df_copy = df_copy.fillna(default_vals)

    # Removing duplicates
    df_copy = df_copy.drop_duplicates(subset=['hex', 'updated'])

    # Converting to imperial 
    df_copy['alt'] = df_copy['alt'].apply(lambda x: x * 3.28084)
    df_copy[['speed', 'v_speed']] = df_copy[['speed', 'v_speed']].apply(lambda x: x * 0.621371)


    # Converting 'updated' values to datetime
    df_copy['updated'] = df_copy['updated'].apply(lambda x: datetime.datetime.fromtimestamp(x))

    # Renaming columns
    renamed_columns = {
        'alt': 'altitude_ft', 'speed': 'speed_mph', 'v_speed': 'v_speed_mph', 'lat': 'latitude', 'lng': 'longitude',
        'dep_icao': 'departure_icao', 'dep_iata': 'departure_iata', 'arr_icao': 'arrival_icao', 'arr_iata': 'arrival_iata'
        }
    
    df_copy = df_copy.rename(columns=renamed_columns)

    print('transform complete')

    return df_copy

def load_to_csv(df_raw, df_clean):
    # Create data folder if it doesn't exist
    os.makedirs('../data', exist_ok=True)

    df_raw.to_csv('../data/flights_data_raw.csv', index=False)
    df_clean.to_csv('../data/flights_data_clean.csv')


def load_to_postgres(df_raw, df_clean, conn):
    df_raw.to_sql(
        name='flights_realtime_raw',
        con=conn,
        if_exists='append',
        index=False
    )

    df_clean.to_sql(
        name='flights_realtime_clean',
        con=conn,
        if_exists='append',
        index=False
    )
    

    print('load complete')