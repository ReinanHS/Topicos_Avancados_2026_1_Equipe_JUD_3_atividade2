import os
from dotenv import load_dotenv

from src.services.judges.base_judge import BaseJudge


class OpenAIJudge(BaseJudge):
    """
    Juiz baseado em modelos OpenAI (ex.: GPT-4o). Usa o SDK oficial `openai`.
    Requer a variável de ambiente OPENAI_API_KEY.
    """

    def __init__(self, model: str, db_model_name: str):
        super().__init__(model=model, db_model_name=db_model_name)
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY não está definida no ambiente. "
                "Configure-a no .env para usar o juiz OpenAI."
            )

        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError(
                "Pacote 'openai' não instalado. Rode `uv sync` após atualizar pyproject.toml."
            ) from e

        self._client = OpenAI(api_key=api_key)

    @property
    def provider(self) -> str:
        return "openai"

    def complete(self, prompt: str) -> str:
        completion = self._client.chat.completions.create(
            model=self.model,
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content or ""
