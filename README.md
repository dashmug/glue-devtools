# Glue DevTools

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

This sub-project provides the boilerplate and tooling to help in
developing AWS Glue ETL Jobs.

## Setup

Make sure you have the following available from your shell (terminal):

- `poetry`
- `python3.10`

If they are missing, you can `brew install` them.

Once the requirements above are ready, you create the poetry environment
and install the project dependencies. To do that,

    make install

## Starting the container

We use the container to emulate Glue's runtime environment.

To start the container,

    make start

This will start the container and run JupyterLab. If the
container is not built yet, it will build first before starting.

Be patient. It will take around 15 minutes to build it for the first
time. But succeeding builds will take a lot less.

To start a bash shell from inside this running container, you can do

    make shell

## Using JupyterLab

Once the container has successfully started, point your browser to
<http://127.0.0.1:8888/lab>.

## Running a PySpark shell

To run a PySpark shell,

    make pyspark

## Developing Glue/PySpark scripts using Jupyter Notebook

Using the JupyterLab, you can create a PySpark notebook which imports
your Glue/PySpark code and run things there.

## Adding runtime dependencies

Please check [Python modules already provided in AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html#glue-modules-provided)
to see if the library that you need is already included in the AWS Glue
runtime.

If the desired version of the library is already included, we only need
it to our local environment.

    poetry add --group=runtime {{library name}}=={{exact version}}

If you need to add a new runtime library, you need to add it in our local
environment,

    poetry add --group=runtime {{library name}}

and make sure to use the `--additional-python-modules` option when
defining your Glue script.

## Adding development dependencies

```shell
$ poetry add {{library name}}
# To update the docker/requirements.txt file
$ make docker/requirements.txt
# To rebuild the docker container for local testing purposes
$ make start
```

## Installing Git Hooks

This project includes git hooks that will execute several checks when
making commits. This gives us feedback during development on checks
that would otherwise fail in CI.

To install them,

    make githooks

After installation, it will do an initial run to check all files.

## List of Makefile commands

```
=== Glue Dev Tools ===

Available commands:
all                  Show help (default)
install              Create virtualenv and install dependencies
outdated             Check for outdated dependencies
start                Rebuild and start the development container
format               Format project source code
lint                 Check source code for common errors
typecheck            Check type annotations
test                 Run automated tests
coverage             Generate test coverage HTML report
githooks             Install/update project git hooks
synth                Synthesizes and prints the CloudFormation template
diff                 Compares the specified stack with the deployed stack
deploy               Deploy the application including the necessary infrastructure
shell                Start a bash shell session inside the container
clean-notebooks      Removes output cells from Jupyter notebooks
pyspark              Start a Spark shell session
clean                Delete generated artifacts
```
