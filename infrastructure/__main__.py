import os

import aws_cdk as cdk
from cdk_nag import (
    AwsSolutionsChecks,
    HIPAASecurityChecks,
    NagPack,
    NIST80053R5Checks,
    PCIDSS321Checks,
)

from infrastructure.stacks.sample import SampleStack

NAG_PACKS: list[type[NagPack]] = [
    AwsSolutionsChecks,
    HIPAASecurityChecks,
    PCIDSS321Checks,
    NIST80053R5Checks,
]

if __name__ == "__main__":
    app = cdk.App()

    SampleStack(app, "SampleStack")

    if os.getenv("CDK_NAG"):
        for nag in NAG_PACKS:
            cdk.Aspects.of(app).add(nag(verbose=True))

    app.synth()
