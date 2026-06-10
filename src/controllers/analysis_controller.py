from itertools import combinations
from pathlib import Path

from src.controllers.seed_controller import EXTRACTORS
from src.services.analysis import ChartService, SpearmanAnalysisService

# owner (ex.: 'ericles') -> source_file gravado em perguntas.metadados
# (ex.: 'EriclesExtractor'). Mantém-se em sincronia com EXTRACTORS.
OWNER_TO_SOURCE_FILE = {owner: cls.__name__ for owner, cls in EXTRACTORS.items()}


def _resolve_source_file(owner: str | None) -> str | None:
    """Valida o --owner e devolve o source_file correspondente (ou None)."""
    if owner is None:
        return None
    owner = owner.strip().lower()
    if owner not in OWNER_TO_SOURCE_FILE:
        raise ValueError(
            f"--owner inválido: '{owner}'. Use um de: "
            f"{', '.join(OWNER_TO_SOURCE_FILE)}."
        )
    return OWNER_TO_SOURCE_FILE[owner]


def _interpret_rho(rho: float | None) -> str:
    """Classifica a força da correlação conforme orientação do enunciado."""
    if rho is None:
        return "indefinida"
    if rho >= 0.7:
        return "forte alinhamento"
    if rho >= 0.3:
        return "alinhamento moderado"
    if rho >= 0:
        return "alinhamento fraco"
    return "discordância (correlação negativa)"


