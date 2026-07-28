"""Custom CSS styles and responsive design system for Daniel AI."""

from __future__ import annotations

import streamlit as st

CUSTOM_CSS = """
<style>
/* App Background & Base Layout */
.stApp {
    background-color: #0E1117;
}

/* Framed Main App Container Window */
.main .block-container {
    padding: 2.5rem 2.5rem 3rem 2.5rem;
    max-width: 880px;
    background: rgba(22, 27, 34, 0.85);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 18px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
    margin-top: 2rem;
    margin-bottom: 3rem;
}

/* Typography & Headers */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-weight: 700;
    letter-spacing: -0.02em;
}

/* Clean Corporate Badges for Citations */
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
    background-color: rgba(59, 130, 246, 0.12);
    color: #60A5FA;
    border: 1px solid rgba(59, 130, 246, 0.3);
    padding: 5px 14px;
    border-radius: 14px;
    font-size: 0.82rem;
    font-weight: 600;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

/* Category Grid & Buttons Styling */
div[data-testid="column"] button {
    border-radius: 10px !important;
    font-weight: 500 !important;
    padding: 12px 14px !important;
    min-height: 56px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    background-color: rgba(255, 255, 255, 0.03) !important;
    transition: all 0.2s ease-in-out !important;
}

div[data-testid="column"] button:hover {
    border-color: #3B82F6 !important;
    background-color: rgba(59, 130, 246, 0.1) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15) !important;
}

/* Mobile Responsiveness Rules */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1.5rem 1rem 2rem 1rem;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        border-radius: 12px;
    }

    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
        margin-bottom: 8px !important;
    }

    div[data-testid="column"] button {
        min-height: 48px !important;
        font-size: 0.9rem !important;
        padding: 10px 12px !important;
    }

    .source-badge {
        font-size: 0.78rem;
        padding: 4px 10px;
    }
}
</style>
"""


def load_custom_css() -> None:
    """Inject custom executive & mobile responsive CSS rules."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

