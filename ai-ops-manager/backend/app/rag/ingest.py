from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# backend/app/rag/ingest.py -> backend/
BACKEND_DIR = Path(__file__).resolve().parents[2]
# docs is a sibling of backend (ai-ops-manager/docs)
DOCS_DIR = BACKEND_DIR.parent / "docs"
# vectorstore is inside backend (ai-ops-manager/backend/vectorstore)
VECTOR_DIR = BACKEND_DIR / "vectorstore"
COLLECTION_NAME = "docs"

router = APIRouter()


def ingest_docs() -> dict:
    docs = []
    skipped: list[dict] = []

    if not DOCS_DIR.exists():
        raise FileNotFoundError(f"Docs directory not found: {DOCS_DIR}")

    files_scanned = 0
    for file in sorted(DOCS_DIR.rglob("*")):
        if not file.is_file():
            continue
        files_scanned += 1

        if file.stat().st_size == 0:
            skipped.append({"file": str(file.name), "reason": "empty"})
            continue

        try:
            if file.suffix.lower() == ".pdf":
                docs.extend(PyPDFLoader(str(file)).load())
            elif file.suffix.lower() in {".md", ".txt", ".text"}:
                docs.extend(TextLoader(str(file), encoding="utf-8").load())
            else:
                skipped.append({"file": str(file.name), "reason": "unsupported_extension"})
        except Exception as e:
            skipped.append({"file": str(file.name), "reason": f"loader_error: {e}"})

    if not docs:
        return {
            "ok": True,
            "message": "No documents loaded (nothing to ingest).",
            "docs_dir": str(DOCS_DIR),
            "vector_dir": str(VECTOR_DIR),
            "files_scanned": files_scanned,
            "docs_loaded": 0,
            "skipped": skipped,
        }

    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    vectordb = Chroma.from_documents(
        docs,
        embedding=OllamaEmbeddings(model="nomic-embed-text"),
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTOR_DIR),
    )
    vectordb.persist()

    return {
        "ok": True,
        "message": "Ingestion complete.",
        "docs_dir": str(DOCS_DIR),
        "vector_dir": str(VECTOR_DIR),
        "collection_name": COLLECTION_NAME,
        "files_scanned": files_scanned,
        "docs_loaded": len(docs),
        "skipped": skipped,
    }


@router.post("/ingest")
def ingest_endpoint():
    return ingest_docs()


if __name__ == "__main__":
    print(ingest_docs())
