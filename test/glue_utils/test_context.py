from awsglue.context import GlueContext
from pyspark.sql import SparkSession

from glue_utils.context import ManagedGlueContext


class TestManagedGlueContext:
    def test_init_without_options(self):
        context = ManagedGlueContext()

        assert context.job_options == {}

    def test_init_with_options(self):
        context = ManagedGlueContext(
            job_options={"JOB_NAME": "test_job", "SOME_OPTION": "some_value"}
        )

        assert context.job_options == {
            "JOB_NAME": "test_job",
            "SOME_OPTION": "some_value",
        }

    def test_as_context_manager(self):
        with ManagedGlueContext() as context:
            assert isinstance(context, GlueContext)
            assert isinstance(context.spark_session, SparkSession)
