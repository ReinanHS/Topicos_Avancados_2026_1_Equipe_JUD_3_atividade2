"""
Análise estatística baseada nos dados do banco.

Implementa a correlação de Spearman entre o Juiz-IA e o Gabarito Humano,
seguindo a metodologia descrita no enunciado da Atividade 2:

- Cenário A (múltipla escolha): converte o gabarito humano em uma nota
  binarizada (5 se a resposta do modelo contém a alternativa correta, 1
  caso contrário) e correlaciona com a nota atribuída pelo juiz.
- Cenário B (questões abertas): como não há nota humana, reporta a
  correlação inter-juízes entre pares de juízes que avaliaram as mesmas
  respostas.
"""

import re

from scipy.stats import spearmanr

from src.repositories import AvaliacaoRepository


class SpearmanAnalysisService:
    """Serviço de análise estatística com correlação de Spearman."""

    def __init__(self):
        self.avaliacao_repo = AvaliacaoRepository()

    def _extract_gold_letter(self, metadados: dict) -> str | None:
        """Tenta identificar a alternativa correta nos metadados da pergunta."""
        if not isinstance(metadados, dict):
            return None
        for key in ("alternativa_correta", "answerKey", "answer_key", "gabarito"):
            value = metadados.get(key)
            if value:
                letter = str(value).strip().upper()
                if letter in {"A", "B", "C", "D", "E"}:
                    return letter
        return None

    def _response_contains_letter(self, texto: str, letter: str) -> bool:
        """Heurística para detectar se o modelo escolheu a letra correta."""
        normalized = (texto or "").strip().upper()
        if not normalized:
            return False
        if normalized == letter:
            return True
        return bool(re.search(rf"\b{letter}\b|\b{letter}\)", normalized))

    def judge_vs_gold(self, judge_name: str) -> dict:
        """
        Correlação Spearman entre nota_humana (binarizada) e nota_atribuida,
        considerando apenas as questões de múltipla escolha que possuem o
        gabarito disponível nos metadados.
        """
        rows = self.avaliacao_repo.fetch_judge_vs_gold(judge_name)

        notas_humanas: list[int] = []
        notas_juiz: list[int] = []
        skipped = 0

        for row in rows:
            if row["tipo_pergunta"] != "multipla_escolha":
                continue
            gold = self._extract_gold_letter(row["metadados"])
            if gold is None:
                skipped += 1
                continue
            humano = (
                5 if self._response_contains_letter(row["texto_resposta"], gold) else 1
            )
            notas_humanas.append(humano)
            notas_juiz.append(row["nota_atribuida"])

        if len(notas_humanas) < 2 or len(set(notas_juiz)) < 2:
            return {
                "judge": judge_name,
                "n": len(notas_humanas),
                "skipped_sem_gabarito": skipped,
                "rho": None,
                "p_value": None,
                "motivo": "Amostra insuficiente ou notas do juiz constantes.",
            }

        rho, p_value = spearmanr(notas_humanas, notas_juiz)
        return {
            "judge": judge_name,
            "n": len(notas_humanas),
            "skipped_sem_gabarito": skipped,
            "rho": float(rho),
            "p_value": float(p_value),
        }

    def inter_judge(self, judge_a: str, judge_b: str) -> dict:
        """Correlação Spearman entre as notas de dois juízes nas mesmas respostas."""
        pares = self.avaliacao_repo.fetch_judge_pair(judge_a, judge_b)

        if len(pares) < 2:
            return {
                "judge_a": judge_a,
                "judge_b": judge_b,
                "n": len(pares),
                "rho": None,
                "p_value": None,
                "motivo": "Não há respostas comuns suficientes entre os dois juízes.",
            }

        notas_a = [p[0] for p in pares]
        notas_b = [p[1] for p in pares]
        if len(set(notas_a)) < 2 or len(set(notas_b)) < 2:
            return {
                "judge_a": judge_a,
                "judge_b": judge_b,
                "n": len(pares),
                "rho": None,
                "p_value": None,
                "motivo": "Notas constantes em um dos juízes — Spearman indefinido.",
            }

        rho, p_value = spearmanr(notas_a, notas_b)
        return {
            "judge_a": judge_a,
            "judge_b": judge_b,
            "n": len(pares),
            "rho": float(rho),
            "p_value": float(p_value),
        }

    def summary(self) -> list[dict]:
        """Relatório agregado por (dataset, candidato, juiz)."""
        return self.avaliacao_repo.summary_by_dataset_candidate_judge()

    def list_judges(self) -> list[str]:
        """Lista juízes que já têm avaliações registradas no banco."""
        return self.avaliacao_repo.list_distinct_judges()
