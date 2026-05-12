"""
Templates de prompt para o Juiz Jurídico (LLM-as-a-Judge).

Baseado na rubrica oficial da Atividade 2 (Desembargador / Professor Doutor em Direito).
"""

PROMPT_TEMPLATE = """[PERSONA]
Você é um Desembargador e Professor Doutor em Direito com vasta experiência em exames da OAB. Sua tarefa é avaliar a resposta de uma IA (candidata) a uma questão jurídica.

[CONTEXTO]
Pergunta: {pergunta}

Tipo da questão: {tipo_pergunta}

Gabarito / Referência: {resposta_ouro}

Legislação básica relacionada: {legislacao_basica}

Resposta da IA a ser avaliada:
{resposta_modelo}

[RUBRICA DE AVALIAÇÃO]
- Nota 1: Resposta incorreta, cita leis inexistentes ou confunde institutos básicos.
- Nota 2: Conclusão correta, mas a fundamentação é vaga ou cita artigos de lei errados.
- Nota 3: Resposta correta e bem fundamentada, mas falta clareza ou omite detalhes importantes do gabarito.
- Nota 4: Resposta excelente, alinhada ao gabarito, com fundamentação legal precisa.
- Nota 5: Resposta excepcional, fundamentada, cita jurisprudência relevante (STF/STJ) e demonstra raciocínio jurídico mestre.

[INSTRUÇÕES DE SAÍDA]
Analise a resposta da IA comparando-a com o Gabarito quando disponível. Ignore o tamanho do texto; foque na precisão do Direito brasileiro.

Forneça o veredito EXATAMENTE no formato abaixo, sem texto adicional após a NOTA:

RACIOCÍNIO: <explique de forma detalhada por que a nota foi dada>
NOTA: <apenas o número de 1 a 5>
"""


def _format_resposta_ouro(pergunta: dict) -> str:
    """
    Constrói o trecho de 'Gabarito / Referência' a partir do que existir na
    pergunta. Em múltipla escolha, o gabarito pode estar embutido nos metadados;
    em discursiva, geralmente há diretrizes (`values`/guidelines).
    """
    metadados = pergunta.get("metadados") or {}

    if pergunta.get("tipo_pergunta") == "multipla_escolha":
        alternativa = metadados.get("alternativa_correta") or metadados.get("answerKey")
        if alternativa:
            return f"Alternativa correta: {alternativa}"
        return (
            "Gabarito explícito não disponível neste registro. "
            "Avalie com base no seu conhecimento do Direito brasileiro."
        )

    guidelines = (
        metadados.get("guidelines")
        or metadados.get("values")
        or metadados.get("reference")
    )
    if guidelines:
        return str(guidelines)
    return (
        "Diretrizes de correção não disponíveis neste registro. "
        "Avalie com base no seu conhecimento do Direito brasileiro."
    )


def build_prompt(pergunta: dict, resposta_modelo: str) -> str:
    """
    Monta o prompt final do juiz a partir do dicionário de pergunta vindo do
    repositório (com `enunciado`, `tipo_pergunta`, `metadados`, etc.) e do texto
    de resposta do modelo candidato.
    """
    return PROMPT_TEMPLATE.format(
        pergunta=pergunta.get("enunciado", "").strip(),
        tipo_pergunta=pergunta.get("tipo_pergunta", "discursiva"),
        resposta_ouro=_format_resposta_ouro(pergunta),
        legislacao_basica=(
            pergunta.get("legislacao_basica") or "Não informada"
        ).strip(),
        resposta_modelo=(resposta_modelo or "").strip(),
    )
