from aws_cdk import (
    Stack,
    aws_mwaa as mwaa,
    aws_s3 as s3,
    aws_iam as iam,
    aws_ec2 as ec2
)
from constructs import Construct

class MwaaStack(Stack):
    def __init__(self, scope: Construct, id: str, existing_s3_bucket: s3.IBucket, vpc: ec2.Vpc, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create an IAM role for MWAA
        mwaa_role = iam.Role(
            self, "MwaaExecutionRole",
            assumed_by=iam.ServicePrincipal("airflow-env.amazonaws.com"),  # Ensure correct service principal
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")  # Adjust permissions as needed
            ]
        )

        # Get the private subnets from the VPC
        private_subnets = [subnet.subnet_id for subnet in vpc.private_subnets]

        # Define the MWAA environment
        mwaa_env = mwaa.CfnEnvironment(
            self, "MWAAEnvironment",
            name="MyMWAAEnvironment",
            airflow_version="2.10.1",  # Update as needed
            execution_role_arn=mwaa_role.role_arn,
            source_bucket_arn=existing_s3_bucket.bucket_arn,
            dag_s3_path="dags/",  # Folder where Airflow DAGs are stored
            environment_class="mw1.micro",  # Adjust based on your needs
            max_workers=1,
            network_configuration=mwaa.CfnEnvironment.NetworkConfigurationProperty(
                security_group_ids=[vpc.vpc_default_security_group],
                subnet_ids=private_subnets  # Use private subnets for security
            ),
            webserver_access_mode="PUBLIC_ONLY",
            tags={
                "Project": "Airflow"
            }
        )

        # Allow MWAA to access the S3 bucket
        existing_s3_bucket.grant_read_write(mwaa_role)
