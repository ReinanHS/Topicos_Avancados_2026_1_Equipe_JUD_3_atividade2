import os
import requests
from dotenv import load_dotenv

from src.services.judges.base_judge import BaseJudge


class OllamaJudge(BaseJudge):
    """
    Juiz baseado em Ollama (modelos locais). Comunica-se via HTTP REST,
    sem dependência de SDK externo.
    """

    DEFAULT_HOST = "http://localhost:11434"
    REQUEST_TIMEOUT = 300  # modelos locais maiores podem levar minutos

    def __init__(self, model: str, db_model_name: str):
        super().__init__(model=model, db_model_name=db_model_name)
        load_dotenv()
        self.host = os.getenv("OLLAMA_HOST", self.DEFAULT_HOST).rstrip("/")

    @property
    def provider(self) -> str:
        return "ollama"

    def complete(self, prompt: str) -> str:
        """Chama o endpoint /api/generate do Ollama e devolve o texto bruto."""
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.0},
        }
        response = requests.post(url, json=payload, timeout=self.REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
