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

    def find_id(self, id_pergunta: int, id_modelo: int) -> int | None:
        """
        Retorna o id_resposta da resposta gerada pelo `id_modelo` para a
        `id_pergunta`, ou None se não houver. Usada no fluxo de import de
        avaliações para traduzir chaves naturais em IDs.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id_resposta
                        FROM respostas_atividade_1
                        WHERE id_pergunta = %s AND id_modelo = %s
                        LIMIT 1;
                        """,
                        (id_pergunta, id_modelo),
                    )
                    row = cur.fetchone()
                    return row[0] if row else None
        except Exception as e:
            print(
                f"Erro ao buscar id_resposta para pergunta {id_pergunta} / modelo {id_modelo}: {e}"
            )
            raise e

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

    def fetch_for_export(self) -> list[dict]:
        """
        Retorna todas as respostas com chaves naturais resolvidas
        (dataset.nome, id_externo_pergunta, modelo.nome_modelo).
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT
                            d.nome AS dataset,
                            p.id_externo AS id_externo_pergunta,
                            m.nome_modelo AS modelo,
                            r.texto_resposta,
                            r.tempo_inferencia_ms
                        FROM respostas_atividade_1 r
                        JOIN perguntas p ON p.id_pergunta = r.id_pergunta
                        JOIN datasets d ON d.id_dataset = p.id_dataset
                        JOIN modelos m ON m.id_modelo = r.id_modelo
                        ORDER BY d.nome, p.id_externo, m.nome_modelo;
                        """
                    )
                    rows = cur.fetchall()
                    return [
                        {
                            "dataset": row[0],
                            "id_externo_pergunta": row[1],
                            "modelo": row[2],
                            "texto_resposta": row[3],
                            "tempo_inferencia_ms": (
                                float(row[4]) if row[4] is not None else None
                            ),
                        }
                        for row in rows
                    ]
        except Exception as e:
            print(f"Erro ao exportar respostas: {e}")
            raise e
