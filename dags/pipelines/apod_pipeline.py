"""Extract data from NASA APOD API and load to s3"""
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

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

# NASA API key and URL for the Astronomy Picture of the Day (APOD) API
NASA_API_KEY = os.getenv('NASA_API_KEY')
URL = 'https://api.nasa.gov/planetary/apod'

# Get the current date as a string (YYYY-MM-DD)
date_today = datetime.now().date()
date_today_str = date_today.strftime('%Y-%m-%d')

# Parameters for the API request
params = {
    'date': date_today_str,
    # 'count': 5,  # Uncomment to fetch multiple pictures
    'thumbs': True,
    'api_key': NASA_API_KEY
}

def extract():
    """
    Calls the NASA APOD API to extract the astronomy picture of the day data.

    Returns:
        List[Dict]: A list of dictionaries containing the API response.
    """
    return make_api_call(URL, params, date_today_str)

def transform() -> str:
    """
    Transforms the raw API data into a DataFrame and saves it locally as a CSV file.

    Returns:
        str: The local file path where the data was saved.
    """
    all_df = pd.DataFrame()
    
    # Concatenate all extracted data into a single DataFrame
    for data in extract():
        all_df = pd.concat([all_df, pd.DataFrame(data, index=[0])])

    # Save the DataFrame to a CSV file locally
    return save_data_locally(all_df, f'apod_extract_{date_today_str}.csv')

def apod_pipeline() -> None:
    """
    The main pipeline function that extracts, transforms, and loads data.

    It extracts data from the API, transforms it into a DataFrame, 
    saves it locally, and loads it into the destination system.
    """
    local_path = transform()

    # Load the transformed data into the destination system
    load(local_path, 'apod', date_today_str)

# Uncomment the line below to run the pipeline when needed
# print(apod_pipeline())
