from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

# --- Learning Resources Schema ---
class LearningResourceItem(BaseModel):
    id: str = Field(..., description="Unique resource ID")
    title: str = Field(..., description="Title of video, course, or documentation")
    url: str = Field(..., description="Verified direct URL (YouTube, official docs, learning platform)")
    resource_type: str = Field("youtube_video", description="'youtube_video', 'youtube_playlist', 'documentation', 'website', 'practice_platform'")
    channel_or_platform: str = Field(..., description="Creator channel or platform (e.g. Vamsi Bhavani, Chai aur Code, CampusX, DeepLearning.AI)")
    language: str = Field("English", description="Resource language e.g. 'Telugu', 'Hindi', 'English'")
    skill_level: str = Field("Beginner", description="'Beginner', 'Intermediate', 'Advanced', 'All Levels'")
    duration_or_read_time: Optional[str] = Field(None, description="e.g. '45 mins', 'Full Playlist', 'Documentation'")
    why_useful: str = Field(..., description="Detailed explanation of why this resource is recommended and what concepts it teaches")
    topic_tag: str = Field("General", description="Topic category e.g. 'Python', 'LLMs & RAG', 'LangGraph & Agents'")
    thumbnail_url: Optional[str] = Field(None, description="Optional preview thumbnail URL")

# --- Node 1: Goal Understanding ---
class GoalObject(BaseModel):
    objective: str = Field(..., description="Primary research objective")
    scope: str = Field(..., description="Boundaries and constraints of the inquiry")
    target_audience: str = Field(..., description="Intended audience for the research report")
    constraints: List[str] = Field(default_factory=list, description="Explicit or implicit constraints")
    desired_outcome: str = Field(..., description="Actionable outcome or deliverable requested")
    clarification_notes: Optional[str] = Field(None, description="Notes on minor ambiguities resolved")
    preferred_language: str = Field("en", description="'en', 'te', 'hi'")
    skill_level: str = Field("beginner", description="'beginner', 'intermediate', 'advanced'")
    study_time_hours_per_week: str = Field("10-15", description="Study time commitment")

# --- Node 2: Research Planning ---
class ResearchPlan(BaseModel):
    primary_questions: List[str] = Field(..., description="Key research sub-questions to investigate")
    search_keywords: List[str] = Field(..., description="High-yield search queries and concepts")
    target_source_types: List[str] = Field(..., description="Required source types (docs, papers, industry reports, web)")
    evidence_criteria: str = Field(..., description="Criteria required to substantiate or refute findings")

# --- Node 3: Source Collection ---
class SourceItem(BaseModel):
    id: str = Field(..., description="Unique source identifier")
    title: str = Field(..., description="Title of the source webpage or document")
    url: str = Field(..., description="Canonical URL or file identifier")
    publisher: Optional[str] = Field("Unknown", description="Publisher or publication venue")
    publication_date: Optional[str] = Field(None, description="Date published if detectable")
    retrieval_date: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d"), description="Date retrieved")
    snippet: str = Field(..., description="Key excerpt or abstract")
    source_type: str = Field("web", description="'web', 'academic', 'documentation', or 'local_kb'")
    is_primary: bool = Field(False, description="Whether this is a primary or official source")

# --- Node 4: Information Extraction ---
class ExtractedClaim(BaseModel):
    id: str = Field(..., description="Unique claim ID")
    claim_text: str = Field(..., description="Atomic factual claim or recommendation")
    source_id: str = Field(..., description="Associated source ID")
    source_url: str = Field(..., description="Direct URL of the supporting source")
    evidence_type: str = Field("fact", description="'statistic', 'fact', 'recommendation', 'trend', or 'definition'")
    is_direct_quote: bool = Field(False, description="Direct quote vs model interpretation")
    extracted_snippet: str = Field(..., description="Original text excerpt backing the claim")

