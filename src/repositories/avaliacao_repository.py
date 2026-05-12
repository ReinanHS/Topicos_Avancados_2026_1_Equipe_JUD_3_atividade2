import psycopg2
from src.database.connection import DatabaseManager


class AvaliacaoRepository:
    """
    Repositório para gerenciar operações de banco de dados relacionadas à tabela avaliacoes_juiz.
    """

    def __init__(self):
        self.db_manager = DatabaseManager()

    def _get_connection(self):
        """Retorna uma nova conexão com o banco de dados."""
        conn_str = self.db_manager.get_connection_string
        return psycopg2.connect(conn_str)

    def exists(self, id_resposta_ativa1: int, id_modelo_juiz: int) -> bool:
        """
        Verifica se já existe uma avaliação para o mesmo par (resposta, juiz).
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT 1
                        FROM avaliacoes_juiz
                        WHERE id_resposta_ativa1 = %s AND id_modelo_juiz = %s;
                        """,
                        (id_resposta_ativa1, id_modelo_juiz),
                    )
                    return cur.fetchone() is not None
        except Exception as e:
            print(f"Erro ao verificar existência de avaliação: {e}")
            raise e

    def create(
        self,
        id_resposta_ativa1: int,
        id_modelo_juiz: int,
        nota_atribuida: int,
        chain_of_thought: str,
    ) -> None:
        """
        Cadastra uma avaliação no banco de dados.
        Ignora caso já exista uma avaliação para o mesmo par (resposta, juiz).
        """
        if self.exists(id_resposta_ativa1, id_modelo_juiz):
            return

        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO avaliacoes_juiz (
                            id_resposta_ativa1, id_modelo_juiz, nota_atribuida, chain_of_thought
                        )
                        VALUES (%s, %s, %s, %s);
                        """,
                        (
                            id_resposta_ativa1,
                            id_modelo_juiz,
                            nota_atribuida,
                            chain_of_thought,
                        ),
                    )
                conn.commit()
        except Exception as e:
            print(
                f"Erro ao inserir avaliação para resposta '{id_resposta_ativa1}' "
                f"do juiz '{id_modelo_juiz}': {e}"
            )
            raise e

    def list_pending(self, id_modelo_juiz: int, limit: int | None = None) -> list[dict]:
        """
        Retorna as respostas de respostas_atividade_1 que ainda não foram avaliadas
        pelo juiz informado, já com JOIN em perguntas para evitar consultas extras.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    query = """
                        SELECT
                            r.id_resposta,
                            r.texto_resposta,
                            p.id_pergunta,
                            p.enunciado,
                            p.tipo_pergunta,
                            p.legislacao_basica,
                            p.metadados,
                            m.nome_modelo AS modelo_candidato
                        FROM respostas_atividade_1 r
                        JOIN perguntas p ON p.id_pergunta = r.id_pergunta
                        JOIN modelos m ON m.id_modelo = r.id_modelo
                        WHERE NOT EXISTS (
                            SELECT 1
                            FROM avaliacoes_juiz a
                            WHERE a.id_resposta_ativa1 = r.id_resposta
                              AND a.id_modelo_juiz = %s
                        )
                        ORDER BY r.id_resposta
                    """
                    params = [id_modelo_juiz]
                    if limit is not None:
                        query += " LIMIT %s"
                        params.append(limit)

                    cur.execute(query, tuple(params))
                    rows = cur.fetchall()
                    return [
                        {
                            "id_resposta": row[0],
                            "texto_resposta": row[1],
                            "id_pergunta": row[2],
                            "enunciado": row[3],
                            "tipo_pergunta": row[4],
                            "legislacao_basica": row[5],
                            "metadados": row[6],
                            "modelo_candidato": row[7],
                        }
                        for row in rows
                    ]
        except Exception as e:
            print(
                f"Erro ao listar respostas pendentes para juiz '{id_modelo_juiz}': {e}"
            )
            raise e

    def summary_by_dataset_candidate_judge(self) -> list[dict]:
        """
        Retorna estatísticas agregadas por (dataset, modelo candidato, modelo juiz).
        Útil para a query de relatório sugerida no enunciado da atividade.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT
                            d.nome AS dataset,
                            m_cand.nome_modelo AS candidato,
                            m_juiz.nome_modelo AS juiz,
                            ROUND(AVG(a.nota_atribuida)::numeric, 3) AS media,
                            ROUND(STDDEV_SAMP(a.nota_atribuida)::numeric, 3) AS desvio,
                            COUNT(a.id_avaliacao) AS total
                        FROM avaliacoes_juiz a
                        JOIN respostas_atividade_1 r ON r.id_resposta = a.id_resposta_ativa1
                        JOIN perguntas p ON p.id_pergunta = r.id_pergunta
                        JOIN datasets d ON d.id_dataset = p.id_dataset
                        JOIN modelos m_cand ON m_cand.id_modelo = r.id_modelo
                        JOIN modelos m_juiz ON m_juiz.id_modelo = a.id_modelo_juiz
                        GROUP BY d.nome, m_cand.nome_modelo, m_juiz.nome_modelo
                        ORDER BY d.nome, m_juiz.nome_modelo, m_cand.nome_modelo;
                        """
                    )
                    rows = cur.fetchall()
                    return [
                        {
                            "dataset": row[0],
                            "candidato": row[1],
                            "juiz": row[2],
                            "media": float(row[3]) if row[3] is not None else None,
                            "desvio": float(row[4]) if row[4] is not None else None,
                            "total": int(row[5]),
                        }
                        for row in rows
                    ]
        except Exception as e:
            print(f"Erro ao recuperar resumo agregado: {e}")
            raise e

    def fetch_judge_vs_gold(self, judge_name: str) -> list[dict]:
        """
        Retorna pares (nota_atribuida, texto_resposta, metadados, tipo_pergunta)
        para um determinado juiz. Usado para o cálculo de Spearman contra o
        gabarito humano (especialmente em múltipla escolha).
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT
                            a.nota_atribuida,
                            r.texto_resposta,
                            p.metadados,
                            p.tipo_pergunta,
                            d.nome AS dataset
                        FROM avaliacoes_juiz a
                        JOIN respostas_atividade_1 r ON r.id_resposta = a.id_resposta_ativa1
                        JOIN perguntas p ON p.id_pergunta = r.id_pergunta
                        JOIN datasets d ON d.id_dataset = p.id_dataset
                        JOIN modelos m_juiz ON m_juiz.id_modelo = a.id_modelo_juiz
                        WHERE m_juiz.nome_modelo = %s;
                        """,
                        (judge_name,),
                    )
                    rows = cur.fetchall()
                    return [
                        {
                            "nota_atribuida": int(row[0]),
                            "texto_resposta": row[1] or "",
                            "metadados": row[2] or {},
                            "tipo_pergunta": row[3],
                            "dataset": row[4],
                        }
                        for row in rows
                    ]
        except Exception as e:
            print(f"Erro ao recuperar avaliações do juiz '{judge_name}': {e}")
            raise e

    def fetch_judge_pair(self, judge_a: str, judge_b: str) -> list[tuple[int, int]]:
        """
        Retorna pares (nota_judge_a, nota_judge_b) das respostas que ambos os
        juízes avaliaram. Usado para correlação inter-juízes.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT a1.nota_atribuida, a2.nota_atribuida
                        FROM avaliacoes_juiz a1
                        JOIN avaliacoes_juiz a2
                          ON a2.id_resposta_ativa1 = a1.id_resposta_ativa1
                        JOIN modelos m1 ON m1.id_modelo = a1.id_modelo_juiz
                        JOIN modelos m2 ON m2.id_modelo = a2.id_modelo_juiz
                        WHERE m1.nome_modelo = %s
                          AND m2.nome_modelo = %s
                          AND m1.id_modelo <> m2.id_modelo;
                        """,
                        (judge_a, judge_b),
                    )
                    return [(int(r[0]), int(r[1])) for r in cur.fetchall()]
        except Exception as e:
            print(f"Erro ao recuperar pares ({judge_a}, {judge_b}): {e}")
            raise e

    def fetch_for_export(self, judge_db_model_name: str) -> list[dict]:
        """
        Retorna as avaliações de um juiz com as chaves naturais já resolvidas
        (dataset, id_externo da pergunta, nome do modelo candidato), prontas
        para serialização em JSON portável entre ambientes.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT
                            d.nome AS dataset,
                            p.id_externo AS id_externo_pergunta,
                            m_cand.nome_modelo AS candidato,
                            a.nota_atribuida,
                            a.chain_of_thought,
                            a.data_avaliacao
                        FROM avaliacoes_juiz a
                        JOIN respostas_atividade_1 r ON r.id_resposta = a.id_resposta_ativa1
                        JOIN perguntas p ON p.id_pergunta = r.id_pergunta
                        JOIN datasets d ON d.id_dataset = p.id_dataset
                        JOIN modelos m_cand ON m_cand.id_modelo = r.id_modelo
                        JOIN modelos m_juiz ON m_juiz.id_modelo = a.id_modelo_juiz
                        WHERE m_juiz.nome_modelo = %s
                        ORDER BY d.nome, p.id_externo, m_cand.nome_modelo;
                        """,
                        (judge_db_model_name,),
                    )
                    rows = cur.fetchall()
                    return [
                        {
                            "dataset": row[0],
                            "id_externo_pergunta": row[1],
                            "candidato": row[2],
                            "nota": int(row[3]),
                            "chain_of_thought": row[4],
                            "data_avaliacao": row[5].isoformat() if row[5] else None,
                        }
                        for row in rows
                    ]
        except Exception as e:
            print(f"Erro ao exportar avaliações do juiz '{judge_db_model_name}': {e}")
            raise e

    def list_distinct_judges(self) -> list[str]:
        """Lista os nomes de modelos juízes que já têm avaliações registradas."""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT DISTINCT m.nome_modelo
                        FROM avaliacoes_juiz a
                        JOIN modelos m ON m.id_modelo = a.id_modelo_juiz
                        ORDER BY m.nome_modelo;
                        """
                    )
                    return [row[0] for row in cur.fetchall()]
        except Exception as e:
            print(f"Erro ao listar juízes com avaliações: {e}")
            raise e
