"""
rag_engine.py

O "cérebro" do Daniel: recebe uma pergunta, busca os trechos relevantes na
base vetorial (vector_store) e usa o Gemini para gerar uma resposta,
SEMPRE citando as fontes e NUNCA inventando informação fora do contexto
recuperado.
"""

import os

import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

from src.core.vector_store import query as vector_query

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=_PROJECT_ROOT / ".env")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_NAME = "gemini-flash-latest"

SYSTEM_PROMPT = """Você é o Daniel, o assistente corporativo inteligente da
empresa DNEL SOM Serviços Inteligentes.

REGRAS OBRIGATÓRIAS:
1. Responda SOMENTE com base nos trechos de contexto fornecidos abaixo.
2. Se a resposta não estiver claramente presente no contexto, diga que não
   encontrou essa informação na base de conhecimento e sugira o setor
   responsável para o usuário procurar.
3. Nunca invente, deduza ou complete informações que não estejam no contexto.
4. Sempre que possível, cite o documento de origem da informação.
5. Seja claro, objetivo e use linguagem profissional, mas acessível.
6. {instrucao_apresentacao}
"""

INSTRUCAO_PRIMEIRA_INTERACAO = (
    "Esta é a primeira pergunta da conversa: pode se apresentar brevemente "
    "como o Daniel antes de responder."
)
INSTRUCAO_DEMAIS_INTERACOES = (
    "Você já se apresentou anteriormente nesta conversa. NÃO se apresente "
    "de novo (não repita seu nome, função ou saudação institucional) — "
    "vá direto ao ponto e responda a pergunta."
)

SETORES_ESCALONAMENTO = {
    "rh": "rh@dnelsom.com.br",
    "ti": "ti@dnelsom.com.br",
    "juridico": "juridico@dnelsom.com.br",
    "comercial": "comercial@dnelsom.com.br",
    "atendimento": "atendimento@dnelsom.com.br",
    "financeiro": "financeiro@dnelsom.com.br",
}


def _montar_contexto(trechos: list[dict]) -> str:
    if not trechos:
        return "Nenhum trecho relevante foi encontrado na base de conhecimento."

    partes = []
    for t in trechos:
        partes.append(f"[Fonte: {t['fonte']} | Setor: {t['setor']}]\n{t['texto']}")

    return "\n\n---\n\n".join(partes)


def ask(pergunta: str, n_results: int = 4, primeira_interacao: bool = False) -> dict:
    """
    Executa o fluxo completo de RAG: busca + geração de resposta.

    Args:
        pergunta: pergunta do usuário
        n_results: quantos trechos buscar na base vetorial
        primeira_interacao: se True, o Daniel pode se apresentar. Se False,
            ele é instruído a não repetir a apresentação institucional.

    Returns:
        dict com "resposta" (str) e "fontes" (list de nomes de arquivo únicos)
    """
    trechos = vector_query(pergunta, n_results=n_results)
    contexto = _montar_contexto(trechos)

    instrucao_apresentacao = (
        INSTRUCAO_PRIMEIRA_INTERACAO if primeira_interacao else INSTRUCAO_DEMAIS_INTERACOES
    )
    system_prompt = SYSTEM_PROMPT.format(instrucao_apresentacao=instrucao_apresentacao)

    prompt_completo = f"""{system_prompt}

CONTEXTO RECUPERADO DA BASE DE CONHECIMENTO:
{contexto}

PERGUNTA DO USUÁRIO:
{pergunta}

Responda seguindo estritamente as regras acima."""

    model = genai.GenerativeModel(MODEL_NAME)
    resposta = model.generate_content(prompt_completo)

    fontes_unicas = sorted({t["fonte"] for t in trechos}) if trechos else []

    return {
        "resposta": resposta.text,
        "fontes": fontes_unicas,
    }


def sugerir_escalonamento(setor: str) -> str:
    """Retorna o e-mail de contato do setor, para uso quando o Daniel não sabe a resposta."""
    setor = setor.lower().strip()
    email = SETORES_ESCALONAMENTO.get(setor)
    if email:
        return f"Recomendo entrar em contato com o setor de {setor.upper()} pelo e-mail {email}."
    return "Recomendo procurar o setor responsável internamente para mais informações."