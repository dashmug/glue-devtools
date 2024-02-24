from contextlib import ContextDecorator
from types import TracebackType
from typing import cast

from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark import SparkConf, SparkContext


class ManagedGlueContext(ContextDecorator):
    options: dict[str, str]
    conf: SparkConf | None
    job: Job

    def __init__(
        self,
        *,
        options: dict[str, str] | None = None,
        conf: SparkConf | None = None,
    ) -> None:
        """Creates a context manager that wraps a GlueContext and
        ensures that Job.commit() is called.

        Parameters
        ----------
        options, optional
            Dictionary of key-value pairs to pass to Job.init().
            Defaults to None.
        conf, optional
            Custom SparkConf to use with SparkContext.getOrCreate().
            Defaults to None.
        """
        self.options = options or {}
        self.conf = conf

        super().__init__()

    def __enter__(self) -> GlueContext:
        job_name = self.options.get("JOB_NAME", "")

        conf = self.conf or SparkConf()
        conf = conf.setAppName(job_name)

        spark_context = SparkContext.getOrCreate(conf)
        self.glue_context = GlueContext(spark_context)

        self.job = Job(self.glue_context)
        self.job.init(job_name, self.options)

        return self.glue_context

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        self.job.commit()

        return cast(bool, False)  # noqa: FBT003
