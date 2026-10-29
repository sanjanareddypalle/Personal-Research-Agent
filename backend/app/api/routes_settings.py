import os
from fastapi import APIRouter
from pydantic import BaseModel
from app.config import settings

router = APIRouter(prefix="/settings", tags=["Settings"])

class SettingsResponse(BaseModel):
    llm_provider: str
    llm_model: str
    search_provider: str
    has_gemini_key: bool
    has_openai_key: bool
    has_tavily_key: bool
    is_demo_mode: bool

class UpdateSettingsRequest(BaseModel):
    llm_provider: str
    search_provider: str
    demo_mode: bool

@router.get("", response_model=SettingsResponse)
def get_settings():
    gemini_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")
    openai_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")
    tavily_key = settings.TAVILY_API_KEY or os.getenv("TAVILY_API_KEY", "")

    return SettingsResponse(
        llm_provider=settings.LLM_PROVIDER,
        llm_model=settings.LLM_MODEL,
        search_provider=settings.SEARCH_PROVIDER,
        has_gemini_key=bool(gemini_key),
        has_openai_key=bool(openai_key),
        has_tavily_key=bool(tavily_key),
        is_demo_mode=settings.DEMO_MODE or (not gemini_key and not openai_key)
    )

@router.post("")
def update_settings(req: UpdateSettingsRequest):
    settings.LLM_PROVIDER = req.llm_provider
    settings.SEARCH_PROVIDER = req.search_provider
    settings.DEMO_MODE = req.demo_mode
    return {"status": "success", "message": "Settings updated successfully."}
