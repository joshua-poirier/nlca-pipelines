GIT_HASH ?= $(shell git log --format="%h" -n 1)
IMAGE_TAG = ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_REPOSITORY}:${GIT_HASH}

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
	pipenv run python -m mypy nlca_pipelines --install-types --non-interactive
	pipenv run python -m mypy tests --install-types --non-interactive

.PHONY: format
format:
	pipenv run python -m isort nlca_pipelines
	pipenv run python -m black nlca_pipelines --preview
	pipenv run python -m isort tests
	pipenv run python -m black tests --preview

.PHONY: test
test:
	pipenv run pytest -x --nf tests

.PHONY: docs
docs:
	pipenv run pdoc -d google -o docs --math nlca_pipelines !nlca_pipelines.helper

.PHONY: docker_clean
docker_clean:
	docker container prune
	docker image prune

.PHONY: ecr_login
ecr_login:
	aws ecr get-login-password --region ${AWS_REGION} | \
		docker login \
		--username AWS \
		--password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

.PHONY: build
build:
	docker build \
		--tag ${IMAGE_TAG} \
		.

.PHONY: push
push:
	docker push \
		${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_REPOSITORY}:${GIT_HASH}

.PHONY: start
start:
	docker run \
		-p 8080:80 \
		-it ${IMAGE_TAG}
