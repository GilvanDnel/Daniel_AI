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
- Definir conteúdo real dos `company_docs` (documentação da empresa fictícia)
- Definir datasets fictícios (clientes, produtos, vendas, metas, ocorrências, atendimentos)
