"""RAG engine for Daniel Knowledge."""

from __future__ import annotations

import google.generativeai as genai

from src.config.settings import settings
from src.core.errors import build_quota_message, is_quota_error
from src.core.escalation import build_escalation_message
from src.core.vector_store import has_relevant_context, query as vector_query


SYSTEM_PROMPT = """Você é Daniel, assistente corporativo inteligente da DNEL SOM Serviços Inteligentes.

Regras obrigatórias:
1. Responda somente com base no contexto recuperado.
2. Se o contexto não responder claramente, diga que não encontrou a informação.
3. Nunca invente dados, políticas, valores, prazos ou nomes.
4. Cite documentos de origem quando possível.
5. Use linguagem profissional, direta e acessível.
6. {presentation_instruction}
"""

FIRST_INTERACTION = "Esta é a primeira interação: pode se apresentar brevemente antes da resposta."
NEXT_INTERACTIONS = "Você já se apresentou. Não repita saudação institucional; responda direto."


def _configure_model():
    if not settings.google_api_key:
        raise EnvironmentError("GOOGLE_API_KEY não configurada. Verifique o arquivo .env.")
    genai.configure(api_key=settings.google_api_key)
    return genai.GenerativeModel(settings.chat_model)


def _build_context(passages: list[dict]) -> str:
    parts = []
    for passage in passages:
        parts.append(
            f"[Fonte: {passage['fonte']} | Setor: {passage['setor']} | "
            f"Distância: {passage.get('distancia', 'n/a')}]\n{passage['texto']}"
        )
    return "\n\n---\n\n".join(parts)


def ask(question: str, first_interaction: bool = False) -> dict:
    try:
        passages = vector_query(question)
    except Exception as exc:
        if is_quota_error(exc):
            return {
                "resposta": build_quota_message(exc),
                "fontes": [],
                "encaminhado": False,
                "quota_exceeded": True,
            }
        raise

    if not has_relevant_context(passages):
        return {
            "resposta": build_escalation_message(question),
            "fontes": [],
            "encaminhado": True,
        }

    presentation_instruction = FIRST_INTERACTION if first_interaction else NEXT_INTERACTIONS
    prompt = SYSTEM_PROMPT.format(presentation_instruction=presentation_instruction)
    prompt += f"""

CONTEXTO RECUPERADO:
{_build_context(passages)}

PERGUNTA DO USUÁRIO:
{question}

Responda seguindo estritamente as regras acima.
"""

    sources = sorted({passage["fonte"] for passage in passages})
    model = _configure_model()

    try:
        response = model.generate_content(prompt)
    except Exception as exc:
        if is_quota_error(exc):
            return {
                "resposta": build_quota_message(exc),
                "fontes": sources,
                "encaminhado": False,
                "quota_exceeded": True,
            }
        raise

    return {
        "resposta": response.text,
        "fontes": sources,
        "encaminhado": False,
    }
