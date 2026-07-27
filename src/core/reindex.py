"""
reindex.py

Script de linha de comando para o administrador (re)construir a base
vetorial a partir dos documentos em company_docs/.

Uso:
    python -m src.core.reindex
"""

from src.core.vector_store import rebuild_base

if __name__ == "__main__":
    print("🔄 Reconstruindo a base vetorial a partir de company_docs/ ...")
    resultado = rebuild_base()

    if not resultado:
        print("⚠️  Nenhum documento encontrado em company_docs/.")
    else:
        print("✅ Base reconstruída com sucesso:\n")
        for arquivo, qtd_chunks in resultado.items():
            print(f"  - {arquivo}: {qtd_chunks} chunks indexados")
