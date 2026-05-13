import os
from dotenv import load_dotenv

from src.services.judges.base_judge import BaseJudge


class GoogleJudge(BaseJudge):
    """
    Juiz baseado em modelos Google (ex.: Gemini 1.5 Pro). Usa o SDK `google-genai`.
    Requer a variável de ambiente GOOGLE_CLOUD_API_KEY.
    """

    def __init__(self, model: str, db_model_name: str):
        super().__init__(model=model, db_model_name=db_model_name)
        load_dotenv()

        api_key = os.getenv("GOOGLE_CLOUD_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GOOGLE_CLOUD_API_KEY não está definida no ambiente. "
                "Configure-a no .env para usar o juiz do Google."
            )

        try:
            from google import genai
        except ImportError as e:
            raise ImportError(
                "Pacote 'google-genai' não instalado. Rode `uv add google-genai` ou adicione no pyproject.toml."
            ) from e

        self._client = genai.Client(api_key=api_key)

    @property
    def provider(self) -> str:
        return "google"

    def complete(self, prompt: str) -> str:
        from google import genai

        completion = self._client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=genai.types.GenerateContentConfig(temperature=0.0),
        )
        return completion.text or ""
