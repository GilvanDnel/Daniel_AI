"""
vector_store.py
 
Responsável por transformar documentos em embeddings e armazená-los
no ChromaDB (base vetorial permanente), além de permitir consultas
por similaridade.
 
Só o administrador deve poder chamar add_document() / rebuild().
Usuários comuns apenas consultam (query()).
"""
 
from __future__ import annotations
 
# --- Fix: ChromaDB exige sqlite3 >= 3.35.0, que costuma não estar disponível
# no Python padrão do Windows/algumas distros Linux. Troca pelo pysqlite3-binary
# (instalado via requirements.txt) ANTES de importar o chromadb.
try:
    __import__("pysqlite3")
    import sys
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass  # sistema já tem uma versão de sqlite3 compatível
 
import os
from pathlib import Path
 
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import google.generativeai as genai
from dotenv import load_dotenv
 
from src.utils.file_readers import read_document
 
# Garante que o .env é sempre lido a partir da raiz do projeto (3 níveis
# acima deste arquivo: core/ -> src/ -> raiz), independente de onde o
# comando "streamlit run" ou "python -m ..." for executado.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=_PROJECT_ROOT / ".env")
 
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
COMPANY_DOCS_PATH = os.getenv("COMPANY_DOCS_PATH", "./company_docs")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
 
COLLECTION_NAME = "daniel_base_corporativa"
 
# Tamanho aproximado (em caracteres) de cada "pedaço" de texto indexado.
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
 
 
EMBEDDING_MODEL = "models/gemini-embedding-001"
 
 
class GeminiEmbeddingFunction(EmbeddingFunction):
    """
    Função de embeddings própria, chamando a API do Gemini diretamente.
 
    Evita depender do wrapper embutido do ChromaDB
    (chromadb.utils.embedding_functions.GoogleGenerativeAiEmbeddingFunction),
    que apresentou incompatibilidade de versão com a lib google-generativeai
    (erro: "ClientOptions does not accept an option 'headers'").
    """
 
    def __init__(self, api_key: str, task_type: str = "retrieval_document"):
        genai.configure(api_key=api_key)
        self.task_type = task_type
 
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for texto in input:
            resultado = genai.embed_content(
                model=EMBEDDING_MODEL,
                content=texto,
                task_type=self.task_type,
            )
            embeddings.append(resultado["embedding"])
        return embeddings
 
    @staticmethod
    def name() -> str:
        return "gemini_embedding_function"
 
 
def _get_client():
    return chromadb.PersistentClient(path=CHROMA_DB_PATH)
 
 
def _get_embedding_function():
    if not GOOGLE_API_KEY:
        raise EnvironmentError(
            "GOOGLE_API_KEY não configurada. Verifique o arquivo .env."
        )
    return GeminiEmbeddingFunction(
        api_key=GOOGLE_API_KEY,
        task_type="retrieval_document",
    )
 
 
def _get_collection():
    client = _get_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=_get_embedding_function(),
    )
 
 
def _chunk_text(texto: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Divide um texto longo em pedaços menores, com sobreposição entre eles."""
    if len(texto) <= chunk_size:
        return [texto]
 
    chunks = []
    inicio = 0
    while inicio < len(texto):
        fim = inicio + chunk_size
        chunks.append(texto[inicio:fim])
        inicio += chunk_size - overlap
 
    return chunks
 
 
def add_document(file_path: str | Path, setor: str, classificacao: str = "publica") -> int:
    """
    Lê um documento, divide em chunks, gera embeddings e adiciona à base vetorial.
 
    Args:
        file_path: caminho do arquivo (.pdf, .docx, .pptx)
        setor: setor responsável (ex: "rh", "ti", "juridico")
        classificacao: "publica" ou "restrita". Documentos "confidencial"
                        NUNCA devem ser passados para esta função.
 
    Returns:
        Número de chunks adicionados.
    """
    if classificacao == "confidencial":
        raise ValueError(
            "Documentos classificados como 'confidencial' nunca devem ser "
            "adicionados à base vetorial."
        )
 
    file_path = Path(file_path)
    texto = read_document(file_path)
    chunks = _chunk_text(texto)
 
    collection = _get_collection()
 
    ids = [f"{file_path.stem}_{i}" for i in range(len(chunks))]
    metadatas = [
        {
            "fonte": file_path.name,
            "setor": setor,
            "classificacao": classificacao,
        }
        for _ in chunks
    ]
 
    collection.add(documents=chunks, ids=ids, metadatas=metadatas)
    return len(chunks)
 
 
def add_documents_from_folder(folder_path: str | Path = None) -> dict:
    """
    Varre a pasta company_docs/ (organizada por setor em subpastas) e indexa
    todos os documentos suportados (.pdf, .docx, .pptx).
 
    Returns:
        Dicionário {nome_do_arquivo: quantidade_de_chunks}
    """
    folder_path = Path(folder_path or COMPANY_DOCS_PATH)
    resultado = {}
    extensoes_suportadas = {".pdf", ".docx", ".pptx", ".md"}
 
    for setor_dir in folder_path.iterdir():
        if not setor_dir.is_dir():
            continue
        setor = setor_dir.name
 
        for arquivo in setor_dir.iterdir():
            if arquivo.suffix.lower() in extensoes_suportadas:
                qtd_chunks = add_document(arquivo, setor=setor)
                resultado[arquivo.name] = qtd_chunks
 
    return resultado
 
 
def query(pergunta: str, n_results: int = 4) -> list[dict]:
    """
    Consulta a base vetorial por similaridade semântica.
 
    Returns:
        Lista de dicts com "texto", "fonte" e "setor" dos trechos mais relevantes.
    """
    collection = _get_collection()
    resultados = collection.query(query_texts=[pergunta], n_results=n_results)
 
    trechos = []
    documentos = resultados.get("documents", [[]])[0]
    metadados = resultados.get("metadatas", [[]])[0]
 
    for texto, meta in zip(documentos, metadados):
        trechos.append({
            "texto": texto,
            "fonte": meta.get("fonte", "desconhecida"),
            "setor": meta.get("setor", "desconhecido"),
        })
 
    return trechos
 
 
def rebuild_base():
    """
    Apaga a coleção atual e reconstrói do zero a partir de company_docs/.
    Uso exclusivo do administrador.
    """
    client = _get_client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # coleção pode não existir ainda
 
    return add_documents_from_folder()
 
