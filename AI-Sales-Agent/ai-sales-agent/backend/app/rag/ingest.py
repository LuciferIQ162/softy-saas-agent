import os
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# --------------------------------------------------
# Resolve project root
# --------------------------------------------------
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)

DOCS_DIR = os.path.join(BASE_DIR, "docs")
VECTOR_DIR = os.path.join(BASE_DIR, "vectorstore")

# --------------------------------------------------
# Ingest function
# --------------------------------------------------
def ingest_sales_docs():
    if not os.path.exists(DOCS_DIR):
        raise FileNotFoundError(f"Directory not found: {DOCS_DIR}")

    docs = []

    print("📂 Docs directory:", DOCS_DIR)
    print("📦 Vectorstore directory:", VECTOR_DIR)

    for file in os.listdir(DOCS_DIR):
        path = os.path.join(DOCS_DIR, file)

        # ✅ Only load markdown files
        if not file.endswith(".md"):
            continue

        # ✅ Skip empty files
        if os.path.getsize(path) == 0:
            print(f"⚠️ Skipping empty file: {file}")
            continue

        print(f"📄 Loading: {file}")
        docs.extend(TextLoader(path).load())

    print("✅ Documents loaded:", len(docs))

    if not docs:
        raise RuntimeError("No documents loaded. RAG will be empty.")

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=OllamaEmbeddings(model="nomic-embed-text"),
        persist_directory=VECTOR_DIR
    )

    vectordb.persist()

    print("✅ Vectorstore successfully created")
    print("📍 Stored at:", VECTOR_DIR)

# --------------------------------------------------
# CLI entrypoint
# --------------------------------------------------
if __name__ == "__main__":
    ingest_sales_docs()
