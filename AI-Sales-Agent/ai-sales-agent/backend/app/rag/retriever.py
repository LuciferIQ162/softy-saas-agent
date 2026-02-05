import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
VECTOR_DIR = os.path.join(BASE_DIR, "vectorstore")

vdb = Chroma(
    persist_directory=VECTOR_DIR,
    embedding_function=OllamaEmbeddings(model="nomic-embed-text")
)

def get_sales_context(query: str) -> str:
    docs = vdb.similarity_search(query, k=3)
    return "\n".join(d.page_content for d in docs)
