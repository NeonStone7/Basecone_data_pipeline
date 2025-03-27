from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

class VpcStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create a new VPC with private and public subnets
        self.vpc = ec2.Vpc(
            self, "MWAAVpc",
            max_azs=2,  # Use two availability zones
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet", subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                ),
            ],
        )
