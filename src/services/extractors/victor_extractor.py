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

    def extract_questions(self) -> list:
        """
        Extrai as perguntas de todos os datasets suportados.
        """
        questions = []
        questions.extend(self.extract_questions_oab_bench())
        questions.extend(self.extract_questions_oab_exams())
        return questions

    def find_curatorship_by_question_id(
        self, question_id: str, data_curatorship: dict, id_field: str = "question_id"
    ) -> dict:
        for item in data_curatorship:
            if item.get(id_field) == question_id:
                return item
        return None

    def _process_dataset_questions(
        self,
        dataset_name: str,
        slice_start: int,
        slice_end: int,
        question_id_field: str,
        statement_field: str,
        tipo_pergunta: str,
        extract_metadados: callable,
    ) -> list:
        """
        Método genérico para processar e extrair perguntas de um determinado dataset.
        """
        print(f"[{self.__class__.__name__}] Processando dataset: {dataset_name}")

        dataset_name_url = "J1_inferencia_Victor_ANALITICA"
        if "oab_exams" in dataset_name:
            dataset_name_url = "J2_curadoria_Victor_FINAL"

        url = f"{self.base_raw_url}/{dataset_name_url}.csv"
        data_curatorship = self.fetch_csv_to_dict(url)

        dataset = self.dataset_loader.create(dataset_name)
        questions_data = dataset.load_questions(
            slice_start=slice_start, slice_end=slice_end
        )
        dataset_id = self.find_dataset_id(dataset_name)

        data = []

        for question in questions_data:
            question_id = str(question[question_id_field])
            curatorship = self.find_curatorship_by_question_id(
                question_id, data_curatorship, id_field=question_id_field
            )

            if not curatorship:
                continue

            subdominio = curatorship["Subdominio_Semantico"].replace(
                "Subdomínio: ", " "
            )
            subdominios = subdominio.split(" e ")

            category_id = self.find_category_id(subdominios[0].strip())
            match curatorship["Complexidade_Raciocinio_LLM"]:
                case "Hermenêutica Jurídica Complexa":
                    difficulty = 3
                case "Recuperação Factual Direta":
                    difficulty = 2
                case "Raciocínio Lógico-Dedutivo":
                    difficulty = 1

            data.append(
                {
                    "id_dataset": dataset_id,
                    "id_categoria": category_id,
                    "id_externo": question_id,
                    "tipo_pergunta": tipo_pergunta,
                    "enunciado": question[statement_field],
                    "nivel_dificuldade": f"Nivel {difficulty}",
                    "legislacao_basica": curatorship["Corpus_Aterramento"]
                    .replace("Corpus: ", "")
                    .strip(),
                    "metadados": extract_metadados(question),
                }
            )

        return data

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
        )

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