class AnalysisController:
    """
    Controller responsável por orquestrar a análise estatística sobre as
    avaliações do juiz (Spearman + estatísticas descritivas).
    """

    def __init__(self):
        self.service = SpearmanAnalysisService()
        self.chart_service = ChartService()

    def _print_summary(self) -> None:
        rows = self.service.summary()
        if not rows:
            print("Nenhuma avaliação encontrada no banco.")
            return

        print("\n=== Resumo por (dataset, candidato, juiz) ===")
        header = f"{'Dataset':<14} {'Candidato':<22} {'Juiz':<22} {'Média':>8} {'Desv.':>8} {'N':>6}"
        print(header)
        print("-" * len(header))
        for row in rows:
            media = "—" if row["media"] is None else f"{row['media']:.3f}"
            desvio = "—" if row["desvio"] is None else f"{row['desvio']:.3f}"
            print(
                f"{row['dataset']:<14} {row['candidato']:<22} {row['juiz']:<22} "
                f"{media:>8} {desvio:>8} {row['total']:>6}"
            )

    def _print_judge_vs_gold(self, judges: list[str]) -> None:
        print("\n=== Spearman: Juiz vs Gabarito Humano (múltipla escolha) ===")
        for judge in judges:
            result = self.service.judge_vs_gold(judge)
            rho = result.get("rho")
            if rho is None:
                print(
                    f"- {judge}: n={result['n']} | skipped(sem gabarito)="
                    f"{result['skipped_sem_gabarito']} | {result.get('motivo', '')}"
                )
                continue
            print(
                f"- {judge}: ρ = {rho:+.3f} | p = {result['p_value']:.4f} | "
                f"n = {result['n']} | skipped(sem gabarito) = "
                f"{result['skipped_sem_gabarito']} | {_interpret_rho(rho)}"
            )

    def _print_inter_judge(self, judges: list[str]) -> None:
        if len(judges) < 2:
            print("\n=== Correlação inter-juízes ===")
            print("Apenas 1 juiz no banco; correlação inter-juízes não se aplica.")
            return

        print("\n=== Spearman: Correlação inter-juízes ===")
        for judge_a, judge_b in combinations(judges, 2):
            result = self.service.inter_judge(judge_a, judge_b)
            rho = result.get("rho")
            if rho is None:
                print(
                    f"- {judge_a} × {judge_b}: n={result['n']} | "
                    f"{result.get('motivo', '')}"
                )
                continue
            print(
                f"- {judge_a} × {judge_b}: ρ = {rho:+.3f} | p = {result['p_value']:.4f} | "
                f"n = {result['n']} | {_interpret_rho(rho)}"
            )

    @staticmethod
    def _fmt(value: float | None, casas: int = 3) -> str:
        return "—" if value is None else f"{value:.{casas}f}"

    @staticmethod
    def _fmt_ganho(ganho: float | None) -> str:
        if ganho is None:
            return "-"
        seta = "^" if ganho > 0 else ("v" if ganho < 0 else "=")
        return f"{ganho:+.3f}{seta}"

    @staticmethod
    def _fmt_total(bucket: dict) -> str:
        return str(bucket.get("total")) if bucket else "—"

    def _print_rag_row(self, row: dict) -> None:
        sem = row["sem_rag"] or {}
        com = row["com_rag"] or {}
        print(
            f"{row['dataset']:<12} {row['candidato']:<20} {row['juiz']:<20} "
            f"{self._fmt(sem.get('media')):>12} {self._fmt(com.get('media')):>12} "
            f"{self._fmt_ganho(row['ganho']):>8} "
            f"{self._fmt_total(sem):>8} {self._fmt_total(com):>8}"
        )

    def _print_rag_comparison(
        self, source_file: str | None = None, owner: str | None = None
    ) -> None:
        rows = self.service.rag_comparison(source_file)
        escopo = f" — aluno: {owner}" if owner else ""
        if not rows:
            print(f"\n=== Comparativo SEM RAG × COM RAG{escopo} ===")
            filtro_msg = f" para o aluno '{owner}'" if owner else ""
            print(f"Nenhuma avaliação encontrada no banco{filtro_msg}.")
            return

        print(f"\n=== Comparativo SEM RAG × COM RAG (nota média do juiz){escopo} ===")
        header = (
            f"{'Dataset':<12} {'Candidato':<20} {'Juiz':<20} "
            f"{'Média s/RAG':>12} {'Média c/RAG':>12} {'Ganho':>8} "
            f"{'N s/RAG':>8} {'N c/RAG':>8}"
        )
        print(header)
        print("-" * len(header))
        for row in rows:
            self._print_rag_row(row)

        self._print_rag_overall(rows)

    def _print_rag_overall(self, rows: list[dict]) -> None:
        """Média ponderada geral sem/com RAG (visão consolidada)."""

        def weighted(bucket: str) -> tuple[float | None, int]:
            soma, n = 0.0, 0
            for row in rows:
                b = row[bucket]
                if b and b["media"] is not None:
                    soma += b["media"] * b["total"]
                    n += b["total"]
            return (soma / n if n else None, n)

        media_sem, n_sem = weighted("sem_rag")
        media_com, n_com = weighted("com_rag")
        print("-" * 12)
        print(
            f"GERAL (média ponderada): s/RAG = {self._fmt(media_sem)} (n={n_sem}) | "
            f"c/RAG = {self._fmt(media_com)} (n={n_com}) | "
            f"ganho = {self._fmt((media_com - media_sem) if (media_sem is not None and media_com is not None) else None)}"
        )

    def _print_judge_vs_gold_by_rag(
        self,
        judges: list[str],
        source_file: str | None = None,
        owner: str | None = None,
    ) -> None:
        escopo = f" — aluno: {owner}" if owner else ""
        print(
            f"\n=== Spearman: Juiz vs Gabarito Humano — SEM RAG × COM RAG{escopo} ==="
        )
        for judge in judges:
            result = self.service.judge_vs_gold_by_rag(judge, source_file)
            for label, key in (("s/RAG", "sem_rag"), ("c/RAG", "com_rag")):
                cenario = result[key]
                rho = cenario.get("rho")
                if rho is None:
                    print(
                        f"- {judge} [{label}]: n={cenario['n']} | "
                        f"skipped(sem gabarito)={cenario['skipped_sem_gabarito']} | "
                        f"{cenario.get('motivo', '')}"
                    )
                    continue
                print(
                    f"- {judge} [{label}]: rho = {rho:+.3f} | p = {cenario['p_value']:.4f} | "
                    f"n = {cenario['n']} | {_interpret_rho(rho)}"
                )

    def generate_charts(
        self, output: Path | None = None, owner: str | None = None
    ) -> None:
        """Gera os gráficos PNG do comparativo sem RAG × com RAG."""
        source_file = _resolve_source_file(owner)
        escopo = f" (aluno: {owner})" if owner else ""
        print(f"\n=== Gerando gráficos do comparativo RAG{escopo} ===")
        paths = self.chart_service.generate(
            output_dir=output, source_file=source_file, owner=owner
        )
        if not paths:
            filtro_msg = f" para o aluno '{owner}'" if owner else ""
            print(f"Nenhuma avaliação encontrada no banco{filtro_msg} — nada a plotar.")
            return
        for path in paths:
            print(f"  - {path}")
        print(f"{len(paths)} gráfico(s) gerado(s).")

    def run_rag(
        self,
        charts: bool = False,
        output: Path | None = None,
        owner: str | None = None,
    ) -> None:
        """Executa somente o comparativo sem RAG × com RAG."""
        source_file = _resolve_source_file(owner)
        judges = self.service.list_judges()
        if not judges:
            print("Nenhuma avaliação encontrada. Rode `db judge evaluate` antes.")
            return
        print(f"Juízes com avaliações no banco: {', '.join(judges)}")
        self._print_rag_comparison(source_file, owner)
        self._print_judge_vs_gold_by_rag(judges, source_file, owner)
        if charts:
            self.generate_charts(output, owner)
        print("\nComparativo RAG concluído.")

    def run(self) -> None:
        """Executa todas as análises e imprime o relatório."""
        judges = self.service.list_judges()
        if not judges:
            print("Nenhuma avaliação encontrada. Rode `db judge evaluate` antes.")
            return

        print(f"Juízes com avaliações no banco: {', '.join(judges)}")
        self._print_summary()
        self._print_judge_vs_gold(judges)
        self._print_inter_judge(judges)
        self._print_rag_comparison()
        self._print_judge_vs_gold_by_rag(judges)
        print("\nAnálise concluída.")
