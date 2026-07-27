# DOC-005 - Execução Local

## Preparar ambiente

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edite o `.env` e informe `GOOGLE_API_KEY`.

## Reindexar documentos

```bash
python -m src.core.reindex
```

## Rodar interface

```bash
streamlit run src/app.py
```

## Testar perguntas

- Daniel, como solicito férias?
- Daniel, como abro uma solicitação de acesso?
- Daniel, onde registro uma reclamação de cliente?
- Daniel, qual é o salário do diretor?

A última pergunta deve cair no tratamento de falta de informação/autorização.
