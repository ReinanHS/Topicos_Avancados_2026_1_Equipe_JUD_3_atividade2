from .base_extractor import BaseExtractor


class ReinanExtractor(BaseExtractor):
    """
    Extrator específico para o repositório feito por ReinanHS.
    URL Base: https://github.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1
    """

    def __init__(self):
        super().__init__()
        self.base_raw_url = "https://raw.githubusercontent.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1/refs/heads/results"

    def extract_perguntas(self) -> list:
        """
        Extrai as perguntas e respostas do arquivo JSON como exemplo.
        """

        url = (
            f"{self.base_raw_url}/results/oab_bench/model_curatorship/gpt-4o-mini.json"
        )

        print(f"[{self.__class__.__name__}] Baixando dados de: {url}")
        data = self.fetch_json(url)

        return data
