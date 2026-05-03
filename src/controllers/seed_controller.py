from src.repositories import CategoriaRepository, DatasetRepository, PerguntaRepository
from src.services.extractors.reinan_extractor import ReinanExtractor
from src.services.extractors.ericles_extractor import EclerkExtractor
from src.services.extractors.fernanda_extractor import FernandaExtractor


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
            "Direito Constitucional",
            "Direito da Criança e do Adolescente",
            "Direito do Consumidor",
            "Direito do Trabalho",
            "Direito Empresarial",
            "Direito Internacional",
            "Direito Penal",
            "Direito Processual Civil",
            "Direito Processual do Trabalho",
            "Direito Processual Penal",
            "Direito Tributário",
            "Direitos Humanos",
            "Ética Profissional e Estatuto da OAB",
            "Filosofia do Direito",
            "Direito Trabalhista",
            "Direito Previdenciário",
            "Estatuto da OAB",
            "Direito Disciplinar",
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
        pergunta_repo = PerguntaRepository()

        perguntas = []
        perguntas.extend(reinan_extractor.extract_questions())
        perguntas.extend(ericles_extractor.extract_questions())
        perguntas.extend(fernanda_extractor.extract_questions())

        for pergunta in perguntas:
            pergunta_repo.create(**pergunta)

        print("Perguntas semeadas com sucesso!")
