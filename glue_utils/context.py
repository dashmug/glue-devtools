from contextlib import ContextDecorator
from types import TracebackType
from typing import cast

from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark import SparkConf
from pyspark.sql import SparkSession


class ManagedGlueContext(ContextDecorator):
    options: dict[str, str]
    job: Job

    def __init__(self, options: dict[str, str] | None = None) -> None:
        self.options = options or {}

        super().__init__()

    def __enter__(self) -> GlueContext:
        glue_context = self.create_glue_context(self.create_spark_session())

        self.job = Job(glue_context)
        self.job.init(self.options.get("JOB_NAME", ""), self.options)

        return glue_context

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        self.job.commit()

        return cast(bool, False)  # noqa: FBT003

    def create_spark_conf(self) -> SparkConf:
        return SparkConf()

    def create_spark_session(self) -> SparkSession:
        conf = self.create_spark_conf()

        return (
            SparkSession.builder.appName(name=self.options.get("JOB_NAME", ""))
            .config(conf=conf)
            .getOrCreate()
        )

    def create_glue_context(self, spark_session: SparkSession) -> GlueContext:
        return GlueContext(spark_session)
