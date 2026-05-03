"""
Pacote principal do projeto.

Re-exporta as classes públicas dos subpacotes para conveniência.
"""

from src.cli import app

__all__ = ["app"]
