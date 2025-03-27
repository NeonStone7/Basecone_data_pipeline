import sys
import os
from pathlib import Path
from typing import List

# Add the current and parent directory to sys.path for importing modules
myDir = os.getcwd()
sys.path.append(myDir)

path = Path(myDir)
parent_dir = str(path.parent.absolute())

sys.path.append(parent_dir)

# Import necessary variables and functions
from dags.utils.variables import (
    DAGS_BUCKET, DATA_BUCKET, DAGS_FOLDER_NAME, DATA_FOLDER_NAME
)
from dags.utils.general_functions import upload_objects_to_s3

def upload_folders_to_s3(folders: List[str], buckets: List[str]) -> None:
    """
    Uploads folders to respective S3 buckets.

    Args:
        folders (List[str]): List of folder names to upload.
        buckets (List[str]): List of corresponding S3 buckets to upload to.

    Returns:
        None
    """
    # Loop through each folder and bucket pair and upload using the upload_objects_to_s3 function
    for folder, bucket in zip(folders, buckets):
        upload_objects_to_s3(bucket_name=bucket, key_name=folder)
        print(f"Uploaded folder '{folder}' to bucket '{bucket}'")

# Call the function to upload the folders to their respective S3 buckets
upload_folders_to_s3([DAGS_FOLDER_NAME, DATA_FOLDER_NAME], [DAGS_BUCKET, DATA_BUCKET])
