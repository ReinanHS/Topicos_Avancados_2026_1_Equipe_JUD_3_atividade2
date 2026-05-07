import psycopg2
from src.database.connection import DatabaseManager


class RespostaRepository:
    """
    Repositório para gerenciar operações de banco de dados relacionadas à tabela
    respostas_atividade_1.
    """

    def __init__(self):
        self.db_manager = DatabaseManager()

    def _get_connection(self):
        """Retorna uma nova conexão com o banco de dados."""
        conn_str = self.db_manager.get_connection_string
        return psycopg2.connect(conn_str)

    def create(
        self,
        id_externo: str,
        nome_modelo: str,
        versao_modelo: str,
        texto_resposta: str,
        tempo_inferencia_ms: float | None = None,
    ) -> bool:
        """
        Cadastra uma resposta da Atividade 1 no banco de dados.

        As FKs (id_pergunta, id_modelo) são resolvidas em runtime via subquery,
        usando `id_externo` (em `perguntas`) e `(nome_modelo, versao)` (em
        `modelos`) como chaves naturais. Retorna True se a linha foi inserida;
        False se a pergunta ou o modelo não foram encontrados.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO respostas_atividade_1
                            (id_pergunta, id_modelo, texto_resposta, tempo_inferencia_ms)
                        SELECT p.id_pergunta, m.id_modelo, %s, %s
                        FROM perguntas p, modelos m
                        WHERE p.id_externo = %s
                          AND m.nome_modelo = %s
                          AND m.versao = %s;
                        """,
                        (
                            texto_resposta,
                            tempo_inferencia_ms,
                            id_externo,
                            nome_modelo,
                            versao_modelo,
                        ),
                    )
                    inserted = cur.rowcount
                conn.commit()
            return inserted > 0
        except Exception as e:
            print(
                f"Erro ao inserir resposta para id_externo='{id_externo}' "
                f"modelo='{nome_modelo} {versao_modelo}': {e}"
            )
            raise e
