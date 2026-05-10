from src.services.extractors.base_extractor import BaseExtractor


class VictorExtractor(BaseExtractor):
    """
    Extrator específico para o repositório feito por Victor.
    URL Base: https://github.com/Leomascarenhas91/Topicos_Avancados_2026-1_Equipe_JUD_3_Victor_atividade1
    """

    def __init__(self):
        super().__init__()
        self.base_raw_url = "https://raw.githubusercontent.com/Leomascarenhas91/Topicos_Avancados_2026-1_Equipe_JUD_3_Victor_atividade1/refs/heads/main"
        self.dataset_range = {
            "oab_bench": {
                "slice_start": 200,
                "slice_end": 210,
            },
            "oab_exams": {
                "slice_start": 2091,
                "slice_end": 2210,
            },
        }

    def get_curatorship_data(self, dataset_name: str) -> list[dict]:
        dataset_name_url = "J1_inferencia_Victor_ANALITICA"
        if "oab_exams" in dataset_name:
            dataset_name_url = "J2_curadoria_Victor_FINAL"

        url = f"{self.base_raw_url}/{dataset_name_url}.csv"
        return self.fetch_csv_to_dict(url)

    def parse_curatorship(self, curatorship: dict) -> dict:
        subdominio = curatorship["Subdominio_Semantico"].replace("Subdomínio: ", " ")
        subdominios = subdominio.split(" e ")
        category_name = subdominios[0].strip()

        match curatorship["Complexidade_Raciocinio_LLM"]:
            case "Hermenêutica Jurídica Complexa":
                difficulty = 3
            case "Recuperação Factual Direta":
                difficulty = 2
            case "Raciocínio Lógico-Dedutivo":
                difficulty = 1
            case _:
                difficulty = 3

        legislation = curatorship["Corpus_Aterramento"].replace("Corpus: ", "").strip()

        return {
            "category": category_name,
            "difficulty": difficulty,
            "legislation": legislation,
        }

    def extract_questions_oab_exams(self) -> list:
        """
        Extrai as perguntas do OAB Exams.
        """
        return self._process_dataset_questions(
            dataset_name="oab_exams",
            slice_start=self.dataset_range["oab_exams"]["slice_start"],
            slice_end=self.dataset_range["oab_exams"]["slice_end"],
            question_id_field="id",
            statement_field="question",
            tipo_pergunta="multipla_escolha",
            extract_metadados=lambda q: {
                "question_number": q.get("question_number"),
                "exam_id": q.get("exam_id"),
                "exam_year": q.get("exam_year"),
                "question_type": q.get("question_type"),
                "nullified": q.get("nullified"),
            },
        )
