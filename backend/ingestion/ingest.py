import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

PDF_PATH = os.path.join(os.path.dirname(__file__), "../../data/rules/fifa_rules.pdf")
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "../../data/chroma")

def ingest():
    print("Loading PDF...")
    loader = PyPDFLoader(PDF_PATH)
    pages = loader.load()
    print(f"Loaded {len(pages)} pages")

    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(pages)
    print(f"Created {len(chunks)} chunks")

    print("Storing in ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection("fifa_rules")

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk.page_content],
            metadatas=[{"page": chunk.metadata.get("page", 0)}],
            ids=[f"chunk_{i}"]
        )

    print(f"Done! Stored {len(chunks)} chunks in ChromaDB.")

if __name__ == "__main__":
    ingest()