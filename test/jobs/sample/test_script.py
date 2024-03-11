from unittest.mock import patch

from jobs.sample import script


@patch("glue_utils.context.GlueContext")
def test_extract(mock_glue_context):
    expected_count = 1961
    mock_glue_context.create_dynamic_frame_from_options.return_value.toDF.return_value.count.return_value = expected_count

    path = "s3://some-bucket-out-there/persons.json"

    dyf = script.extract(glue_context=mock_glue_context, path=path)

    assert dyf.toDF().count() == expected_count
    mock_glue_context.create_dynamic_frame_from_options.assert_called_once_with(
        connection_type="s3",
        connection_options={"paths": [path], "recurse": True},
        format="json",
    )


@patch("glue_utils.context.GlueContext")
@patch("jobs.sample.script.ManagedGlueContext")
def test_run(mock_managed_glue_context, mock_glue_context):
    mock_managed_glue_context.return_value.__enter__.return_value = mock_glue_context

    script.run()

    mock_glue_context.create_dynamic_frame_from_options.assert_called_once_with(
        connection_type="s3",
        connection_options={
            "paths": ["s3://awsglue-datasets/examples/us-legislators/all/persons.json"],
            "recurse": True,
        },
        format="json",
    )
