#victor
import json
import os
import re
from typing import Any

import requests


class LLMJudgeClient:
    """
    Cliente responsável por chamar o modelo Juiz-IA.

    Implementação atual:
    - roda LOCALMENTE via Ollama;
    - usa o endpoint http://localhost:11434/api/generate;
    - não depende de chave de API;
    - é adequada para testes locais e execução reprodutível do trabalho.

    Possível implementação futura:
    - usar OpenAI API ou Gemini API;
    - nesses casos, será necessário criar um novo método de geração;
    - também será necessário configurar a chave da API por variável de ambiente;
    - o método generate deverá ser alterado para chamar o provedor escolhido.
    """

    def __init__(
        self,
        model: str = "llama3.1",
        base_url: str = "http://localhost:11434",
        timeout: int = 180,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, prompt: str) -> str:
        """
        Envia o prompt para o modelo juiz e retorna a resposta textual.

        Nesta versão, a execução é LOCAL via Ollama.

        Para usar uma API externa no futuro, altere o retorno deste método.
        Exemplos:
            return self._generate_openai_api(prompt)
            return self._generate_gemini_api(prompt)
        """
        return self._generate_ollama(prompt)

        # Opções futuras, caso a equipe decida usar API externa:
        # return self._generate_openai_api(prompt)
        # return self._generate_gemini_api(prompt)

    def _generate_ollama(self, prompt: str) -> str:
        """
        Execução local via Ollama.

        Requisitos:
        - Ollama instalado no Windows;
        - modelo baixado localmente, por exemplo:
              ollama pull llama3.1
        - servidor Ollama ativo em:
              http://localhost:11434

        Observação:
        - Docker/PostgreSQL podem continuar rodando normalmente;
        - o Ollama roda separado do Docker neste projeto.
        """
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.0,
                "num_ctx": 8192,
            },
        }

        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()

        data = response.json()
        return data.get("response", "")

    # ---------------------------------------------------------------------
    # OPÇÃO FUTURA 1: OPENAI API
    # ---------------------------------------------------------------------
    # Sugestão:
    # - usar OpenAI API com saída estruturada/JSON.
    #
    # Motivo:
    # - boa aderência ao formato JSON;
    # - possibilidade de uso de modelos mais robustos;
    # - útil quando a equipe quiser reduzir erros de estrutura na resposta.
    #
    # Antes de usar:
    # 1. Criar uma chave de API da OpenAI.
    # 2. Definir a variável de ambiente OPENAI_API_KEY.
    # 3. Alterar o método generate para:
    #       return self._generate_openai_api(prompt)
    #
    # Exemplo no PowerShell:
    #       $env:OPENAI_API_KEY="sua-chave-aqui"
    #
    # Observação:
    # - este bloco está comentado de propósito;
    # - ele serve como documentação para uma possível evolução do projeto;
    # - não será executado enquanto generate usar _generate_ollama.
    # ---------------------------------------------------------------------
    #
    # def _generate_openai_api(self, prompt: str) -> str:
    #     """
    #     Exemplo de implementação futura usando OpenAI API.
    #
    #     Para ativar:
    #     - descomente este método;
    #     - altere generate para retornar self._generate_openai_api(prompt);
    #     - configure OPENAI_API_KEY no ambiente.
    #     """
    #     api_key = os.getenv("OPENAI_API_KEY")
    #
    #     if not api_key:
    #         raise ValueError(
    #             "Variável de ambiente OPENAI_API_KEY não encontrada. "
    #             "Configure a chave antes de usar a OpenAI API."
    #         )
    #
    #     url = "https://api.openai.com/v1/chat/completions"
    #
    #     payload = {
    #         "model": "gpt-4.1-mini",
    #         "messages": [
    #             {
    #                 "role": "system",
    #                 "content": (
    #                     "Você é um Juiz-IA especializado em avaliação jurídica. "
    #                     "Responda somente em JSON válido com nota e justificativa."
    #                 ),
    #             },
    #             {
    #                 "role": "user",
    #                 "content": prompt,
    #             },
    #         ],
    #         "temperature": 0,
    #         "response_format": {
    #             "type": "json_object"
    #         },
    #     }
    #
    #     headers = {
    #         "Authorization": f"Bearer {api_key}",
    #         "Content-Type": "application/json",
    #     }
    #
    #     response = requests.post(
    #         url,
    #         headers=headers,
    #         json=payload,
    #         timeout=self.timeout,
    #     )
    #     response.raise_for_status()
    #
    #     data = response.json()
    #     return data["choices"][0]["message"]["content"]

    # ---------------------------------------------------------------------
    # OPÇÃO FUTURA 2: GEMINI API
    # ---------------------------------------------------------------------
    # Sugestão:
    # - usar Gemini API com structured output.
    #
    # Motivo:
    # - permite solicitar respostas estruturadas;
    # - pode ser uma alternativa para comparação com o juiz local;
    # - pode ser útil caso a equipe queira avaliar desempenho/custo/qualidade.
    #
    # Antes de usar:
    # 1. Criar uma chave de API do Gemini.
    # 2. Definir a variável de ambiente GEMINI_API_KEY.
    # 3. Alterar o método generate para:
    #       return self._generate_gemini_api(prompt)
    #
    # Exemplo no PowerShell:
    #       $env:GEMINI_API_KEY="sua-chave-aqui"
    #
    # Observação:
    # - este bloco está comentado de propósito;
    # - ele serve como documentação para uma possível evolução do projeto;
    # - não será executado enquanto generate usar _generate_ollama.
    # ---------------------------------------------------------------------
    #
    # def _generate_gemini_api(self, prompt: str) -> str:
    #     """
    #     Exemplo de implementação futura usando Gemini API.
    #
    #     Para ativar:
    #     - descomente este método;
    #     - altere generate para retornar self._generate_gemini_api(prompt);
    #     - configure GEMINI_API_KEY no ambiente.
    #     """
    #     api_key = os.getenv("GEMINI_API_KEY")
    #
    #     if not api_key:
    #         raise ValueError(
    #             "Variável de ambiente GEMINI_API_KEY não encontrada. "
    #             "Configure a chave antes de usar a Gemini API."
    #         )
    #
    #     model_name = "gemini-2.5-flash"
    #     url = (
    #         "https://generativelanguage.googleapis.com/v1beta/models/"
    #         f"{model_name}:generateContent?key={api_key}"
    #     )
    #
    #     payload = {
    #         "contents": [
    #             {
    #                 "parts": [
    #                     {
    #                         "text": prompt
    #                     }
    #                 ]
    #             }
    #         ],
    #         "generationConfig": {
    #             "temperature": 0,
    #             "responseMimeType": "application/json",
    #             "responseSchema": {
    #                 "type": "object",
    #                 "properties": {
    #                     "nota": {
    #                         "type": "integer",
    #                         "minimum": 1,
    #                         "maximum": 5
    #                     },
    #                     "justificativa": {
    #                         "type": "string"
    #                     }
    #                 },
    #                 "required": [
    #                     "nota",
    #                     "justificativa"
    #                 ]
    #             }
    #         }
    #     }
    #
    #     headers = {
    #         "Content-Type": "application/json",
    #     }
    #
    #     response = requests.post(
    #         url,
    #         headers=headers,
    #         json=payload,
    #         timeout=self.timeout,
    #     )
    #     response.raise_for_status()
    #
    #     data = response.json()
    #     return data["candidates"][0]["content"]["parts"][0]["text"]

    @staticmethod
    def parse_judge_response(raw_response: str) -> dict[str, Any]:
        """
        Extrai nota e justificativa de uma resposta JSON do modelo juiz.
        """
        text = (raw_response or "").strip()

        # Remove blocos markdown, caso o modelo ignore a instrução.
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

        parsed = None

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            # Tenta recuperar o primeiro objeto JSON dentro do texto.
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))

        if not isinstance(parsed, dict):
            raise ValueError(f"Resposta do juiz não é um JSON válido: {raw_response}")

        nota = parsed.get("nota") or parsed.get("score") or parsed.get("nota_atribuida")

        justificativa = (
            parsed.get("justificativa")
            or parsed.get("justification")
            or parsed.get("chain_of_thought")
            or parsed.get("raciocinio")
            or parsed.get("raciocínio")
        )

        try:
            nota = int(nota)
        except Exception as exc:
            raise ValueError(f"Nota inválida na resposta do juiz: {raw_response}") from exc

        if nota < 1 or nota > 5:
            raise ValueError(f"Nota fora da faixa 1..5: {nota}")

        if not justificativa:
            justificativa = "Avaliação gerada sem justificativa textual pelo modelo juiz."

        return {
            "nota": nota,
            "justificativa": str(justificativa).strip(),
            "raw_response": raw_response,
        }