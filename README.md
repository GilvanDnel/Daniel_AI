# Daniel AI

Assistente corporativo inteligente da **DNEL SOM Serviços Inteligentes**, desenvolvido para o Challenge Final da Alura (Alura Agent).

> Daniel não é um chatbot genérico. Ele é uma camada inteligente de acesso ao conhecimento autorizado da empresa — responde com base em documentos internos reais, nunca inventa informação, e encaminha para o setor certo quando não encontra a resposta.

🔗 **Aplicação rodando ao vivo na Oracle Cloud (OCI):**  
[http://163.176.65.156:8501](http://163.176.65.156:8501)

---

## O que o Daniel faz

- 📚 **Knowledge (RAG):** responde perguntas sobre documentos internos da empresa (RH, TI, Jurídico, Comercial, Atendimento, Compliance, Financeiro), sempre citando as fontes autorizadas formatadas sem expor nomes de arquivos crus.
- 📊 **Analytics:** analisa arquivos temporários enviados pelo usuário (CSV/Excel com suporte a encodings e separadores brasileiros `,` e `;`), gerando KPIs, rankings, gráficos interativos e leitura executiva com IA.
- 🔍 **Filtro por Setor:** permite refinar a busca semântica para áreas específicas da empresa (ex: *Recursos Humanos, TI, Financeiro*).
- 💡 **Perguntas Relacionadas:** sugere automaticamente perguntas de acompanhamento clicáveis após as respostas do RAG.
- 🔊 **Leitura por Voz (TTS):** botão de narração em áudio nativo (`pt-BR`) para acessibilidade.
- 📥 **Exportação de Histórico e Relatórios:** permite baixar o histórico do atendimento em PDF/TXT e relatórios de planilhas em CSV, Excel, PDF executivo e PowerPoint.
- 🔀 **Escalonamento:** quando não encontra a resposta na base, encaminha o usuário para o e-mail do setor corporativo responsável.
- 🔑 **Painel Administrativo Completo:** área autenticada (HMAC) com controle de sessão (Logout), upload de documentos por setor, exclusão de arquivos, reindexação da base e **Dashboard de Métricas e Saúde do Sistema**.
- 📱 **Interface Responsiva Mobile-First:** adaptada para navegação em celulares, tablets e computadores.

---

## 📄 Documentação Técnica Avançada & Governança

Para um detalhamento aprofundado sobre a arquitetura de software, governança documental, LGPD e runbooks de produção, consulte o relatório completo na pasta `docs/`:

📖 **[Relatório Técnico de Engenharia, Governança e Arquitetura RAG](docs/relatorio_tecnico_completo.md)**

### Destaques de Engenharia e Governança:
- **Desmembramento Documental (*Sharding*):** Fatiamento em 10 arquivos Markdown (`.md`) especializados em 7 setores operacionais para redução de consumo de tokens e aumento da precisão vetorial.
- **Tratamento de Rate Limit (HTTP 429):** Algoritmo de retentativa automática com espera exponencial (*Exponential Backoff*) na API de Embeddings do Gemini.
- **Governança LGPD:** Diretrizes de proteção de dados de clientes e protocolos de descarte (*Wipe / Format*) em equipamentos deixados em assistência técnica.
- **Segurança Lógica (Nível L5):** Princípio de privilégio mínimo e isolamento contra engenharia de prompt (*Prompt Injection* e *Antijailbreak*).

---

## Exemplos de perguntas e respostas

**Pergunta:** "Posso fracionar minhas férias em quantos períodos?"  
**Resposta:** _De acordo com a **Política de Férias**, as férias podem ser fracionadas em até 3 períodos, sendo que um deles não pode ser inferior a 14 dias corridos, e os demais não podem ser inferiores a 5 dias corridos cada._  
📄 **Fonte consultada:** `Política de Férias`

**Pergunta:** "Quais são os direitos do titular de dados segundo a LGPD?"  
**Resposta:** _De acordo com a **Política de LGPD e Privacidade**, o titular pode solicitar confirmação de tratamento, acesso, correção, anonimização/bloqueio/eliminação, portabilidade e revogação do consentimento, a qualquer momento._  
📄 **Fonte consultada:** `Política de LGPD e Privacidade`

**Pergunta:** "Se eu tiver 9 meses de empresa, já posso tirar férias?"  
**Resposta:** _O Daniel identifica que a base não contém uma regra específica para esse caso, informa que o direito padrão é de 30 dias após 12 meses de trabalho, e sugere contato com o setor de RH (`rh@dnelsom.com.br`) para o caso específico — sem inventar uma resposta._

---

## Arquitetura

```text
Usuário → Interface Mobile-First (Streamlit) → Router (classifica a intenção)
                                                     │
                 ┌───────────────────────────────────┼───────────────────────────────────┐
                 ▼                                   ▼                                   ▼
           RAG Engine                          Analytics Engine                    Escalonamento
     (busca vetorial + RAG +                  (Pandas + Plotly +                  (setor + e-mail
      Gemini + filtro setor +                  Gemini + exportação                 de contato)
      citação limpa de fontes)                 CSV/Excel/PDF/PPTX)
                 │
                 ▼
           ChromaDB (base vetorial persistente,
           embeddings gerados via Gemini API)
```

---

## Tecnologias

| Camada         | Tecnologia                                |
| -------------- | ----------------------------------------- |
| Frontend       | Streamlit + CSS Customizado (Mobile-First)|
| Backend        | Python 3.9+                               |
| IA LLM         | Google Gemini API (`gemini-flash-latest`) |
| Embeddings     | Gemini (`gemini-embedding-001`)           |
| Banco Vetorial | ChromaDB (persistente)                    |
| Analytics      | Pandas + Plotly                           |
| Relatórios     | ReportLab (PDF) + python-pptx (PowerPoint)|
| Acessibilidade | Web Speech API (TTS nativo)               |
| Deploy         | Oracle Cloud Infrastructure (OCI Compute) |

---

## Estrutura do repositório

```text
Daniel_AI/
├── company_docs/          # Base de conhecimento corporativa organizada por setor
│   ├── atendimento/ comercial/ compliance/ financeiro/ juridico/ rh/ ti/
├── datasets/               # Datasets de exemplo para testes de Analytics
├── docs/                    # Documentação formal e relatório técnico do projeto
├── src/
│   ├── admin/               # Autenticação HMAC e gestão de documentos pelo Admin
│   ├── analytics/           # Análise de planilhas (data_analyzer.py)
│   ├── config/               # Configurações e variáveis de ambiente (settings.py)
│   ├── core/                  # RAG, roteamento, escalonamento, erros e ChromaDB
│   ├── reports/               # Exportadores de relatórios e histórico (exporters.py)
│   ├── services/               # Orquestração do chat e documentos temporários
│   ├── ui/                      # Visualização, barra lateral, CSS e badges
│   ├── utils/                    # Leitores de arquivos e formatador de fontes
│   └── app.py                    # Ponto de entrada da aplicação
├── tests/                    # Suíte de testes automatizados (25 testes unitários)
├── requirements.txt
└── .env.example
```

---

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

---

## Executando os Testes Automatizados

Para validar o funcionamento de todos os módulos (RAG, Admin, Analytics, Exporters, Formatação de Fontes):

```bash
python -m unittest discover tests
```

---

## Deploy (OCI Compute)

A aplicação está hospedada em uma instância **Always Free** da Oracle Cloud (Ubuntu 24.04), rodando como serviço `systemd` (reinício automático em caso de falha, e inicialização automática com a máquina):

```bash
sudo systemctl status daniel     # verificar status
sudo journalctl -u daniel -f     # ver logs em tempo real
sudo systemctl restart daniel    # reiniciar após atualizar o código
```

---

## Status

✅ RAG funcional, com citação de fontes limpas, filtro de setor e perguntas sugeridas  
✅ Analytics funcional (upload CSV/Excel → KPIs, gráficos, relatórios e follow-up IA)  
✅ Painel administrativo completo (autenticação, upload/exclusão por setor, métricas de banco e logout)  
✅ Acessibilidade com narração de áudio por voz (TTS)  
✅ Exportação do histórico da conversa em PDF e TXT  
✅ Interface responsiva Mobile-First refinada  
✅ Documentação Técnica e Governança LGPD compilada em `docs/`  
✅ Deploy ao vivo na OCI  
