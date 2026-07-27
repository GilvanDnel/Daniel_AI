# DOC-003 - Requisitos

## Funcionais

- RF01 - O sistema deve permitir chat em linguagem natural.
- RF02 - O sistema deve consultar documentos corporativos via RAG.
- RF03 - O sistema deve exibir fontes consultadas.
- RF04 - O sistema deve permitir reindexação administrativa.
- RF05 - O sistema deve bloquear documentos confidenciais.
- RF06 - O sistema deve encaminhar perguntas fora de escopo.
- RF07 - O sistema deve aceitar upload temporário de arquivos.
- RF08 - O sistema deve analisar CSV/XLSX em sprint posterior.
- RF09 - O sistema deve exportar resultados em sprint posterior.

## Não funcionais

- RNF01 - Rodar via navegador.
- RNF02 - Ser implantável na OCI.
- RNF03 - Não versionar `.env`, ChromaDB, uploads temporários ou arquivos gerados.
- RNF04 - Separar claramente código, documentos, datasets e relatórios.
