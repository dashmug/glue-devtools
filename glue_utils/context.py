from contextlib import ContextDecorator
from types import TracebackType
from typing import cast

from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark import SparkConf, SparkContext


class ManagedGlueContext(ContextDecorator):
    job_options: dict[str, str]
    spark_conf: SparkConf | None
    job: Job

    def __init__(
        self,
        *,
        job_options: dict[str, str] | None = None,
        spark_conf: SparkConf | None = None,
    ) -> None:
        """Creates a context manager that wraps a GlueContext and
        ensures that Job.commit() is called.

        Parameters
        ----------
        init_options, optional
            Dictionary of key-value pairs to pass to Job.init().
            Defaults to None.
        conf, optional
            Custom SparkConf to use with SparkContext.getOrCreate().
            Defaults to None.
        """
        self.job_options = job_options or {}
        self.spark_conf = spark_conf

        super().__init__()

    def __enter__(self) -> GlueContext:
        job_name = self.job_options.get("JOB_NAME", "")

        conf = self.spark_conf or SparkConf()
        conf = conf.setAppName(job_name)

        spark_context = SparkContext.getOrCreate(conf)
        self.glue_context = GlueContext(spark_context)

        self.job = Job(self.glue_context)
        self.job.init(job_name, self.job_options)

        return self.glue_context

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        self.job.commit()

        return cast(bool, False)  # noqa: FBT003
