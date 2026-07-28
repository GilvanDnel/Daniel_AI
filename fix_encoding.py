"""
fix_encoding.py

Corrige o bug de "mojibake" (texto UTF-8 que foi salvo/lido com codificação
errada, tipo "JurÃdico" em vez de "Jurídico") em todos os arquivos .py e .md
do projeto.
"""

from pathlib import Path

try:
    import ftfy
except ImportError:
    raise SystemExit(
        "Falta instalar a biblioteca 'ftfy'. Rode: pip install ftfy"
    )

PASTAS_ALVO = ["src", "company_docs", "docs"]
EXTENSOES = {".py", ".md"}

arquivos_corrigidos = []

for pasta in PASTAS_ALVO:
    caminho_pasta = Path(pasta)
    if not caminho_pasta.exists():
        continue

    for arquivo in caminho_pasta.rglob("*"):
        if arquivo.suffix not in EXTENSOES or not arquivo.is_file():
            continue

        texto_original = arquivo.read_text(encoding="utf-8", errors="replace")
        texto_corrigido = ftfy.fix_text(texto_original)

        if texto_corrigido != texto_original:
            arquivo.write_text(texto_corrigido, encoding="utf-8")
            arquivos_corrigidos.append(str(arquivo))

if arquivos_corrigidos:
    print(f"{len(arquivos_corrigidos)} arquivo(s) corrigido(s):\n")
    for a in arquivos_corrigidos:
        print(f"  - {a}")
else:
    print("Nenhum arquivo com problema de encoding foi encontrado.")