"""Custom CSS styles and responsive design system for Daniel AI."""

from __future__ import annotations

import streamlit as st

CUSTOM_CSS = """
<style>
/* 1. ABSOLUTE REMOVAL OF ALL CHAT AVATARS (No robot icon, no human icon) */
[data-testid="stChatMessageAvatar"],
div[data-testid="stChatMessageAvatar"],
.stChatMessageAvatar,
img[data-testid="stChatMessageAvatar"] {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    visibility: hidden !important;
    opacity: 0 !important;
}

div[data-testid="stChatMessage"] {
    padding-left: 0 !important;
    margin-bottom: 12px !important;
}

/* 2. BASE FRAMEWORK FOR MAIN WINDOW CARD */
.main .block-container {
    max-width: 860px !important;
    border-radius: 16px !important;
    padding: 2.2rem 2.5rem 2.5rem 2.5rem !important;
    margin-top: 1.5rem !important;
    margin-bottom: 4.5rem !important;
    transition: background-color 0.2s ease, border-color 0.2s ease !important;
}

/* 3. DARK MODE RULES (Default & Dark Theme) */
@media (prefers-color-scheme: dark), [data-theme="dark"] {
    html, body, .stApp {
        background-color: #080A0F !important;
        color: #F1F5F9 !important;
    }

    .main .block-container {
        background-color: #121722 !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.75) !important;
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
    }

    div[data-testid="column"] button:hover {
        border-color: #3B82F6 !important;
        background-color: #2563EB !important;
        color: #FFFFFF !important;
    }

    .source-badge {
        background-color: rgba(59, 130, 246, 0.15) !important;
        color: #60A5FA !important;
        border: 1px solid rgba(59, 130, 246, 0.35) !important;
    }

    .app-footer-fixed {
        background-color: #080A0F !important;
        border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #94A3B8 !important;
    }

    .app-footer-fixed a {
        color: #60A5FA !important;
    }
}

/* 4. LIGHT MODE RULES (Legibilidade e contraste perfeito em Modo Claro) */
@media (prefers-color-scheme: light), [data-theme="light"] {
    html, body, .stApp {
        background-color: #EEF2F6 !important;
        color: #0F172A !important;
    }

    .main .block-container {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.08) !important;
    }

    .main .block-container p, 
    .main .block-container span, 
    .main .block-container div,
    .main .block-container li,
    .main .block-container label {
        color: #0F172A !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #0F172A !important;
    }

    .stCaption, caption {
        color: #475569 !important;
    }

    div[data-testid="column"] button {
        height: 52px !important;
        min-height: 52px !important;
        max-height: 52px !important;
        border-radius: 10px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        line-height: 1.2 !important;
        padding: 6px 10px !important;
    }

    div[data-testid="column"] button:hover {
        border-color: #2563EB !important;
        background-color: #2563EB !important;
        color: #FFFFFF !important;
    }

    .source-badge {
        background-color: #EFF6FF !important;
        color: #1D4ED8 !important;
        border: 1px solid #93C5FD !important;
    }

    .app-footer-fixed {
        background-color: #F8FAFC !important;
        border-top: 1px solid #E2E8F0 !important;
        color: #475569 !important;
    }

    .app-footer-fixed a {
        color: #2563EB !important;
    }
}

/* Common Layout Elements */
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
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    z-index: 9999;
}

.app-footer-fixed a {
    text-decoration: none;
    font-weight: 500;
    margin: 0 4px;
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




