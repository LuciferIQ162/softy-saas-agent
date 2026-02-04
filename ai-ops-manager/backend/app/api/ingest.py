"""
API router entrypoint for document ingestion.

We keep the ingestion implementation in `app.rag.ingest` and re-export the
FastAPI router from here so `app.api.*` imports remain consistent.
"""

from app.rag.ingest import router

