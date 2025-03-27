"""Extract data from NASA NEO API and load to s3"""
import os
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set the current working directory and add it to sys.path for imports
MYDIR = os.getcwd()
sys.path.append(MYDIR)

# Set path for the parent directory
path = Path(MYDIR)
PARENT_DIR = str(path.parent.absolute())

# Append the parent directory to sys.path for module import
sys.path.append(PARENT_DIR)

from dags.utils.general_functions import (
    make_api_call, 
    save_data_locally,
    load
)
# NASA API key from environment variable
NASA_API_KEY = os.getenv('NASA_API_KEY')

# NASA NEO (Near-Earth Object) API URL
URL = "https://api.nasa.gov/neo/rest/v1/feed?"

# Number of days to capture data for
NUMBER_DAYS_TO_CAPTURE = 3

# Get the current date and format it as a string (YYYY-MM-DD)
end_date = datetime.now()
end_date_str = end_date.strftime('%Y-%m-%d')

# Calculate the start date for data capture
start_date = end_date - timedelta(days=NUMBER_DAYS_TO_CAPTURE)
start_date_str = start_date.strftime('%Y-%m-%d')

# List of dates to capture data for, based on the range of NUMBER_DAYS_TO_CAPTURE
all_dates = [(start_date + timedelta(days=day)).strftime('%Y-%m-%d') for day in range(NUMBER_DAYS_TO_CAPTURE)]

def extract_data():
    """
    Extracts data from the NASA NEO API for the specified date range.

    Returns:
        List[Dict]: A list of dictionaries containing NEO data for each day in the date range.
    """
    params = {
        'start_date': start_date_str,
        'end_date': end_date_str,
        'api_key': NASA_API_KEY
    }
    return make_api_call(URL, params, end_date_str)

def transform() -> str:
    """
    Transforms the extracted NEO data into a DataFrame and saves it locally.

    Iterates over each day's data, extracts relevant information about each asteroid,
    and stores the data in a DataFrame, which is then saved to a CSV file.

    Returns:
        str: The local file path where the data was saved.
    """
    all_df = pd.DataFrame()

    # Process each page of JSON data
    for page_json in extract_data():
        for date in all_dates:
            # Get data for the specific date
            date_data = page_json['near_earth_objects'][date]

            # Iterate over each asteroid's data and extract relevant fields
            for asteroid in date_data:
                extracted_data = {
                    'id': asteroid['id'],
                    'date_recorded': date,
                    'neo_reference_id': asteroid['neo_reference_id'],
                    'name': asteroid['name'],
                    'nasa_jpl_url': asteroid['nasa_jpl_url'],
                    'absolute_magnitude_h': asteroid['absolute_magnitude_h'],
                    'estimated_diameter_km_min': asteroid['estimated_diameter']['kilometers']['estimated_diameter_min'],
                    'estimated_diameter_km_max': asteroid['estimated_diameter']['kilometers']['estimated_diameter_max'],
                    'is_potentially_hazardous_asteroid': asteroid['is_potentially_hazardous_asteroid'],
                    'close_approach_data_date': asteroid['close_approach_data'][0]['close_approach_date_full'],
                    'close_approach_data_relative_velocity_kms': asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_second'],
                    'close_approach_data_miss_distance': asteroid['close_approach_data'][0]['miss_distance']['kilometers'],
                    'close_approach_data_orbiting_body': asteroid['close_approach_data'][0]['orbiting_body'],
                    'is_sentry_object': asteroid['is_sentry_object']
                }

                # Convert extracted data into a DataFrame and concatenate it
                extracted_df = pd.DataFrame(extracted_data, index=[0])
                all_df = pd.concat([all_df, extracted_df])

    # Save the DataFrame to a CSV file
    return save_data_locally(all_df, f'neo_extract_{end_date_str}.csv')

def neo_pipeline() -> None:
    """
    Main pipeline function for extracting, transforming, and loading NEO data.

    This function extracts NEO data from the API, transforms it into a DataFrame, 
    saves it locally, and loads it into the destination system.
    """
    local_path = transform()

    # Load the transformed data into the destination system
    load(local_path, 'neo', end_date_str)

# Uncomment the line below to run the pipeline when needed
# print(neo_pipeline())
