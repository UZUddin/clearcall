from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import explain, incidents

app = FastAPI(title="ClearCall API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(explain.router)
app.include_router(incidents.router)

@app.get("/health")
def health():
    return {"status": "ok"}