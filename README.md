# Daniel AI

Assistente corporativo inteligente da **DNEL SOM Serviços Inteligentes**.

> Daniel não é um chatbot. Ele é uma camada inteligente de acesso ao conhecimento
> autorizado da empresa.

## O que o Daniel faz

- Responde perguntas sobre documentos internos (RAG)
- Analisa arquivos enviados pelo usuário (PDF, DOCX, PPTX, CSV, XLSX)
- Gera KPIs, rankings, gráficos e relatórios a partir de planilhas
- Exporta resultados em PDF, CSV, Excel e PowerPoint
- Encaminha para o setor responsável quando não encontra a resposta

Daniel nunca inventa respostas. Se não sabe, informa e encaminha.

## Tecnologias

| Camada         | Tecnologia                          |
|----------------|--------------------------------------|
| Frontend       | Streamlit                            |
| Backend        | Python                               |
| IA             | Google Gemini API                    |
| Framework IA   | LangChain                            |
| Banco Vetorial | ChromaDB                             |
| Analytics      | Pandas                               |
| Visualização   | Plotly                               |
| Leitura        | PyPDF, python-docx, openpyxl, python-pptx |
| Deploy         | Oracle Cloud Infrastructure (OCI)    |

## Estrutura do repositório

```
Daniel-AI/
├── docs/            # Documentação formal do projeto (DOC-000 a DOC-009)
├── company_docs/    # Base de conhecimento corporativa (RH, Comercial, TI, Jurídico, Atendimento)
├── datasets/         # Datasets fictícios (clientes, vendas, metas...)
├── src/
│   ├── core/         # RAG, integração com Gemini, lógica de negócio
│   ├── utils/         # Leitura de arquivos, helpers
│   └── ui/            # Componentes da interface Streamlit
├── assets/           # Imagens, ícones, logo
├── tests/            # Testes automatizados
├── requirements.txt
└── .env.example
```

## Como executar

```bash
# 1. Clone o repositório
git clone <url-do-repo>
cd Daniel-AI

# 2. Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# edite o .env com sua chave da API do Gemini

# 5. Execute
streamlit run src/app.py
```

## Público

- **Administrador**: possui login, gerencia a base corporativa (adicionar, excluir, atualizar documentos, reconstruir base vetorial)
- **Usuário comum**: acessa direto o chat, sem login. Pode conversar, enviar arquivos temporários e baixar resultados

## Roadmap

- [x] Sprint 0 — Documentação e planejamento
- [x] Sprint 1 — Estrutura do projeto
- [ ] Sprint 2 — RAG
- [ ] Sprint 3 — Analytics
- [ ] Sprint 4 — Painel Administrativo
- [ ] Sprint 5 — Deploy OCI

## Status

🚧 Em desenvolvimento — Challenge Final Alura

## Troubleshooting

### Erro: `RuntimeError: unsupported version of sqlite3` (Windows)

O ChromaDB exige SQLite >= 3.35.0, e o Python no Windows costuma vir com uma
versão mais antiga. Para corrigir:

1. Rode em um terminal Python: `import sys; print(sys.executable)` — isso mostra
   o caminho da sua instalação do Python (algo como
   `C:\Users\SEU_USUARIO\AppData\Local\Programs\Python\Python39\`).
2. Baixe a versão mais recente do SQLite para Windows em
   [sqlite.org/download.html](https://www.sqlite.org/download.html)
   (procure por **sqlite-dll-win64-x64-*.zip**, ou win32 se seu Python for 32 bits).
3. Extraia o zip e copie o arquivo `sqlite3.dll`.
4. Cole esse arquivo dentro da pasta `DLLs` da sua instalação do Python
   (ex: `...\Python39\DLLs\sqlite3.dll`), substituindo o arquivo existente.
5. Feche e reabra o terminal (e o venv), depois rode `streamlit run src/app.py`
   novamente.

Isso não afeta o deploy futuro na Oracle Cloud (Linux), que usa uma correção
diferente já preparada no `requirements.txt`.
