from src.services.extractors.ericles_extractor import EclerkExtractor


class JuliaExtractor(EclerkExtractor):
    """
    Extrator para as questões da Julia.

    A inferencia e a curadoria das questoes da Julia foram executadas dentro
    do repositorio da Atividade 1 do Ericles (junto com as questoes dele e
    da Mikaela), entao reaproveitamos o mesmo `base_raw_url` e o mesmo formato
    de `curator_annotations.json` (heranca do EclerkExtractor) — apenas
    sobrescrevemos o range para extrair somente as perguntas dela.

    URL Base: https://github.com/Ericles-Porty/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1
    """

    def __init__(self):
        super().__init__()
        self.dataset_range = {
            "oab_bench": {
                "slice_start": 165,
                "slice_end": 177,
            },
            "oab_exams": {
                "slice_start": 1723,
                "slice_end": 1846,
            },
        }
