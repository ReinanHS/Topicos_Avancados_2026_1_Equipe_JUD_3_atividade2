from src.services.judges.base_judge import BaseJudge
from src.services.judges.ollama_judge import OllamaJudge
from src.services.judges.anthropic_judge import AnthropicJudge
from src.services.judges.openai_judge import OpenAIJudge


class JudgeFactory:
    """
    Fábrica responsável por instanciar o juiz correto a partir de uma spec
    no formato 'provedor:modelo' (ex.: 'ollama:llama3.1:8b', 'openai:gpt-4o').

    Mantém um mapeamento entre a spec e o `nome_modelo` registrado em `modelos`
    para que o controller consiga resolver o `id_modelo_juiz` ao gravar
    avaliações.
    """

    _providers = {
        "ollama": OllamaJudge,
        "anthropic": AnthropicJudge,
        "openai": OpenAIJudge,
    }

    _db_model_map = {
        "ollama:llama3.1:8b": "Llama 3.1",
        "ollama:qwen2.5:7b": "Qwen 2.5",
        "anthropic:claude-sonnet-4-6": "Claude Sonnet 4.6",
        "openai:gpt-4o": "GPT-4o",
        "openai:gpt-4o-mini": "GPT-4o mini",
    }

    @classmethod
    def create(cls, judge_spec: str) -> BaseJudge:
        """
        Cria a instância do juiz correspondente à spec informada.
        Formato: 'provedor:modelo[:variante]'.
        """
        provider, _, model = judge_spec.partition(":")
        if not provider or not model:
            raise ValueError(
                f"Spec de juiz inválida: '{judge_spec}'. "
                f"Use o formato 'provedor:modelo' (ex.: 'ollama:llama3.1:8b')."
            )

        judge_class = cls._providers.get(provider)
        if judge_class is None:
            available = ", ".join(cls._providers.keys())
            raise ValueError(
                f"Provedor '{provider}' não reconhecido. Disponíveis: {available}"
            )

        db_model_name = cls._db_model_map.get(judge_spec)
        if db_model_name is None:
            available_specs = ", ".join(cls._db_model_map.keys())
            raise ValueError(
                f"Spec '{judge_spec}' não está pré-configurada. "
                f"Specs disponíveis: {available_specs}. "
                f"Para adicionar uma nova, registre-a em JudgeFactory._db_model_map "
                f"e em SeedController.seed_modelos."
            )

        return judge_class(model=model, db_model_name=db_model_name)

    @classmethod
    def available(cls) -> list[str]:
        """Lista as specs de juízes pré-configuradas."""
        return list(cls._db_model_map.keys())
