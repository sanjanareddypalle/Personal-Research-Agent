import json
import asyncio
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.session import get_db, SyncSessionLocal
from app.database.repository import ResearchRepository
from app.schemas.research import (
    CreateResearchRequest, ResearchJobSummary, ResearchJobDetail,
    ResearchReport, TaskUpdateStatusRequest, GoalObject, ResearchPlan,
    SourceItem, FindingItem, EvidenceComparisonItem, ActionRoadmap,
    LearningResourceItem
)
from app.services.research_service import research_service
from app.services.export_service import export_report_to_markdown, export_report_to_pdf

router = APIRouter(prefix="/research", tags=["Research"])

@router.post("", response_model=dict)
async def create_research(req: CreateResearchRequest):
    """Initiates a new research inquiry and triggers the LangGraph workflow."""
    job_id = await research_service.start_research_job(
        query=req.query,
        depth=req.depth,
        constraints=req.constraints,
        source_preferences=req.source_preferences,
        include_kb=req.include_knowledge_base,
        language=req.language or "en",
        skill_level=req.skill_level or "beginner",
        study_time_hours_per_week=req.study_time_hours_per_week or "10-15"
    )
    return {"id": job_id, "message": "Research job submitted successfully."}

@router.get("", response_model=List[ResearchJobSummary])
def list_research_jobs():
    with SyncSessionLocal() as session:
        repo = ResearchRepository(session)
        jobs = repo.list_jobs(limit=50)
        results = []
        for j in jobs:
            results.append(ResearchJobSummary(
                id=j.id,
                query=j.query,
                status=j.status,
                current_stage=j.current_stage,
                stage_index=j.stage_index,
                total_stages=9,
                created_at=j.created_at.strftime("%Y-%m-%d %H:%M"),
                updated_at=j.updated_at.strftime("%Y-%m-%d %H:%M"),
                depth=j.depth or "standard",
                is_demo_mode=bool(j.is_demo_mode),
                language=j.language or "en",
                skill_level=j.skill_level or "beginner",
                study_time_hours_per_week=j.study_time_hours_per_week or "10-15"
            ))
        return results

@router.get("/{research_id}", response_model=ResearchJobDetail)
def get_research_detail(research_id: str):
    with SyncSessionLocal() as session:
        repo = ResearchRepository(session)
        j = repo.get_job(research_id)
        if not j:
            raise HTTPException(status_code=404, detail="Research job not found")

        # Parse payloads
        goal = GoalObject.model_validate(json.loads(j.goal_json)) if j.goal_json else None
        plan = ResearchPlan.model_validate(json.loads(j.plan_json)) if j.plan_json else None
        sources = [SourceItem.model_validate(s) for s in json.loads(j.sources_json)] if j.sources_json else []
        findings = [FindingItem.model_validate(f) for f in json.loads(j.findings_json)] if j.findings_json else []
        comparisons = [EvidenceComparisonItem.model_validate(c) for c in json.loads(j.comparisons_json)] if j.comparisons_json else []
        roadmap = ActionRoadmap.model_validate(json.loads(j.roadmap_json)) if j.roadmap_json else None
        report = ResearchReport.model_validate(json.loads(j.report_json)) if j.report_json else None
        
        learning_resources = []
        if j.learning_resources_json:
            try:
                learning_resources = [LearningResourceItem.model_validate(r) for r in json.loads(j.learning_resources_json)]
            except Exception:
                pass
        elif report and report.learning_resources:
            learning_resources = report.learning_resources

        return ResearchJobDetail(
            id=j.id,
            query=j.query,
            status=j.status,
            current_stage=j.current_stage,
            stage_index=j.stage_index,
            total_stages=9,
            created_at=j.created_at.strftime("%Y-%m-%d %H:%M"),
            updated_at=j.updated_at.strftime("%Y-%m-%d %H:%M"),
            depth=j.depth or "standard",
            constraints=j.constraints,
            is_demo_mode=bool(j.is_demo_mode),
            language=j.language or "en",
            skill_level=j.skill_level or "beginner",
            study_time_hours_per_week=j.study_time_hours_per_week or "10-15",
            goal=goal,
            plan=plan,
            sources=sources,
            findings=findings,
            comparisons=comparisons,
            roadmap=roadmap,
            learning_resources=learning_resources,
            report=report,
            error_message=j.error_message
        )

@router.get("/{research_id}/events")
async def stream_research_events(research_id: str):
    """Server-Sent Events (SSE) streaming real-time stage progress."""
    queue = research_service.subscribe(research_id)

    async def event_generator():
        try:
            yield f"event: ping\ndata: {json.dumps({'message': 'Connected to research stream'})}\n\n"
            
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=25.0)
                    yield f"event: {event['event']}\ndata: {json.dumps(event['data'])}\n\n"
                    if event["event"] in ["complete", "error"]:
                        break
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
        finally:
            research_service.unsubscribe(research_id, queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.get("/{research_id}/report", response_model=ResearchReport)
def get_report(research_id: str):
    with SyncSessionLocal() as session:
        repo = ResearchRepository(session)
        j = repo.get_job(research_id)
        if not j or not j.report_json:
            raise HTTPException(status_code=404, detail="Report not ready or job not found")
        return ResearchReport.model_validate(json.loads(j.report_json))

@router.get("/{research_id}/export/markdown")
def export_markdown(research_id: str):
    with SyncSessionLocal() as session:
        repo = ResearchRepository(session)
        j = repo.get_job(research_id)
        if not j or not j.report_json:
            raise HTTPException(status_code=404, detail="Report not ready or job not found")
        report = ResearchReport.model_validate(json.loads(j.report_json))
        md_text = export_report_to_markdown(report)
        return Response(
            content=md_text,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename=research_report_{research_id[:8]}.md"}
        )

@router.get("/{research_id}/export/pdf")
def export_pdf(research_id: str):
    with SyncSessionLocal() as session:
        repo = ResearchRepository(session)
        j = repo.get_job(research_id)
        if not j or not j.report_json:
            raise HTTPException(status_code=404, detail="Report not ready or job not found")
        report = ResearchReport.model_validate(json.loads(j.report_json))
        pdf_bytes = export_report_to_pdf(report)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=research_report_{research_id[:8]}.pdf"}
        )

@router.patch("/{research_id}/tasks/{task_id}")
def update_task_progress(research_id: str, task_id: str, req: TaskUpdateStatusRequest):
    """Updates user check state for a roadmap task and persists to DB."""
    with SyncSessionLocal() as session:
        repo = ResearchRepository(session)
        phase_num = 1
        parts = task_id.split("_")
        if len(parts) >= 2 and parts[1].isdigit():
            phase_num = int(parts[1])
        item = repo.update_task_progress(research_id, phase_num, task_id, req.is_completed)
        return {"status": "success", "task_id": task_id, "is_completed": item.is_completed}

@router.delete("/{research_id}")
def delete_research(research_id: str):
    with SyncSessionLocal() as session:
        repo = ResearchRepository(session)
        success = repo.delete_job(research_id)
        if not success:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"status": "success", "message": f"Research job {research_id} deleted."}
