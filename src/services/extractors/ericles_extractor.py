from src.helper import parse_answer_with_justificativa
from src.services.extractors.base_extractor import BaseExtractor


class EriclesExtractor(BaseExtractor):
    """
    Extrator específico para o repositório feito por Ericles.
    URL Base: https://github.com/Ericles-Porty/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1
    """

    def __init__(self):
        super().__init__()
        self.base_raw_url = "https://raw.githubusercontent.com/Ericles-Porty/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1/3b8c42d181714bee4272e2c4cbf77b3ebb3c0e20"
        # Respostas geradas COM RAG (arquivos open_questions_rag.json e
        # multiple_choice_rag.json) ficam na branch da inferência com RAG.
        # Atualize este ref para o commit/branch onde os *_rag.json foram
        # commitados após rodar `python main.py --stage mc/open --rag`.
        self.rag_base_raw_url = "https://raw.githubusercontent.com/Ericles-Porty/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1/refs/heads/feature/rag-inference"
        self.dataset_range = {
            "oab_bench": {
                "slice_start": 153,
                "slice_end": 165,
            },
            "oab_exams": {
                "slice_start": 1600,
                "slice_end": 1723,
            },
        }

    def get_curatorship_data(self, dataset_name: str) -> list[dict]:
        url = f"{self.base_raw_url}/src/results/curator_annotations.json"
        return self.fetch_json(url)

    def parse_curatorship(self, curatorship: dict) -> dict:
        difficulty = curatorship["dificuldade"]
        if difficulty is None:
            difficulty = 3

        subdomains = curatorship["subdominio_semantico"].split(" e ")
        category_name = subdomains[0].strip()

        return {
            "category": category_name,
            "difficulty": difficulty,
            "legislation": curatorship["corpus_referencia"],
        }

    def _process_item(
        self,
        item: dict,
        answer_parser: callable,
        dataset_id: int,
        usou_rag: bool = False,
    ) -> dict | None:
        parsed = answer_parser(item)
        if not parsed:
            return None

        if isinstance(parsed, tuple):
            texto_resposta, justificativa = parsed
        else:
            texto_resposta, justificativa = parsed, None

        if not texto_resposta:
            return None

        db_model_name = self.get_db_model_name(item.get("model", ""))
        model_data = self.modelo_repo.get_by_name(db_model_name)
        id_modelo = model_data["id_modelo"] if model_data else None

        id_externo = str(item.get("question_id"))
        id_pergunta = self.pergunta_repo.get_id(id_externo, dataset_id)

        if id_pergunta and id_modelo:
            return {
                "id_pergunta": id_pergunta,
                "id_modelo": id_modelo,
                "texto_resposta": texto_resposta,
                "justificativa": justificativa,
                "tempo_inferencia_ms": None,
                "usou_rag": usou_rag,
            }
        print(
            f"[Info] Pergunta {id_pergunta} ou modelo {id_modelo} não encontrado: {id_externo}"
        )
        return None

    def _process_dataset_answers(
        self,
        dataset_name: str,
        url_suffix: str,
        answer_parser: callable,
        usou_rag: bool = False,
    ) -> list:
        print(
            f"[{self.__class__.__name__}] Extraindo respostas {'RAG ' if usou_rag else ''}do dataset: {dataset_name}"
        )
        dataset_id = self.find_dataset_id(dataset_name)

        base_url = self.rag_base_raw_url if usou_rag else self.base_raw_url
        url = f"{base_url}/src/results/{url_suffix}"
        answers = []
        try:
            data = self.fetch_json(url)
            for item in data:
                processed = self._process_item(
                    item, answer_parser, dataset_id, usou_rag=usou_rag
                )
                if processed:
                    answers.append(processed)
        except Exception as e:
            print(
                f"Aviso: Não foi possível processar {url_suffix} para {dataset_name}: {e}"
            )

        return answers

    # ── Respostas sem RAG (linha de base) ───────────────────────────────────────

    def extract_answers_oab_bench(self) -> list:
        def parser(item):
            return str(item.get("answer", ""))

        return self._process_dataset_answers("oab_bench", "open_questions.json", parser)

    def extract_answers_oab_exams(self) -> list:
        def parser(item):
            answer_text = str(item.get("answer", "")).strip()
            return parse_answer_with_justificativa(answer_text)

        return self._process_dataset_answers(
            "oab_exams", "multiple_choice.json", parser
        )

    def extract_answers(self) -> list:
        answers = []
        answers.extend(self.extract_answers_oab_bench())
        answers.extend(self.extract_answers_oab_exams())
        return answers

    # ── Respostas geradas COM RAG (arquivos *_rag.json) ─────────────────────────

    def extract_answers_oab_bench_rag(self) -> list:
        def parser(item):
            return str(item.get("answer", ""))

        return self._process_dataset_answers(
            "oab_bench", "open_questions_rag.json", parser, usou_rag=True
        )

    def extract_answers_oab_exams_rag(self) -> list:
        def parser(item):
            answer_text = str(item.get("answer", "")).strip()
            return parse_answer_with_justificativa(answer_text)

        return self._process_dataset_answers(
            "oab_exams", "multiple_choice_rag.json", parser, usou_rag=True
        )

    def extract_answers_rag(self) -> list:
        answers = []
        answers.extend(self.extract_answers_oab_bench_rag())
        answers.extend(self.extract_answers_oab_exams_rag())
        return answers
