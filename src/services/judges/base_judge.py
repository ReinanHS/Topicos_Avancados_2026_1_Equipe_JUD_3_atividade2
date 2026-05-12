from abc import ABC, abstractmethod


class BaseJudge(ABC):
    """
    Contrato base para um juiz LLM.

    Cada juiz concreto sabe falar com um provedor (Ollama local, Anthropic API,
    OpenAI API). A responsabilidade aqui é apenas: receber um prompt textual
    e devolver o output bruto do modelo. A construção do prompt fica em
    `prompts.py` e o parsing do veredito fica em `parser.py`.
    """

    def __init__(self, model: str, db_model_name: str):
        self.model = model
        self.db_model_name = db_model_name

    @property
    def name(self) -> str:
        """Identificador legível do juiz (provedor:modelo)."""
        return f"{self.provider}:{self.model}"

    @property
    @abstractmethod
    def provider(self) -> str:
        """Nome do provedor (ex: 'ollama', 'anthropic', 'openai')."""
        ...

    @abstractmethod
    def complete(self, prompt: str) -> str:
        """Envia um prompt ao modelo e retorna o texto bruto da resposta."""
        ...
