import psycopg2
from src.database.connection import DatabaseManager


class DatasetRepository:
    """
    Repositório para gerenciar operações de banco de dados relacionadas à tabela datasets.
    """

    def __init__(self):
        self.db_manager = DatabaseManager()

    def _get_connection(self):
        """Retorna uma nova conexão com o banco de dados."""
        conn_str = self.db_manager.get_connection_string
        return psycopg2.connect(conn_str)

    def create(
        self,
        nome: str,
        url_origem: str,
        dominio: str,
        tipo_tarefa: str,
        versao: str,
        descricao: str,
    ) -> None:
        """
        Cadastra um dataset no banco de dados.
        Ignora caso já exista um dataset com o mesmo nome.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO datasets (nome, url_origem, dominio, tipo_tarefa, versao, descricao)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (nome) DO NOTHING;
                        """,
                        (nome, url_origem, dominio, tipo_tarefa, versao, descricao),
                    )
                conn.commit()
        except Exception as e:
            print(f"Erro ao inserir dataset '{nome}': {e}")
            raise e

    def get_by_name(self, nome: str) -> dict | None:
        """
        Recupera as informações de um dataset a partir de seu nome.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id_dataset, nome, url_origem, dominio, tipo_tarefa, versao, descricao, created_at 
                        FROM datasets 
                        WHERE nome = %s;
                        """,
                        (nome,),
                    )
                    row = cur.fetchone()
                    if row:
                        return {
                            "id_dataset": row[0],
                            "nome": row[1],
                            "url_origem": row[2],
                            "dominio": row[3],
                            "tipo_tarefa": row[4],
                            "versao": row[5],
                            "descricao": row[6],
                            "created_at": row[7],
                        }
                    return None
        except Exception as e:
            print(f"Erro ao recuperar dataset '{nome}': {e}")
            raise e
