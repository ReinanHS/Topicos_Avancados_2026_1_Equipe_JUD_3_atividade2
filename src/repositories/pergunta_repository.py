import json
import psycopg2
from src.database.connection import DatabaseManager


class PerguntaRepository:
    """
    Repositório para gerenciar operações de banco de dados relacionadas à tabela perguntas.
    """

    def __init__(self):
        self.db_manager = DatabaseManager()

    def _get_connection(self):
        """Retorna uma nova conexão com o banco de dados."""
        conn_str = self.db_manager.get_connection_string
        return psycopg2.connect(conn_str)

    def create(
        self,
        id_dataset: int,
        id_categoria: int,
        id_externo: str,
        tipo_pergunta: str,
        enunciado: str,
        resposta_ouro: str,
        nivel_dificuldade: str,
        legislacao_basica: str = None,
        metadados: dict = None,
    ) -> None:
        """
        Cadastra uma pergunta no banco de dados.
        Ignora caso já exista uma pergunta com o mesmo id_dataset e id_externo.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO perguntas (
                            id_dataset, id_categoria, id_externo, tipo_pergunta, 
                            enunciado, resposta_ouro, nivel_dificuldade,
                            legislacao_basica, metadados
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id_dataset, id_externo) DO NOTHING;
                        """,
                        (
                            id_dataset,
                            id_categoria,
                            id_externo,
                            tipo_pergunta,
                            enunciado,
                            resposta_ouro,
                            nivel_dificuldade,
                            legislacao_basica,
                            json.dumps(metadados) if metadados else None,
                        ),
                    )
                conn.commit()
        except Exception as e:
            print(f"Erro ao inserir pergunta '{id_externo}': {e}")
            raise e

    def get_id(self, id_externo: str, id_dataset: int) -> int | None:
        """
        Recupera o ID da pergunta a partir de seu id_externo e id_dataset.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id_pergunta
                        FROM perguntas
                        WHERE id_externo = %s AND id_dataset = %s;
                        """,
                        (id_externo, id_dataset),
                    )
                    row = cur.fetchone()
                    if row:
                        return row[0]
                    return None
        except Exception as e:
            print(f"Erro ao recuperar ID da pergunta '{id_externo}': {e}")
            raise e
        #victor
        def get_by_id(self, id_pergunta: int) -> dict | None:
        """
        Recupera uma pergunta completa pelo ID interno do banco.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT
                            p.id_pergunta,
                            p.id_dataset,
                            d.nome AS nome_dataset,
                            p.id_categoria,
                            c.nome AS nome_categoria,
                            p.id_externo,
                            p.tipo_pergunta,
                            p.enunciado,
                            p.nivel_dificuldade,
                            p.legislacao_basica,
                            p.metadados
                        FROM perguntas p
                        JOIN datasets d ON d.id_dataset = p.id_dataset
                        JOIN categorias c ON c.id_categoria = p.id_categoria
                        WHERE p.id_pergunta = %s;
                        """,
                        (id_pergunta,),
                    )

                    row = cur.fetchone()

                    if row:
                        return {
                            "id_pergunta": row[0],
                            "id_dataset": row[1],
                            "nome_dataset": row[2],
                            "id_categoria": row[3],
                            "nome_categoria": row[4],
                            "id_externo": row[5],
                            "tipo_pergunta": row[6],
                            "enunciado": row[7],
                            "nivel_dificuldade": row[8],
                            "legislacao_basica": row[9],
                            "metadados": row[10],
                        }

                    return None

        except Exception as e:
            print(f"Erro ao recuperar pergunta {id_pergunta}: {e}")
            raise e