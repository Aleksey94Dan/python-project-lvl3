install:
		@poetry install

test:
		poetry run pytest
lint:
		poetry run flake8 page-loader
check:
		@poetry check
.PHONY: install test lint check
