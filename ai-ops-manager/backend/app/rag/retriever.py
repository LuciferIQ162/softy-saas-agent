from __future__ import annotations

from pathlib import Path

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# backend/app/rag/retriever.py -> backend/
BACKEND_DIR = Path(__file__).resolve().parents[2]
VECTOR_DIR = BACKEND_DIR / "vectorstore"
COLLECTION_NAME = "docs"


def retrieve_context(query: str, k: int = 3) -> str:
    if not query or not query.strip():
        return ""
    if not VECTOR_DIR.exists():
        return ""

    vector_db = Chroma(
        persist_directory=str(VECTOR_DIR),
        collection_name=COLLECTION_NAME,
        embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
    )
    docs = vector_db.similarity_search(query, k=k)
    if docs:
        return "\n".join(d.page_content for d in docs if d.page_content)

    # Fallback: if similarity search returns nothing but the collection has docs,
    # return the first few stored documents so `context_used` isn't blank.
    try:
        stored = vector_db.get(limit=k)
        stored_docs = stored.get("documents") or []
        return "\n".join(d for d in stored_docs if d)
    except Exception:
        return ""
