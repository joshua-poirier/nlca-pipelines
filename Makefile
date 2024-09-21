.PHONY: init
init:
	pip install pipenv
	pipenv install --dev

.PHONY: lint
lint:
	pipenv run pylint nlca_pipelines
	pipenv run python -m flake8 nlca_pipelines

.PHONY: check_format
check_format:
	pipenv run python -m isort nlca_pipelines --check-only
	pipenv run python -m black nlca_pipelines --diff

.PHONY: check_type
check_type:
	pipenv run python -m mypy nlca_pipelines

.PHONY: format
format:
	pipenv run python -m isort nlca_pipelines
	pipenv run python -m black nlca_pipelines --preview

.PHONY: test
test:
	pipenv run pytest tests

.PHONY: docs
docs:
	pipenv run pdoc -d google -o docs --math nlca_pipelines
