import csv
import io
import requests
from abc import ABC, abstractmethod
from src.services.datasets.loader_factory import DatasetLoaderFactory
from src.repositories.dataset_repository import DatasetRepository
from src.repositories.categoria_repository import CategoriaRepository


class BaseExtractor(ABC):
    """
    Classe base responsável por fornecer os métodos de extração de dados
    e leitura de arquivos (como JSON) a partir de repositórios do GitHub.
    """

    def __init__(self):
        super().__init__()
        self.dataset_loader = DatasetLoaderFactory()
        self.dataset_repo = DatasetRepository()
        self.categoria_repo = CategoriaRepository()

    def fetch_json(self, raw_url: str) -> dict | list:
        """
        Faz o download de um arquivo JSON a partir de uma URL RAW e
        retorna o objeto (dict ou list) carregado.
        """
        try:
            response = requests.get(raw_url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao buscar o JSON na URL '{raw_url}': {e}")
            raise e

    def fetch_csv_to_dict(self, raw_url: str) -> list[dict]:
        """
        Faz o download de um arquivo CSV a partir de uma URL RAW e
        retorna uma lista de dicionários.
        """
        try:
            response = requests.get(raw_url)
            response.raise_for_status()

            # Decode the response content to string, handling common encodings
            # Some files might be latin-1 or utf-8 with BOM
            response.encoding = response.apparent_encoding or "utf-8"
            content = response.text

            csv_file = io.StringIO(content)
            # Use a semicolon separator if comma is not found
            # DictReader will map the first row to dictionary keys
            reader = csv.DictReader(csv_file)

            return list(reader)
        except Exception as e:
            print(f"Erro ao buscar o CSV na URL '{raw_url}': {e}")
            raise e

    @abstractmethod
    def extract_questions(self) -> list:
        """
        Método a ser implementado pelas classes filhas para extrair as
        perguntas específicas de cada repositório.
        """
        pass

    def find_dataset_id(self, dataset_name: str) -> int:
        dataset_name = dataset_name.strip()
        dataset = self.dataset_repo.get_by_name(dataset_name)
        if dataset:
            return dataset["id_dataset"]
        raise ValueError(f"Dataset '{dataset_name}' não encontrado no banco de dados.")

    def find_category_id(self, category_name: str) -> int:
        category_name = category_name.strip()
        category = self.categoria_repo.get_by_name(category_name)
        if category:
            return category["id_categoria"]
        raise ValueError(
            f"Categoria '{category_name}' não encontrada no banco de dados."
        )
