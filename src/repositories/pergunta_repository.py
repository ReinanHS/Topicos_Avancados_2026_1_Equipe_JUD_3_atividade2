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
                            enunciado, resposta_ouro, nivel_dificuldade, legislacao_basica, metadados
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

    def fetch_for_export(self) -> list[dict]:
        """
        Retorna todas as perguntas com chaves naturais já resolvidas
        (dataset.nome, categoria.nome) prontas para serialização em JSON
        portável.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT
                            d.nome AS dataset,
                            c.nome AS categoria,
                            p.id_externo,
                            p.tipo_pergunta,
                            p.enunciado,
                            p.resposta_ouro,
                            p.nivel_dificuldade,
                            p.legislacao_basica,
                            p.metadados
                        FROM perguntas p
                        JOIN datasets d ON d.id_dataset = p.id_dataset
                        JOIN categorias c ON c.id_categoria = p.id_categoria
                        ORDER BY d.nome, p.id_externo;
                        """
                    )
                    rows = cur.fetchall()
                    return [
                        {
                            "dataset": row[0],
                            "categoria": row[1],
                            "id_externo": row[2],
                            "tipo_pergunta": row[3],
                            "enunciado": row[4],
                            "resposta_ouro": row[5],
                            "nivel_dificuldade": row[6],
                            "legislacao_basica": row[7],
                            "metadados": row[8],
                        }
                        for row in rows
                    ]
        except Exception as e:
            print(f"Erro ao exportar perguntas: {e}")
            raise e
