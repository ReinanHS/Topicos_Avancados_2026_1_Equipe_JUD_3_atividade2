"""
Importa as respostas dos modelos candidatos geradas no repositório da
Atividade 1 do Ericles, normalizando-as para o formato esperado pela tabela
`respostas_atividade_1`.

A inferência (chamadas ao Ollama) já foi feita uma única vez naquele
repositório, cobrindo as questões do Ericles + Júlia + Mikaela. Aqui só
baixamos os JSONs via raw URL e mapeamos o identificador do Ollama para o
`(nome_modelo, versao)` inseridos por `SeedController.seed_modelos`.
"""

import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


_BASE_URL = (
    "https://raw.githubusercontent.com/Ericles-Porty/"
    "Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1/refs/heads/main"
)


class Atividade1Importer:
    """Baixa e normaliza as respostas geradas na Atividade 1 do Ericles."""

    SOURCES = [
        ("discursiva", f"{_BASE_URL}/src/results/open_questions.json"),
        ("multipla_escolha", f"{_BASE_URL}/src/results/multiple_choice.json"),
    ]

    OLLAMA_TO_MODELO = {
        "llama3.2:3b": {"nome_modelo": "Llama 3.2", "versao": "3B"},
        "gemma2:2b":   {"nome_modelo": "Gemma 2",   "versao": "2B"},
        "qwen2.5:3b":  {"nome_modelo": "Qwen 2.5",  "versao": "3B"},
    }

    def fetch_json(self, url: str) -> list:
        """Faz o download de um arquivo JSON a partir de uma URL RAW."""
        try:
            with urlopen(url, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError) as e:
            print(f"[erro] falha ao baixar {url}: {e}")
            return []

    def normalize(self, entry: dict, tipo_pergunta: str) -> dict | None:
        """Converte uma entrada bruta no formato esperado pelo `RespostaRepository`."""
        ollama_id = entry.get("model")
        mapping = self.OLLAMA_TO_MODELO.get(ollama_id)
        if mapping is None:
            print(f"[aviso] modelo Ollama '{ollama_id}' sem mapeamento — pulando")
            return None

        texto = (entry.get("answer") or "").strip()
        if not texto:
            return None

        return {
            "id_externo": str(entry["question_id"]),
            "tipo_pergunta": tipo_pergunta,
            "nome_modelo": mapping["nome_modelo"],
            "versao_modelo": mapping["versao"],
            "texto_resposta": texto,
            "tempo_inferencia_ms": entry.get("tempo_inferencia_ms"),
        }

    def extract_respostas(self) -> list[dict]:
        """Baixa e normaliza todas as respostas (abertas + múltipla escolha)."""
        respostas = []
        for tipo_pergunta, url in self.SOURCES:
            for entry in self.fetch_json(url):
                normalized = self.normalize(entry, tipo_pergunta=tipo_pergunta)
                if normalized:
                    respostas.append(normalized)
        return respostas
