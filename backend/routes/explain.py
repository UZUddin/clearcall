from fastapi import APIRouter
from pydantic import BaseModel
from rag.retriever import retrieve
from rag.prompt import build_prompt
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

router = APIRouter(prefix="/explain", tags=["explain"])

credentials = Credentials(
    url=os.getenv("WATSONX_URL"),
    api_key=os.getenv("WATSONX_API_KEY"),
)

model = ModelInference(
    model_id="ibm/granite-4-h-small",
    credentials=credentials,
    project_id=os.getenv("WATSONX_PROJECT_ID"),
)

class ExplainRequest(BaseModel):
    incident: str
    question: str

@router.post("/")
def explain_incident(data: ExplainRequest):
    rules = retrieve(data.question)
    prompt = build_prompt(data.incident, data.question, rules)
    try:
        response = model.generate_text(prompt=prompt)
        explanation = response
    except Exception as e:
        explanation = f"[LLM temporarily unavailable due to high demand: {str(e)[:100]}]"
    return {
        "explanation": explanation,
        "rules_used": rules
    }
