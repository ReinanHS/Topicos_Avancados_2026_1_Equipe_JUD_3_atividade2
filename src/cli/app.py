"""
Módulo CLI principal — interface de linha de comando baseada em Typer.
"""

import typer

from src.controllers import MigrationController, SeedController, JudgeController

app = typer.Typer(no_args_is_help=True)
db_app = typer.Typer(no_args_is_help=True, help="Gerenciamento do banco de dados.")
app.add_typer(db_app, name="db")
#victor
judge_app = typer.Typer(no_args_is_help=True, help="Pipeline LLM-as-a-Judge.")
app.add_typer(judge_app, name="judge")

seed_app = typer.Typer(
    no_args_is_help=True, help="Semeia dados iniciais no banco de dados."
)
db_app.add_typer(seed_app, name="seed")


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
#victor
@judge_app.command("run")
def judge_run(
    modelo_juiz_db: str = typer.Option(
        "Llama 3.1",
        "--modelo-juiz-db",
        help="Nome do modelo juiz cadastrado na tabela modelos.",
    ),
    ollama_model: str = typer.Option(
        "llama3.1",
        "--ollama-model",
        help="Nome do modelo instalado no Ollama. Ex.: llama3.1, qwen2.5, mistral.",
    ),
    base_url: str = typer.Option(
        "http://localhost:11434",
        "--base-url",
        help="URL base do Ollama.",
    ),
    limit: int = typer.Option(
        10,
        "--limit",
        "-l",
        help="Quantidade máxima de respostas avaliadas nesta execução. Use 0 para todas.",
    ),
    use_mock: bool = typer.Option(
        False,
        "--mock",
        help="Executa avaliação simples sem chamar LLM. Use apenas para testar o pipeline.",
    ),
    # ---------------------------------------------------------------------
    # PREPARAÇÃO FUTURA PARA API EXTERNA
    # ---------------------------------------------------------------------
    # Caso a equipe decida usar OpenAI API ou Gemini API, uma evolução
    # possível seria adicionar uma opção provider no comando:
    #
    # provider: str = typer.Option(
    #     "ollama",
    #     "--provider",
    #     help="Provedor do Juiz-IA: ollama, openai ou gemini.",
    # ),
    #
    # Exemplos futuros de uso:
    #
    # python -m uv run python main.py judge run --provider ollama
    # python -m uv run python main.py judge run --provider openai
    # python -m uv run python main.py judge run --provider gemini
    #
    # Para isso, também seria necessário adaptar:
    # - JudgeController;
    # - JudgeService;
    # - LLMJudgeClient.
    #
    # Nesta versão, mantemos apenas Ollama ativo para não quebrar
    # o pipeline local.
    # ---------------------------------------------------------------------
):
    """Executa o pipeline do Juiz-IA e salva as avaliações no banco."""
    controller = JudgeController()

    result = controller.run(
        modelo_juiz_db=modelo_juiz_db,
        ollama_model=ollama_model,
        base_url=base_url,
        limit=None if limit == 0 else limit,
        use_mock=use_mock,
    )

    typer.echo(f"Resultado: {result}")

@app.callback()
def main_callback():
    """
    CLI para manipulação de dados.
    """
    pass
