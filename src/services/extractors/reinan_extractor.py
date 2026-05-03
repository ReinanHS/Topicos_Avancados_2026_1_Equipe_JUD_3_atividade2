from src.services.extractors.base_extractor import BaseExtractor


class ReinanExtractor(BaseExtractor):
    """
    Extrator específico para o repositório feito por ReinanHS.
    URL Base: https://github.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1
    """

    def __init__(self):
        super().__init__()
        self.base_raw_url = "https://raw.githubusercontent.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1/refs/heads/results"

    def extract_questions(self) -> list:
        """
        Extrai as perguntas.
        """

        questions_oab_bench = self.extract_questions_oab_bench()

        return questions_oab_bench

    def find_curatorship_by_question_id(
        self, question_id: str, data_curatorship: dict
    ) -> dict:
        for item in data_curatorship:
            if item["question_id"] == question_id:
                return item
        return None

    def extract_questions_oab_bench(self) -> list:
        """
        Extrai as perguntas e respostas do arquivo JSON como exemplo.
        """

        url = (
            f"{self.base_raw_url}/results/oab_bench/model_curatorship/gpt-4o-mini.json"
        )

        print(f"[{self.__class__.__name__}] Baixando dados de: {url}")
        data_curatorship = self.fetch_json(url)

        dataset_name = "oab_bench"

        oab_bench_dataset = self.dataset_loader.create(dataset_name)
        questions_data = oab_bench_dataset.load_questions(
            slice_start=176, slice_end=188
        )
        dataset_id = self.find_dataset_id(dataset_name)

        data = []

        for question in questions_data:
            question_id = str(question["question_id"])
            curatorship = self.find_curatorship_by_question_id(
                question_id, data_curatorship
            )
            category_id = self.find_category_id(
                curatorship["curatorship"]["area_expertise"]
            )

            difficulty = curatorship["curatorship"]["difficulty_question"]

            data.append(
                {
                    "id_dataset": dataset_id,
                    "id_categoria": category_id,
                    "id_externo": question_id,
                    "tipo_pergunta": "discursiva",
                    "enunciado": question["statement"],
                    "nivel_dificuldade": f"Nivel {difficulty}",
                    "legislacao_basica": curatorship["curatorship"][
                        "basic_legislation"
                    ],
                    "metadados": {
                        "values": question["values"],
                    },
                }
            )

        return data
