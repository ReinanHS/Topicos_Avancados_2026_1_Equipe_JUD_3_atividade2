from src.repositories import CategoriaRepository, DatasetRepository, PerguntaRepository


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
        ]

        try:
            for cat in categorias:
                repo.create(cat)

            print("Categorias semeadas com sucesso!")
        except Exception as e:
            print(f"Erro ao semear categorias: {e}")

    def seed_perguntas(self):
        """Insere as perguntas no banco de dados."""
        dataset_repo = DatasetRepository()
        categoria_repo = CategoriaRepository()
        pergunta_repo = PerguntaRepository()

        dataset = dataset_repo.get_by_name("oab_exams")
        categoria = categoria_repo.get_by_name("Direito Penal")

        if not dataset or not categoria:
            print(
                "Erro: Dataset 'oab_exams' ou Categoria 'Direito Penal' não encontrados. Rode 'db seed dataset' e 'db seed categorias' primeiro."
            )
            return

        pergunta_exemplo = {
            "id_dataset": dataset["id_dataset"],
            "id_categoria": categoria["id_categoria"],
            "id_externo": "exemplo_123",
            "tipo_pergunta": "multipla_escolha",
            "enunciado": "Qual das alternativas abaixo caracteriza crime de furto privilegiado?",
            "nivel_dificuldade": "Nivel 1",
            "legislacao_basica": "Art. 155, § 2º, CP",
            "metadados": {"fonte": "Exame OAB 2023"},
        }

        try:
            pergunta_repo.create(**pergunta_exemplo)
            print("Pergunta de exemplo semeada com sucesso!")
        except Exception as e:
            print(f"Erro ao semear pergunta: {e}")
