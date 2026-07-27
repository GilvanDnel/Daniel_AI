# Daniel AI

Assistente corporativo inteligente da **DNEL SOM Serviços Inteligentes**, desenvolvido para o Challenge Final da Alura (Alura Agent).

> Daniel não é um chatbot genérico. Ele é uma camada inteligente de acesso ao
> conhecimento autorizado da empresa — responde com base em documentos internos
> reais, nunca inventa informação, e encaminha para o setor certo quando não sabe.

🔗 **Aplicação rodando ao vivo na Oracle Cloud (OCI):**
[http://163.176.65.156:8501](http://163.176.65.156:8501)

---

## O que o Daniel faz

- **Knowledge (RAG):** responde perguntas sobre documentos internos da empresa
  (RH, TI, Jurídico, Comercial, Atendimento, Compliance, Financeiro), sempre
  citando a fonte consultada
- **Analytics:** analisa arquivos temporários enviados pelo usuário (CSV/Excel)
  e gera KPIs, rankings e gráficos
- **Escalonamento:** quando não encontra a resposta na base, encaminha o
  usuário para o setor responsável (com e-mail de contato)
- **Painel administrativo:** área autenticada para gerenciar a base de
  conhecimento

Daniel nunca inventa respostas. Se a informação não está nos documentos
autorizados, ele diz isso claramente.

## Exemplos de perguntas e respostas

**Pergunta:** "Posso fracionar minhas férias em quantos períodos?"
**Resposta:** _De acordo com a Política de Férias (documento `politica_de_ferias.md`), as férias podem ser fracionadas em até 3 períodos, sendo que um deles não pode ser inferior a 14 dias corridos, e os demais não podem ser inferiores a 5 dias corridos cada._

**Pergunta:** "Quais são os direitos do titular de dados segundo a LGPD?"
**Resposta:** _De acordo com a política de LGPD (`lgpd.md`), o titular pode solicitar confirmação de tratamento, acesso, correção, anonimização/bloqueio/eliminação, portabilidade e revogação do consentimento, a qualquer momento._

**Pergunta:** "Se eu tiver 9 meses de empresa, já posso tirar férias?"
**Resposta:** _O Daniel identifica que a base não contém uma regra específica para esse caso, informa que o direito padrão é de 30 dias após 12 meses de trabalho, e sugere contato com o setor de RH (rh@dnelsom.com.br) para o caso específico — sem inventar uma resposta._

## Arquitetura

```
Usuário → Interface (Streamlit) → Router (classifica a intenção)
                                        │
                    ┌───────────────────┼────────────────────┐
                    ▼                   ▼                    ▼
              RAG Engine          Analytics Engine      Escalonamento
           (busca vetorial +      (Pandas + Plotly       (setor + e-mail
            Gemini + citação        sobre arquivo          de contato)
            de fontes)              enviado)
                    │
                    ▼
              ChromaDB (base vetorial persistente,
              embeddings gerados via Gemini API)
```

O `router` analisa a pergunta do usuário e decide se ela deve ser respondida
via base de conhecimento (RAG), via análise de dados (Analytics), ou
encaminhada para um setor humano — sem exigir que o usuário escolha o modo
manualmente.

## Tecnologias

| Camada         | Tecnologia                                |
| -------------- | ----------------------------------------- |
| Frontend       | Streamlit                                 |
| Backend        | Python 3.9+                               |
| IA             | Google Gemini API (`gemini-flash-latest`) |
| Embeddings     | Gemini (`gemini-embedding-001`)           |
| Banco Vetorial | ChromaDB (persistente)                    |
| Analytics      | Pandas                                    |
| Visualização   | Plotly                                    |
| Leitura        | PyPDF, python-docx, python-pptx, Markdown |
| Deploy         | Oracle Cloud Infrastructure (OCI Compute) |

## Estrutura do repositório

```
Daniel_AI/
├── company_docs/       # Base de conhecimento corporativa, por setor
│   ├── rh/  ti/  juridico/  comercial/  atendimento/  compliance/  financeiro/
├── datasets/            # Datasets de exemplo para testes de Analytics
├── docs/                 # Documentação formal do projeto
├── src/
│   ├── admin/            # Autenticação do administrador
│   ├── analytics/        # Análise de planilhas (data_analyzer.py)
│   ├── config/            # Configurações e variáveis de ambiente (settings.py)
│   ├── core/               # Motor de RAG, roteamento de intenção, escalonamento,
│   │                        tratamento de erros e conexão com o ChromaDB
│   ├── reports/            # Geração/exportação de relatórios
│   ├── services/            # Orquestração: chat, documentos, upload
│   ├── ui/                   # Componentes visuais do Streamlit
│   ├── utils/                 # Leitura de arquivos (PDF, DOCX, PPTX, MD)
│   └── app.py                 # Ponto de entrada da aplicação
├── requirements.txt
└── .env.example
```

## Como executar localmente

```bash
git clone https://github.com/SEU_USUARIO/Daniel_AI.git
cd Daniel_AI

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# edite o .env com sua GOOGLE_API_KEY (gerada em aistudio.google.com)

python -m src.core.reindex     # indexa os documentos de company_docs/
streamlit run src/app.py
```

Acesse em `http://localhost:8501`.

## Deploy (OCI Compute)

A aplicação está hospedada em uma instância **Always Free** da Oracle Cloud
(Ubuntu 24.04), rodando como serviço `systemd` (reinício automático em caso
de falha, e inicialização automática com a máquina):

```bash
sudo systemctl status daniel     # verificar status
sudo journalctl -u daniel -f     # ver logs em tempo real
sudo systemctl restart daniel    # reiniciar após atualizar o código
```

A porta 8501 está liberada tanto na Security List da VCN quanto no firewall
local (`iptables`) da instância.

## Status

✅ RAG funcional, com citação de fontes e escalonamento por setor
✅ Analytics funcional (upload de CSV/Excel → KPIs e gráficos)
✅ Deploy ao vivo na OCI
🚧 Painel administrativo (autenticação pronta, interface em desenvolvimento)
🚧 Refinamentos de UX (menu de opções guiado na saudação inicial)
