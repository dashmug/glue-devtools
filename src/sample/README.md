# Sample Glue Job from AWS Glue Documentation

This script and its corresponding test script are taken from AWS Glue documentation on [using a Docker image for local development](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-libraries.html#develop-local-docker-image).

## Running the script

The script needs to be executed inside the container so it can simulate 
the AWS Glue runtime.

Make sure you start the container.

    $ make start

In a separate terminal, do this to open a shell inside the docker 
container

    $ make shell

Once inside the container, you can use manually execute the script via

    [glue_user@7634c978b92c workspace]$ spark-submit src/sample/script.py