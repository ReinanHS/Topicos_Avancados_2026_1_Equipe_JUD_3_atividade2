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
db-dump-schema:
	@echo "Salvando schema do banco de dados..."
	docker exec -t postgres_jud_db pg_dump -U admin -s -F p -E UTF-8 jud_db > database/schema.sql

db-dump-full:
	@echo "Salvando dump completo do banco de dados (com instruções de limpeza)..."
	docker exec -t postgres_jud_db pg_dump -U admin --clean --if-exists -F p -E UTF-8 jud_db > database/dump.sql

db-restore-full:
	@echo "Limpando banco de dados para importação limpa..."
	docker exec -t postgres_jud_db psql -U admin -d jud_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	@echo "Restaurando dump completo do banco de dados..."
	cat database/dump.sql | docker exec -i postgres_jud_db psql -U admin -d jud_db
