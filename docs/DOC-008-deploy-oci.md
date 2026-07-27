# DOC-008 - Deploy na Oracle Cloud Infrastructure

Este roteiro usa OCI Compute com Ubuntu e Streamlit rodando na porta 8501. É o caminho mais direto para demonstrar o Challenge.

## 1. Preparar o repositório

Antes do deploy:

- confirme que `.env` não está versionado;
- confirme que `chroma_db/`, `venv/`, `uploads_temp/` e `exports/` não estão versionados;
- envie o código para o GitHub;
- mantenha `.env.example` no repositório.

## 2. Criar a infraestrutura na OCI

1. Acesse o Console da OCI.
2. Crie ou selecione um compartimento.
3. Crie uma VCN com internet usando o assistente de VCN.
4. Crie uma instância Compute.
5. Escolha Ubuntu como imagem.
6. Escolha shape Always Free se disponível.
7. Marque para atribuir IP público.
8. Cadastre ou baixe a chave SSH.

## 3. Liberar portas

Na VCN, Security List ou Network Security Group, libere:

| Porta | Uso | Origem sugerida |
|---|---|---|
| 22 | SSH | Seu IP |
| 8501 | Streamlit | 0.0.0.0/0 para demo |

Para produção, prefira expor 80/443 com proxy reverso e HTTPS.

## 4. Conectar via SSH

No Windows PowerShell:

```powershell
ssh -i "C:\caminho\para\sua-chave.key" ubuntu@IP_PUBLICO_DA_INSTANCIA
```

Se usar Oracle Linux, o usuário padrão costuma ser `opc`.

## 5. Instalar dependências no servidor

```bash
sudo apt update
sudo apt install -y git python3-venv python3-pip
```

## 6. Clonar o projeto

```bash
git clone https://github.com/GilvanDnel/Daniel_AI.git
cd Daniel_AI
```

## 7. Criar ambiente Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Se o ChromaDB reclamar de SQLite antigo no Linux:

```bash
pip install pysqlite3-binary
```

## 8. Configurar variáveis de ambiente

```bash
cp .env.example .env
nano .env
```

Preencha:

```env
GOOGLE_API_KEY=sua_chave_gemini
ADMIN_USERNAME=admin
ADMIN_PASSWORD=Daniel@2026
```

## 9. Reindexar a base corporativa

```bash
python -m src.core.reindex
```

## 10. Testar manualmente

```bash
streamlit run src/app.py --server.address=0.0.0.0 --server.port=8501 --server.headless=true
```

Acesse:

```text
http://IP_PUBLICO_DA_INSTANCIA:8501
```

## 11. Criar serviço systemd

Crie o arquivo:

```bash
sudo nano /etc/systemd/system/daniel-ai.service
```

Conteúdo:

```ini
[Unit]
Description=Daniel AI Streamlit App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Daniel_AI
Environment="PATH=/home/ubuntu/Daniel_AI/venv/bin"
ExecStart=/home/ubuntu/Daniel_AI/venv/bin/streamlit run src/app.py --server.address=0.0.0.0 --server.port=8501 --server.headless=true
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Ative:

```bash
sudo systemctl daemon-reload
sudo systemctl enable daniel-ai
sudo systemctl start daniel-ai
sudo systemctl status daniel-ai
```

Ver logs:

```bash
journalctl -u daniel-ai -f
```

## 12. Checklist final

- [ ] URL pública abre.
- [ ] Chat responde saudação.
- [ ] Pergunta sobre férias responde com base nos documentos.
- [ ] Pergunta fora de escopo não inventa resposta.
- [ ] Upload de CSV gera dashboard.
- [ ] Erro de cota aparece como aviso amigável.
- [ ] README inclui link ou print da aplicação na OCI.
