from src.services.extractors.base_extractor import BaseExtractor


class EclerkExtractor(BaseExtractor):
    """
    Extrator específico para o repositório feito por Eclerk.
    URL Base: https://github.com/Ericles-Porty/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1
    """

    def __init__(self):
        super().__init__()
        self.base_raw_url = "https://raw.githubusercontent.com/Ericles-Porty/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1/refs/heads/main"
        self.dataset_range = {
            "oab_bench": {
                "slice_start": 153,
                "slice_end": 165,
            },
            "oab_exams": {
                "slice_start": 1600,
                "slice_end": 1723,
            },
        }

    def get_curatorship_data(self, dataset_name: str) -> list[dict]:
        url = f"{self.base_raw_url}/src/results/curator_annotations.json"
        return self.fetch_json(url)

    def parse_curatorship(self, curatorship: dict) -> dict:
        difficulty = curatorship["dificuldade"]
        if difficulty is None:
            difficulty = 3

        return {
            "category": curatorship["subdominio_semantico"],
            "difficulty": difficulty,
            "legislation": curatorship["corpus_referencia"],
        }
