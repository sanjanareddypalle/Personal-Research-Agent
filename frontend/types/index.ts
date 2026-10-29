export interface GoalObject {
  objective: string;
  scope: string;
  target_audience: string;
  constraints: string[];
  desired_outcome: string;
  clarification_notes?: string;
}

export interface ResearchPlan {
  primary_questions: string[];
  search_keywords: string[];
  target_source_types: string[];
  evidence_criteria: string;
}

export interface SourceItem {
  id: string;
  title: string;
  url: string;
  publisher?: string;
  publication_date?: string;
  retrieval_date: string;
  snippet: string;
  source_type: string;
  is_primary: boolean;
}

export interface ExtractedClaim {
  id: string;
  claim_text: string;
  source_id: string;
  source_url: string;
  evidence_type: string;
  is_direct_quote: boolean;
  extracted_snippet: string;
}

export interface EvidenceComparisonItem {
  topic_or_claim: string;
  corroborating_source_ids: string[];
  conflicting_source_ids: string[];
  consensus_level: 'Strong' | 'Moderate' | 'Conflicting' | 'Emerging' | string;
  evidence_strength_rationale: string;
  is_repetition_vs_independent: string;
}

export interface VerificationResultItem {
  claim_id: string;
  claim_text: string;
  source_url: string;
  status: 'Verified' | 'Unverified' | 'Refuted' | 'Ambiguous' | string;
  verification_notes: string;
}

export interface FindingItem {
  title: string;
  explanation: string;
  supporting_evidence: string[];
  citations: string[];
  confidence_level: 'High' | 'Medium' | 'Emerging' | string;
  caveats?: string;
}

export interface LearningResourceItem {
  id: string;
  title: string;
  url: string;
  resource_type: 'youtube_video' | 'youtube_playlist' | 'documentation' | 'practice' | string;
  source: string;
  language: 'en' | 'te' | 'hi' | string;
  language_label: string;
  skill_level: 'beginner' | 'intermediate' | 'advanced' | 'all' | string;
  description: string;
  why_useful: string;
  duration?: string;
  is_verified: boolean;
}

export interface RoadmapTask {
  id: string;
  title: string;
  description: string;
  deliverable: string;
  completion_criteria: string;
  is_completed: boolean;
  is_agent_estimate: boolean;
  practical_exercise?: string;
  project_idea?: string;
  recommended_videos?: { title: string; url: string; channel?: string; language?: string }[];
  useful_websites?: { title: string; url: string; name?: string }[];
}

export interface RoadmapPhase {
  phase_number: number;
  phase_title: string;
  duration: string;
  skills_covered: string[];
  prerequisites: string[];
  resources: { title: string; url: string }[];
  tasks: RoadmapTask[];
  milestone: string;
  weekly_breakdown?: string[];
  phase_project?: string;
  video_tutorials?: { title: string; url: string; channel?: string; language?: string }[];
}

export interface ActionRoadmap {
  total_estimated_timeline: string;
  planning_assumptions: string;
  phases: RoadmapPhase[];
  target_language?: string;
  skill_level?: string;
  weekly_study_commitment?: string;
  learning_strategy_summary?: string;
}

export interface ResearchReport {
  title: string;
  executive_summary: string;
  objective_and_scope: string;
  methodology: string;
  key_findings: FindingItem[];
  evidence_comparisons: EvidenceComparisonItem[];
  conflicts_and_uncertainties: string;
  strategic_recommendations: string[];
  roadmap: ActionRoadmap;
  sources_and_citations: SourceItem[];
  limitations_and_future_work: string;
  generated_at: string;
  is_demo_mode: boolean;
  language?: string;
  skill_level?: string;
  study_time_hours_per_week?: string;
  learning_resources?: LearningResourceItem[];
}

export interface ResearchJobSummary {
  id: string;
  query: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | string;
  current_stage: string;
  stage_index: number;
  total_stages: number;
  created_at: string;
  updated_at: string;
  depth: string;
  is_demo_mode: boolean;
  language?: string;
  skill_level?: string;
  study_time_hours_per_week?: string;
}

export interface ResearchJobDetail extends ResearchJobSummary {
  constraints?: string;
  goal?: GoalObject;
  plan?: ResearchPlan;
  sources: SourceItem[];
  findings: FindingItem[];
  comparisons: EvidenceComparisonItem[];
  roadmap?: ActionRoadmap;
  learning_resources?: LearningResourceItem[];
  report?: ResearchReport;
  error_message?: string;
}

export interface DocumentResponse {
  id: string;
  filename: string;
  file_type: string;
  file_size_bytes: number;
  chunk_count: number;
  created_at: string;
}

export interface DocumentChunk {
  id: string;
  document_id: string;
  document_name: string;
  page_number?: number;
  chunk_index: number;
  text: string;
  score?: number;
}

export interface SettingsResponse {
  llm_provider: string;
  llm_model: string;
  search_provider: string;
  has_gemini_key: boolean;
  has_openai_key: boolean;
  has_tavily_key: boolean;
  is_demo_mode: boolean;
}
