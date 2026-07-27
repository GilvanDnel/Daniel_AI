"""Simple admin authentication for the MVP."""

from __future__ import annotations

import hmac

from src.config.settings import settings


def validate_admin_login(username: str, password: str) -> bool:
    """Validate admin credentials stored in environment variables."""
    return hmac.compare_digest(username, settings.admin_username) and hmac.compare_digest(
        password,
        settings.admin_password,
    )
