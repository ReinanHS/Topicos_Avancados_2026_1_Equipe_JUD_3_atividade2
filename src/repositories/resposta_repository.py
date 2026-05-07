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
