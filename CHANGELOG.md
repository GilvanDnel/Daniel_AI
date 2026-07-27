# Changelog — Daniel AI

Registro das decisões técnicas tomadas durante o desenvolvimento.
Serve como matéria-prima para a documentação formal (DOC-000 a DOC-009).

## [Sprint 1] — Estrutura do projeto

### Decisões

- Estrutura de pastas definida: `docs/`, `company_docs/`, `datasets/`, `src/` (core, utils, ui), `assets/`, `tests/`
- `company_docs/` subdividido por setor: rh, comercial, atendimento, juridico, ti
- Dependências fixadas em `requirements.txt` com versões mínimas
- Autenticação simples via `.env` (apenas administrador, sem sistema de login robusto no MVP)
- Banco vetorial (ChromaDB) e uploads temporários excluídos do versionamento

### Pendências

- Definir datasets fictícios (clientes, produtos, vendas, metas, ocorrências, atendimentos)

## [Sprint 2] — RAG

### Decisões

- `src/utils/file_readers.py`: leitura de PDF (pypdf), DOCX (python-docx) e PPTX (python-pptx)
- `src/core/vector_store.py`: ChromaDB como banco vetorial persistente, embeddings via
  `GoogleGenerativeAiEmbeddingFunction` (mesma API key do `.env`)
- Chunking simples por tamanho fixo (1000 caracteres, overlap de 150) — sem
  chunking semântico por enquanto (fica como melhoria futura)
- `company_docs/` organizado por setor (subpastas); o setor de cada documento
  vira metadado no ChromaDB, junto com a classificação (`publica`/`restrita`)
- Documentos `confidencial` são bloqueados explicitamente na função `add_document()`
  (nunca podem ir para a base vetorial — regra de governança do projeto)
- `src/core/rag_engine.py`: usa `gemini-2.5-flash` (tier gratuito) com um
  system prompt que proíbe invenção de respostas e exige citar a fonte
- Função `sugerir_escalonamento()` mapeia setor → e-mail de contato, para
  quando o Daniel não encontrar a resposta
- `src/core/reindex.py`: script CLI para o administrador reconstruir a base
  (`python -m src.core.reindex`)
- `src/app.py`: primeira versão da interface Streamlit — chat com barra
  personalizada (anexar à esquerda, enviar à direita) e feedback visual
  de progresso ("🧠 Analisando...", "📚 Consultando documentos...")
- Upload de arquivo na interface já existe visualmente, mas a análise
  (Analytics) ainda não foi implementada — fica para o Sprint 3

### Pendências

- Implementar de fato a leitura/análise de arquivos temporários enviados pelo usuário
- Painel administrativo (adicionar/excluir documentos pela interface, sem precisar do script)
- Tratar limite de rate do tier gratuito do Gemini (10 req/min, 500 req/dia)

### Correção

- Adicionado suporte à leitura de arquivos `.md` (Markdown) em `file_readers.py`,
  `vector_store.py` e no uploader do `app.py` — o documento de teste
  `politica_de_ferias.md` estava sendo ignorado silenciosamente pela indexação
  porque o leitor só reconhecia `.pdf`, `.docx` e `.pptx`
- Corrigido `RuntimeError: unsupported version of sqlite3` do ChromaDB (comum
  em Python 3.9/3.10, especialmente no Windows). `pysqlite3-binary` não tem
  build para Windows, então a correção ficou em duas partes:
  - Windows (ambiente de desenvolvimento): substituição manual do `sqlite3.dll`
    na pasta `DLLs` da instalação do Python (ver instruções no README)
  - Linux (ex: deploy futuro na OCI): `pysqlite3-binary` comentado no
    `requirements.txt`, pronto para ser ativado nesse ambiente
  - Mantido o hotswap em `vector_store.py` (`sys.modules["sqlite3"] = ...`),
    que só entra em ação se `pysqlite3` estiver instalado — não quebra no Windows
- Corrigido `TypeError: unsupported operand type(s) for |` em `file_readers.py`
  e `vector_store.py` — a sintaxe `str | Path` (PEP 604) só funciona nativamente
  a partir do Python 3.10, e o projeto está sendo rodado em Python 3.9. Adicionado
  `from __future__ import annotations` no topo dos dois arquivos, o que resolve
  sem precisar reescrever as assinaturas de função
- Corrigido `EnvironmentError: GOOGLE_API_KEY não configurada` mesmo com o
  `.env` preenchido corretamente. Causa: `load_dotenv()` sem caminho explícito
  pode não localizar o `.env` dependendo de onde o comando é executado.
  Agora `vector_store.py` e `rag_engine.py` calculam explicitamente a raiz
  do projeto e apontam `load_dotenv(dotenv_path=...)` para lá
- Substituído o `file_uploader` padrão (bloco grande de "arraste e solte")
  por um botão compacto 📎 usando `st.popover`, que abre a área de upload
  apenas quando clicado — visual mais limpo, alinhado com a barra de chat
  inspirada no ChatGPT/Gemini
- Corrigido `ValueError: ClientOptions does not accept an option 'headers'`,
  causado por incompatibilidade de versão entre o wrapper embutido do
  ChromaDB (`GoogleGenerativeAiEmbeddingFunction`) e a versão instalada de
  `google-generativeai`. Solução: criada uma função de embeddings própria
  (`GeminiEmbeddingFunction`, em `vector_store.py`), chamando
  `genai.embed_content()` diretamente, sem depender do wrapper do ChromaDB.
  Modelo usado: `models/text-embedding-004`
- Corrigido `404 models/text-embedding-004 is not found`: esse modelo foi
  descontinuado pelo Google em favor do `gemini-embedding-001`. Atualizado
  `EMBEDDING_MODEL` em `vector_store.py`
- Corrigido `404 models/gemini-2.5-flash is no longer available`. O Google
  descontinua versões específicas do Gemini com frequência. Para evitar
  quebrar de novo a cada troca, `MODEL_NAME` em `rag_engine.py` passou a
  usar o alias `gemini-flash-latest`, que o próprio Google mantém apontado
  para a versão estável mais recente

## [Sprint 2.1] — Ajustes de UX

### Correções

- Corrigido campo de mensagem não ficando fixo na parte inferior da tela.
  Causa: o `st.chat_input` estava dentro de `st.columns()`, o que impede o
  Streamlit de fixá-lo automaticamente. Solução: substituído pelo suporte
  nativo a anexo do `chat_input` (`accept_file=True`), eliminando a
  necessidade de colunas — o clipe de anexo e o botão de enviar já vêm
  embutidos no próprio componente nativo
- Corrigido o Daniel se apresentando institucionalmente em toda resposta.
  Causa: cada chamada à API é isolada (sem memória de conversa), então o
  modelo não "sabia" que já tinha se apresentado antes. Solução: `ask()`
  agora recebe um parâmetro `primeira_interacao`, e o `app.py` controla via
  `session_state` se essa é a primeira pergunta da sessão — o system prompt
  muda dinamicamente para instruir o Daniel a não repetir a apresentação
  nas perguntas seguintes
