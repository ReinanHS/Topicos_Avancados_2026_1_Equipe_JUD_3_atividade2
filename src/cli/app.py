"""
Módulo CLI principal — interface de linha de comando baseada em Typer.
"""

import typer
from yoyo import read_migrations

from src.database import DatabaseManager

app = typer.Typer(no_args_is_help=True)
db_app = typer.Typer(no_args_is_help=True, help="Gerenciamento do banco de dados.")
app.add_typer(db_app, name="db")


def _get_backend():
    """Retorna o backend do yoyo-migrations utilizando o DatabaseManager."""
    db_manager = DatabaseManager()
    return db_manager.get_yoyo_backend()


@db_app.command("migrate")
def db_migrate():
    """Aplica todas as migrações pendentes no banco de dados."""
    backend = _get_backend()
    migrations = read_migrations("database/migrations")
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
    print("Migracoes aplicadas com sucesso.")


@db_app.command("rollback")
def db_rollback(
    all: bool = typer.Option(True, help="Reverter todas as migrações (padrão)."),
):
    """Reverte as migrações aplicadas no banco de dados."""
    backend = _get_backend()
    migrations = read_migrations("database/migrations")
    with backend.lock():
        to_rollback = backend.to_rollback(migrations)
        if not to_rollback:
            print("Nenhuma migracao para reverter.")
            return

        if not all:
            to_rollback = [to_rollback[0]]

        backend.rollback_migrations(to_rollback)

    if all:
        print("Rollback completo: todas as migracoes foram revertidas.")
    else:
        print("Rollback: ultima migracao revertida com sucesso.")


@app.callback()
def main_callback():
    """
    CLI para manipulação de dados.
    """
    pass
