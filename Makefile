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
	@echo "Salvando dump completo do banco de dados..."
	docker exec postgres_jud_db sh -c "pg_dump -U admin -F p -E UTF-8 jud_db > /tmp/dump.sql"
	docker cp postgres_jud_db:/tmp/dump.sql database/dump.sql
	docker exec postgres_jud_db rm /tmp/dump.sql

db-restore-full:
	@echo "Restaurando dump completo do banco de dados..."
	docker cp database/dump.sql postgres_jud_db:/tmp/dump.sql
	docker exec postgres_jud_db sh -c "psql -U admin -d jud_db -f /tmp/dump.sql"
	docker exec postgres_jud_db rm /tmp/dump.sql

