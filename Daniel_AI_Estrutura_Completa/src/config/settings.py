"""Central configuration for Daniel AI."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    admin_username: str = os.getenv("ADMIN_USERNAME", "admin")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "Daniel@2026")
    chroma_db_path: Path = Path(os.getenv("CHROMA_DB_PATH", PROJECT_ROOT / "chroma_db"))
    company_docs_path: Path = Path(os.getenv("COMPANY_DOCS_PATH", PROJECT_ROOT / "company_docs"))
    temp_uploads_path: Path = Path(os.getenv("TEMP_UPLOADS_PATH", PROJECT_ROOT / "uploads_temp"))
    exports_path: Path = Path(os.getenv("EXPORTS_PATH", PROJECT_ROOT / "exports"))
    chat_model: str = os.getenv("GEMINI_CHAT_MODEL", "gemini-flash-latest")
    embedding_model: str = os.getenv("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001")
    rag_n_results: int = int(os.getenv("RAG_N_RESULTS", "4"))
    rag_max_distance: float = float(os.getenv("RAG_MAX_DISTANCE", "0.55"))


settings = Settings()
