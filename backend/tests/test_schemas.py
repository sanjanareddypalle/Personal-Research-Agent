import pytest
from app.schemas.research import (
    GoalObject, ResearchPlan, SourceItem, ExtractedClaim,
    EvidenceComparisonItem, VerificationResultItem, FindingItem,
    ActionRoadmap, RoadmapPhase, RoadmapTask, ResearchReport
)

def test_goal_object_validation():
    goal = GoalObject(
        objective="Investigate GenAI skills for 2027",
        scope="Focus on AI systems engineering",
        target_audience="Software Engineers",
        constraints=["Production focus"],
        desired_outcome="Structured roadmap"
    )
    assert goal.objective == "Investigate GenAI skills for 2027"
    assert len(goal.constraints) == 1

def test_research_plan_validation():
    plan = ResearchPlan(
        primary_questions=["Q1?", "Q2?"],
        search_keywords=["kw1", "kw2"],
        target_source_types=["documentation"],
        evidence_criteria="Peer-reviewed or official"
    )
    assert len(plan.primary_questions) == 2
    assert len(plan.search_keywords) == 2

def test_source_item_validation():
    source = SourceItem(
        id="src_1",
        title="Berkeley BAIR",
        url="https://bair.berkeley.edu/blog/test",
        snippet="Compound systems surpass monolithic LLMs.",
        source_type="academic",
        is_primary=True
    )
    assert source.id == "src_1"
    assert source.is_primary is True

def test_full_report_structure():
    task = RoadmapTask(
        id="t1",
        title="Task 1",
        description="Desc",
        deliverable="Code",
        completion_criteria="Tests pass",
        is_completed=False
    )
    phase = RoadmapPhase(
        phase_number=1,
        phase_title="Phase 1",
        duration="4 Weeks",
        milestone="Core MVP",
        tasks=[task]
    )
    roadmap = ActionRoadmap(
        total_estimated_timeline="6 Months",
        planning_assumptions="Standard pace",
        phases=[phase]
    )
    report = ResearchReport(
        title="Report Title",
        executive_summary="Summary",
        objective_and_scope="Scope",
        methodology="Methodology",
        key_findings=[],
        evidence_comparisons=[],
        conflicts_and_uncertainties="Conflicts",
        strategic_recommendations=["Rec 1"],
        roadmap=roadmap,
        sources_and_citations=[],
        limitations_and_future_work="Limitations",
        is_demo_mode=True
    )
    assert report.is_demo_mode is True
    assert len(report.roadmap.phases) == 1
