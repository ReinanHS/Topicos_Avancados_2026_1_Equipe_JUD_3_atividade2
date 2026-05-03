from src.services.extractors.base_extractor import BaseExtractor


class EclerkExtractor(BaseExtractor):
    """
    Extrator específico para o repositório feito por Eclerk.
    URL Base: https://github.com/Ericles-Porty/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1
    """

    def __init__(self):
        super().__init__()
        self.base_raw_url = "https://raw.githubusercontent.com/Ericles-Porty/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1/refs/heads/main"

    def extract_questions(self) -> list:
        """
        Extrai as perguntas de todos os datasets suportados.
        """
        questions = []
        questions.extend(self.extract_questions_oab_bench())
        questions.extend(self.extract_questions_oab_exams())
        return questions

    def find_curatorship_by_question_id(
        self, question_id: str, data_curatorship: dict
    ) -> dict:
        for item in data_curatorship:
            if item["question_id"] == question_id:
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

        url = f"{self.base_raw_url}/src/results/curator_annotations.json"
        data_curatorship = self.fetch_json(url)

        dataset = self.dataset_loader.create(dataset_name)
        questions_data = dataset.load_questions(
            slice_start=slice_start, slice_end=slice_end
        )
        dataset_id = self.find_dataset_id(dataset_name)

        data = []

        for question in questions_data:
            question_id = str(question[question_id_field])
            curatorship = self.find_curatorship_by_question_id(
                question_id, data_curatorship
            )

            if not curatorship:
                continue

            category_id = self.find_category_id(curatorship["subdominio_semantico"])
            difficulty = curatorship["dificuldade"]
            if difficulty is None:
                difficulty = 3

            data.append(
                {
                    "id_dataset": dataset_id,
                    "id_categoria": category_id,
                    "id_externo": question_id,
                    "tipo_pergunta": tipo_pergunta,
                    "enunciado": question[statement_field],
                    "nivel_dificuldade": f"Nivel {difficulty}",
                    "legislacao_basica": curatorship["corpus_referencia"],
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
            slice_start=153,
            slice_end=165,
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
            slice_start=1600,
            slice_end=1723,
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
