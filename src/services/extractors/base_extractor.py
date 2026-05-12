import csv
import io
import requests
from abc import ABC, abstractmethod
from src.services.datasets.loader_factory import DatasetLoaderFactory
from src.repositories.dataset_repository import DatasetRepository
from src.repositories.categoria_repository import CategoriaRepository
from src.repositories.pergunta_repository import PerguntaRepository
from src.repositories.modelo_repository import ModeloRepository


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
        self.pergunta_repo = PerguntaRepository()
        self.modelo_repo = ModeloRepository()
        self.dataset_range = {
            "oab_bench": {
                "slice_start": 0,
                "slice_end": 0,
            },
            "oab_exams": {
                "slice_start": 0,
                "slice_end": 0,
            },
        }

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

            response.encoding = response.apparent_encoding or "utf-8"
            content = response.text

            csv_file = io.StringIO(content)
            reader = csv.DictReader(csv_file)

            return list(reader)
        except Exception as e:
            print(f"Erro ao buscar o CSV na URL '{raw_url}': {e}")
            raise e

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

    @abstractmethod
    def get_curatorship_data(self, dataset_name: str) -> list[dict]:
        """Baixa e retorna os dados de curadoria do dataset específico."""
        pass

    @abstractmethod
    def parse_curatorship(self, curatorship: dict) -> dict:
        """
        Analisa o dicionário de curadoria e retorna um dicionário padrão:
        {
            "category": str,
            "difficulty": int,
            "legislation": str
        }
        """
        pass

    def find_curatorship_by_question_id(
        self,
        question_id: str,
        data_curatorship: list[dict],
        id_field: str = "question_id",
    ) -> dict:
        for item in data_curatorship:
            if item.get(id_field) == question_id:
                return item
        return None

    def _build_ref_map(
        self,
        dataset,
        dataset_name: str,
        slice_start: int,
        slice_end: int,
        question_id_field: str,
        extract_resposta_ouro: callable,
    ) -> dict:
        """
        Constrói um mapa {question_id: resposta_ouro} a partir das referências do dataset.
        """
        ref_map = {}

        if not hasattr(dataset, "load_references"):
            return ref_map

        references = dataset.load_references(
            slice_start=slice_start, slice_end=slice_end
        )

        for ref in references:
            qid = str(ref.get(question_id_field) or ref.get("id"))
            ref_map[qid] = extract_resposta_ouro(ref)

        return ref_map

    def _process_dataset_questions(
        self,
        dataset_name: str,
        slice_start: int,
        slice_end: int,
        question_id_field: str,
        statement_field: str,
        tipo_pergunta: str,
        extract_metadados: callable,
        extract_resposta_ouro: callable = None,
    ) -> list:
        """
        Método genérico para processar e extrair perguntas de um determinado dataset.
        """
        print(f"[{self.__class__.__name__}] Processando dataset: {dataset_name}")

        data_curatorship = self.get_curatorship_data(dataset_name)

        dataset = self.dataset_loader.create(dataset_name)
        questions_data = dataset.load_questions(
            slice_start=slice_start, slice_end=slice_end
        )
        dataset_id = self.find_dataset_id(dataset_name)

        ref_map = self._build_ref_map(
            dataset,
            dataset_name,
            slice_start,
            slice_end,
            question_id_field,
            extract_resposta_ouro or (lambda q: ""),
        )

        data = []

        for question in questions_data:
            question_id = str(question.get(question_id_field) or question.get("id"))
            curatorship = self.find_curatorship_by_question_id(
                question_id, data_curatorship, id_field=question_id_field
            )

            if not curatorship:
                continue

            parsed_curatorship = self.parse_curatorship(curatorship)
            category_id = self.find_category_id(parsed_curatorship["category"])
            difficulty = parsed_curatorship["difficulty"]

            resposta_ouro = ref_map.get(question_id, "")
            if extract_resposta_ouro and not resposta_ouro:
                resposta_ouro = extract_resposta_ouro(question)

            data.append(
                {
                    "id_dataset": dataset_id,
                    "id_categoria": category_id,
                    "id_externo": question_id,
                    "tipo_pergunta": tipo_pergunta,
                    "enunciado": question[statement_field],
                    "resposta_ouro": resposta_ouro,
                    "nivel_dificuldade": f"Nivel {difficulty}",
                    "legislacao_basica": parsed_curatorship["legislation"],
                    "metadados": extract_metadados(question)
                    | {"source_file": self.__class__.__name__},
                }
            )

        return data

    @staticmethod
    def _extract_oab_bench_resposta_ouro(ref: dict) -> str:
        """Extrai a resposta ouro do OAB Bench juntando os turns das choices."""
        choices = ref.get("choices", [])
        if not choices:
            return ""
        turns = choices[0].get("turns", [])
        parts = []
        for t in turns:
            text = t if isinstance(t, str) else str(t)
            parts.append(text)
        return "\n\n".join(parts)

    def extract_questions_oab_bench(self) -> list:
        """
        Extrai as perguntas do OAB Bench.
        """
        return self._process_dataset_questions(
            dataset_name="oab_bench",
            slice_start=self.dataset_range["oab_bench"]["slice_start"],
            slice_end=self.dataset_range["oab_bench"]["slice_end"],
            question_id_field="question_id",
            statement_field="statement",
            tipo_pergunta="discursiva",
            extract_metadados=lambda q: {"values": q.get("values")},
            extract_resposta_ouro=self._extract_oab_bench_resposta_ouro,
        )

    def extract_questions_oab_exams(self) -> list:
        """
        Extrai as perguntas do OAB Exams.
        """
        return self._process_dataset_questions(
            dataset_name="oab_exams",
            slice_start=self.dataset_range["oab_exams"]["slice_start"],
            slice_end=self.dataset_range["oab_exams"]["slice_end"],
            question_id_field="question_id",
            statement_field="question",
            tipo_pergunta="multipla_escolha",
            extract_metadados=lambda q: {
                "question_number": q.get("question_number"),
                "exam_id": q.get("exam_id"),
                "exam_year": q.get("exam_year"),
                "question_type": q.get("question_type"),
                "nullified": q.get("nullified"),
                "answerKey": q.get("answerKey"),
            },
            extract_resposta_ouro=lambda q: str(q.get("answerKey", "")),
        )

    def extract_questions(self) -> list:
        """
        Extrai as perguntas de todos os datasets suportados.
        """
        questions = []
        questions.extend(self.extract_questions_oab_bench())
        questions.extend(self.extract_questions_oab_exams())
        return questions

    def get_db_model_name(self, raw_model_name: str) -> str:
        """
        Mapeia os nomes dos modelos nos arquivos JSON para os nomes dos modelos no banco de dados.
        """
        name = raw_model_name.lower().replace(":", "-")
        if "llama3.2" in name or "llama-3.2" in name:
            return "Llama 3.2"
        if "llama3.1" in name or "llama-3.1" in name:
            return "Llama 3.1"
        if "gemma2" in name or "gemma-2" in name:
            return "Gemma 2"
        if "qwen" in name:
            return "Qwen 2.5"
        if "mistral" in name:
            return "Mistral"
        if "deepseek" in name:
            return "DeepSeek-R1"
        return raw_model_name

    def extract_answers(self) -> list:
        """
        Extrai as respostas de todos os datasets suportados.
        Pode ser sobrescrito nas classes filhas.
        """
        return []
