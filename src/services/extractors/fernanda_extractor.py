from src.services.extractors.ericles_extractor import EriclesExtractor


class FernandaExtractor(EriclesExtractor):
    """
    Extrator específico para o repositório feito por Fernanda.
    URL Base: https://github.com/safira1344/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1
    """

    def __init__(self):
        super().__init__()
        self.base_raw_url = "https://raw.githubusercontent.com/safira1344/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1/refs/heads/main"
        self.dataset_range = {
            "oab_bench": {
                "slice_start": 141,
                "slice_end": 153,
            },
            "oab_exams": {
                "slice_start": 1477,
                "slice_end": 1600,
            },
        }
