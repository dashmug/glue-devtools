from typing import Any

from aws_cdk import aws_glue as glue
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3_assets as s3_assets
from constructs import Construct

from infrastructure.constructs.base import BaseStack


class SampleStack(BaseStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role(
            self,
            "Role",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "CloudWatchFullAccessV2"
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSGlueServiceRole"
                ),
            ],
        )

        security_config = glue.CfnSecurityConfiguration(
            self,
            "SecurityConfig",
            name="security-configuration",
            encryption_configuration=glue.CfnSecurityConfiguration.EncryptionConfigurationProperty(
                s3_encryptions=[
                    glue.CfnSecurityConfiguration.S3EncryptionProperty(
                        s3_encryption_mode="SSE-S3"
                    )
                ],
            ),
        )

        script = s3_assets.Asset(self, "Script", path="jobs/sample/script.py")

        glue.CfnJob(
            self,
            "SampleJob",
            name="sample-job",
            role=role.role_arn,
            command=glue.CfnJob.JobCommandProperty(
                name="glueetl",
                script_location=script.s3_object_url,
            ),
            execution_class="FLEX",
            glue_version="4.0",
            security_configuration=security_config.name,
            timeout=30,
            worker_type="G.1X",
            number_of_workers=2,
            default_arguments={
                "--job-language": "python",
                "--enable-continuous-cloudwatch-log": True,
                "--enable-continuous-log-filter": True,
                "--enable-job-insights": True,
                "--enable-metrics": True,
                "--enable-observability-metrics": True,
                "--enable-spark-ui": True,
            },
        )
