"""Custom CSS styles and responsive design system for Daniel AI."""

from __future__ import annotations

import streamlit as st

CUSTOM_CSS = """
<style>
/* Main App Container */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 900px;
}

/* Typography & Headers - Adaptive to Light & Dark themes */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-weight: 700;
}

/* Corporate Badges for Citations - Adaptive */
.source-badge-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
    margin-bottom: 8px;
}

.source-badge {
    display: inline-flex;
    align-items: center;
    background-color: rgba(59, 130, 246, 0.15);
    color: #3B82F6;
    border: 1px solid rgba(59, 130, 246, 0.35);
    padding: 4px 12px;
    border-radius: 16px;
    font-size: 0.82rem;
    font-weight: 600;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}

/* Category Grid & Buttons - Adaptive Styling */
div[data-testid="column"] button {
    border-radius: 10px !important;
    font-weight: 500 !important;
    padding: 12px 14px !important;
    min-height: 60px !important;
    transition: all 0.2s ease-in-out !important;
}

div[data-testid="column"] button:hover {
    border-color: #3B82F6 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 6px rgba(59, 130, 246, 0.15) !important;
}

/* Mobile Responsiveness Rules (@media query) */
@media (max-width: 768px) {
    .main .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Stack column buttons on mobile screens */
    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
        margin-bottom: 8px !important;
    }

    div[data-testid="column"] button {
        min-height: 50px !important;
        font-size: 0.9rem !important;
        padding: 10px 12px !important;
    }

    .source-badge {
        font-size: 0.78rem;
        padding: 3px 10px;
    }
}
</style>
"""


def load_custom_css() -> None:
    """Inject custom executive & mobile responsive CSS rules."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
