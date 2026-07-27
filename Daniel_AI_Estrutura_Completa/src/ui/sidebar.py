"""Sidebar UI components."""

from __future__ import annotations

import streamlit as st

from src.admin.auth import validate_admin_login
from src.core.vector_store import rebuild_base


def render_sidebar() -> None:
    st.sidebar.title("Daniel AI")
    st.sidebar.caption("DNEL SOM Serviços Inteligentes")

    with st.sidebar.expander("Admin", expanded=False):
        username = st.text_input("Usuário admin")
        password = st.text_input("Senha", type="password")
        if st.button("Entrar como admin"):
            st.session_state.admin_authenticated = validate_admin_login(username, password)
            if st.session_state.admin_authenticated:
                st.success("Admin autenticado.")
            else:
                st.error("Credenciais inválidas.")

        if st.session_state.get("admin_authenticated"):
            st.warning("A reindexação chama embeddings e pode consumir cota da API.")
            if st.button("Reindexar base corporativa"):
                with st.spinner("Reconstruindo base vetorial..."):
                    result = rebuild_base()
                if result:
                    st.success("Base reconstruída.")
                    st.json(result)
                else:
                    st.info("Nenhum documento encontrado em company_docs/.")
