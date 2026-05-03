"""
Módulo CLI principal — interface de linha de comando baseada em Typer.
"""

import typer

from src.controllers import DatabaseController

app = typer.Typer(no_args_is_help=True)
db_app = typer.Typer(no_args_is_help=True, help="Gerenciamento do banco de dados.")
app.add_typer(db_app, name="db")

seed_app = typer.Typer(
    no_args_is_help=True, help="Semeia dados iniciais no banco de dados."
)
db_app.add_typer(seed_app, name="seed")


@db_app.command("migrate")
def db_migrate():
    """Aplica todas as migrações pendentes no banco de dados."""
    controller = DatabaseController()
    controller.migrate()


@db_app.command("rollback")
def db_rollback(
    all: bool = typer.Option(True, help="Reverter todas as migrações (padrão)."),
):
    """Reverte as migrações aplicadas no banco de dados."""
    controller = DatabaseController()
    controller.rollback(all_migrations=all)


@seed_app.command("dataset")
def seed_dataset():
    """Insere as informações dos datasets no banco de dados."""
    controller = DatabaseController()
    controller.seed_datasets()


@app.callback()
def main_callback():
    """
    CLI para manipulação de dados.
    """
    pass
