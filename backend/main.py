from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import explain, incidents
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="ClearCall API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    import chromadb
    CHROMA_PATH = os.path.join(os.path.dirname(__file__), "../data/chroma")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection("fifa_rules")
    if collection.count() == 0:
        print("ChromaDB empty — running ingestion...")
        from ingestion.ingest import ingest
        ingest()
    else:
        print(f"ChromaDB already has {collection.count()} chunks.")

app.include_router(explain.router)
app.include_router(incidents.router)

@app.get("/health")
def health():
    return {"status": "ok"}