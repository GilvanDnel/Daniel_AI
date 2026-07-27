"""Main Streamlit app for Daniel AI."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st

from src.core.errors import build_quota_message, is_quota_error
from src.services.chat_service import ChatResult, handle_message
from src.ui.chat_view import render_history, render_result
from src.ui.sidebar import render_sidebar


SUPPORTED_UPLOADS = ["pdf", "docx", "pptx", "csv", "xlsx", "md", "txt"]


if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Olá! Eu sou o Daniel, assistente da DNEL SOM. Você pode me perguntar "
                    "livremente, ou usar estas ideias como ponto de partida:\n\n"
                    "1️⃣ Férias, benefícios e banco de horas (RH)\n"
                    "2️⃣ Senhas, acessos e VPN (TI)\n"
                    "3️⃣ LGPD e questões contratuais (Jurídico)\n"
                    "4️⃣ Comissões, descontos e vendas (Comercial)\n"
                    "5️⃣ Trocas, garantias e reembolsos (Atendimento/Financeiro)\n"
                    "6️⃣ Analisar uma planilha ou documento que você enviar\n\n"
                    "Pode digitar o número, ou já escrever sua pergunta direto."
                ),
            }
        ]
    if "first_question_done" not in st.session_state:
        st.session_state.first_question_done = False
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
    if "last_analysis" not in st.session_state:
        st.session_state.last_analysis = None


def _chat_input():
    """Use Streamlit native file-aware chat input when available."""
    try:
        return st.chat_input(
            "Digite sua pergunta para o Daniel...",
            accept_file=True,
            file_type=SUPPORTED_UPLOADS,
        )
    except TypeError:
        question = st.chat_input("Digite sua pergunta para o Daniel...")
        uploaded_file = st.file_uploader("Anexar arquivo", type=SUPPORTED_UPLOADS)
        if question:
            return {"text": question, "files": [uploaded_file] if uploaded_file else []}
        return None


def _extract_input(raw_input):
    if raw_input is None:
        return None, None
    if isinstance(raw_input, dict):
        files = raw_input.get("files") or []
        return raw_input.get("text"), files[0] if files else None

    question = getattr(raw_input, "text", None)
    files = getattr(raw_input, "files", None) or []
    return question, files[0] if files else None


def _handle_message_safely(question: str, uploaded_file):
    try:
        return handle_message(
            question,
            uploaded_file=uploaded_file,
            first_interaction=not st.session_state.first_question_done,
            last_analysis=st.session_state.last_analysis,
        )
    except Exception as exc:
        if is_quota_error(exc):
            return ChatResult(
                mode="quota",
                answer=build_quota_message(exc),
                sources=[],
                payload=None,
            )
        return ChatResult(
            mode="error",
            answer=(
                "Encontrei um erro inesperado ao processar sua solicitação. "
                "Tente novamente em alguns instantes ou procure o administrador do Daniel AI."
            ),
            sources=[],
            payload=None,
        )


def main() -> None:
    st.set_page_config(page_title="Daniel AI - DNEL SOM", page_icon="🤖", layout="centered")
    _init_state()
    render_sidebar()

    st.title("🤖 Daniel AI")
    st.caption("Assistente corporativo inteligente da DNEL SOM Serviços Inteligentes")

    render_history(st.session_state.messages)

    raw_input = _chat_input()
    question, uploaded_file = _extract_input(raw_input)

    if not question:
        return

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("🧠 Analisando solicitação...")
        placeholder.markdown("📚 Buscando o melhor caminho...")

        result = _handle_message_safely(question, uploaded_file)
        st.session_state.first_question_done = True
        if result.mode == "analytics" and result.payload is not None:
            st.session_state.last_analysis = result.payload
        placeholder.empty()
        answer = render_result(result, key_prefix=f"current_{len(st.session_state.messages)}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "result": result,
        }
    )


if __name__ == "__main__":
    main()
