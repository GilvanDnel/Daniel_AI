# DOC-001 - Arquitetura

```text
Colaborador                       Administrador
     |                                  |
     v                                  v
Daniel Chat                    Daniel Admin Console
     |                                  |
     +---------------+------------------+
                     v
              Orquestrador
                     |
    +----------------+----------------+
    |                |                |
    v                v                v
Daniel Knowledge  Daniel Analyst   Daniel Support
    |                |                |
RAG + ChromaDB    Pandas/Plotly     Encaminhamento
    |                |                |
    +----------------+----------------+
                     v
              Gemini API
```

## Componentes

- `src/core`: RAG, roteamento, embeddings, escalonamento.
- `src/admin`: autenticação e console administrativo.
- `src/analytics`: análise de CSV/XLSX.
- `src/reports`: exportações PDF, CSV, Excel e PowerPoint.
- `src/services`: orquestração entre UI, documentos, analytics e RAG.
- `src/ui`: componentes Streamlit.
- `src/utils`: leitores e utilitários.
