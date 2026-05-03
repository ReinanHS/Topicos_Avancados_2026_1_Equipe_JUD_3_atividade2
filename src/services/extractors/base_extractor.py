import json
import urllib.request
from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """
    Classe base responsável por fornecer os métodos de extração de dados
    e leitura de arquivos (como JSON) a partir de repositórios do GitHub.
    """

    def fetch_json(self, raw_url: str) -> dict | list:
        """
        Faz o download de um arquivo JSON a partir de uma URL RAW e
        retorna o objeto (dict ou list) carregado.
        """
        try:
            with urllib.request.urlopen(raw_url) as response:
                if response.status == 200:
                    data = response.read()
                    return json.loads(data)
                else:
                    raise Exception(f"Erro HTTP {response.status} ao acessar {raw_url}")
        except Exception as e:
            print(f"Erro ao buscar o JSON na URL '{raw_url}': {e}")
            raise e

    @abstractmethod
    def extract_perguntas(self) -> list:
        """
        Método a ser implementado pelas classes filhas para extrair as
        perguntas específicas de cada repositório.
        """
        pass
