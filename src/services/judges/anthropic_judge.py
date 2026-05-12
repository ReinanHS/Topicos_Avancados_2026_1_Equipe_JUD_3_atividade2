import os
from dotenv import load_dotenv

from src.services.judges.base_judge import BaseJudge


class AnthropicJudge(BaseJudge):
    """
    Juiz baseado em modelos Anthropic (Claude). Usa o SDK oficial `anthropic`.
    Requer a variável de ambiente ANTHROPIC_API_KEY.
    """

    MAX_TOKENS = 2048

    def __init__(self, model: str, db_model_name: str):
        super().__init__(model=model, db_model_name=db_model_name)
        load_dotenv()

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY não está definida no ambiente. "
                "Configure-a no .env para usar o juiz Anthropic."
            )

        try:
            from anthropic import Anthropic
        except ImportError as e:
            raise ImportError(
                "Pacote 'anthropic' não instalado. Rode `uv sync` após atualizar pyproject.toml."
            ) from e

        self._client = Anthropic(api_key=api_key)

    @property
    def provider(self) -> str:
        return "anthropic"

    def complete(self, prompt: str) -> str:
        message = self._client.messages.create(
            model=self.model,
            max_tokens=self.MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
        parts = [
            block.text
            for block in message.content
            if getattr(block, "type", None) == "text"
        ]
        return "".join(parts)
