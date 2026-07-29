"""Custom CSS styles and responsive design system for Daniel AI."""

from __future__ import annotations

import streamlit as st

CUSTOM_CSS = """
<style>
/* 1. REMOVE ALL CHAT AVATARS (Hides robot and user emoji icons completely) */
[data-testid="stChatMessageAvatar"],
div[data-testid="stChatMessage"] [data-testid="stChatMessageAvatar"],
.stChatMessageAvatar {
    display: none !important;
}

div[data-testid="stChatMessage"] {
    padding-left: 0 !important;
    margin-bottom: 12px !important;
}

/* 2. BASE & DARK THEME STYLING (Default & Dark Mode) */
html, body, .stApp {
    background-color: #0B0E14 !important;
    color: #F1F5F9 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

.main .block-container {
    max-width: 860px !important;
    background-color: #141A26 !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 16px !important;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.75), 0 0 0 1px rgba(0, 0, 0, 0.4) !important;
    padding: 2.2rem 2.5rem 2.5rem 2.5rem !important;
    margin-top: 1.5rem !important;
    margin-bottom: 4.5rem !important;
}

.main .block-container p, 
.main .block-container span, 
.main .block-container div,
.main .block-container li,
.main .block-container label {
    color: #E2E8F0 !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #F8FAFC !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}

.stCaption, caption {
    color: #94A3B8 !important;
}

div[data-testid="column"] button {
    height: 52px !important;
    min-height: 52px !important;
    max-height: 52px !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    background-color: #1E2638 !important;
    color: #F8FAFC !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    line-height: 1.2 !important;
    padding: 6px 10px !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
}

div[data-testid="column"] button:hover {
    border-color: #3B82F6 !important;
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
}

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
    color: #60A5FA;
    border: 1px solid rgba(59, 130, 246, 0.35);
    padding: 5px 14px;
    border-radius: 14px;
    font-size: 0.82rem;
    font-weight: 600;
}

div[data-testid="stBottom"] {
    bottom: 32px !important;
    background-color: transparent !important;
}

.app-footer-fixed {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 32px;
    background-color: #0B0E14;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    color: #94A3B8;
    z-index: 9999;
}

.app-footer-fixed a {
    color: #60A5FA;
    text-decoration: none;
    font-weight: 500;
    margin: 0 4px;
}

/* 3. LIGHT THEME OVERRIDES (Garante 100% de legibilidade perfeita no modo Claro) */
[data-theme="light"] .stApp, 
body[data-theme="light"] .stApp {
    background-color: #F1F5F9 !important;
    color: #0F172A !important;
}

[data-theme="light"] .main .block-container {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.08) !important;
}

[data-theme="light"] .main .block-container p, 
[data-theme="light"] .main .block-container span, 
[data-theme="light"] .main .block-container div,
[data-theme="light"] .main .block-container li,
[data-theme="light"] .main .block-container label {
    color: #1E293B !important;
}

[data-theme="light"] h1, 
[data-theme="light"] h2, 
[data-theme="light"] h3, 
[data-theme="light"] h4, 
[data-theme="light"] h5, 
[data-theme="light"] h6 {
    color: #0F172A !important;
}

[data-theme="light"] .stCaption, 
[data-theme="light"] caption {
    color: #64748B !important;
}

[data-theme="light"] div[data-testid="column"] button {
    background-color: #F8FAFC !important;
    color: #0F172A !important;
    border: 1px solid #CBD5E1 !important;
}

[data-theme="light"] div[data-testid="column"] button:hover {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border-color: #2563EB !important;
}

[data-theme="light"] .source-badge {
    background-color: #EFF6FF !important;
    color: #1D4ED8 !important;
    border: 1px solid #93C5FD !important;
}

[data-theme="light"] .app-footer-fixed {
    background-color: #F8FAFC !important;
    border-top: 1px solid #E2E8F0 !important;
    color: #64748B !important;
}

[data-theme="light"] .app-footer-fixed a {
    color: #2563EB !important;
}

/* Mobile Responsiveness Rules */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1.5rem 1rem 2rem 1rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 4rem !important;
        border-radius: 12px !important;
    }

    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
        margin-bottom: 8px !important;
    }

    div[data-testid="column"] button {
        height: 48px !important;
        min-height: 48px !important;
        max-height: 48px !important;
        font-size: 0.88rem !important;
    }
}
</style>
"""


def load_custom_css() -> None:
    """Inject custom executive & mobile responsive CSS rules."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)



