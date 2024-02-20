"""
This script is taken from the AWS Glue documentation
https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-libraries.html#develop-local-docker-image
"""

import sys

from awsglue import DynamicFrame
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext


class GluePythonSampleTest:
    def __init__(self) -> None:
        params = []
        if "--JOB_NAME" in sys.argv:
            params.append("JOB_NAME")
        args = getResolvedOptions(sys.argv, params)

        self.context = GlueContext(SparkContext.getOrCreate())
        self.job = Job(self.context)

        jobname = args.get("JOB_NAME", "test")
        self.job.init(jobname, args)

    def run(self) -> None:
        dyf = read_json(
            self.context,
            "s3://awsglue-datasets/examples/us-legislators/all/persons.json",
        )
        dyf.printSchema()

        self.job.commit()


def read_json(glue_context: GlueContext, path: str) -> DynamicFrame:
    return glue_context.create_dynamic_frame.from_options(
        connection_type="s3",
        connection_options={"paths": [path], "recurse": True},
        format="json",
    )


if __name__ == "__main__":
    GluePythonSampleTest().run()
