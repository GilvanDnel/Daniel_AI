import pandas as pd

from src.analytics.data_analyzer import analyze_dataframe


def test_analyze_dataframe_generates_basic_kpis():
    df = pd.DataFrame(
        {
            "data": ["2026-01-01", "2026-01-15", "2026-02-01"],
            "vendedor": ["Ana", "Ana", "Joao"],
            "valor_total": [100.0, 150.0, 80.0],
        }
    )

    result = analyze_dataframe(df)

    assert result.summary["linhas"] == 3
    assert result.summary["medida_principal"] == "valor_total"
    assert "ranking_por_vendedor" in result.rankings
    assert result.rankings["ranking_por_vendedor"].iloc[0]["vendedor"] == "Ana"
    assert result.time_series is not None
    assert result.insights
    assert result.recommendations
