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
4. Não mencione nomes brutos de arquivos (ex: rotinas_financeiras.md) nem extensoes (.md, .pdf) no texto da resposta, pois as fontes sao exibidas automaticamente pela interface.
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


def _generate_suggested_questions(passages: list[dict]) -> list[str]:
    sectors = {p.get("setor", "").lower() for p in passages}
    suggestions = []
    if "rh" in sectors:
        suggestions.extend(["Como solicito o fracionamento de férias?", "Quais são as regras do banco de horas?"])
    if "ti" in sectors:
        suggestions.extend(["Como redefinir a minha senha de acesso?", "Quais os requisitos de segurança em TI?"])
    if "juridico" in sectors:
        suggestions.extend(["Quais os direitos do titular na LGPD?", "Como enviar um contrato para análise?"])
    if "comercial" in sectors:
        suggestions.extend(["Quais são as regras de comissões?", "Como funciona a política de descontos?"])
    if "atendimento" in sectors:
        suggestions.extend(["Como funciona a garantia de produtos?", "Quais são os prazos de devolução?"])
    if "compliance" in sectors:
        suggestions.extend(["Quais as diretrizes do código de conduta?", "Como relatar uma inconformidade?"])
    if "financeiro" in sectors:
        suggestions.extend(["Qual o prazo para reembolso de despesas?", "Quais os comprovantes necessários para prestação de contas?"])

    if not suggestions:
        suggestions = ["Quais são as políticas internas da empresa?", "Como entrar em contato com o setor responsável?"]

    return list(dict.fromkeys(suggestions))[:2]


def ask(question: str, first_interaction: bool = False, sector_filter: str | None = None) -> dict:
    try:
        passages = vector_query(question, sector_filter=sector_filter)
    except Exception as exc:
        if is_quota_error(exc):
            return {
                "resposta": build_quota_message(exc),
                "fontes": [],
                "encaminhado": False,
                "quota_exceeded": True,
                "suggested_questions": [],
            }
        raise

    if not has_relevant_context(passages):
        return {
            "resposta": build_escalation_message(question),
            "fontes": [],
            "encaminhado": True,
            "suggested_questions": [],
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
                "suggested_questions": [],
            }
        raise

    return {
        "resposta": response.text,
        "fontes": sources,
        "encaminhado": False,
        "suggested_questions": _generate_suggested_questions(passages),
    }

