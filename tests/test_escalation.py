from src.core.escalation import build_escalation_message, detect_sector


def test_detects_rh_question():
    sector = detect_sector("Qual é a regra de férias?")
    assert sector["email"] == "rh@dnelsom.com.br"


def test_builds_fallback_message():
    message = build_escalation_message("Qual é o salário do diretor?")
    assert "Não encontrei" in message
    assert "rh@dnelsom.com.br" in message


def test_generic_fallback_does_not_duplicate_sector_text():
    message = build_escalation_message("conte uma piada")
    assert "setor de setor responsável" not in message
    assert "setor responsável" in message
