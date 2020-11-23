install:
		@poetry install
test:
		poetry run python -m pytest
lint:
		poetry run flake8 page_loader tests
		poetry run mypy page_loader tests
check:
		@poetry check
.PHONY: install test lint check
