# Makefile

install:
	poetry install

run:
	poetry run uvicorn main:app --reload

# Remove generated files and directories
clean:
	rm -rf __pycache__ .pytest_cache

# Remove virtual environment and Poetry-generated files
reset:
	poetry env remove $(shell poetry env list --full-path)

# Display help message
help:
	@echo "Available targets:"
	@echo "  - install   : Install project dependencies"
	@echo "  - run       : Run FastAPI development server"
	@echo "  - clean     : Remove generated files and directories"
	@echo "  - reset     : Remove virtual environment and Poetry-generated files"
