import pandas as pd

from src.analytics.data_analyzer import analyze_dataframe


def test_analyze_dataframe_generates_basic_kpis():
    df = pd.DataFrame(
        {
            "vendedor": ["Ana", "Ana", "Joao"],
            "valor_total": [100.0, 150.0, 80.0],
        }
    )

    result = analyze_dataframe(df)

    assert result.summary["linhas"] == 3
    assert result.summary["medida_principal"] == "valor_total"
    assert "ranking_por_vendedor" in result.rankings
    assert result.rankings["ranking_por_vendedor"].iloc[0]["vendedor"] == "Ana"
