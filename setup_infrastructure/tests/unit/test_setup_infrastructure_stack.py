import aws_cdk as core
import aws_cdk.assertions as assertions

from setup_infrastructure.setup_infrastructure_stack import SetupInfrastructureStack

# example tests. To run these tests, uncomment this file along with the example
# resource in setup_infrastructure/setup_infrastructure_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SetupInfrastructureStack(app, "setup-infrastructure")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
