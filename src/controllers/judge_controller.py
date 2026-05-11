#victor
from src.services.judge import JudgeService


class JudgeController:
    """
    Controller responsável por executar o pipeline do Juiz-IA.
    """

    def run(
        self,
        modelo_juiz_db: str,
        ollama_model: str,
        base_url: str,
        limit: int | None,
        use_mock: bool,
    ) -> dict:
        service = JudgeService(
            modelo_juiz_db=modelo_juiz_db,
            ollama_model=ollama_model,
            base_url=base_url,
            use_mock=use_mock,
        )

        return service.run(limit=limit)