check:
	uv run ruff check
	uv run ruff format
	uv run complexipy src
install:
	uv sync
run:
	uv run main.py
puml:
	uv run py2puml src src > docs/diagrama_classes.puml
