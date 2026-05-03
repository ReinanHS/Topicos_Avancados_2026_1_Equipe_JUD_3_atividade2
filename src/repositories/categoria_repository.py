import psycopg2
from src.database.connection import DatabaseManager


class CategoriaRepository:
    """
    Repositório para gerenciar operações de banco de dados relacionadas à tabela categorias.
    """

    def __init__(self):
        self.db_manager = DatabaseManager()

    def _get_connection(self):
        """Retorna uma nova conexão com o banco de dados."""
        conn_str = self.db_manager.get_connection_string
        return psycopg2.connect(conn_str)

    def create(self, nome: str) -> None:
        """
        Cadastra uma categoria no banco de dados.
        Ignora caso já exista uma categoria com o mesmo nome.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO categorias (nome)
                        VALUES (%s)
                        ON CONFLICT (nome) DO NOTHING;
                        """,
                        (nome,),
                    )
                conn.commit()
        except Exception as e:
            print(f"Erro ao inserir categoria '{nome}': {e}")
            raise e

    def get_by_name(self, nome: str) -> dict | None:
        """
        Recupera as informações de uma categoria a partir de seu nome.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id_categoria, nome, created_at 
                        FROM categorias 
                        WHERE nome = %s;
                        """,
                        (nome,),
                    )
                    row = cur.fetchone()
                    if row:
                        return {
                            "id_categoria": row[0],
                            "nome": row[1],
                            "created_at": row[2],
                        }
                    return None
        except Exception as e:
            print(f"Erro ao recuperar categoria '{nome}': {e}")
            raise e
