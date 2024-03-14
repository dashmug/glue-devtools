import os

import aws_cdk as cdk

from infrastructure.stacks.sample import SampleStack

if __name__ == "__main__":
    app = cdk.App()

    SampleStack(
        app,
        "SampleStack",
        env=cdk.Environment(
            account=os.getenv("CDK_DEFAULT_ACCOUNT"),
            region=os.getenv("CDK_DEFAULT_REGION"),
        ),
    )

    app.synth()
