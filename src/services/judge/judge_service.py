#victor
import re

from src.repositories import (
    AvaliacaoJuizRepository,
    ModeloRepository,
    PerguntaRepository,
    RespostaRepository,
)
from src.services.judge.llm_judge_client import LLMJudgeClient
from src.services.judge.prompt_builder import JudgePromptBuilder


class JudgeService:
    """
    Orquestra o pipeline LLM-as-a-Judge.

    Fluxo:
    1. Busca o modelo juiz cadastrado na tabela modelos.
    2. Busca respostas da Atividade 1 ainda não avaliadas por esse juiz.
    3. Recupera a pergunta correspondente.
    4. Monta o prompt de avaliação.
    5. Chama o modelo juiz ou usa mock para teste.
    6. Interpreta a nota e a justificativa.
    7. Salva o resultado em avaliacoes_juiz.

    Implementação atual:
    - o juiz roda LOCALMENTE via Ollama;
    - o parâmetro ollama_model representa o nome do modelo local;
    - o parâmetro base_url representa o endereço local do Ollama.

    Possível evolução futura:
    - usar uma API externa, como OpenAI API ou Gemini API;
    - para isso, será necessário adaptar LLMJudgeClient;
    - também será necessário acrescentar um parâmetro provider,
      por exemplo: provider="ollama", provider="openai" ou provider="gemini";
    - a chave da API deve ser configurada em variável de ambiente,
      como OPENAI_API_KEY ou GEMINI_API_KEY.
    """

    def __init__(
        self,
        modelo_juiz_db: str,
        ollama_model: str = "llama3.1",
        base_url: str = "http://localhost:11434",
        use_mock: bool = False,
        # -----------------------------------------------------------------
        # PREPARAÇÃO FUTURA PARA API EXTERNA
        # -----------------------------------------------------------------
        # Este parâmetro está comentado de propósito.
        #
        # Caso a equipe decida usar OpenAI API ou Gemini API,
        # uma evolução possível seria:
        #
        # provider: str = "ollama",
        #
        # E então o LLMJudgeClient poderia decidir internamente:
        # - provider == "ollama" -> chamada local via Ollama;
        # - provider == "openai" -> chamada via OpenAI API;
        # - provider == "gemini" -> chamada via Gemini API.
        #
        # Exemplo futuro:
        #
        # self.llm_client = LLMJudgeClient(
        #     provider=provider,
        #     model=ollama_model,
        #     base_url=base_url,
        # )
        #
        # Nesta versão, mantemos apenas Ollama ativo para evitar quebrar
        # o pipeline local já implementado.
        # -----------------------------------------------------------------
    ):
        self.modelo_juiz_db = modelo_juiz_db
        self.use_mock = use_mock

        self.modelo_repo = ModeloRepository()
        self.pergunta_repo = PerguntaRepository()
        self.resposta_repo = RespostaRepository()
        self.avaliacao_repo = AvaliacaoJuizRepository()

        self.prompt_builder = JudgePromptBuilder()

        self.llm_client = LLMJudgeClient(
            model=ollama_model,
            base_url=base_url,
        )

    def run(self, limit: int | None = 10) -> dict:
        modelo_juiz = self.modelo_repo.get_by_name(self.modelo_juiz_db)

        if not modelo_juiz:
            raise ValueError(
                f"Modelo juiz '{self.modelo_juiz_db}' não encontrado na tabela modelos."
            )

        id_modelo_juiz = modelo_juiz["id_modelo"]

        respostas = self.resposta_repo.get_pendentes_avaliacao(
            id_modelo_juiz=id_modelo_juiz,
            limit=limit,
        )

        total_processadas = 0
        total_erros = 0

        print(f"Respostas pendentes encontradas: {len(respostas)}")

        for resposta in respostas:
            try:
                pergunta = self.pergunta_repo.get_by_id(resposta["id_pergunta"])

                if not pergunta:
                    raise ValueError(
                        f"Pergunta {resposta['id_pergunta']} não encontrada."
                    )

                prompt = self.prompt_builder.build(pergunta, resposta)

                if self.use_mock:
                    parsed = self._mock_evaluation(pergunta, resposta)
                else:
                    # -----------------------------------------------------
                    # CHAMADA DO JUIZ-IA
                    # -----------------------------------------------------
                    # Implementação atual:
                    # - chama o modelo local via Ollama.
                    #
                    # Caso a equipe evolua para API externa:
                    # - a alteração principal deve ocorrer em LLMJudgeClient;
                    # - este ponto do pipeline pode continuar igual,
                    #   pois o método generate(prompt) permaneceria como
                    #   interface única para qualquer provedor.
                    #
                    # Exemplo conceitual:
                    # raw_response = self.llm_client.generate(prompt)
                    #
                    # O provider poderia ser definido no construtor do client:
                    # - "ollama"
                    # - "openai"
                    # - "gemini"
                    # -----------------------------------------------------
                    raw_response = self.llm_client.generate(prompt)
                    parsed = self.llm_client.parse_judge_response(raw_response)

                self.avaliacao_repo.create(
                    id_resposta_ativa1=resposta["id_resposta"],
                    id_modelo_juiz=id_modelo_juiz,
                    nota_atribuida=parsed["nota"],
                    chain_of_thought=parsed["justificativa"],
                )

                total_processadas += 1

                print(
                    f"OK resposta={resposta['id_resposta']} "
                    f"modelo_candidato={resposta['nome_modelo']} "
                    f"nota={parsed['nota']}"
                )

            except Exception as exc:
                total_erros += 1
                print(f"ERRO resposta={resposta.get('id_resposta')}: {exc}")

        return {
            "pendentes_lidas": len(respostas),
            "avaliacoes_salvas": total_processadas,
            "erros": total_erros,
        }

    @staticmethod
    def _extract_option(text: str | None) -> str | None:
        """
        Tenta identificar uma alternativa A, B, C ou D em um texto.
        Usado apenas no modo mock.
        """
        if not text:
            return None

        match = re.search(r"\b([A-D])\b", str(text).upper())

        return match.group(1) if match else None

    def _mock_evaluation(self, pergunta: dict, resposta: dict) -> dict:
        """
        Avaliação simples apenas para testar o pipeline sem chamar o LLM.

        Importante:
        - este modo não deve ser usado como resultado final da atividade;
        - ele serve apenas para verificar se o fluxo banco -> avaliação -> banco funciona.
        """
        tipo = (pergunta.get("tipo_pergunta") or "").lower()
        metadados = pergunta.get("metadados") or {}
        resposta_texto = resposta.get("texto_resposta") or ""

        if "multipla" in tipo or "múltipla" in tipo or "objetiva" in tipo:
            gabarito = None

            if isinstance(metadados, dict):
                gabarito = (
                    metadados.get("answerKey")
                    or metadados.get("answer_key")
                    or metadados.get("correct_answer")
                    or metadados.get("gabarito")
                )

            ref_option = self._extract_option(gabarito)
            ans_option = self._extract_option(resposta_texto)

            nota = 5 if ref_option and ans_option == ref_option else 1

            justificativa = (
                "Avaliação mock para teste técnico do pipeline. "
                f"Gabarito identificado: {ref_option}; "
                f"resposta identificada: {ans_option}."
            )

        else:
            tamanho = len(resposta_texto.strip())
            nota = 1 if tamanho == 0 else 3 if tamanho < 500 else 4

            justificativa = (
                "Avaliação mock para teste técnico do pipeline. "
                "A nota foi estimada apenas pelo tamanho da resposta. "
                "Use o modo com Ollama para avaliação jurídica real."
            )

        return {
            "nota": nota,
            "justificativa": justificativa,
        }