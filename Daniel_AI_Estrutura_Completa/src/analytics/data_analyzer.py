"""Initial analytics module for temporary CSV/XLSX uploads."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any

import pandas as pd

try:
    import plotly.express as px
except ImportError:
    px = None


@dataclass
class AnalysisResult:
    summary: dict[str, Any]
    rankings: dict[str, pd.DataFrame]
    dataframe: pd.DataFrame


def load_dataset(file_obj, file_name: str) -> pd.DataFrame:
    """Load CSV or XLSX from a Streamlit upload or local path."""
    suffix = Path(file_name).suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(file_obj)
    if suffix == ".xlsx":
        return pd.read_excel(file_obj)
    raise ValueError(f"Formato não suportado para analytics: {suffix}")


def _find_measure_column(df: pd.DataFrame) -> str | None:
    preferred = [
        "valor_total",
        "receita",
        "faturamento",
        "valor",
        "total",
        "quantidade",
    ]
    lower_map = {column.lower(): column for column in df.columns}
    for name in preferred:
        if name in lower_map and pd.api.types.is_numeric_dtype(df[lower_map[name]]):
            return lower_map[name]

    numeric_columns = list(df.select_dtypes(include="number").columns)
    return numeric_columns[0] if numeric_columns else None


def _candidate_dimensions(df: pd.DataFrame) -> list[str]:
    preferred = ["vendedor", "produto", "regiao", "cliente", "categoria", "setor"]
    lower_map = {column.lower(): column for column in df.columns}
    dimensions = [lower_map[name] for name in preferred if name in lower_map]
    if dimensions:
        return dimensions
    return list(df.select_dtypes(include=["object", "category"]).columns[:3])


def analyze_dataframe(df: pd.DataFrame) -> AnalysisResult:
    """Generate basic KPIs and rankings from a dataframe."""
    measure = _find_measure_column(df)
    summary = {
        "linhas": int(len(df)),
        "colunas": int(len(df.columns)),
        "colunas_numericas": list(df.select_dtypes(include="number").columns),
        "colunas_texto": list(df.select_dtypes(include=["object", "category"]).columns),
        "valores_ausentes": int(df.isna().sum().sum()),
        "medida_principal": measure,
    }

    if measure:
        summary["total_medida_principal"] = float(df[measure].sum())
        summary["media_medida_principal"] = float(df[measure].mean())

    rankings = {}
    if measure:
        for dimension in _candidate_dimensions(df):
            ranking = (
                df.groupby(dimension, dropna=False)[measure]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
                .head(10)
            )
            rankings[f"ranking_por_{dimension}"] = ranking

    return AnalysisResult(summary=summary, rankings=rankings, dataframe=df)


def build_bar_chart(ranking: pd.DataFrame):
    """Create a Plotly bar chart from a ranking dataframe."""
    if px is None:
        return None
    if ranking.empty or len(ranking.columns) < 2:
        return None
    x_column, y_column = ranking.columns[0], ranking.columns[1]
    return px.bar(
        ranking,
        x=x_column,
        y=y_column,
        title=f"{y_column} por {x_column}",
        text_auto=True,
    )


def dataframe_to_excel_bytes(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="dados")
    return output.getvalue()
