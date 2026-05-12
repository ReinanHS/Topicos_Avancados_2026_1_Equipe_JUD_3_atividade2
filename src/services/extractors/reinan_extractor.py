from src.services.extractors.base_extractor import BaseExtractor


class ReinanExtractor(BaseExtractor):
    """
    Extrator específico para o repositório feito por ReinanHS.
    URL Base: https://github.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1
    """

    def __init__(self):
        super().__init__()
        self.base_raw_url = "https://raw.githubusercontent.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1/refs/heads/results-2"
        self.dataset_range = {
            "oab_bench": {
                "slice_start": 176,
                "slice_end": 188,
            },
            "oab_exams": {
                "slice_start": 1845,
                "slice_end": 1968,
            },
        }

    def get_curatorship_data(self, dataset_name: str) -> list[dict]:
        url = f"{self.base_raw_url}/results/{dataset_name}/model_curatorship/gpt-4o-mini.json"
        return self.fetch_json(url)

    def parse_curatorship(self, curatorship: dict) -> dict:
        category_text = curatorship["curatorship"]["area_expertise"]
        category_name = category_text.split(" e ")[0].strip()

        return {
            "category": category_name,
            "difficulty": curatorship["curatorship"]["difficulty_question"],
            "legislation": curatorship["curatorship"]["basic_legislation"],
        }

    def _process_item(
        self, item: dict, answer_parser: callable, dataset_id: int, id_modelo: int
    ) -> dict | None:
        parsed_text = answer_parser(item)
        if not parsed_text:
            return None

        id_externo = str(item.get("question_id") or item.get("id"))
        id_pergunta = self.pergunta_repo.get_id(id_externo, dataset_id)

        if id_pergunta and id_modelo:
            return {
                "id_pergunta": id_pergunta,
                "id_modelo": id_modelo,
                "texto_resposta": parsed_text,
                "tempo_inferencia_ms": None,
            }
        return None

    def _process_model_answers(
        self,
        model_filename: str,
        dataset_name: str,
        dataset_id: int,
        answer_parser: callable,
    ) -> list:
        """Busca e processa as respostas de um único modelo."""
        db_model_name = self.get_db_model_name(model_filename)
        model_data = self.modelo_repo.get_by_name(db_model_name)
        id_modelo = model_data["id_modelo"] if model_data else None

        url = f"{self.base_raw_url}/results/{dataset_name}/model_answer/{model_filename}.json"
        results = []
        try:
            data = self.fetch_json(url)
            for item in data:
                processed = self._process_item(
                    item, answer_parser, dataset_id, id_modelo
                )
                if processed:
                    results.append(processed)
        except Exception as e:
            print(
                f"Aviso: Não foi possível processar respostas de {model_filename} para {dataset_name}: {e}"
            )
        return results

    def _process_dataset_answers(
        self, dataset_name: str, answer_parser: callable
    ) -> list:
        print(
            f"[{self.__class__.__name__}] Extraindo respostas do dataset: {dataset_name}"
        )
        dataset_id = self.find_dataset_id(dataset_name)

        models_filenames = [
            "gemma2-2b",
            "llama3.2-3b",
            "qwen2.5-3b",
        ]

        answers = []
        for model_filename in models_filenames:
            answers.extend(
                self._process_model_answers(
                    model_filename, dataset_name, dataset_id, answer_parser
                )
            )

        return answers

    def extract_answers_oab_bench(self) -> list:
        def parser(item):
            choices = item.get("choices", [])
            if not choices:
                return ""
            turns = choices[0].get("turns", [])
            return "\n\n".join([t.get("content", "") for t in turns])

        return self._process_dataset_answers("oab_bench", parser)

    def extract_answers_oab_exams(self) -> list:
        def parser(item):
            choices = item.get("choices", [])
            if not choices:
                return ""

            objective_answer = str(choices[0].get("objective_answer", ""))
            justification = str(choices[0].get("justification", ""))

            return f"Resposta: {objective_answer}\nJustificativa: {justification}"

        return self._process_dataset_answers("oab_exams", parser)

    def extract_answers(self) -> list:
        answers = []
        answers.extend(self.extract_answers_oab_bench())
        answers.extend(self.extract_answers_oab_exams())
        return answers
