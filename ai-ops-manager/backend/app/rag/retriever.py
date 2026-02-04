from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
VECTOR_DIR = os.path.join(BASE_DIR, "vectorstore")

vectorDB = Chroma(
    persist_directory='VECOR_DIR',
    embedding_function=OllamaEmbeddings(model="nomic-embed-text")
)

def retrieve_context(query: str):
    docs = vectorDB.similarity_search(query, k=3)
    print("RAG docs found: ", len(docs))
    return "\n".join([d.page_content for d in docs])
    
