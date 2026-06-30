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
        messages = [
            {"role": "system", "content": "You are ClearCall, an AI assistant that explains VAR decisions using the official FIFA Laws of the Game. Be clear, accurate, and accessible."},
            {"role": "user", "content": prompt}
        ]
        response = model.chat(messages=messages, params={"max_new_tokens": 800})
        explanation = response["choices"][0]["message"]["content"]
    except Exception as e:
        import traceback
        print("WATSONX ERROR:", traceback.format_exc())
        explanation = f"[LLM error: {str(e)}]"
    return {
        "explanation": explanation,
        "rules_used": rules
    }