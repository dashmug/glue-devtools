"""
This script is derived from the AWS Glue documentation example
https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-libraries.html#develop-local-docker-image

The code has been simplified to demonstrate how to use the
ManagedGlueContext class from glue_utils.
"""

import sys

from awsglue import DynamicFrame
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark import SparkConf, SparkContext


def extract(glue_context: GlueContext, path: str) -> DynamicFrame:
    return glue_context.create_dynamic_frame_from_options(
        connection_type="s3",
        connection_options={"paths": [path], "recurse": True},
        format="json",
    )


def run() -> None:
    options = getResolvedOptions(sys.argv, [])
    job_name = options.get("JOB_NAME", "test")

    spark_conf = SparkConf().setAppName(job_name)
    glue_context = GlueContext(SparkContext.getOrCreate(spark_conf))

    job = Job(glue_context)
    job.init(job_name, options)

    dynamicframe = extract(
        glue_context=glue_context,
        path="s3://awsglue-datasets/examples/us-legislators/all/persons.json",
    )
    dynamicframe.printSchema()

    job.commit()


if __name__ == "__main__":
    run()
