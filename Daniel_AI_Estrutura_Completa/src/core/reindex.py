"""CLI script for rebuilding Daniel corporate knowledge base."""

from __future__ import annotations

from src.core.vector_store import rebuild_base


def main() -> None:
    print("Reconstruindo base vetorial da DNEL SOM...")
    result = rebuild_base()
    if not result:
        print("Nenhum documento encontrado em company_docs/.")
        return
    print("Base reconstruída com sucesso:")
    for file_name, chunk_count in result.items():
        print(f"- {file_name}: {chunk_count} chunks")


if __name__ == "__main__":
    main()
