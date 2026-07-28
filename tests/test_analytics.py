import io
import unittest
import pandas as pd

from src.analytics.data_analyzer import analyze_dataframe, load_dataset
from src.reports.exporters import export_summary_pdf, export_summary_pptx


class TestAnalytics(unittest.TestCase):
    def test_analyze_dataframe_generates_basic_kpis(self):
        df = pd.DataFrame(
            {
                "data": ["2026-01-01", "2026-01-15", "2026-02-01"],
                "vendedor": ["Ana", "Ana", "Joao"],
                "valor_total": [100.0, 150.0, 80.0],
            }
        )

        result = analyze_dataframe(df)

        self.assertEqual(result.summary["linhas"], 3)
        self.assertEqual(result.summary["medida_principal"], "valor_total")
        self.assertIn("ranking_por_vendedor", result.rankings)
        self.assertEqual(result.rankings["ranking_por_vendedor"].iloc[0]["vendedor"], "Ana")
        self.assertIsNotNone(result.time_series)
        self.assertTrue(result.insights)
        self.assertTrue(result.recommendations)

    def test_load_dataset_semicolon_csv(self):
        csv_data = "vendedor;valor\nMaria;250\nPedro;300\n"
        file_obj = io.BytesIO(csv_data.encode("latin-1"))
        df = load_dataset(file_obj, "vendas_br.csv")

        self.assertEqual(len(df.columns), 2)
        self.assertIn("vendedor", df.columns)
        self.assertEqual(len(df), 2)

    def test_export_pdf_and_pptx_robustness(self):
        df = pd.DataFrame({"item": ["A < B", "C & D"], "valor": [10, 20]})
        result = analyze_dataframe(df)

        pdf_bytes = export_summary_pdf("Relatório Teste", result)
        pptx_bytes = export_summary_pptx("Relatório Teste", result)

        self.assertGreater(len(pdf_bytes), 0)
        self.assertGreater(len(pptx_bytes), 0)


if __name__ == "__main__":
    unittest.main()
