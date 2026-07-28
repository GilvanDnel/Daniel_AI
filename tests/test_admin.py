"""Unit tests for admin auth and document management."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.admin.auth import validate_admin_login
from src.admin.document_manager import (
    delete_admin_document,
    get_available_sectors,
    list_company_documents,
    save_admin_document,
)
from src.config.settings import settings



class TestAdminAuth(unittest.TestCase):
    def test_auth_success(self):
        self.assertTrue(validate_admin_login(settings.admin_username, settings.admin_password))

    def test_auth_failure(self):
        self.assertFalse(validate_admin_login(settings.admin_username, "senha_incorreta_123"))
        self.assertFalse(validate_admin_login("usuario_inexistente_123", settings.admin_password))
        self.assertFalse(validate_admin_login("user", "pass"))


    def test_auth_empty(self):
        self.assertFalse(validate_admin_login("", "pass"))
        self.assertFalse(validate_admin_login("admin", None))
        self.assertFalse(validate_admin_login(None, None))


class TestDocumentManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_available_sectors(self):
        sectors = get_available_sectors()
        self.assertIn("rh", sectors)
        self.assertIn("ti", sectors)
        self.assertIn("juridico", sectors)

    def test_save_list_delete_document(self):
        with patch("src.admin.document_manager.settings") as mock_settings:
            mock_settings.company_docs_path = self.temp_path

            # 1. Save document
            content = b"Conteudo do documento de teste"
            saved_file = save_admin_document(
                file_name="teste_politica.md",
                content_bytes=content,
                sector="rh",
            )
            self.assertTrue(saved_file.exists())
            self.assertEqual(saved_file.read_bytes(), content)

            # 2. List documents
            doc_map = list_company_documents()
            self.assertIn("rh", doc_map)
            self.assertIn("teste_politica.md", doc_map["rh"])

            # 3. Delete document
            deleted = delete_admin_document(sector="rh", file_name="teste_politica.md")
            self.assertTrue(deleted)
            self.assertFalse(saved_file.exists())

            # 4. Delete non-existent document
            deleted_again = delete_admin_document(sector="rh", file_name="teste_politica.md")
            self.assertFalse(deleted_again)


if __name__ == "__main__":
    unittest.main()
