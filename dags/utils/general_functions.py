"""Module for functions that can be reused globally"""
import os
from typing import Optional, Union
import pandas as pd
import boto3
import requests

from dags.utils.variables import (
    DATA_BUCKET,
    DATA_FOLDER_NAME
)

# Initialize S3 client
s3 = boto3.client('s3')

def save_data_locally(data: pd.DataFrame, filename: str) -> str:
    """
    Saves the given DataFrame as a CSV file locally.

    Args:
        data (pd.DataFrame): The DataFrame to save.
        date (str): The date to include in the filename.
        filename (str): The name of the file to save.

    Returns:
        str: The local file path where the data was saved.
    """
    local_dir = './dags/tmp/data/'
    os.makedirs(local_dir, exist_ok=True)

    local_path = os.path.join(local_dir, filename)

    try:
        data.to_csv(local_path, 
                    index=False)
    except OSError as exception:
        print(f"Error saving data locally: {exception}")
    
    return local_path

def upload_objects_to_s3(bucket_name: str, key_name: str, body: Optional[Union[bytes, str]] = None) -> None:
    """
    Uploads a file or object to an S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        key_name (str): The key (path) for the S3 object.
        body (Optional[Union[bytes, str]]): The content of the file to upload. Defaults to None, which uploads an empty object.
    """
    if body is None:
        s3.put_object(Bucket=bucket_name, Key=key_name)
    else:
        s3.put_object(Bucket=bucket_name, Key=key_name, Body=body)

def make_api_call(url: str, params: dict, date_today_str: str):
    """
    Makes a GET request to an API and yields the response as JSON if available.

    Args:
        URL (str): The API endpoint.
        params (dict): The parameters for the API request.
        date_today_str (str): The date as a string to print in case of no data.

    Yields:
        dict: The JSON response from the API if data is available.
    """
    response = requests.get(url, params=params, timeout=3600)

    page_json = response.json()

    if page_json:
        yield page_json
    else:
        print(f'{date_today_str}: No data available')


def load(local_path: str, data_name: str, date: str) -> None:
    """
    Loads data by uploading it to an S3 bucket.

    Args:
        local_path (str): The local path to the file to upload.
        data_name (str): The name of the data being uploaded.
        date (str): The date to include in the S3 object key.
    """
    try:
        with open(local_path, 'rb') as file:
            upload_objects_to_s3(DATA_BUCKET, f"{DATA_FOLDER_NAME}{data_name}_data_{date}.csv", file)
        print('Data uploaded successfully')
    except Exception as error:
        print(f"Error uploading data: {error}")
