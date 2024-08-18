.PHONY: run setup clean

run:
	echo "Running the application"

dev:
	flask --app src.web.app run --debug 

test:
	pytest --verbose

# Install the dependencies to the virtual environment
# Remove unnecessary dependencies
setup: pyproject.toml
	uv sync --all-extras

quality:
	ruff format --config pyproject.toml --line-length 88 --exclude src/notebook .
	ruff check --fix --respect-gitignore --exclude src/notebook --config pyproject.toml .

clean:
	rm -rf __pycache__
	rm -rf .venv

