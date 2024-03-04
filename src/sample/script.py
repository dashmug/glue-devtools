"""
This script is derived from the AWS Glue documentation example
https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-libraries.html#develop-local-docker-image

The code has been simplified to demonstrate how to use the
ManagedGlueContext class from glue_utils.
"""

import sys

from awsglue import DynamicFrame
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions

from glue_utils.context import ManagedGlueContext


def extract(glue_context: GlueContext, path: str) -> DynamicFrame:
    return glue_context.create_dynamic_frame_from_options(
        connection_type="s3",
        connection_options={"paths": [path], "recurse": True},
        format="json",
    )


if __name__ == "__main__":
    options = getResolvedOptions(sys.argv, [])
    with ManagedGlueContext(options=options) as glue_context:
        dyf = extract(
            glue_context=glue_context,
            path="s3://awsglue-datasets/examples/us-legislators/all/persons.json",
        )
        dyf.printSchema()
