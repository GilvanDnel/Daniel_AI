from src.core.intents import is_greeting


def test_detects_simple_greeting():
    assert is_greeting("olá")
    assert is_greeting("ola")
    assert is_greeting("boa tarde")


def test_does_not_treat_question_as_greeting():
    assert not is_greeting("como solicito férias?")
