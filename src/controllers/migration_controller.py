from yoyo import read_migrations
from src.database import DatabaseManager


class MigrationController:
    """
    Controller responsável por orquestrar as migrações e rollbacks do banco de dados.
    """

    def __init__(self):
        self.db_manager = DatabaseManager()

    def _get_backend(self):
        """Retorna o backend do yoyo-migrations utilizando o DatabaseManager."""
        return self.db_manager.get_yoyo_backend()

    def migrate(self):
        """Aplica todas as migrações pendentes."""
        backend = self._get_backend()
        migrations = read_migrations("database/migrations")
        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))
        print("Migracoes aplicadas com sucesso.")

    def rollback(self, all_migrations: bool = True):
        """Reverte migrações."""
        backend = self._get_backend()
        migrations = read_migrations("database/migrations")
        with backend.lock():
            to_rollback = backend.to_rollback(migrations)
            if not to_rollback:
                print("Nenhuma migracao para reverter.")
                return

            if not all_migrations:
                to_rollback = [to_rollback[0]]

            backend.rollback_migrations(to_rollback)

        if all_migrations:
            print("Rollback completo: todas as migracoes foram revertidas.")
        else:
            print("Rollback: ultima migracao revertida com sucesso.")
