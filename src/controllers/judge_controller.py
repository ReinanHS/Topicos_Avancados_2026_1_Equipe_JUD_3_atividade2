from pathlib import Path

from src.repositories import AvaliacaoRepository, ModeloRepository
from src.services.exporters import AvaliacoesExporter
from src.services.judges import BaseJudge, JudgeFactory
from src.services.judges.parser import parse_verdict
from src.services.judges.prompts import build_prompt


class JudgeController:
    """
    Controller responsável por orquestrar o pipeline LLM-as-a-Judge:
    para cada juiz informado, busca as respostas pendentes, gera o prompt,
    chama o modelo, parseia o veredito e persiste a avaliação.
    """

    def __init__(self):
        self.avaliacao_repo = AvaliacaoRepository()
        self.modelo_repo = ModeloRepository()
        self.exporter = AvaliacoesExporter()

    def _resolve_judge_model_id(self, judge: BaseJudge) -> int:
        """Resolve o id_modelo do juiz no banco a partir do nome registrado."""
        modelo = self.modelo_repo.get_by_name(judge.db_model_name)
        if not modelo:
            raise RuntimeError(
                f"Modelo juiz '{judge.db_model_name}' não encontrado no banco. "
                f"Rode `app db seed modelos` antes de avaliar."
            )
        return modelo["id_modelo"]

    def _evaluate_one(
        self, judge: BaseJudge, id_modelo_juiz: int, item: dict
    ) -> tuple[bool, str | None]:
        """
        Avalia uma única resposta. Devolve (sucesso, erro).
        Encapsula o try/except para que falhas isoladas não derrubem o lote.
        """
        try:
            prompt = build_prompt(item, item["texto_resposta"])
            raw_output = judge.complete(prompt)
            nota, chain_of_thought = parse_verdict(raw_output)
            self.avaliacao_repo.create(
                id_resposta_ativa1=item["id_resposta"],
                id_modelo_juiz=id_modelo_juiz,
                nota_atribuida=nota,
                chain_of_thought=chain_of_thought,
            )
            return True, None
        except Exception as e:
            return False, str(e)

    def _evaluate_with_judge(self, judge: BaseJudge, limit: int | None) -> None:
        """Executa o pipeline para um único juiz."""
        print(f"\n=== Juiz: {judge.name} (modelo no banco: {judge.db_model_name}) ===")

        id_modelo_juiz = self._resolve_judge_model_id(judge)
        pendentes = self.avaliacao_repo.list_pending(id_modelo_juiz, limit=limit)
        total = len(pendentes)

        if total == 0:
            print("Nenhuma resposta pendente para este juiz.")
            return

        print(f"Respostas pendentes: {total}")
        sucesso = 0
        falhas = 0

        for idx, item in enumerate(pendentes, start=1):
            ok, err = self._evaluate_one(judge, id_modelo_juiz, item)
            if ok:
                sucesso += 1
                print(f"  [{idx}/{total}] OK  - resposta #{item['id_resposta']}")
            else:
                falhas += 1
                print(
                    f"  [{idx}/{total}] ERRO - resposta #{item['id_resposta']}: {err}"
                )

        print(f"Juiz {judge.name} concluído: {sucesso} sucesso(s), {falhas} falha(s).")

    def evaluate(self, judge_specs: list[str], limit: int | None = None) -> None:
        """
        Executa o pipeline para cada juiz da lista, em sequência.

        Cada juiz é instanciado de forma lazy (no início de seu turno), para que
        falhas de configuração de um (ex.: API key faltando) não bloqueiem os
        demais.
        """
        print(f"Iniciando avaliação com {len(judge_specs)} juiz(es).")

        for spec in judge_specs:
            try:
                judge = JudgeFactory.create(spec)
            except Exception as e:
                print(f"\n=== Juiz: {spec} ===\nFalha ao instanciar: {e}")
                continue

            try:
                self._evaluate_with_judge(judge, limit=limit)
            except Exception as e:
                print(f"Falha geral no juiz '{spec}': {e}")

        print("\nAvaliação finalizada.")

    def _export_one(
        self, spec: str | None, db_model_name: str, output: Path | None
    ) -> None:
        path = self.exporter.export(
            judge_db_model_name=db_model_name,
            judge_spec=spec,
            output_path=output,
        )
        count = self.avaliacao_repo.fetch_for_export(db_model_name).__len__()
        print(f"Exportado: {path} ({count} avaliações)")

    def export(
        self,
        judge_spec: str | None,
        export_all: bool,
        output: Path | None,
    ) -> None:
        """
        Exporta avaliações para JSON. Se `export_all=True`, gera um arquivo
        por juiz registrado no banco; caso contrário, exporta apenas o juiz
        indicado em `judge_spec` (resolvido via JudgeFactory para encontrar
        o nome no banco).
        """
        if export_all:
            judges = self.avaliacao_repo.list_distinct_judges()
            if not judges:
                print("Nenhum juiz tem avaliações no banco — nada a exportar.")
                return
            for db_model_name in judges:
                self._export_one(spec=None, db_model_name=db_model_name, output=None)
            return

        if not judge_spec:
            raise ValueError("Informe --judge/-j ou use --all.")

        # Reusa o factory para mapear spec → nome do modelo no banco.
        db_model_name = JudgeFactory._db_model_map.get(judge_spec)
        if not db_model_name:
            available = ", ".join(JudgeFactory.available())
            raise ValueError(
                f"Spec '{judge_spec}' não está pré-configurada. "
                f"Disponíveis: {available}"
            )
        self._export_one(spec=judge_spec, db_model_name=db_model_name, output=output)

    def import_(self, input_path: Path) -> None:
        """Importa um arquivo de avaliações e imprime o resultado."""
        if not input_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")
        print(f"Importando {input_path}...")
        result = self.exporter.import_file(input_path)
        print(
            f"  importadas: {result['imported']} | "
            f"puladas (já existiam): {result['skipped']} | "
            f"erros: {len(result['errors'])}"
        )
        for err in result["errors"]:
            print(f"    - {err}")

    def import_all(self, directory: Path) -> None:
        """Importa todos os arquivos .json da pasta indicada."""
        if not directory.exists():
            print(f"Pasta não existe: {directory}")
            return
        files = sorted(directory.glob("avaliacoes-*.json"))
        if not files:
            print(f"Nenhum arquivo 'avaliacoes-*.json' em {directory}.")
            return
        for path in files:
            self.import_(path)
