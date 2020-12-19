install:
		@poetry install
test:
		poetry run pytest --cov=gendiff tests/ --cov-report=xml
lint:
		poetry run flake8 page_loader tests
		poetry run mypy page_loader tests
build:
		poetry build
package-install:
		pip install --user dist/*.whl
check:
		@poetry check
.PHONY: install test lint check
