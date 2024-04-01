import os

import aws_cdk as cdk
from cdk_nag import (
    AwsSolutionsChecks,
    HIPAASecurityChecks,
    NagPack,
    NIST80053R5Checks,
    PCIDSS321Checks,
)

from cdk.stacks.sample import SampleStack

# Feel free to enable or disable the checks you want to run.
# More information about the rules can be found here:
# https://github.com/cdklabs/cdk-nag/blob/main/RULES.md
NAG_PACKS: list[NagPack] = [
    # Best practices based on AWS Solutions Security Matrix
    AwsSolutionsChecks(verbose=True),
    # HIPAA Security AWS operational best practices
    # https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-hipaa_security.html
    HIPAASecurityChecks(verbose=True),
    # PCI DSS 3.2.1 AWS operational best practices
    # https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-pci-dss.html
    PCIDSS321Checks(verbose=True),
    # NIST 800-53 rev 5 AWS operational best practices
    # https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-nist-800-53_rev_5.html
    NIST80053R5Checks(verbose=True),
]

# These tags will be added to all resources.
# Feel free to add/edit/remove these tags as you see fit.
# https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html
TAGS = {
    "project:name": "Your Project Name",
    "project:owner": "Your Team",
}

if __name__ == "__main__":
    app = cdk.App()

    SampleStack(app, "SampleStack")

    if os.getenv("CDK_NAG"):
        for check in NAG_PACKS:
            cdk.Aspects.of(app).add(check)

    for key, value in TAGS.items():
        cdk.Tags.of(app).add(key, value)

    app.synth()
