import unittest
from src.core.router import route_request


class TestRouter(unittest.TestCase):
    def test_routes_csv_upload_to_analytics(self):
        self.assertEqual(route_request("Analise este arquivo", "vendas.csv"), "analytics")

    def test_routes_pdf_upload_to_temporary_document(self):
        self.assertEqual(route_request("Resuma este arquivo", "relatorio.pdf"), "temporary_document")

    def test_routes_default_to_knowledge(self):
        self.assertEqual(route_request("Como solicito férias?"), "knowledge")


if __name__ == "__main__":
    unittest.main()
