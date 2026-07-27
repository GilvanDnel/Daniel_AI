from src.core.router import route_request


def test_routes_csv_upload_to_analytics():
    assert route_request("Analise este arquivo", "vendas.csv") == "analytics"


def test_routes_pdf_upload_to_temporary_document():
    assert route_request("Resuma este arquivo", "relatorio.pdf") == "temporary_document"


def test_routes_default_to_knowledge():
    assert route_request("Como solicito férias?") == "knowledge"
