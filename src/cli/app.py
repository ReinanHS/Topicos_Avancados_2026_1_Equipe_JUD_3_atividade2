"""
Módulo CLI principal — interface de linha de comando baseada em Typer.
"""

import typer

from src.controllers import (
    AnalysisController,
    JudgeController,
    MigrationController,
    SeedController,
)
from src.services.judges import JudgeFactory

app = typer.Typer(no_args_is_help=True)
db_app = typer.Typer(no_args_is_help=True, help="Gerenciamento do banco de dados.")
app.add_typer(db_app, name="db")

seed_app = typer.Typer(
    no_args_is_help=True, help="Semeia dados iniciais no banco de dados."
)
db_app.add_typer(seed_app, name="seed")

judge_app = typer.Typer(no_args_is_help=True, help="Pipeline LLM-as-a-Judge.")
db_app.add_typer(judge_app, name="judge")

analysis_app = typer.Typer(
    no_args_is_help=True, help="Análise estatística das avaliações."
)
db_app.add_typer(analysis_app, name="analysis")


@db_app.command("migrate")
def db_migrate():
    """Aplica todas as migrações pendentes no banco de dados."""
    controller = MigrationController()
    controller.migrate()


@db_app.command("rollback")
def db_rollback(
    all: bool = typer.Option(True, help="Reverter todas as migrações (padrão)."),
):
    """Reverte as migrações aplicadas no banco de dados."""
    controller = MigrationController()
    controller.rollback(all_migrations=all)


@seed_app.command("dataset")
def seed_dataset():
    """Insere as informações dos datasets no banco de dados."""
    controller = SeedController()
    controller.seed_datasets()


@seed_app.command("categorias")
def seed_categorias():
    """Insere as categorias de direito no banco de dados."""
    controller = SeedController()
    controller.seed_categorias()


@seed_app.command("perguntas")
def seed_perguntas():
    """Insere as perguntas no banco de dados."""
    controller = SeedController()
    controller.seed_perguntas()


@seed_app.command("modelos")
def seed_modelos():
    """Insere as informações de modelos no banco de dados."""
    controller = SeedController()
    controller.seed_modelos()


@seed_app.command("respostas")
def seed_respostas():
    """Insere as respostas dos modelos no banco de dados."""
    controller = SeedController()
    controller.seed_respostas()


@seed_app.command("all")
def seed_all():
    """Executa todos os seeds na ordem correta."""
    controller = SeedController()
    controller.seed_all()


@judge_app.command("evaluate")
def judge_evaluate(
    judge: list[str] = typer.Option(
        ...,
        "--judge",
        "-j",
        help=(
            "Juiz no formato 'provedor:modelo' (ex.: 'ollama:llama3.1:8b', "
            "'openai:gpt-4o'). Repita para usar de 1 a 3 juízes na mesma execução."
        ),
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Limita o número de respostas avaliadas por juiz (útil para smoke test).",
    ),
):
    """Executa o pipeline LLM-as-a-Judge para os juízes informados."""
    if not 1 <= len(judge) <= 3:
        raise typer.BadParameter("Informe entre 1 e 3 juízes via --judge/-j.")
    JudgeController().evaluate(judge, limit=limit)


@judge_app.command("list-available")
def judge_list_available():
    """Lista as specs de juízes pré-configuradas."""
    print("Juízes disponíveis:")
    for spec in JudgeFactory.available():
        print(f"  - {spec}")


@analysis_app.command("run")
def analysis_run():
    """Executa a análise estatística (Spearman + agregados) sobre as avaliações."""
    AnalysisController().run()


@app.callback()
def main_callback():
    """
    CLI para manipulação de dados.
    """
    pass
