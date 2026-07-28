"""Source name sanitizer and formatter for corporate citations."""

from __future__ import annotations

from pathlib import Path

# Mapping of file stem to clean corporate titles
KNOWN_TITLES: dict[str, str] = {
    "politica_de_ferias": "Política de Férias",
    "politica_banco_de_horas": "Política de Banco de Horas",
    "manual_acesso": "Manual de Acesso e TI",
    "orientacoes_juridicas": "Orientações Jurídicas",
    "politica_contratos": "Política de Contratos Corporativos",
    "politica_comercial": "Política Comercial e Vendas",
    "faq_clientes": "FAQ e Atendimento ao Cliente",
    "codigo_de_conduta": "Código de Conduta & Compliance",
    "politica_reembolso": "Política de Reembolso de Despesas",
    "rotinas_financeiras": "Rotinas Financeiras",
    "lgpd": "Política de LGPD e Privacidade",
}


def format_source_name(raw_source: str) -> str:
    """Convert raw file paths or stems into clean, professional corporate titles.
    
    Examples:
    - 'politica_de_ferias.md' -> 'Política de Férias'
    - 'rh/politica_banco_de_horas.pdf' -> 'Política de Banco de Horas'
    - 'documento_desconhecido.docx' -> 'Documento Desconhecido'
    """
    if not raw_source or not raw_source.strip():
        return "Documento Corporativo"

    stem = Path(raw_source).stem.lower().strip()

    if stem in KNOWN_TITLES:
        return KNOWN_TITLES[stem]

    # General fallback for any new uploaded files:
    # Replace underscores/hyphens with spaces and apply Title Case
    clean = stem.replace("_", " ").replace("-", " ")
    words = clean.split()
    capitalized = [
        word if word.lower() in {"de", "da", "do", "dos", "das", "e", "em"} else word.capitalize()
        for word in words
    ]
    formatted = " ".join(capitalized)
    return formatted if formatted else "Documento Corporativo"
