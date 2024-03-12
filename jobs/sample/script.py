"""
This script is derived from the AWS Glue documentation example
https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-libraries.html#develop-local-docker-image

The code has been refactored to add static types and follow the linting rules.
"""

import sys

from awsglue import DynamicFrame
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark import SparkContext


def read_json(glue_context: GlueContext, path: str) -> DynamicFrame:
    return glue_context.create_dynamic_frame_from_options(
        connection_type="s3",
        connection_options={"paths": [path], "recurse": True},
        format="json",
    )


class GluePythonSample:
    def __init__(self) -> None:
        params = []
        if "--JOB_NAME" in sys.argv:
            params.append("JOB_NAME")
        args = getResolvedOptions(sys.argv, params)

        self.context = GlueContext(SparkContext.getOrCreate())
        self.job = Job(self.context)

        job_name = args.get("JOB_NAME", "test")
        self.job.init(job_name, args)

    def run(self) -> None:
        dynamicframe = read_json(
            self.context,
            "s3://awsglue-datasets/examples/us-legislators/all/persons.json",
        )
        dynamicframe.printSchema()

        self.job.commit()


if __name__ == "__main__":
    GluePythonSample().run()
