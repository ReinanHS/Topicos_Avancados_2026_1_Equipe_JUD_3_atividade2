from src.services.extractors.ericles_extractor import EclerkExtractor


class FernandaExtractor(EclerkExtractor):
    """
    Extrator específico para o repositório feito por Fernanda.
    URL Base: https://github.com/safira1344/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1
    """

    def __init__(self):
        super().__init__()
        self.base_raw_url = "https://raw.githubusercontent.com/safira1344/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1/refs/heads/main"
