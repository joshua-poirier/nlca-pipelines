.PHONY: init
init:
	pip install pipenv
	pipenv install --dev

.PHONY: lint
lint:
	pipenv run pylint nlca_pipelines
	pipenv run python -m flake8 nlca_pipelines
	pipenv run pylint tests
	pipenv run python -m flake8 tests

.PHONY: check_format
check_format:
	pipenv run python -m isort nlca_pipelines --check-only
	pipenv run python -m black nlca_pipelines --diff
	pipenv run python -m isort tests --check-only
	pipenv run python -m black tests --diff

.PHONY: check_type
check_type:
	pipenv run python -m mypy nlca_pipelines
	pipenv run python -m mypy tests

.PHONY: format
format:
	pipenv run python -m isort nlca_pipelines
	pipenv run python -m black nlca_pipelines --preview
	pipenv run python -m isort tests
	pipenv run python -m black tests --preview

.PHONY: test
test:
	pipenv run pytest tests

.PHONY: docs
docs:
	pipenv run pdoc -d google -o docs --math nlca_pipelines
