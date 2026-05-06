import psycopg2
from src.database.connection import DatabaseManager


class ModeloRepository:
    """
    Repositório para gerenciar operações de banco de dados relacionadas à tabela modelos.
    """

    def __init__(self):
        self.db_manager = DatabaseManager()

    def _get_connection(self):
        """Retorna uma nova conexão com o banco de dados."""
        conn_str = self.db_manager.get_connection_string
        return psycopg2.connect(conn_str)

    def create(
        self,
        nome_modelo: str,
        versao: str = None,
        provedor: str = None,
        familia: str = None,
        parametro_precisao: str = None,
    ) -> None:
        """
        Cadastra um modelo no banco de dados.
        Ignora caso já exista um modelo com o mesmo nome.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO modelos (nome_modelo, versao, provedor, familia, parametro_precisao)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (nome_modelo) DO NOTHING;
                        """,
                        (nome_modelo, versao, provedor, familia, parametro_precisao),
                    )
                conn.commit()
        except Exception as e:
            print(f"Erro ao inserir modelo '{nome_modelo}': {e}")
            raise e

    def get_by_name(self, nome_modelo: str) -> dict | None:
        """
        Recupera as informações de um modelo a partir de seu nome.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id_modelo, nome_modelo, versao, provedor, familia, parametro_precisao
                        FROM modelos 
                        WHERE nome_modelo = %s;
                        """,
                        (nome_modelo,),
                    )
                    row = cur.fetchone()
                    if row:
                        return {
                            "id_modelo": row[0],
                            "nome_modelo": row[1],
                            "versao": row[2],
                            "provedor": row[3],
                            "familia": row[4],
                            "parametro_precisao": row[5],
                        }
                    return None
        except Exception as e:
            print(f"Erro ao recuperar modelo '{nome_modelo}': {e}")
            raise e
