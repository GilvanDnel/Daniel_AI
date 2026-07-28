"""Simple admin authentication for the MVP."""

from __future__ import annotations

import hmac

from src.config.settings import settings


def validate_admin_login(username: str | None, password: str | None) -> bool:
    """Validate admin credentials stored in environment variables."""
    if not username or not password:
        return False
    return hmac.compare_digest(str(username), settings.admin_username) and hmac.compare_digest(
        str(password),
        settings.admin_password,
    )

