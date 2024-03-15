import os
from typing import Any

import aws_cdk as cdk
from constructs import Construct


class BaseStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__(
            scope,
            construct_id,
            env=cdk.Environment(
                account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                region=os.getenv("CDK_DEFAULT_REGION"),
            ),
            **kwargs,
        )

        cdk.Tags.of(self).add("stack:name", self.stack_name)

        if description := kwargs.get("description"):
            cdk.Tags.of(self).add("stack:description", description)
