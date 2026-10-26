# make up | run | test | lint | audit | check | down   (make help lists all)
PYTHON ?= $(shell command -v python3.13 || command -v python3.12 || command -v python3)
VENV := .venv
PY := $(VENV)/bin/python
STAMP := $(VENV)/.installed
CLI := $(VENV)/bin/adr-toolkit

-include .env
export

.PHONY: help install env up run report test lint format audit check down clean

help: ## list the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sed -E 's/:.*## /\t/' | sort

$(STAMP): requirements-dev.lock pyproject.toml
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -q --require-hashes -r requirements-dev.lock
	$(VENV)/bin/pip install -q --no-deps -e .
	touch $@

install: $(STAMP) ## create .venv from the hash-pinned lock file

env:
	@[ -f .env ] || { cp .env.example .env; echo "created .env from .env.example"; }

up: env $(STAMP) ## prepare the environment (there are no services to start)

run: up ## run every document check and write the report
	$(CLI) check
	$(CLI) report

report: up ## write build/report.md
	$(CLI) report

test: $(STAMP) ## unit tests with coverage (domain and application must stay at 95% or more)
	$(PY) -m pytest tests --cov=adr_toolkit --cov-report=term
	$(PY) -m coverage report --include='src/adr_toolkit/domain/*,src/adr_toolkit/application/*' --fail-under=95

lint: $(STAMP) ## ruff check, ruff format check, mypy, import-linter, and the document checks
	$(VENV)/bin/ruff check .
	$(VENV)/bin/ruff format --check .
	$(VENV)/bin/mypy
	$(VENV)/bin/lint-imports
	$(CLI) check

format: $(STAMP) ## apply ruff's formatting and safe fixes
	$(VENV)/bin/ruff check --fix .
	$(VENV)/bin/ruff format .

audit: $(STAMP) ## check the locked dependencies for known vulnerabilities
	$(VENV)/bin/pip-audit --no-deps --disable-pip -r requirements-dev.lock

check: lint test ## everything CI runs apart from the audit

down: ## remove generated output (nothing is running)
	rm -rf build

clean: down
	rm -rf $(VENV) .pytest_cache .mypy_cache .ruff_cache .import_linter_cache .coverage htmlcov
