# victor
import psycopg2
from src.database.connection import DatabaseManager


class AvaliacaoJuizRepository:
    """
    Repositório para gerenciar operações relacionadas à tabela avaliacoes_juiz.
    """

    def __init__(self):
        self.db_manager = DatabaseManager()

    def _get_connection(self):
        conn_str = self.db_manager.get_connection_string
        return psycopg2.connect(conn_str)

    def exists(self, id_resposta_ativa1: int, id_modelo_juiz: int) -> bool:
        """
        Verifica se uma resposta já foi avaliada por determinado modelo juiz.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT 1
                        FROM avaliacoes_juiz
                        WHERE id_resposta_ativa1 = %s
                          AND id_modelo_juiz = %s;
                        """,
                        (id_resposta_ativa1, id_modelo_juiz),
                    )

                    return cur.fetchone() is not None

        except Exception as e:
            print(f"Erro ao verificar avaliação existente: {e}")
            raise e

    def create(
        self,
        id_resposta_ativa1: int,
        id_modelo_juiz: int,
        nota_atribuida: int,
        chain_of_thought: str,
    ) -> None:
        """
        Insere uma avaliação feita pelo Juiz-IA.
        """
        if self.exists(id_resposta_ativa1, id_modelo_juiz):
            return

        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO avaliacoes_juiz (
                            id_resposta_ativa1,
                            id_modelo_juiz,
                            nota_atribuida,
                            chain_of_thought
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
            print(f"Erro ao inserir avaliação da resposta {id_resposta_ativa1}: {e}")
            raise e
