check:
	uv run ruff format
	uv run ruff check
	uv run complexipy src
install:
	uv sync
run:
	uv run main.py
puml:
	uv run py2puml src src > docs/diagrama_classes.puml
db-dump:
	@echo "Salvando schema do banco de dados..."
	docker exec -t postgres_jud_db pg_dump -U admin -s -F p -E UTF-8 jud_db > database/schema.sql
db-restore:
	@echo "Restaurando schema do banco de dados..."
	cat database/schema.sql | docker exec -i postgres_jud_db psql -U admin
