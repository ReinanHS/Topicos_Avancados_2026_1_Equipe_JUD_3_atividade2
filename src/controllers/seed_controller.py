from pathlib import Path

from src.repositories import (
    CategoriaRepository,
    DatasetRepository,
    PerguntaRepository,
    ModeloRepository,
)
from src.services.exporters import ExtracaoExporter
from src.services.extractors.reinan_extractor import ReinanExtractor
from src.services.extractors.ericles_extractor import EriclesExtractor
from src.services.extractors.fernanda_extractor import FernandaExtractor
from src.services.extractors.victor_extractor import VictorExtractor
from src.services.extractors.julia_extractor import JuliaExtractor
from src.services.extractors.mikaela_extractor import MikaelaExtractor


class SeedController:
    """
    Controller responsável por orquestrar a inserção de dados iniciais (seeding)
    no banco de dados.
    """

    def seed_datasets(self):
        """Insere as informações de datasets essenciais no banco de dados."""
        repo = DatasetRepository()

        datasets = [
            {
                "nome": "oab_exams",
                "url_origem": "https://huggingface.co/datasets/eduagarcia/oab_exams",
                "dominio": "Direito",
                "tipo_tarefa": "multipla_escolha",
                "versao": "b47d6f3",
                "descricao": "Dataset com questões objetivas de múltipla escolha (1ª fase) dos exames da OAB.",
            },
            {
                "nome": "oab_bench",
                "url_origem": "https://github.com/maritaca-ai/oab-bench",
                "dominio": "Direito",
                "tipo_tarefa": "discursiva",
                "versao": "238e999",
                "descricao": "Dataset com questões discursivas (2ª fase) dos exames da OAB.",
            },
        ]

        try:
            for ds in datasets:
                repo.create(**ds)

            print("Datasets semeados com sucesso!")
        except Exception as e:
            print(f"Erro ao semear datasets: {e}")

    def seed_categorias(self):
        """Insere as categorias de direito no banco de dados."""
        repo = CategoriaRepository()

        categorias = [
            "Direito Administrativo",
            "Direito Ambiental",
            "Direito Civil",
            "Direito Constitucional Tributário",
            "Direito Constitucional",
            "Direito Disciplinar",
            "Direito Empresarial",
            "Direito Internacional",
            "Direito Penal",
            "Direito Previdenciário",
            "Direito Processual Civil",
            "Direito Processual Penal",
            "Direito Processual Tributário",
            "Direito Processual do Trabalho",
            "Direito Trabalhista",
            "Direito Tributário",
            "Direito da Criança",
            "Direito do Consumidor",
            "Direito do Trabalho",
            "Direitos Humanos",
            "Estatuto da OAB",
            "Filosofia do Direito",
            "Ética Profissional",
            "Direito Eleitoral",
        ]

        try:
            for cat in categorias:
                repo.create(cat)

            print("Categorias semeadas com sucesso!")
        except Exception as e:
            print(f"Erro ao semear categorias: {e}")

    def seed_perguntas(self):
        """Insere as perguntas no banco de dados."""
        reinan_extractor = ReinanExtractor()
        ericles_extractor = EriclesExtractor()
        fernanda_extractor = FernandaExtractor()
        victor_extractor = VictorExtractor()
        julia_extractor = JuliaExtractor()
        mikaela_extractor = MikaelaExtractor()
        pergunta_repo = PerguntaRepository()

        perguntas = []
        perguntas.extend(reinan_extractor.extract_questions())
        perguntas.extend(ericles_extractor.extract_questions())
        perguntas.extend(fernanda_extractor.extract_questions())
        perguntas.extend(victor_extractor.extract_questions())
        perguntas.extend(julia_extractor.extract_questions())
        perguntas.extend(mikaela_extractor.extract_questions())

        for pergunta in perguntas:
            pergunta_repo.create(**pergunta)

        print("Perguntas semeadas com sucesso!")

    def seed_modelos(self):
        """Insere as informações de modelos iniciais no banco de dados."""
        repo = ModeloRepository()

        modelos = [
            {
                "nome_modelo": "Llama 3.2",
                "versao": "3B",
                "provedor": "Meta",
                "familia": "Llama",
                "parametro_precisao": "N/A",
            },
            {
                "nome_modelo": "Gemma 2",
                "versao": "2B",
                "provedor": "Google",
                "familia": "Gemma",
                "parametro_precisao": "N/A",
            },
            {
                "nome_modelo": "Qwen 2.5",
                "versao": "3B",
                "provedor": "Alibaba",
                "familia": "Qwen",
                "parametro_precisao": "N/A",
            },
            {
                "nome_modelo": "Llama 3.1",
                "versao": "8B",
                "provedor": "Meta",
                "familia": "Llama",
                "parametro_precisao": "N/A",
            },
            {
                "nome_modelo": "Mistral",
                "versao": "7B",
                "provedor": "Mistral AI",
                "familia": "Mistral",
                "parametro_precisao": "N/A",
            },
            {
                "nome_modelo": "DeepSeek-R1",
                "versao": "8B",
                "provedor": "DeepSeek",
                "familia": "DeepSeek",
                "parametro_precisao": "N/A",
            },
            {
                "nome_modelo": "Claude Sonnet 4.6",
                "versao": "claude-sonnet-4-6",
                "provedor": "Anthropic",
                "familia": "Claude",
                "parametro_precisao": "N/A",
            },
            {
                "nome_modelo": "GPT-4o",
                "versao": "gpt-4o",
                "provedor": "OpenAI",
                "familia": "GPT",
                "parametro_precisao": "N/A",
            },
            {
                "nome_modelo": "GPT-4o mini",
                "versao": "gpt-4o-mini",
                "provedor": "OpenAI",
                "familia": "GPT",
                "parametro_precisao": "N/A",
            },
        ]

        try:
            for mod in modelos:
                repo.create(**mod)

            print("Modelos semeados com sucesso!")
        except Exception as e:
            print(f"Erro ao semear modelos: {e}")

    def seed_respostas(self):
        """Insere as respostas dos modelos no banco de dados."""
        from src.repositories.resposta_repository import RespostaRepository

        reinan_extractor = ReinanExtractor()
        ericles_extractor = EriclesExtractor()
        fernanda_extractor = FernandaExtractor()
        victor_extractor = VictorExtractor()
        julia_extractor = JuliaExtractor()
        mikaela_extractor = MikaelaExtractor()

        resposta_repo = RespostaRepository()

        respostas = []
        respostas.extend(reinan_extractor.extract_answers())
        respostas.extend(ericles_extractor.extract_answers())
        respostas.extend(fernanda_extractor.extract_answers())
        respostas.extend(victor_extractor.extract_answers())
        respostas.extend(julia_extractor.extract_answers())
        respostas.extend(mikaela_extractor.extract_answers())

        for resposta in respostas:
            if resposta.get("id_modelo") and resposta.get("id_pergunta"):
                resposta_repo.create(
                    id_pergunta=resposta["id_pergunta"],
                    id_modelo=resposta["id_modelo"],
                    texto_resposta=resposta["texto_resposta"],
                    tempo_inferencia_ms=resposta["tempo_inferencia_ms"],
                )
            else:
                print(f"Não foi possível semear a resposta: {resposta}")

        print("Respostas semeadas com sucesso!")

    # ------------------------------------------------------------------
    # Export / Import das extrações (perguntas + respostas)
    # ------------------------------------------------------------------

    def export_extracao(self, type_: str) -> None:
        """Exporta `perguntas`, `respostas` ou ambos para JSON portável."""
        exporter = ExtracaoExporter()
        type_ = (type_ or "all").lower()

        if type_ not in {"perguntas", "respostas", "all"}:
            raise ValueError(
                f"--type inválido: '{type_}'. Use 'perguntas', 'respostas' ou 'all'."
            )

        if type_ in {"perguntas", "all"}:
            path = exporter.export_perguntas()
            print(f"Exportado: {path}")
        if type_ in {"respostas", "all"}:
            path = exporter.export_respostas()
            print(f"Exportado: {path}")

    def _print_import_result(self, label: str, result: dict) -> None:
        print(
            f"  {label}: importadas={result['imported']} | "
            f"puladas={result['skipped']} | "
            f"erros={len(result['errors'])}"
        )
        for err in result["errors"]:
            print(f"    - {err}")

    def import_extracao(self, input_path: Path) -> None:
        """
        Importa um arquivo de extração. Decide pelo `type` interno do JSON
        qual fluxo executar (perguntas vs respostas).
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")

        print(f"Importando {input_path}...")
        exporter = ExtracaoExporter()

        # Lê o type antes de decidir o fluxo — evita try/except esquisito.
        import json as _json

        type_ = _json.loads(input_path.read_text(encoding="utf-8")).get("type")

        if type_ == "perguntas":
            result = exporter.import_perguntas_file(input_path)
            self._print_import_result("perguntas", result)
        elif type_ == "respostas":
            result = exporter.import_respostas_file(input_path)
            self._print_import_result("respostas", result)
        else:
            raise ValueError(
                f"Arquivo {input_path} não tem 'type' válido (perguntas|respostas)."
            )

    def import_extracao_all(self, directory: Path | None = None) -> None:
        """Importa perguntas primeiro, depois respostas (ordem das FKs)."""
        directory = directory or ExtracaoExporter.EXPORT_DIR
        if not directory.exists():
            print(f"Pasta não existe: {directory}")
            return

        exporter = ExtracaoExporter()
        perguntas_path = directory / ExtracaoExporter.PERGUNTAS_FILENAME
        respostas_path = directory / ExtracaoExporter.RESPOSTAS_FILENAME

        if perguntas_path.exists():
            print(f"Importando {perguntas_path}...")
            result = exporter.import_perguntas_file(perguntas_path)
            self._print_import_result("perguntas", result)
        else:
            print(f"Aviso: {perguntas_path} não existe — pulando perguntas.")

        if respostas_path.exists():
            print(f"Importando {respostas_path}...")
            result = exporter.import_respostas_file(respostas_path)
            self._print_import_result("respostas", result)
        else:
            print(f"Aviso: {respostas_path} não existe — pulando respostas.")

    def seed_all(self):
        """Executa todos os seeds na ordem correta de dependências."""
        print("=== Iniciando seed completo ===")
        self.seed_modelos()
        self.seed_categorias()
        self.seed_datasets()
        self.seed_perguntas()
        self.seed_respostas()
        print("=== Seed completo finalizado com sucesso! ===")
