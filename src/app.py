"""
app.py

Interface principal do Daniel AI — chat corporativo em Streamlit.
Versão MVP: apenas o fluxo de Knowledge (RAG). Analytics e painel
administrativo entram em sprints seguintes.
"""

import sys
from pathlib import Path

# Garante que a raiz do projeto (pasta que contém "src/") esteja no sys.path,
# independente de onde o comando "streamlit run" for executado.
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st

from src.core.rag_engine import ask

st.set_page_config(
    page_title="Daniel AI — DNEL SOM",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Daniel")
st.caption("Assistente corporativo inteligente da DNEL SOM Serviços Inteligentes")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {
            "role": "assistant",
            "content": "Olá! Eu sou o Daniel. Posso responder perguntas sobre "
                       "documentos internos da empresa. Como posso ajudar?",
        }
    ]

if "primeira_pergunta_feita" not in st.session_state:
    st.session_state.primeira_pergunta_feita = False

# Exibe o histórico da conversa
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Barra de chat (nativa do Streamlit, com anexo embutido) ---
# Usar accept_file mantém o chat_input "solto" na página, o que faz o
# Streamlit fixá-lo automaticamente na parte inferior da tela — colocar
# esse widget dentro de st.columns() quebra essa fixação.
entrada = st.chat_input(
    "Digite sua pergunta para o Daniel...",
    accept_file=True,
    file_type=["pdf", "docx", "pptx", "csv", "xlsx", "md"],
)

pergunta = None
arquivo = None

if entrada:
    pergunta = entrada.text
    if entrada.files:
        arquivo = entrada.files[0]

if pergunta:
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("🧠 Analisando...")
        placeholder.markdown("📚 Consultando documentos...")

        resultado = ask(pergunta, primeira_interacao=not st.session_state.primeira_pergunta_feita)
        st.session_state.primeira_pergunta_feita = True

        resposta = resultado["resposta"]
        fontes = resultado["fontes"]

        if fontes:
            resposta += "\n\n---\n📄 **Fontes consultadas:** " + ", ".join(fontes)

        placeholder.markdown(resposta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})

if arquivo is not None:
    st.info(
        f"📎 Arquivo '{arquivo.name}' anexado. A análise de arquivos temporários "
        f"será implementada no próximo sprint (Analytics)."
    )