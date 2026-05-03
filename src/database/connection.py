import os
from dotenv import load_dotenv
from yoyo import get_backend


class DatabaseManager:
    """
    Classe especializada em fornecer as configurações e conexões com o banco de dados.
    """

    def __init__(self):
        load_dotenv()

    @property
    def get_connection_string(self) -> str:
        """Constrói e retorna a string de conexão baseada nas variáveis de ambiente."""
        user = os.getenv("POSTGRES_USER", "admin")
        password = os.getenv("POSTGRES_PASSWORD", "adminpassword")
        db = os.getenv("POSTGRES_DB", "jud_db")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"

    def get_yoyo_backend(self):
        """Retorna o backend do yoyo-migrations configurado."""
        return get_backend(self.get_connection_string)
