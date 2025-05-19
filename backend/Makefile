default: help

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: run
run: # Run the application.
	uv run -m src

.PHONY: test
test: # Run all tests in the codebase.
	uv run pytest ./tests -v -s

.PHONY: test-filter
test-filter: # Run tests with a specific filter.
	uv run pytest ./tests -v -s -k $(filter)

.PHONY: test-coverage
test-coverage: # Run tests with coverage.
	uv run pytest --cov=src tests/

.PHONY: lint
lint: # Run linters on the codebase.
	uv run ruff format src tests
	uv run ruff check src tests --fix --unsafe-fixes