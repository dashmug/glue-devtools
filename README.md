# Glue PySpark Dev Tools

This sub-project provides the boilerplate and tooling to help in
developing AWS Glue ETL Jobs in PySpark.

## Setup

Make sure you have the following available from your shell (terminal):

- `poetry`
- `python3.10`

If they are missing, you can `brew install` them.

Once the requirements above are ready, you create the poetry environment 
and install the project dependencies. To do that,

    $ make install

## Starting the container

We use the container to emulate Glue's runtime environment.

To start the container,

    $ make start

This will start the container and run JupyterLab. If the
container is not built yet, it will build first before starting.

Be patient. It will take around 15 minutes to build it for the first
time. But succeeding builds will take a lot less.

To start a bash shell from inside this running container, you can do

    $ make shell

## Using JupyterLab

Once the container has successfully started, point your browser to
http://127.0.0.1:8888/lab.

## Running a PySpark shell

To run a PySpark shell,

    $ make pyspark

## Developing Glue/PySpark scripts using Jupyter Notebook

Using the JupyterLab, you can create a PySpark notebook which imports
your Glue/PySpark code and run things there.

## Adding runtime dependencies

Please check [Python modules already provided in AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html#glue-modules-provided)
to see if the library that you need is already included in the AWS Glue
runtime.

If the desired version of the library is already included, we only need
it to our local environment.

    $ poetry add --group=runtime {{library name}}=={{exact version}}

If you need to add a new runtime library, you need to add it in our local
environment,

    $ poetry add --group=runtime {{library name}}

and make sure to use the `--additional-python-modules` option when
defining your Glue script.

## Adding development dependencies

```shell
$ poetry add {{library name}}
# To update the requirements.txt
$ make requirements.container.txt 
# To rebuild the docker container for local testing purposes
$ make start 
```

## List of Makefile commands

```
=== Glue PySpark Dev Tools ===

Available commands:
help                 Show help (default)
install              Create virtualenv and install dependencies
outdated             Check for outdated dependencies
start                Rebuild and start the development container
format               Format project source code
lint                 Check source code for common errors
typecheck            Check type annotations
test                 Run automated tests
coverage             Generate test coverage HTML report
shell                Start a bash shell session inside the container
clean-notebooks      Removes output cells from Jupyter notebooks
pyspark              Start a Spark shell session
audit                Audit dependencies for security issues
clean                Delete generated artifacts
```
