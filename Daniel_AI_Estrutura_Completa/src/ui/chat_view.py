"""Chat UI rendering helpers."""

from __future__ import annotations

import streamlit as st

from src.analytics.data_analyzer import build_bar_chart
from src.reports.exporters import (
    export_dataframe_csv,
    export_dataframe_excel,
    export_summary_pdf,
    export_summary_pptx,
)
from src.services.chat_service import ChatResult


def render_history(messages: list[dict]) -> None:
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def render_result(result: ChatResult) -> str:
    answer = result.answer
    if result.sources:
        answer += "\n\n---\n**Fontes consultadas:** " + ", ".join(result.sources)

    st.markdown(answer)

    if result.mode == "analytics" and result.payload is not None:
        analysis = result.payload
        st.subheader("KPIs")
        st.json(analysis.summary)

        for name, ranking in analysis.rankings.items():
            st.subheader(name.replace("_", " ").title())
            st.dataframe(ranking, use_container_width=True)
            figure = build_bar_chart(ranking)
            if figure is not None:
                st.plotly_chart(figure, use_container_width=True)

        st.download_button(
            "Baixar dados em CSV",
            export_dataframe_csv(analysis.dataframe),
            "daniel_analise.csv",
            "text/csv",
        )
        st.download_button(
            "Baixar dados em Excel",
            export_dataframe_excel(analysis.dataframe),
            "daniel_analise.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        st.download_button(
            "Baixar resumo em PDF",
            export_summary_pdf("Relatório Daniel AI", analysis.summary),
            "daniel_relatorio.pdf",
            "application/pdf",
        )
        st.download_button(
            "Baixar apresentação em PowerPoint",
            export_summary_pptx("Relatório Daniel AI", analysis.summary),
            "daniel_relatorio.pptx",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )

    return answer
