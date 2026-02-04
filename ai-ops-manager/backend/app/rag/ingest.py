import os
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Docs live next to backend (ai-ops-manager/docs); vectorstore inside backend
_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
_DOCS_DIR = _BACKEND_DIR.parent / "docs"
_VECTOR_DIR = _BACKEND_DIR / "vectorstore"


def ingest_docs():
    docs = []
    if not _DOCS_DIR.exists():
        return 0

    for file in sorted(_DOCS_DIR.iterdir()):
        if file.suffix.lower() == ".pdf":
            docs.extend(PyPDFLoader(str(file)).load())
        elif file.suffix.lower() in (".md", ".txt", ".text"):
            docs.extend(TextLoader(str(file)).load())

    if not docs:
        return 0

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=str(_VECTOR_DIR),
    )
    vector_db.persist()
    return len(docs)