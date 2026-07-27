"""Fallback routing for unanswered or out-of-scope questions."""

from __future__ import annotations

import unicodedata


SECTORS = {
    "rh": {
        "name": "Recursos Humanos",
        "email": "rh@dnelsom.com.br",
        "keywords": ["ferias", "beneficio", "salario", "folga", "banco de horas", "jornada"],
    },
    "ti": {
        "name": "Tecnologia e Dados",
        "email": "suporte.ti@dnelsom.com.br",
        "keywords": ["vpn", "acesso", "senha", "sistema", "computador", "erro tecnico"],
    },
    "juridico": {
        "name": "Jurídico",
        "email": "juridico@dnelsom.com.br",
        "keywords": ["contrato", "clausula", "juridico", "processo", "risco legal"],
    },
    "compliance": {
        "name": "Compliance",
        "email": "compliance@dnelsom.com.br",
        "keywords": ["fraude", "denuncia", "etica", "conduta", "assedio"],
    },
    "comercial": {
        "name": "Comercial",
        "email": "comercial@dnelsom.com.br",
        "keywords": ["venda", "cliente", "meta", "comissao", "pedido"],
    },
    "financeiro": {
        "name": "Financeiro",
        "email": "financeiro@dnelsom.com.br",
        "keywords": ["pagamento", "reembolso", "nota fiscal", "cobranca", "financeiro"],
    },
    "atendimento": {
        "name": "Atendimento",
        "email": "atendimento@dnelsom.com.br",
        "keywords": ["reclamacao", "troca", "suporte cliente", "atendimento"],
    },
}


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(char for char in text if not unicodedata.combining(char))


def detect_sector(question: str) -> dict:
    """Return the most likely responsible sector for a question."""
    normalized = normalize_text(question)
    for sector in SECTORS.values():
        if any(keyword in normalized for keyword in sector["keywords"]):
            return sector
    return {
        "name": "setor responsável",
        "email": "atendimento@dnelsom.com.br",
        "keywords": [],
    }


def build_escalation_message(question: str) -> str:
    """Create a deterministic fallback message."""
    sector = detect_sector(question)
    return (
        "Não encontrei essa informação na base de conhecimento autorizada da DNEL SOM. "
        f"Para esse assunto, recomendo procurar o setor de {sector['name']} pelo e-mail "
        f"{sector['email']}."
    )
