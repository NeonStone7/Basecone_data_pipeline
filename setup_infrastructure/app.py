#!/usr/bin/env python3
import os

import aws_cdk as cdk

from setup_infrastructure.setup_infrastructure_stack import SetupInfrastructureStack
from setup_infrastructure.aws_mwaa_stack import MwaaStack
from setup_infrastructure.vpc_stack import VpcStack


app = cdk.App()
s3_stack = SetupInfrastructureStack(app, "SetupInfrastructureStack")
vpc_stack = VpcStack(app, "VpcStack")
mwaa_stack = MwaaStack(app, "MWAAStack", existing_s3_bucket=s3_stack.bucket_2, vpc=vpc_stack.vpc)

app.synth()
