from abc import ABC, abstractmethod
from typing import Any, Dict, List


class DatasetLoader(ABC):
    """
    Contrato base para carregadores de datasets da OAB.
    """

    @abstractmethod
    def load_questions(
        self, slice_start: int | None = None, slice_end: int | None = None
    ) -> List[Dict[str, Any]]:
        """Carrega e retorna a lista de questões do dataset."""
        ...

    @abstractmethod
    def load_references(
        self, slice_start: int | None = None, slice_end: int | None = None
    ) -> List[Dict[str, Any]]:
        """
        Carrega e retorna respostas de referência / gabaritos.

        Deve retornar lista vazia caso o dataset não possua referências.
        """
        ...
