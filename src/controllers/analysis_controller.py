from itertools import combinations

from src.services.analysis import SpearmanAnalysisService


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
        print("\nAnálise concluída.")
