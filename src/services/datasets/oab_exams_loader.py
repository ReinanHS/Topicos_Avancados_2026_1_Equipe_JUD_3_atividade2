from typing import Any, Dict, List

from src.services.datasets.base import DatasetLoader


class OABExamsLoader(DatasetLoader):
    """
    Carregador para o dataset eduagarcia/oab_exams.
    """

    DATASET_NAME = "eduagarcia/oab_exams"

    def load_questions(
        self, slice_start: int | None = None, slice_end: int | None = None
    ) -> List[Dict[str, Any]]:
        """Baixa as questões do oab_exams via HuggingFace e retorna o lote designado."""
        from datasets import load_dataset

        ds_exams = load_dataset(self.DATASET_NAME)
        questions = list(ds_exams["train"])
        return questions[slice_start:slice_end]

    def load_references(
        self, slice_start: int | None = None, slice_end: int | None = None
    ) -> List[Dict[str, Any]]:
        """
        O dataset oab_exams não possui respostas de referência separadas.
        O gabarito está embutido no campo `answerKey` de cada questão.
        """
        return []
