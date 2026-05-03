from src.services.extractors.base_extractor import BaseExtractor


class ReinanExtractor(BaseExtractor):
    """
    Extrator específico para o repositório feito por ReinanHS.
    URL Base: https://github.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1
    """

    def __init__(self):
        super().__init__()
        self.base_raw_url = "https://raw.githubusercontent.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1/refs/heads/results"
        self.dataset_range = {
            "oab_bench": {
                "slice_start": 176,
                "slice_end": 188,
            },
            "oab_exams": {
                "slice_start": 1845,
                "slice_end": 1967,
            },
        }

    def get_curatorship_data(self, dataset_name: str) -> list[dict]:
        url = f"{self.base_raw_url}/results/{dataset_name}/model_curatorship/gpt-4o-mini.json"
        return self.fetch_json(url)

    def parse_curatorship(self, curatorship: dict) -> dict:
        category_text = curatorship["curatorship"]["area_expertise"]
        category_name = category_text.split(" e ")[0].strip()

        return {
            "category": category_name,
            "difficulty": curatorship["curatorship"]["difficulty_question"],
            "legislation": curatorship["curatorship"]["basic_legislation"],
        }
