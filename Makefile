SHELL:=/usr/bin/env bash

install:
		@poetry install
test:
		poetry run pytest --cov=page_loader tests/ --cov-report=xml
lint:
		poetry run flake8 page_loader tests
		poetry run mypy page_loader tests
build:
		poetry build
publish:
		poetry publish -r test

package-install:
		pip install --user dist/*.whl
check:
		@poetry check

clean:
		find . -type f -name *.pyc -delete
		find . -type d -name __pycache__ -delete

.PHONY: install test lint check clean
