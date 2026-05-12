"""
Serviço de export/import dos dados extraídos da Atividade 1 — `perguntas`
e `respostas_atividade_1` — em JSON portável.

Permite que um membro da equipe execute os extractors uma única vez (lento,
HTTP-bound) e os demais importem o resultado já compilado a partir do
repositório, sem refazer chamadas a GitHub.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from src.repositories import (
    CategoriaRepository,
    DatasetRepository,
    ModeloRepository,
    PerguntaRepository,
    RespostaRepository,
)


class ExtracaoExporter:
    EXPORT_DIR = Path("Atividade_2/exports")
    VERSION = 1
    PERGUNTAS_FILENAME = "extracao-perguntas.json"
    RESPOSTAS_FILENAME = "extracao-respostas.json"

    def __init__(self):
        self.pergunta_repo = PerguntaRepository()
        self.resposta_repo = RespostaRepository()
        self.dataset_repo = DatasetRepository()
        self.categoria_repo = CategoriaRepository()
        self.modelo_repo = ModeloRepository()

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat(timespec="seconds")

    @staticmethod
    def _write_json(path: Path, payload: dict) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return path

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_perguntas(self, output_path: Path | None = None) -> Path:
        perguntas = self.pergunta_repo.fetch_for_export()
        payload = {
            "version": self.VERSION,
            "type": "perguntas",
            "generated_at": self._now_iso(),
            "count": len(perguntas),
            "perguntas": perguntas,
        }
        destination = output_path or (self.EXPORT_DIR / self.PERGUNTAS_FILENAME)
        return self._write_json(destination, payload)

    def export_respostas(self, output_path: Path | None = None) -> Path:
        respostas = self.resposta_repo.fetch_for_export()
        payload = {
            "version": self.VERSION,
            "type": "respostas",
            "generated_at": self._now_iso(),
            "count": len(respostas),
            "respostas": respostas,
        }
        destination = output_path or (self.EXPORT_DIR / self.RESPOSTAS_FILENAME)
        return self._write_json(destination, payload)

    # ------------------------------------------------------------------
    # Import
    # ------------------------------------------------------------------

    def _load_and_validate(self, input_path: Path, expected_type: str) -> dict:
        raw = input_path.read_text(encoding="utf-8")
        payload = json.loads(raw)

        if payload.get("version") != self.VERSION:
            raise ValueError(
                f"Versão {payload.get('version')} incompatível "
                f"(esperado {self.VERSION}) em {input_path}"
            )
        if payload.get("type") != expected_type:
            raise ValueError(
                f"Tipo '{payload.get('type')}' não bate com o esperado "
                f"'{expected_type}' em {input_path}"
            )
        return payload

    def _resolve_dataset(self, name: str) -> dict:
        dataset = self.dataset_repo.get_by_name(name)
        if not dataset:
            raise LookupError(f"dataset '{name}' não existe")
        return dataset

    def _resolve_categoria(self, name: str) -> dict:
        categoria = self.categoria_repo.get_by_name(name)
        if not categoria:
            raise LookupError(f"categoria '{name}' não existe")
        return categoria

    def _resolve_modelo(self, name: str) -> dict:
        modelo = self.modelo_repo.get_by_name(name)
        if not modelo:
            raise LookupError(f"modelo '{name}' não existe")
        return modelo

    def _import_single_pergunta(self, entry: dict) -> str:
        """Processa uma única pergunta. Retorna 'imported' ou 'skipped'."""
        dataset = self._resolve_dataset(entry["dataset"])
        categoria = self._resolve_categoria(entry["categoria"])

        id_dataset = dataset["id_dataset"]
        if self.pergunta_repo.get_id(entry["id_externo"], id_dataset):
            return "skipped"

        self.pergunta_repo.create(
            id_dataset=id_dataset,
            id_categoria=categoria["id_categoria"],
            id_externo=entry["id_externo"],
            tipo_pergunta=entry["tipo_pergunta"],
            enunciado=entry["enunciado"],
            nivel_dificuldade=entry["nivel_dificuldade"],
            legislacao_basica=entry.get("legislacao_basica"),
            metadados=entry.get("metadados"),
        )
        return "imported"

    def _import_single_resposta(self, entry: dict) -> str:
        """Processa uma única resposta. Retorna 'imported' ou 'skipped'."""
        dataset = self._resolve_dataset(entry["dataset"])
        modelo = self._resolve_modelo(entry["modelo"])

        id_pergunta = self.pergunta_repo.get_id(
            entry["id_externo_pergunta"], dataset["id_dataset"]
        )
        if not id_pergunta:
            raise LookupError(
                f"pergunta '{entry['id_externo_pergunta']}' não "
                f"encontrada em '{entry['dataset']}' (importe perguntas antes)"
            )

        if self.resposta_repo.exists(id_pergunta, modelo["id_modelo"]):
            return "skipped"

        self.resposta_repo.create(
            id_pergunta=id_pergunta,
            id_modelo=modelo["id_modelo"],
            texto_resposta=entry["texto_resposta"],
            tempo_inferencia_ms=entry.get("tempo_inferencia_ms"),
        )
        return "imported"

    def import_perguntas_file(self, input_path: Path) -> dict:
        """
        Importa perguntas de um arquivo JSON. Idempotente:
        `PerguntaRepository.create` já usa `ON CONFLICT DO NOTHING`.
        """
        payload = self._load_and_validate(input_path, "perguntas")
        items = payload.get("perguntas", [])
        imported = 0
        skipped = 0
        errors: list[str] = []

        for idx, entry in enumerate(items, start=1):
            try:
                status = self._import_single_pergunta(entry)
                imported += status == "imported"
                skipped += status == "skipped"
            except Exception as e:
                errors.append(f"#{idx} ({entry.get('id_externo')}): {e}")

        return {"imported": imported, "skipped": skipped, "errors": errors}

    def import_respostas_file(self, input_path: Path) -> dict:
        """
        Importa respostas de um arquivo JSON. Idempotente:
        `RespostaRepository.create` já tem `exists()` check interno.
        """
        payload = self._load_and_validate(input_path, "respostas")
        items = payload.get("respostas", [])
        imported = 0
        skipped = 0
        errors: list[str] = []

        for idx, entry in enumerate(items, start=1):
            try:
                status = self._import_single_resposta(entry)
                imported += status == "imported"
                skipped += status == "skipped"
            except Exception as e:
                errors.append(f"#{idx} ({entry.get('id_externo_pergunta')}): {e}")

        return {"imported": imported, "skipped": skipped, "errors": errors}
