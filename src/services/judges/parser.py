"""
Parser do veredito do Juiz-IA.

Extrai (nota, chain_of_thought) do texto bruto retornado pelo modelo,
tolerando variações de caixa, acentuação e formatação.
"""

import re

_NOTA_PATTERN = re.compile(
    r"(?:NOTA|SCORE|Nota|Score|NOTE)\s*[:=\-]?\s*\*?\*?\s*([1-5])",
    re.IGNORECASE,
)


def _extract_chain_of_thought(raw: str, nota_match: re.Match) -> str:
    """Devolve a parte 'raciocínio' do output, sem a linha da nota."""
    before_nota = raw[: nota_match.start()].strip()

    # Remove o prefixo "RACIOCÍNIO:" / "REASONING:" se presente, mas
    # mantém todo o conteúdo subsequente.
    prefix_re = re.compile(
        r"^(?:RACIOC[IÍ]NIO|REASONING|JUSTIFICATIVA|ANÁLISE|ANALISE)\s*[:=\-]\s*",
        re.IGNORECASE,
    )
    cleaned = prefix_re.sub("", before_nota, count=1).strip()

    return cleaned or raw.strip()


def parse_verdict(raw: str) -> tuple[int, str]:
    """
    Extrai (nota_atribuida, chain_of_thought) do output do juiz.

    Levanta ValueError se não conseguir localizar uma nota entre 1 e 5.
    """
    if not raw or not raw.strip():
        raise ValueError("Output do juiz está vazio.")

    match = _NOTA_PATTERN.search(raw)
    if not match:
        raise ValueError(
            f"Não foi possível extrair a nota do output do juiz. Output bruto: {raw[:500]}"
        )

    nota = int(match.group(1))
    if not 1 <= nota <= 5:
        raise ValueError(f"Nota fora da faixa esperada (1-5): {nota}")

    chain_of_thought = _extract_chain_of_thought(raw, match)
    return nota, chain_of_thought
