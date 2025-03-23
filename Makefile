DEFAULT_GOAL := help
APP_INSTANCE ?= app

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf " %-20s %s\n", $$1, $$2}'

run: ## Run the application using uvicorn with provided arguments or defaults
	poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload --env-file .local.env

run_test: ## Run the application using uvicorn with provided arguments or defaults
	poetry run uvicorn test:$(APP_INSTANCE) --host 0.0.0.0 --port 8000 --reload


migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head

install: ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall: ## Uninstall a dependency using poetry
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)
