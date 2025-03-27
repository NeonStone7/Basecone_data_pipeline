"""Create S3 buckets"""
from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_s3 as s3,
)
from constructs import Construct
import os
import sys
from pathlib import Path

myDir = os.getcwd()
sys.path.append(myDir)

path = Path(myDir)
a=str(path.parent.absolute())

sys.path.append(a)

from dags.utils.variables import (
    DAGS_BUCKET, DATA_BUCKET)


class SetupInfrastructureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket_1 = s3.Bucket(
            self,
            DATA_BUCKET,
            bucket_name=DATA_BUCKET,  # Explicitly set the bucket name
            versioned = True,
            removal_policy=RemovalPolicy.DESTROY
        )

        self.bucket_2 = s3.Bucket(
            self,
            DAGS_BUCKET,
            bucket_name=DAGS_BUCKET,  # Explicitly set the bucket name
            versioned = True,
            removal_policy=RemovalPolicy.DESTROY
        )
