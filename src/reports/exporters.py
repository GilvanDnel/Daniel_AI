"""Report export helpers for Daniel AI."""

from __future__ import annotations

from io import BytesIO
from typing import Any

import pandas as pd
from pptx import Presentation
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def export_dataframe_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")


def export_dataframe_excel(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="resultado")
    return output.getvalue()


def _analysis_parts(analysis_or_summary: Any) -> tuple[dict[str, Any], list[str], list[str]]:
    if isinstance(analysis_or_summary, dict):
        return analysis_or_summary, [], []
    return (
        getattr(analysis_or_summary, "summary", {}),
        getattr(analysis_or_summary, "insights", []),
        getattr(analysis_or_summary, "recommendations", []),
    )


def export_summary_pdf(title: str, analysis_or_summary: Any) -> bytes:
    summary, insights, recommendations = _analysis_parts(analysis_or_summary)
    output = BytesIO()
    document = SimpleDocTemplate(output, pagesize=A4, title=title)
    styles = getSampleStyleSheet()
    story = [Paragraph(title, styles["Title"]), Spacer(1, 12)]

    if insights:
        story.append(Paragraph("Leitura Executiva", styles["Heading2"]))
        for insight in insights:
            story.append(Paragraph(f"- {insight}", styles["BodyText"]))
        story.append(Spacer(1, 10))

    if recommendations:
        story.append(Paragraph("Recomendações", styles["Heading2"]))
        for recommendation in recommendations:
            story.append(Paragraph(f"- {recommendation}", styles["BodyText"]))
        story.append(Spacer(1, 10))

    story.append(Paragraph("KPIs", styles["Heading2"]))
    for key, value in summary.items():
        label = key.replace("_", " ").title()
        story.append(Paragraph(f"<b>{label}:</b> {value}", styles["BodyText"]))
        story.append(Spacer(1, 5))

    document.build(story)
    return output.getvalue()


def export_summary_pptx(title: str, analysis_or_summary: Any) -> bytes:
    summary, insights, recommendations = _analysis_parts(analysis_or_summary)
    presentation = Presentation()

    slide = presentation.slides.add_slide(presentation.slide_layouts[0])
    slide.shapes.title.text = title
    slide.placeholders[1].text = "Resumo executivo gerado pelo Daniel AI"

    if insights:
        slide = presentation.slides.add_slide(presentation.slide_layouts[1])
        slide.shapes.title.text = "Leitura Executiva"
        body = slide.placeholders[1].text_frame
        body.clear()
        for insight in insights[:5]:
            paragraph = body.add_paragraph()
            paragraph.text = insight
            paragraph.level = 0

    if recommendations:
        slide = presentation.slides.add_slide(presentation.slide_layouts[1])
        slide.shapes.title.text = "Recomendações"
        body = slide.placeholders[1].text_frame
        body.clear()
        for recommendation in recommendations[:5]:
            paragraph = body.add_paragraph()
            paragraph.text = recommendation
            paragraph.level = 0

    slide = presentation.slides.add_slide(presentation.slide_layouts[1])
    slide.shapes.title.text = "Principais Indicadores"
    body = slide.placeholders[1].text_frame
    body.clear()
    for key, value in summary.items():
        paragraph = body.add_paragraph()
        paragraph.text = f"{key.replace('_', ' ').title()}: {value}"
        paragraph.level = 0

    output = BytesIO()
    presentation.save(output)
    return output.getvalue()
