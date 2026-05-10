import json
import re


def _clean_json_string(text: str) -> str:
    """Limpa a string JSON de blocos markdown e escapes desnecessários."""
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.replace("\\", "").replace("'", '"')

    if text.startswith('"') and text.endswith('"'):
        try:
            inner = json.loads(text)
            if isinstance(inner, str):
                return inner
        except json.JSONDecodeError:
            pass
    return text


def _extract_from_dict(answer_dict: dict) -> str | None:
    """Extrai a resposta se o JSON decodificado for um dicionário."""
    resposta = answer_dict.get("resposta", "")
    if resposta:
        match = re.search(r"^([A-D])", str(resposta).strip(), re.IGNORECASE)
        return match.group(1).upper() if match else str(resposta)
    return None


def _extract_from_string(answer_str: str) -> str | None:
    """Extrai a resposta se o JSON decodificado for uma string."""
    match = re.search(r"^([A-D])(?:\)|$|\s)", answer_str.strip(), re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return None


def _fallback_regex_match(text: str) -> str | None:
    """Usa Expressão Regular como fallback se o parse do JSON falhar."""
    match = re.search(r'"resposta"\s*:\s*"?([A-D])"?', text, re.IGNORECASE)
    if match:
        return match.group(1).upper()

    match = re.search(r'^"?([A-D])"?(?:\)|$|\s|})', text, re.IGNORECASE)
    if match:
        return match.group(1).upper()

    return None


def _try_parse_json(text: str) -> str | None:
    """Tenta decodificar o texto como JSON e extrair a resposta."""
    try:
        answer_json = json.loads(text)
        if isinstance(answer_json, dict):
            return _extract_from_dict(answer_json)
        if isinstance(answer_json, str):
            return _extract_from_string(answer_json)
    except json.JSONDecodeError:
        pass
    return None


def parse_answer_json(answer_text: str) -> str:
    """Função auxiliar para processar o JSON e retornar a resposta."""
    cleaned_text = _clean_json_string(answer_text)
    extracted = _try_parse_json(cleaned_text)
    fallback = _fallback_regex_match(cleaned_text)
    return extracted or fallback or cleaned_text
