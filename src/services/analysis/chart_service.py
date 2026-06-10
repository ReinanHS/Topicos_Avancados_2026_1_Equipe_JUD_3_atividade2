"""
Geração de gráficos do comparativo SEM RAG × COM RAG.

Consome o resultado de `SpearmanAnalysisService.rag_comparison()` e produz
arquivos PNG prontos para colar no relatório:

- Um gráfico por juiz com barras agrupadas (nota média sem/com RAG por
  dataset+candidato) e barras de ganho ao lado.
- Um gráfico consolidado com a média ponderada geral sem/com RAG por juiz.

Usa o backend "Agg" (não interativo) para funcionar em ambiente headless.
"""

import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.services.analysis import SpearmanAnalysisService

SEM_RAG_COLOR = "#6c8ebf"
COM_RAG_COLOR = "#82b366"
GANHO_POS_COLOR = "#82b366"
GANHO_NEG_COLOR = "#b85450"


class ChartService:
    """Gera os gráficos do comparativo RAG a partir dos dados do banco."""

    OUTPUT_DIR = Path("database/charts")

    def __init__(self):
        self.service = SpearmanAnalysisService()

    @staticmethod
    def _slugify(name: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

    @staticmethod
    def _group_by_judge(rows: list[dict]) -> dict[str, list[dict]]:
        grupos: dict[str, list[dict]] = {}
        for row in rows:
            grupos.setdefault(row["juiz"], []).append(row)
        return grupos

    def _plot_judge(
        self,
        judge: str,
        rows: list[dict],
        output_dir: Path,
        prefix: str = "",
        label: str = "",
    ) -> Path:
        """Gera o gráfico (média agrupada + ganho) de um único juiz."""
        # Ordena por dataset/candidato para um eixo estável e legível.
        rows = sorted(rows, key=lambda r: (r["dataset"], r["candidato"]))
        labels = [f"{r['dataset']}\n{r['candidato']}" for r in rows]

        def media(bucket: str, r: dict) -> float:
            b = r[bucket]
            return b["media"] if b and b["media"] is not None else 0.0

        medias_sem = [media("sem_rag", r) for r in rows]
        medias_com = [media("com_rag", r) for r in rows]
        ganhos = [r["ganho"] if r["ganho"] is not None else 0.0 for r in rows]

        x = range(len(rows))
        largura = 0.38

        fig, (ax_media, ax_ganho) = plt.subplots(
            1, 2, figsize=(max(10, len(rows) * 1.6), 6), width_ratios=[2, 1]
        )

        # --- Barras agrupadas: média sem/com RAG ---
        barras_sem = ax_media.bar(
            [i - largura / 2 for i in x],
            medias_sem,
            largura,
            label="Sem RAG",
            color=SEM_RAG_COLOR,
        )
        barras_com = ax_media.bar(
            [i + largura / 2 for i in x],
            medias_com,
            largura,
            label="Com RAG",
            color=COM_RAG_COLOR,
        )
        ax_media.bar_label(barras_sem, fmt="%.2f", padding=2, fontsize=8)
        ax_media.bar_label(barras_com, fmt="%.2f", padding=2, fontsize=8)
        sufixo = f" ({label})" if label else ""
        ax_media.set_title(f"Nota média do juiz — {judge}{sufixo}")
        ax_media.set_ylabel("Nota média (1–5)")
        ax_media.set_ylim(0, 5.5)
        ax_media.set_xticks(list(x))
        ax_media.set_xticklabels(labels, fontsize=8)
        ax_media.legend()
        ax_media.grid(axis="y", linestyle=":", alpha=0.5)

        # --- Barras de ganho (com RAG − sem RAG) ---
        cores = [GANHO_POS_COLOR if g >= 0 else GANHO_NEG_COLOR for g in ganhos]
        barras_ganho = ax_ganho.barh(list(x), ganhos, color=cores)
        ax_ganho.bar_label(barras_ganho, fmt="%+.2f", padding=3, fontsize=8)
        ax_ganho.set_title("Ganho com RAG")
        ax_ganho.set_xlabel("Δ nota média")
        ax_ganho.set_yticks(list(x))
        ax_ganho.set_yticklabels(labels, fontsize=8)
        ax_ganho.axvline(0, color="#333333", linewidth=0.8)
        ax_ganho.grid(axis="x", linestyle=":", alpha=0.5)

        fig.tight_layout()
        destino = output_dir / f"{prefix}comparativo-rag-{self._slugify(judge)}.png"
        fig.savefig(destino, dpi=130)
        plt.close(fig)
        return destino

    def _plot_overall(
        self, rows: list[dict], output_dir: Path, prefix: str = "", label: str = ""
    ) -> Path:
        """Gráfico consolidado: média ponderada geral sem/com RAG por juiz."""
        grupos = self._group_by_judge(rows)

        def weighted(bucket: str, judge_rows: list[dict]) -> float:
            soma, n = 0.0, 0
            for r in judge_rows:
                b = r[bucket]
                if b and b["media"] is not None:
                    soma += b["media"] * b["total"]
                    n += b["total"]
            return soma / n if n else 0.0

        juizes = sorted(grupos.keys())
        medias_sem = [weighted("sem_rag", grupos[j]) for j in juizes]
        medias_com = [weighted("com_rag", grupos[j]) for j in juizes]

        x = range(len(juizes))
        largura = 0.38

        fig, ax = plt.subplots(figsize=(max(7, len(juizes) * 2), 5.5))
        barras_sem = ax.bar(
            [i - largura / 2 for i in x],
            medias_sem,
            largura,
            label="Sem RAG",
            color=SEM_RAG_COLOR,
        )
        barras_com = ax.bar(
            [i + largura / 2 for i in x],
            medias_com,
            largura,
            label="Com RAG",
            color=COM_RAG_COLOR,
        )
        ax.bar_label(barras_sem, fmt="%.2f", padding=2, fontsize=9)
        ax.bar_label(barras_com, fmt="%.2f", padding=2, fontsize=9)
        sufixo = f" ({label})" if label else ""
        ax.set_title(f"Nota média geral (ponderada) — Sem RAG × Com RAG{sufixo}")
        ax.set_ylabel("Nota média (1–5)")
        ax.set_ylim(0, 5.5)
        ax.set_xticks(list(x))
        ax.set_xticklabels(juizes)
        ax.legend()
        ax.grid(axis="y", linestyle=":", alpha=0.5)

        fig.tight_layout()
        destino = output_dir / f"{prefix}comparativo-rag-geral.png"
        fig.savefig(destino, dpi=130)
        plt.close(fig)
        return destino

    def generate(
        self,
        output_dir: Path | None = None,
        source_file: str | None = None,
        owner: str | None = None,
    ) -> list[Path]:
        """
        Gera todos os gráficos do comparativo RAG e retorna os caminhos criados.
        Retorna lista vazia se não houver dados no banco.

        `source_file` (opcional) restringe às perguntas de um aluno; `owner`
        é usado apenas para nomear/rotular os arquivos quando há filtro.
        """
        rows = self.service.rag_comparison(source_file)
        if not rows:
            return []

        destino = output_dir or self.OUTPUT_DIR
        destino.mkdir(parents=True, exist_ok=True)

        prefix = f"{owner}-" if owner else ""
        label = owner or ""

        gerados: list[Path] = []
        for judge, judge_rows in self._group_by_judge(rows).items():
            gerados.append(self._plot_judge(judge, judge_rows, destino, prefix, label))
        gerados.append(self._plot_overall(rows, destino, prefix, label))
        return gerados
