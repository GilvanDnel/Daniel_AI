"""High-level request orchestration for Daniel AI."""

from __future__ import annotations

from dataclasses import dataclass

from src.analytics.data_analyzer import analyze_dataframe, load_dataset
from src.core.rag_engine import ask as ask_knowledge_base
from src.core.router import route_request
from src.services.document_service import summarize_temporary_document
from src.services.upload_service import save_uploaded_file


@dataclass
class ChatResult:
    mode: str
    answer: str
    sources: list[str]
    payload: object | None = None


def handle_message(question: str, uploaded_file=None, first_interaction: bool = False) -> ChatResult:
    """Route a user message to the correct Daniel module."""
    file_name = getattr(uploaded_file, "name", None)
    mode = route_request(question, uploaded_file_name=file_name)

    if mode == "analytics" and uploaded_file is not None:
        df = load_dataset(uploaded_file, file_name)
        analysis = analyze_dataframe(df)
        measure = analysis.summary.get("medida_principal") or "medida numérica"
        answer = (
            "Analisei a planilha enviada. "
            f"Encontrei {analysis.summary['linhas']} linhas, "
            f"{analysis.summary['colunas']} colunas e usei '{measure}' como medida principal."
        )
        return ChatResult(mode=mode, answer=answer, sources=[], payload=analysis)

    if mode == "temporary_document" and uploaded_file is not None:
        temporary_path = save_uploaded_file(uploaded_file)
        preview = summarize_temporary_document(temporary_path)
        return ChatResult(
            mode=mode,
            answer=(
                "Recebi e li o documento temporário. Ele não foi adicionado à base corporativa "
                "permanente.\n\n"
                f"Prévia extraída:\n\n{preview}"
            ),
            sources=[],
            payload=temporary_path,
        )

    result = ask_knowledge_base(question, first_interaction=first_interaction)
    return ChatResult(
        mode="knowledge",
        answer=result["resposta"],
        sources=result.get("fontes", []),
        payload=result,
    )
