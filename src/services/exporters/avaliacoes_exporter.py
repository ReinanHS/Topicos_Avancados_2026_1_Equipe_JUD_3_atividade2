"""
Serviço de export/import das avaliações do juiz em JSON portável.

Objetivo: permitir que um membro da equipe rode o pipeline LLM-as-a-Judge,
exporte os resultados para um arquivo no repositório e que os demais
membros importem sem precisar pagar a API novamente.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from src.repositories import (
    AvaliacaoRepository,
    DatasetRepository,
    ModeloRepository,
    PerguntaRepository,
    RespostaRepository,
)


class AvaliacoesExporter:
    EXPORT_DIR = Path("Atividade_2/exports")
    VERSION = 1

    def __init__(self):
        self.avaliacao_repo = AvaliacaoRepository()
        self.dataset_repo = DatasetRepository()
        self.modelo_repo = ModeloRepository()
        self.pergunta_repo = PerguntaRepository()
        self.resposta_repo = RespostaRepository()

    @staticmethod
    def slugify(name: str) -> str:
        """Converte 'GPT-4o mini' em 'gpt-4o-mini' para nome de arquivo."""
        return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

    def default_path_for(self, judge_db_model_name: str) -> Path:
        return self.EXPORT_DIR / f"avaliacoes-{self.slugify(judge_db_model_name)}.json"

    def export(
        self,
        judge_db_model_name: str,
        judge_spec: str | None = None,
        output_path: Path | None = None,
    ) -> Path:
        """
        Exporta todas as avaliações do juiz para um JSON portável.
        Retorna o caminho do arquivo gerado.
        """
        evaluations = self.avaliacao_repo.fetch_for_export(judge_db_model_name)

        payload = {
            "version": self.VERSION,
            "judge": {
                "spec": judge_spec,
                "db_model_name": judge_db_model_name,
            },
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "count": len(evaluations),
            "evaluations": evaluations,
        }

        destination = output_path or self.default_path_for(judge_db_model_name)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return destination

    def _resolve_ids(self, entry: dict) -> tuple[int, int] | None:
        """
        Resolve (id_resposta, id_modelo_juiz) — None se algum lookup falhar.
        O caller decide o que fazer com o None (reportar como erro / pular).
        """
        dataset = self.dataset_repo.get_by_name(entry["dataset"])
        if not dataset:
            raise LookupError(f"dataset '{entry['dataset']}' não existe no banco")

        id_pergunta = self.pergunta_repo.get_id(
            entry["id_externo_pergunta"], dataset["id_dataset"]
        )
        if not id_pergunta:
            raise LookupError(
                f"pergunta '{entry['id_externo_pergunta']}' não encontrada no dataset "
                f"'{entry['dataset']}'"
            )

        modelo_candidato = self.modelo_repo.get_by_name(entry["candidato"])
        if not modelo_candidato:
            raise LookupError(f"modelo candidato '{entry['candidato']}' não existe")

        id_resposta = self.resposta_repo.find_id(
            id_pergunta, modelo_candidato["id_modelo"]
        )
        if not id_resposta:
            raise LookupError(
                f"resposta do modelo '{entry['candidato']}' à pergunta "
                f"'{entry['id_externo_pergunta']}' não encontrada"
            )

        return id_resposta

    def import_file(self, input_path: Path) -> dict:
        """
        Importa as avaliações de um arquivo JSON. Idempotente:
        avaliações já existentes (par único resposta+juiz) são puladas.

        Retorna: {"imported": int, "skipped": int, "errors": list[str]}
        """
        raw = input_path.read_text(encoding="utf-8")
        payload = json.loads(raw)

        if payload.get("version") != self.VERSION:
            raise ValueError(
                f"Versão {payload.get('version')} incompatível "
                f"(esperado {self.VERSION}) em {input_path}"
            )

        judge_name = payload["judge"]["db_model_name"]
        modelo_juiz = self.modelo_repo.get_by_name(judge_name)
        if not modelo_juiz:
            raise LookupError(
                f"Juiz '{judge_name}' não existe no banco. "
                f"Rode `db seed modelos` antes de importar."
            )
        id_modelo_juiz = modelo_juiz["id_modelo"]

        evaluations = payload.get("evaluations", [])
        imported = 0
        skipped = 0
        errors: list[str] = []

        for idx, entry in enumerate(evaluations, start=1):
            try:
                id_resposta = self._resolve_ids(entry)
                if self.avaliacao_repo.exists(id_resposta, id_modelo_juiz):
                    skipped += 1
                    continue
                self.avaliacao_repo.create(
                    id_resposta_ativa1=id_resposta,
                    id_modelo_juiz=id_modelo_juiz,
                    nota_atribuida=entry["nota"],
                    chain_of_thought=entry["chain_of_thought"],
                )
                imported += 1
            except Exception as e:
                errors.append(f"#{idx} ({entry.get('id_externo_pergunta')}): {e}")

        return {"imported": imported, "skipped": skipped, "errors": errors}
