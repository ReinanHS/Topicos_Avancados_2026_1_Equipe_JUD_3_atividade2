from src.services.extractors.base_extractor import BaseExtractor


class VictorExtractor(BaseExtractor):
    """
    Extrator específico para o repositório feito por Victor.
    URL Base: https://github.com/Leomascarenhas91/Topicos_Avancados_2026-1_Equipe_JUD_3_Victor_atividade1
    """

    def __init__(self):
        super().__init__()
        self.base_raw_url = "https://raw.githubusercontent.com/Leomascarenhas91/Topicos_Avancados_2026-1_Equipe_JUD_3_Victor_atividade1/refs/heads/main"
        self.dataset_range = {
            "oab_bench": {
                "slice_start": 200,
                "slice_end": 210,
            },
            "oab_exams": {
                "slice_start": 2091,
                "slice_end": 2210,
            },
        }

    def get_curatorship_data(self, dataset_name: str) -> list[dict]:
        dataset_name_url = "J1_inferencia_Victor_ANALITICA"
        if "oab_exams" in dataset_name:
            dataset_name_url = "J2_curadoria_Victor_FINAL"

        url = f"{self.base_raw_url}/{dataset_name_url}.csv"
        return self.fetch_csv_to_dict(url)

    def parse_curatorship(self, curatorship: dict) -> dict:
        subdominio = curatorship["Subdominio_Semantico"].replace("Subdomínio: ", " ")
        subdominios = subdominio.split(" e ")
        category_name = subdominios[0].strip()

        match curatorship["Complexidade_Raciocinio_LLM"]:
            case "Hermenêutica Jurídica Complexa":
                difficulty = 3
            case "Recuperação Factual Direta":
                difficulty = 2
            case "Raciocínio Lógico-Dedutivo":
                difficulty = 1
            case _:
                difficulty = 3

        legislation = curatorship["Corpus_Aterramento"].replace("Corpus: ", "").strip()

        return {
            "category": category_name,
            "difficulty": difficulty,
            "legislation": legislation,
        }

    def extract_questions_oab_exams(self) -> list:
        """
        Extrai as perguntas do OAB Exams.
        """
        return self._process_dataset_questions(
            dataset_name="oab_exams",
            slice_start=self.dataset_range["oab_exams"]["slice_start"],
            slice_end=self.dataset_range["oab_exams"]["slice_end"],
            question_id_field="id",
            statement_field="question",
            tipo_pergunta="multipla_escolha",
            extract_metadados=lambda q: {
                "question_number": q.get("question_number"),
                "exam_id": q.get("exam_id"),
                "exam_year": q.get("exam_year"),
                "question_type": q.get("question_type"),
                "nullified": q.get("nullified"),
            },
        )

    def get_answers_data(self, dataset_name: str) -> list[dict]:
        dataset_name_url = "J1_inferencia_Victor_ANALITICA"
        if "oab_exams" in dataset_name:
            dataset_name_url = "Resultados_J2_Inferencias"

        url = f"{self.base_raw_url}/{dataset_name_url}.csv"
        return self.fetch_csv_to_dict(url)

    def _process_item(
        self, item: dict, answer_parser: callable, dataset_id: int
    ) -> dict | None:
        parsed_text = answer_parser(item)
        if not parsed_text:
            return None

        id_externo = str(item.get("question_id") or item.get("id"))
        id_pergunta = self.pergunta_repo.get_id(id_externo, dataset_id)

        llama_model_data = self.modelo_repo.get_by_name("Llama 3.1")
        id_llama = llama_model_data["id_modelo"] if llama_model_data else None

        mistral_model_data = self.modelo_repo.get_by_name("Mistral")
        id_mistral = mistral_model_data["id_modelo"] if mistral_model_data else None

        deepseek_model_data = self.modelo_repo.get_by_name("DeepSeek-R1")
        id_deepseek = deepseek_model_data["id_modelo"] if deepseek_model_data else None

        if id_pergunta and id_llama and id_mistral and id_deepseek:
            return [
                {
                    "id_pergunta": id_pergunta,
                    "id_modelo": id_llama,
                    "texto_resposta": parsed_text["llama"],
                    "tempo_inferencia_ms": None,
                },
                {
                    "id_pergunta": id_pergunta,
                    "id_modelo": id_mistral,
                    "texto_resposta": parsed_text["mistral"],
                    "tempo_inferencia_ms": None,
                },
                {
                    "id_pergunta": id_pergunta,
                    "id_modelo": id_deepseek,
                    "texto_resposta": parsed_text["deepseek"],
                    "tempo_inferencia_ms": None,
                },
            ]
        return None

    def _process_dataset_answers(
        self, dataset_name: str, url_suffix: str, answer_parser: callable
    ) -> list:
        print(
            f"[{self.__class__.__name__}] Extraindo respostas do dataset: {dataset_name}"
        )
        dataset_id = self.find_dataset_id(dataset_name)
        answers = []
        try:
            data = self.get_answers_data(dataset_name)
            for item in data:
                processed = self._process_item(item, answer_parser, dataset_id)
                if processed:
                    answers.append(processed[0])
                    answers.append(processed[1])
                    answers.append(processed[2])
        except Exception as e:
            print(
                f"Aviso: Não foi possível processar {url_suffix} para {dataset_name}: {e}"
            )

        return answers

    def extract_answers_oab_bench(self) -> list:
        def parser(item):
            return {
                "llama": str(item.get("Resposta_Llama_3.1_8B", "")),
                "mistral": str(item.get("Resposta_Mistral_7B", "")),
                "deepseek": str(item.get("Resposta_DeepSeek_R1_8B", "")),
            }

        return self._process_dataset_answers(
            "oab_bench", "J1_inferencia_Victor_ANALITICA.csv", parser
        )

    def extract_answers_oab_exams(self) -> list:
        def parser(item):
            return {
                "llama": str(item.get("Resposta_llama3.1", "")),
                "mistral": str(item.get("Resposta_mistral", "")),
                "deepseek": str(item.get("Resposta_deepseek-r1:8b", "")),
            }

        return self._process_dataset_answers(
            "oab_exams", "Resultados_J2_Inferencias.csv", parser
        )

    def extract_answers(self) -> list:
        answers = []
        answers.extend(self.extract_answers_oab_bench())
        answers.extend(self.extract_answers_oab_exams())
        return answers
