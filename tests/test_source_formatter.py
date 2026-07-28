import unittest
from src.utils.source_formatter import format_source_name


class TestSourceFormatter(unittest.TestCase):
    def test_format_known_titles(self):
        self.assertEqual(format_source_name("politica_de_ferias.md"), "Política de Férias")
        self.assertEqual(format_source_name("codigo_de_conduta.md"), "Código de Conduta & Compliance")
        self.assertEqual(format_source_name("politica_reembolso.md"), "Política de Reembolso de Despesas")

    def test_format_unknown_titles(self):
        self.assertEqual(format_source_name("novo_documento_teste.pdf"), "Novo Documento Teste")
        self.assertEqual(format_source_name("guia-de-acesso.docx"), "Guia de Acesso")

    def test_empty_or_none(self):
        self.assertEqual(format_source_name(""), "Documento Corporativo")
        self.assertEqual(format_source_name(None), "Documento Corporativo")


if __name__ == "__main__":
    unittest.main()
