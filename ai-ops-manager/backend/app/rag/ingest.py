import os
from pathlib import Path
from fastapi import APIRouter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Docs live next to backend (ai-ops-manager/docs); vectorstore inside backend
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = BACKEND_DIR.parent / "docs"
VECTOR_DIR = BACKEND_DIR / "vectorstore"

router = APIRouter()

@router.post("/ingest")
def ingest_docs():
    docs = []
    if not DOCS_DIR.exists():
        return 0

    for file in sorted(DOCS_DIR.iterdir()):
        if file.suffix.lower() == ".pdf":
            docs.extend(PyPDFLoader(str(file)).load())
        elif file.suffix.lower() in (".md", ".txt", ".text"):
            docs.extend(TextLoader(str(file)).load())

    if not docs:
        return 0

    vector_db = Chroma.from_documents(
        docs,
        embeddings = OllamaEmbeddings(model="nomic-embed-text"),
        persist_directory=VECTOR_DIR,
    )
    if __name__ == "__main__":
        ingest_docs()
        print("Documents ingested successfully")
    else:
        print("Documents not ingested")