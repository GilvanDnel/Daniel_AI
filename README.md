# Daniel AI

Assistente corporativo inteligente da **DNEL SOM Serviços Inteligentes**.

> Daniel não é apenas um chatbot. Ele é uma camada inteligente de acesso ao conhecimento autorizado da empresa.

## Status do MVP

Esta estrutura separa claramente o que já deve ser entregue no MVP e o que fica como evolução.

### Implementar primeiro

- Chat em Streamlit.
- RAG sobre documentos corporativos autorizados.
- Base vetorial com ChromaDB.
- Respostas com fontes.
- Fallback com encaminhamento por setor.
- Login simples apenas para administrador.
- Reindexação da base corporativa.
- Análise inicial de CSV/XLSX com KPIs, rankings, gráficos e recomendações.
- Exportação inicial em CSV, Excel, PDF e PowerPoint.

### Próximas camadas

- Melhorar análise com perguntas livres sobre a planilha.
- Painel administrativo completo para cadastrar e remover documentos.
- Deploy na Oracle Cloud Infrastructure.

## Estrutura

```text
Daniel_AI/
├── assets/
├── company_docs/
│   ├── atendimento/
│   ├── comercial/
│   ├── compliance/
│   ├── financeiro/
│   ├── juridico/
│   ├── rh/
│   └── ti/
├── datasets/
│   └── exemplos/
├── docs/
├── src/
│   ├── admin/
│   ├── analytics/
│   ├── config/
│   ├── core/
│   ├── reports/
│   ├── services/
│   ├── ui/
│   └── utils/
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

## Como executar

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run src/app.py
```

Antes de perguntar ao Daniel sobre os documentos, reindexe a base:

```bash
python -m src.core.reindex
```

## Perfis

| Perfil | Acesso | Observação |
|---|---|---|
| Colaborador | Chat sem login | Pode perguntar e enviar arquivos temporários. |
| Administrador | Login simples | Pode reindexar e futuramente gerenciar documentos oficiais. |

## Governança

- Documentos confidenciais não entram na base.
- Daniel responde somente com base no contexto recuperado.
- Se não houver informação suficiente, encaminha ao setor responsável.
- Arquivos temporários enviados pelo usuário não viram conhecimento permanente.

## Teste rápido de Analytics

Use o arquivo `datasets/exemplos/vendas_exemplo.csv` no chat e pergunte:

```text
Daniel, analise essa planilha e me diga o que devo fazer.
```

O Daniel deve mostrar leitura executiva, recomendações, KPIs, rankings, gráfico temporal e downloads.

## Deploy

O passo a passo de deploy na Oracle Cloud Infrastructure está em:

`docs/DOC-008-deploy-oci.md`

## Limite de cota da API

Se a API do Gemini retornar erro 429 por limite de uso, o Daniel exibe uma mensagem amigável orientando o usuário a aguardar e tentar novamente. Isso evita que o usuário final veja stack trace técnico.
