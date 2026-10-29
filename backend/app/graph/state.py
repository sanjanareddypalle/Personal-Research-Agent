from typing import List, Optional, Dict, Any, Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel
from app.schemas.research import (
    GoalObject, ResearchPlan, SourceItem, ExtractedClaim,
    EvidenceComparisonItem, VerificationResultItem, FindingItem,
    ActionRoadmap, ResearchReport, LearningResourceItem
)

class ResearchState(TypedDict, total=False):
    research_id: str
    query: str
    depth: str
    constraints: Optional[str]
    source_preferences: List[str]
    is_demo_mode: bool
    
    # Personalization & Multilingual
    language: str  # "en", "te", "hi"
    skill_level: str  # "beginner", "intermediate", "advanced"
    study_time_hours_per_week: str  # e.g. "10-15"
    
    # Node outputs
    goal: Optional[GoalObject]
    plan: Optional[ResearchPlan]
    sources: List[SourceItem]
    claims: List[ExtractedClaim]
    comparisons: List[EvidenceComparisonItem]
    verifications: List[VerificationResultItem]
    findings: List[FindingItem]
    roadmap: Optional[ActionRoadmap]
    learning_resources: List[LearningResourceItem]
    report: Optional[ResearchReport]
    
    # Orchestration & Progress tracking
    current_stage: str
    stage_index: int
    retry_count: int
    errors: List[str]
    logs: List[str]
    status: str