# --- Node 5: Evidence Comparison ---
class EvidenceComparisonItem(BaseModel):
    topic_or_claim: str = Field(..., description="Core subject or assertion being compared")
    corroborating_source_ids: List[str] = Field(default_factory=list, description="Sources agreeing with or reinforcing this")
    conflicting_source_ids: List[str] = Field(default_factory=list, description="Sources disagreeing or presenting alternatives")
    consensus_level: str = Field("Strong", description="'Strong', 'Moderate', 'Conflicting', or 'Emerging'")
    evidence_strength_rationale: str = Field(..., description="Why this strength score was assigned")
    is_repetition_vs_independent: str = Field(..., description="Distinguishes independent confirmation from replicated claims")

# --- Node 6: Source Verification ---
class VerificationResultItem(BaseModel):
    claim_id: str = Field(..., description="ID of claim tested")
    claim_text: str = Field(..., description="The tested assertion")
    source_url: str = Field(..., description="Source checked")
    status: str = Field("Verified", description="'Verified', 'Unverified', 'Refuted', or 'Ambiguous'")
    verification_notes: str = Field(..., description="Rationale for verification state")

# --- Node 7: Knowledge Synthesis ---
class FindingItem(BaseModel):
    title: str = Field(..., description="Concise finding headline")
    explanation: str = Field(..., description="Detailed synthesis and implications")
    supporting_evidence: List[str] = Field(default_factory=list, description="Bullet points of verified supporting evidence")
    citations: List[str] = Field(default_factory=list, description="Source URLs or titles cited")
    confidence_level: str = Field("High", description="'High', 'Medium', or 'Emerging'")
    caveats: Optional[str] = Field(None, description="Important qualifications or constraints")

# --- Node 8: Action Roadmap ---
class RoadmapTask(BaseModel):
    id: str = Field(..., description="Unique task ID e.g. task_1_1")
    title: str = Field(..., description="Actionable task headline")
    description: str = Field(..., description="Detailed instructions and steps")
    deliverable: str = Field(..., description="Concrete output or milestone proof")
    completion_criteria: str = Field(..., description="Clear criteria to verify completion")
    is_completed: bool = Field(False, description="User checked completion status")
    is_agent_estimate: bool = Field(False, description="True if planning estimate vs source-derived")
    practical_exercise: Optional[str] = Field(None, description="Hands-on coding exercise or practical drill")
    project_idea: Optional[str] = Field(None, description="Mini project applying this task")
    recommended_videos: List[LearningResourceItem] = Field(default_factory=list, description="Recommended video tutorials")
    useful_websites: List[Dict[str, str]] = Field(default_factory=list, description="Helpful websites or docs")

class RoadmapPhase(BaseModel):
    phase_number: int = Field(..., description="Phase sequence index")
    phase_title: str = Field(..., description="Phase name (e.g. Phase 1: Core Fundamentals)")
    duration: str = Field(..., description="Estimated timeline e.g. 'Weeks 1-4'")
    skills_covered: List[str] = Field(default_factory=list, description="Skills acquired in this phase")
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisite knowledge or tasks")
    resources: List[Dict[str, str]] = Field(default_factory=list, description="List of dicts with title & url")
    tasks: List[RoadmapTask] = Field(default_factory=list, description="Actionable tasks")
    milestone: str = Field(..., description="Capstone milestone for the phase")
    weekly_breakdown: List[str] = Field(default_factory=list, description="Weekly or daily breakdown of topics")
    phase_project: Optional[str] = Field(None, description="Capstone project to build for this phase")
    video_tutorials: List[LearningResourceItem] = Field(default_factory=list, description="Top video tutorials matching phase")

class ActionRoadmap(BaseModel):
    total_estimated_timeline: str = Field(..., description="Overall duration e.g. '6 Months (12-15 hours/week)'")
    planning_assumptions: str = Field(..., description="Assumptions made regarding hours/week, background, etc.")
    target_language: str = Field("en", description="'en', 'te', 'hi'")
    skill_level: str = Field("beginner", description="'beginner', 'intermediate', 'advanced'")
    weekly_study_commitment: str = Field("10-15 hrs/week", description="Study time commitment")
    learning_strategy_summary: str = Field("", description="High-level personalized strategy statement")
    phases: List[RoadmapPhase] = Field(default_factory=list)

