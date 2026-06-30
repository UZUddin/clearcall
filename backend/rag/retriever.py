import chromadb
import os

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "../../data/chroma")

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection("fifa_rules")

def retrieve(query: str, n_results: int = 3) -> list[str]:
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"][0]
