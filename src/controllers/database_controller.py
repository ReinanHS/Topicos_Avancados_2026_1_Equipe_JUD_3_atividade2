from yoyo import read_migrations
from src.database import DatabaseManager
from src.repositories import DatasetRepository


class DatabaseController:
    """
    Controller responsável por orquestrar ações relacionadas ao banco de dados,
    como migrações, rollbacks e inserção de dados iniciais (seeding).
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

    def seed_datasets(self):
        """Insere as informações de datasets essenciais no banco de dados."""
        repo = DatasetRepository()

        datasets = [
            {
                "nome": "oab_exams",
                "url_origem": "https://huggingface.co/datasets/eduagarcia/oab_exams",
                "dominio": "Direito",
                "tipo_tarefa": "multipla_escolha",
                "versao": "b47d6f3",
                "descricao": "Dataset com questões objetivas de múltipla escolha (1ª fase) dos exames da OAB.",
            },
            {
                "nome": "oab_bench",
                "url_origem": "https://github.com/maritaca-ai/oab-bench",
                "dominio": "Direito",
                "tipo_tarefa": "discursiva",
                "versao": "238e999",
                "descricao": "Dataset com questões discursivas (2ª fase) dos exames da OAB.",
            },
        ]

        try:
            for ds in datasets:
                repo.create(**ds)

            print("Datasets semeados com sucesso!")
        except Exception as e:
            print(f"Erro ao semear datasets: {e}")