# --- Node 9: Final Report (10 Sections + Learning Resources) ---
class ResearchReport(BaseModel):
    title: str = Field(..., description="Comprehensive research title")
    executive_summary: str = Field(..., description="Section 1: High-level executive summary")
    objective_and_scope: str = Field(..., description="Section 2: Research questions and boundaries")
    methodology: str = Field(..., description="Section 3: Pipeline and search methodology used")
    key_findings: List[FindingItem] = Field(default_factory=list, description="Section 4: Thematic verified findings")
    evidence_comparisons: List[EvidenceComparisonItem] = Field(default_factory=list, description="Section 5: Cross-source matrix")
    conflicts_and_uncertainties: str = Field(..., description="Section 6: Conflicting data and unresolved questions")
    strategic_recommendations: List[str] = Field(default_factory=list, description="Section 7: Clear recommendations")
    roadmap: ActionRoadmap = Field(..., description="Section 8: Prioritized execution roadmap")
    sources_and_citations: List[SourceItem] = Field(default_factory=list, description="Section 9: Complete bibliography")
    limitations_and_future_work: str = Field(..., description="Section 10: Study constraints and follow-up paths")
    learning_resources: List[LearningResourceItem] = Field(default_factory=list, description="Recommended YouTube tutorials, playlists, websites, and courses")
    target_language: str = Field("en", description="'en' (English), 'te' (Telugu), 'hi' (Hindi)")
    skill_level: str = Field("beginner", description="'beginner', 'intermediate', 'advanced'")
    weekly_study_commitment: str = Field("10-15 hrs/week", description="Study time allocation")
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))
    is_demo_mode: bool = Field(False, description="Flag indicating if generated via Demo Mode")

# --- API Request / Response Schemas ---
class CreateResearchRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Research question")
    depth: str = Field("standard", description="'quick', 'standard', 'comprehensive'")
    source_preferences: List[str] = Field(
        default=["documentation", "research_papers", "industry_reports", "general_web"],
        description="Preferences for source selection"
    )
    constraints: Optional[str] = Field(None, description="Optional custom constraints or timeline")
    include_knowledge_base: bool = Field(True, description="Whether to include indexed local RAG documents")
    language: str = Field("en", description="Target learning language: 'en' (English), 'te' (Telugu), 'hi' (Hindi)")
    skill_level: str = Field("beginner", description="User's current knowledge level: 'beginner', 'intermediate', 'advanced'")
    study_time_hours_per_week: str = Field("10-15", description="Weekly study commitment: '5-10', '10-15', '15-20', '20+'")

class TaskUpdateStatusRequest(BaseModel):
    is_completed: bool

class ResearchJobSummary(BaseModel):
    id: str
    query: str
    status: str
    current_stage: str
    stage_index: int
    total_stages: int = 9
    created_at: str
    updated_at: str
    depth: str
    is_demo_mode: bool
    language: str = "en"
    skill_level: str = "beginner"
    study_time_hours_per_week: str = "10-15"

class ResearchJobDetail(BaseModel):
    id: str
    query: str
    status: str
    current_stage: str
    stage_index: int
    total_stages: int = 9
    created_at: str
    updated_at: str
    depth: str
    constraints: Optional[str] = None
    is_demo_mode: bool = False
    language: str = "en"
    skill_level: str = "beginner"
    study_time_hours_per_week: str = "10-15"
    goal: Optional[GoalObject] = None
    plan: Optional[ResearchPlan] = None
    sources: List[SourceItem] = []
    findings: List[FindingItem] = []
    comparisons: List[EvidenceComparisonItem] = []
    roadmap: Optional[ActionRoadmap] = None
    learning_resources: List[LearningResourceItem] = []
    report: Optional[ResearchReport] = None
    error_message: Optional[str] = None
