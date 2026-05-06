from src.repositories import (
    CategoriaRepository,
    DatasetRepository,
    PerguntaRepository,
    ModeloRepository,
)
from src.services.extractors.reinan_extractor import ReinanExtractor
from src.services.extractors.ericles_extractor import EclerkExtractor
from src.services.extractors.fernanda_extractor import FernandaExtractor
from src.services.extractors.victor_extractor import VictorExtractor


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
        ericles_extractor = EclerkExtractor()
        fernanda_extractor = FernandaExtractor()
        victor_extractor = VictorExtractor()
        pergunta_repo = PerguntaRepository()

        perguntas = []
        perguntas.extend(reinan_extractor.extract_questions())
        perguntas.extend(ericles_extractor.extract_questions())
        perguntas.extend(fernanda_extractor.extract_questions())
        perguntas.extend(victor_extractor.extract_questions())

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
        ]

        try:
            for mod in modelos:
                repo.create(**mod)

            print("Modelos semeados com sucesso!")
        except Exception as e:
            print(f"Erro ao semear modelos: {e}")
