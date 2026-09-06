PIP ?= python -m pip
PYTHON ?= python
RUFF ?= $(PYTHON) -m ruff
PYTEST ?= $(PYTHON) -m pytest

setup:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

lint:
	$(RUFF) check src tests

format:
	$(RUFF) format src tests

format-check:
	$(RUFF) format --check src tests

test:
	$(PYTEST) tests

check:
	$(MAKE) lint
	$(MAKE) format-check
	$(MAKE) test
