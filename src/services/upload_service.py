"""Upload handling for temporary user files."""

from __future__ import annotations

from pathlib import Path

from src.config.settings import settings


def save_uploaded_file(uploaded_file) -> Path:
    """Save a Streamlit uploaded file under the temporary upload directory."""
    settings.temp_uploads_path.mkdir(parents=True, exist_ok=True)
    safe_name = Path(uploaded_file.name).name
    target = settings.temp_uploads_path / safe_name
    target.write_bytes(uploaded_file.getvalue())
    return target
