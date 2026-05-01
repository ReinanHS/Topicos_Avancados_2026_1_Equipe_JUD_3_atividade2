"""
Módulo CLI principal — interface de linha de comando baseada em Typer.
"""

import typer

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main_callback():
    """
    CLI para manipulação de dados.
    """
    pass
