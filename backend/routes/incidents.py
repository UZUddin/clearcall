from fastapi import APIRouter

router = APIRouter(prefix="/incidents", tags=["incidents"])

INCIDENTS = [
    {"id": 1, "match": "France vs Argentina (2022 Final)", "incident": "Mbappe's offside goal disallowed", "type": "offside"},
    {"id": 2, "match": "England vs France (2022 QF)", "incident": "Kane's missed penalty in extra time", "type": "penalty"},
    {"id": 3, "match": "Brazil vs Croatia (2022 QF)", "incident": "Neymar's goal disallowed for offside", "type": "offside"},
    {"id": 4, "match": "Portugal vs South Korea (2022 GS)", "incident": "Ronaldo's disputed goal credit", "type": "goal"},
    {"id": 5, "match": "Spain vs Morocco (2022 R16)", "incident": "Moroccan goal ruled out for offside", "type": "offside"},
]

@router.get("/")
def get_incidents():
    return INCIDENTS
