MAKEFLAGS += --no-print-directory

DOCKER_COMPOSE = USER_ID=$$(id -u) docker compose -f docker/docker-compose.yml

COMPOSE_RUN = $(DOCKER_COMPOSE) run --rm --remove-orphans --build glue

COMPOSE_EXEC = $(DOCKER_COMPOSE) exec glue


.PHONY: all
all: ## Show help (default)
	@echo "=== Glue PySpark Dev Tools ==="
	@echo
	@echo "Available commands:"
	@grep --extended-regexp '^[ /.a-zA-Z0-9_-]+:.*?## .*$$' Makefile | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


docker/.env:
	@cp -n docker/.env.sample docker/.env
	@echo "Created docker/.env file."


poetry.lock:
	@poetry lock --no-update


.PHONY: install
install: docker/.env ## Create virtualenv and install dependencies
ifeq ($(PLATFORM), docker)
	@echo "ERROR: `make install` is meant to be used outside the container." && false
else
	@poetry install --no-root --sync
endif


.PHONY: outdated
outdated: ## Check for outdated dependencies
ifeq ($(PLATFORM), docker)
	@echo "ERROR: Please run the same command outside the container." && false
else
	@poetry show --latest --outdated
endif


docker/requirements.txt: poetry.lock
ifeq ($(PLATFORM), docker)
	@echo "ERROR: Please run the same command outside the container." && false
else
	@poetry export --with=dev --output docker/requirements.txt
endif


.PHONY: start
start: install docker/requirements.txt ## Rebuild and start the development container
ifeq ($(PLATFORM), docker)
	@echo "ERROR: `make start` is meant to be used outside the container." && false
else
	@$(DOCKER_COMPOSE) up --build --remove-orphans
endif


.PHONY: format
format: ## Format project source code
ifeq ($(PLATFORM), docker)
	@ruff check . --fix --unsafe-fixes
	@ruff format .
else
	@poetry run ruff check . --fix --unsafe-fixes
	@poetry run ruff format .
endif


.PHONY: lint
lint: ## Check source code for common errors
ifeq ($(PLATFORM), docker)
	@ruff format . --check
	@ruff check .
else
	@poetry run ruff format . --check
	@poetry run ruff check .
	@poetry run lint-imports
endif


.PHONY: typecheck
typecheck: ## Check type annotations
ifeq ($(PLATFORM), docker)
	@mypy
else
	@poetry run mypy
endif


.PHONY: test
test: docker/requirements.txt ## Run automated tests
ifeq ($(PLATFORM), docker)
	@python3 -m pytest
else
	@$(COMPOSE_RUN) -c "make test"
endif


.PHONY: coverage
coverage: docker/requirements.txt ## Generate test coverage HTML report
ifeq ($(PLATFORM), docker)
	@python3 -m pytest --cov=glueetl --cov-branch --cov-report=term
	@python3 -m coverage html
else
	@$(COMPOSE_RUN) -c "make coverage"
endif


.PHONY: checks
checks: format typecheck


.PHONY: githooks
githooks: ## Install project git hooks
	@poetry run pre-commit install --install-hooks
	@poetry run pre-commit run --all-files


.PHONY: synth
synth: ## Synthesizes and prints the CloudFormation template
ifeq ($(PLATFORM), docker)
	@echo "ERROR: `make synth` is meant to be used outside the container." && false
else
	@cdk synth --strict
endif


.PHONY: diff
diff: ## Compares the specified stack with the deployed stack
ifeq ($(PLATFORM), docker)
	@echo "ERROR: `make diff` is meant to be used outside the container." && false
else
	@cdk diff --strict
endif


.PHONY: deploy
deploy: ## Deploy the application including the necessary infrastructure
ifeq ($(PLATFORM), docker)
	@echo "ERROR: `make deploy` is meant to be used outside the container." && false
else
	@cdk deploy --strict
endif


.PHONY: shell
shell: ## Start a bash shell session inside the container
ifeq ($(PLATFORM), docker)
	@echo "ERROR: You are already typing in a shell inside the container." && false
else
	@$(COMPOSE_EXEC) bash
endif


.PHONY: clean-notebooks
clean-notebooks: ## Removes output cells from Jupyter notebooks
ifeq ($(PLATFORM), docker)
	@jupyter nbconvert --clear-output notebooks/**/*.ipynb
else
	@$(COMPOSE_RUN) -c "make clean-notebooks"
endif


.PHONY: pyspark
pyspark: ## Start a Spark shell session
ifeq ($(PLATFORM), docker)
	@pyspark
else
	@$(COMPOSE_RUN) -c pyspark
endif


.PHONY: clean
clean: ## Delete generated artifacts
	@rm -rf cdk.out __pycache__ .coverage .mypy_cache .pytest_cache .ruff_cache htmlcov
	@poetry run pre-commit gc
