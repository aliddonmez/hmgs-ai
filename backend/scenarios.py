# backend/scenarios.py

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from app.scenario_storage import get_all_scenarios, get_scenario_by_id, get_random_scenario

router = APIRouter(prefix="/api/scenarios", tags=["Scenarios"])

class ScenarioResponse(BaseModel):
    id: int
    title: str
    course: str
    topic: str
    subtopic: Optional[str]
    difficulty: str
    scenario_text: str
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    explanation: str
    legal_basis: Optional[str]

@router.get("/", response_model=List[ScenarioResponse])
def list_scenarios():
    """Tüm senaryoları listeler."""
    return get_all_scenarios()

@router.get("/random", response_model=ScenarioResponse)
def random_scenario():
    """Rastgele bir senaryo getirir (Senaryo başlat)."""
    scenario = get_random_scenario()
    if not scenario:
        raise HTTPException(status_code=404, detail="Senaryo bulunamadı.")
    return scenario

@router.get("/{scenario_id}", response_model=ScenarioResponse)
def get_scenario(scenario_id: int):
    """ID'ye göre senaryo detayını getirir."""
    scenario = get_scenario_by_id(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Senaryo bulunamadı.")
    return scenario
