"""Sidebar UI components with Admin features, Sector Filters, and System Metrics."""

from __future__ import annotations

import streamlit as st

from src.admin.auth import validate_admin_login
from src.admin.document_manager import (
    delete_admin_document,
    get_available_sectors,
    list_company_documents,
    save_admin_document,
)
from src.core.errors import build_quota_message, is_quota_error
from src.core.vector_store import SUPPORTED_DOC_EXTENSIONS, get_vector_store_stats, rebuild_base

ALLOWED_FILE_TYPES = [ext.lstrip(".") for ext in SUPPORTED_DOC_EXTENSIONS]


def render_sidebar() -> None:
    st.sidebar.title("Daniel AI")
    st.sidebar.caption("DNEL SOM Serviços Inteligentes")

    st.sidebar.divider()

    # --- 1. Filtro de Busca por Setor ---
    st.sidebar.markdown("### Filtro de Busca")
    sectors = get_available_sectors()
    sector_options = ["Todos os setores"] + [s.upper() for s in sectors]

    if "selected_sector_filter" not in st.session_state:
        st.session_state.selected_sector_filter = "Todos os setores"

    selected_filter = st.sidebar.selectbox(
        "Refinar busca por área:",
        sector_options,
        index=sector_options.index(st.session_state.selected_sector_filter)
        if st.session_state.selected_sector_filter in sector_options
        else 0,
        key="sector_filter_selectbox",
    )
    st.session_state.selected_sector_filter = selected_filter

    st.sidebar.divider()

    # --- 2. Painel Admin ---
    with st.sidebar.expander("Painel Admin", expanded=st.session_state.get("admin_authenticated", False)):
        if not st.session_state.get("admin_authenticated"):
            username = st.text_input("Usuário admin", key="admin_user_input")
            password = st.text_input("Senha", type="password", key="admin_pass_input")
            if st.button("Entrar como admin", use_container_width=True):
                if validate_admin_login(username, password):
                    st.session_state.admin_authenticated = True
                    st.success("Admin autenticado.")
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")
        else:
            st.success("Sessão Admin Ativa")
            if st.button("Sair / Encerrar Sessão", use_container_width=True):
                st.session_state.admin_authenticated = False
                st.rerun()

            st.divider()

            # --- Dashboard de Métricas da Base ---
            st.markdown("### Saúde & Métricas da Base")
            try:
                stats = get_vector_store_stats()
                st.metric("Total de Chunks Indexados", stats["total_chunks"])
                st.metric("Tamanho no Disco", f"{stats['db_size_mb']} MB")
                if stats["sector_counts"]:
                    with st.expander("Distribuição por Setor", expanded=False):
                        for s_name, count in stats["sector_counts"].items():
                            st.write(f"• **{s_name.upper()}**: {count} chunks")
            except Exception as err:
                st.caption(f"Erro ao obter estatísticas: {err}")

            st.divider()

            # --- Upload de novo documento ---
            st.markdown("### Enviar Documento")
            selected_sector = st.selectbox("Setor do documento", sectors, key="upload_sector_select")
            uploaded_doc = st.file_uploader(
                "Escolha o arquivo",
                type=ALLOWED_FILE_TYPES,
                key="admin_doc_uploader",
            )
            auto_reindex = st.checkbox("Reindexar automaticamente", value=True, key="auto_reindex_cb")

            if st.button("Salvar Documento", use_container_width=True):
                if uploaded_doc is not None:
                    try:
                        content = uploaded_doc.read()
                        save_admin_document(
                            file_name=uploaded_doc.name,
                            content_bytes=content,
                            sector=selected_sector,
                        )
                        st.success(f"Arquivo `{uploaded_doc.name}` salvo no setor `{selected_sector}`!")

                        if auto_reindex:
                            with st.spinner("Reconstruindo base vetorial..."):
                                result = rebuild_base()
                                st.success("Base atualizada!")
                                st.json(result)
                    except Exception as exc:
                        st.error(f"Erro ao salvar arquivo: {exc}")
                else:
                    st.warning("Selecione um arquivo para enviar.")

            st.divider()

            # --- Listar e excluir documentos ---
            st.markdown("### Documentos da Empresa")
            doc_map = list_company_documents()
            total_docs = sum(len(files) for files in doc_map.values())

            if total_docs == 0:
                st.info("Nenhum documento cadastrado.")
            else:
                for sector, files in doc_map.items():
                    if files:
                        with st.expander(f"{sector.upper()} ({len(files)})", expanded=False):
                            for fname in files:
                                col1, col2 = st.columns([3, 1])
                                col1.write(f"`{fname}`")
                                if col2.button("Excluir", key=f"del_{sector}_{fname}", help=f"Excluir {fname}"):
                                    if delete_admin_document(sector, fname):
                                        st.success(f"Removido: `{fname}`")
                                        if auto_reindex:
                                            rebuild_base()
                                        st.rerun()
                                    else:
                                        st.error("Erro ao remover arquivo.")

            st.divider()

            # --- Reindexação Manual ---
            st.markdown("### Manutenção")
            st.caption("A reindexação chama embeddings da Gemini API e pode consumir cota.")
            if st.button("Reindexar Base Inteira", use_container_width=True):
                try:
                    with st.spinner("Reconstruindo base vetorial..."):
                        result = rebuild_base()
                    if result:
                        st.success("Base reconstruída com sucesso!")
                        st.json(result)
                    else:
                        st.info("Nenhum documento encontrado em company_docs/.")
                except Exception as exc:
                    if is_quota_error(exc):
                        st.error(build_quota_message(exc))
                    else:
                        st.error(f"Erro ao reindexar: {exc}")

