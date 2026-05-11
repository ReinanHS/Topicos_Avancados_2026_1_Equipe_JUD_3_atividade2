import psycopg2
from src.database.connection import DatabaseManager


class RespostaRepository:
    """
    Repositório para gerenciar operações de banco de dados relacionadas à tabela respostas_atividade_1.
    """

    def __init__(self):
        self.db_manager = DatabaseManager()

    def _get_connection(self):
        """Retorna uma nova conexão com o banco de dados."""
        conn_str = self.db_manager.get_connection_string
        return psycopg2.connect(conn_str)

    def exists(self, id_pergunta: int, id_modelo: int) -> bool:
        """
        Verifica se já existe uma resposta para a mesma pergunta pelo mesmo modelo.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT 1
                        FROM respostas_atividade_1
                        WHERE id_pergunta = %s AND id_modelo = %s;
                        """,
                        (id_pergunta, id_modelo),
                    )
                    return cur.fetchone() is not None
        except Exception as e:
            print(f"Erro ao verificar existência de resposta: {e}")
            raise e

    def create(
        self,
        id_pergunta: int,
        id_modelo: int,
        texto_resposta: str,
        tempo_inferencia_ms: float = None,
    ) -> None:
        """
        Cadastra uma resposta no banco de dados.
        Ignora caso já exista uma resposta para a mesma pergunta pelo mesmo modelo.
        """
        if self.exists(id_pergunta, id_modelo):
            return

        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO respostas_atividade_1 (
                            id_pergunta, id_modelo, texto_resposta, tempo_inferencia_ms
                        )
                        VALUES (%s, %s, %s, %s);
                        """,
                        (id_pergunta, id_modelo, texto_resposta, tempo_inferencia_ms),
                    )
                conn.commit()
        except Exception as e:
            print(f"Erro ao inserir resposta para pergunta '{id_pergunta}': {e}")
            raise e
    #victor
    def get_pendentes_avaliacao(self, id_modelo_juiz: int, limit: int | None = 10) -> list[dict]:
        """
        Lista respostas da Atividade 1 que ainda não foram avaliadas
        pelo modelo juiz informado.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    sql = """
                        SELECT
                            r.id_resposta,
                            r.id_pergunta,
                            r.id_modelo,
                            m.nome_modelo,
                            r.texto_resposta,
                            r.tempo_inferencia_ms,
                            r.data_geracao
                        FROM respostas_atividade_1 r
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

                    if limit is not None and limit > 0:
                        sql += " LIMIT %s"
                        params.append(limit)

                    cur.execute(sql, tuple(params))
                    rows = cur.fetchall()

                    return [
                        {
                            "id_resposta": row[0],
                            "id_pergunta": row[1],
                            "id_modelo": row[2],
                            "nome_modelo": row[3],
                            "texto_resposta": row[4],
                            "tempo_inferencia_ms": row[5],
                            "data_geracao": row[6],
                        }
                        for row in rows
                    ]

        except Exception as e:
            print(f"Erro ao listar respostas pendentes de avaliação: {e}")
            raise e