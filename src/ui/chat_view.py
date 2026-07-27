"""Chat UI rendering helpers."""

from __future__ import annotations

import streamlit as st

from src.analytics.data_analyzer import build_bar_chart, build_time_series_chart
from src.reports.exporters import (
    export_dataframe_csv,
    export_dataframe_excel,
    export_summary_pdf,
    export_summary_pptx,
)
from src.services.chat_service import ChatResult


def _format_number(value, measure: str | None = None) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        if measure and any(token in measure.lower() for token in ["valor", "receita", "faturamento", "total"]):
            return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return str(value)


def _render_analytics_panel(analysis, key_prefix: str) -> None:
    measure = analysis.summary.get("medida_principal")

    st.markdown("#### Painel executivo")
    col1, col2, col3 = st.columns(3)
    col1.metric("Registros", analysis.summary.get("linhas", 0))
    col2.metric("Colunas", analysis.summary.get("colunas", 0))
    col3.metric("Total", _format_number(analysis.summary.get("total_medida_principal"), measure))

    if analysis.summary.get("valores_ausentes"):
        st.warning(
            f"Foram encontrados {analysis.summary['valores_ausentes']} valores ausentes. "
            "Use a análise como sinal inicial e valide a base antes de decisões finais."
        )

    if analysis.time_series is not None:
        st.markdown("#### Evolução temporal")
        st.dataframe(analysis.time_series, use_container_width=True)
        figure = build_time_series_chart(analysis.time_series)
        if figure is not None:
            st.plotly_chart(figure, use_container_width=True, key=f"{key_prefix}_time_series")

    for index, (name, ranking) in enumerate(analysis.rankings.items(), start=1):
        title = name.replace("_", " ").title()
        st.markdown(f"#### {title}")
        st.dataframe(ranking, use_container_width=True)
        figure = build_bar_chart(ranking)
        if figure is not None:
            st.plotly_chart(figure, use_container_width=True, key=f"{key_prefix}_ranking_{index}")

    with st.expander("Baixar resultados", expanded=False):
        st.download_button(
            "CSV",
            export_dataframe_csv(analysis.dataframe),
            "daniel_analise.csv",
            "text/csv",
            key=f"{key_prefix}_csv",
        )
        st.download_button(
            "Excel",
            export_dataframe_excel(analysis.dataframe),
            "daniel_analise.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"{key_prefix}_xlsx",
        )
        st.download_button(
            "PDF executivo",
            export_summary_pdf("Relatório Daniel AI", analysis),
            "daniel_relatorio.pdf",
            "application/pdf",
            key=f"{key_prefix}_pdf",
        )
        st.download_button(
            "PowerPoint executivo",
            export_summary_pptx("Relatório Daniel AI", analysis),
            "daniel_relatorio.pptx",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            key=f"{key_prefix}_pptx",
        )


def render_history(messages: list[dict]) -> None:
    for index, message in enumerate(messages):
        with st.chat_message(message["role"]):
            result = message.get("result")
            if result is not None:
                render_result(result, key_prefix=f"history_{index}")
            else:
                st.markdown(message["content"])


def render_result(result: ChatResult, key_prefix: str = "current") -> str:
    answer = result.answer
    if result.sources:
        answer += "\n\n---\n**Fontes consultadas:** " + ", ".join(result.sources)

    st.markdown(answer)

    if result.mode == "analytics" and result.payload is not None:
        _render_analytics_panel(result.payload, key_prefix=key_prefix)

    return answer
