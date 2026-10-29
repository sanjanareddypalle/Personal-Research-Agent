import asyncio
import json
import logging
import uuid
from typing import Dict, Any, AsyncGenerator, Optional, List
from datetime import datetime

from app.graph.workflow import research_graph
from app.graph.state import ResearchState
from app.database.session import SyncSessionLocal
from app.database.repository import ResearchRepository
from app.config import settings
from app.agents.llm import LLMClient

logger = logging.getLogger(__name__)

class ResearchService:
    def __init__(self):
        self._listeners: Dict[str, List[asyncio.Queue]] = {}
        self.llm_client = LLMClient()

    def subscribe(self, job_id: str) -> asyncio.Queue:
        q = asyncio.Queue()
        if job_id not in self._listeners:
            self._listeners[job_id] = []
        self._listeners[job_id].append(q)
        return q

    def unsubscribe(self, job_id: str, q: asyncio.Queue):
        if job_id in self._listeners and q in self._listeners[job_id]:
            self._listeners[job_id].remove(q)
            if not self._listeners[job_id]:
                del self._listeners[job_id]

    async def broadcast_event(self, job_id: str, event_type: str, data: Dict[str, Any]):
        if job_id in self._listeners:
            payload = {
                "event": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            }
            for q in list(self._listeners[job_id]):
                try:
                    await q.put(payload)
                except Exception as e:
                    logger.warning(f"Failed to push SSE event to queue: {e}")

    async def start_research_job(
        self,
        query: str,
        depth: str = "standard",
        constraints: Optional[str] = None,
        source_preferences: Optional[List[str]] = None,
        include_kb: bool = True,
        language: str = "en",
        skill_level: str = "beginner",
        study_time_hours_per_week: str = "10-15"
    ) -> str:
        job_id = str(uuid.uuid4())
        is_demo = self.llm_client.is_demo_mode()
        prefs = source_preferences or ["documentation", "research_papers", "industry_reports", "general_web"]

        with SyncSessionLocal() as session:
            repo = ResearchRepository(session)
            repo.create_job(
                job_id=job_id,
                query=query,
                depth=depth,
                constraints=constraints,
                source_preferences=prefs,
                is_demo=is_demo,
                language=language,
                skill_level=skill_level,
                study_time_hours_per_week=study_time_hours_per_week
            )

        asyncio.create_task(self._run_pipeline(
            job_id=job_id,
            query=query,
            depth=depth,
            constraints=constraints,
            source_preferences=prefs,
            is_demo=is_demo,
            language=language,
            skill_level=skill_level,
            study_time_hours_per_week=study_time_hours_per_week
        ))
        return job_id

    async def _run_pipeline(
        self,
        job_id: str,
        query: str,
        depth: str,
        constraints: Optional[str],
        source_preferences: List[str],
        is_demo: bool,
        language: str = "en",
        skill_level: str = "beginner",
        study_time_hours_per_week: str = "10-15"
    ):
        initial_state: ResearchState = {
            "research_id": job_id,
            "query": query,
            "depth": depth,
            "constraints": constraints,
            "source_preferences": source_preferences,
            "is_demo_mode": is_demo,
            "language": language,
            "skill_level": skill_level,
            "study_time_hours_per_week": study_time_hours_per_week,
            "stage_index": 0,
            "current_stage": "Starting",
            "retry_count": 0,
            "logs": [],
            "status": "running"
        }

        await self.broadcast_event(job_id, "stage_change", {
            "stage_name": "Starting",
            "stage_index": 0,
            "message": "Initializing personalized research & learning agent..."
        })

        try:
            async for output in research_graph.astream(initial_state):
                for node_name, state_update in output.items():
                    stage_name = state_update.get("current_stage", node_name)
                    stage_idx = state_update.get("stage_index", 1)
                    logs = state_update.get("logs", [])
                    latest_log = logs[-1] if logs else f"Completed {stage_name}"

                    await self.broadcast_event(job_id, "stage_change", {
                        "stage_name": stage_name,
                        "stage_index": stage_idx,
                        "message": latest_log,
                        "status": "running"
                    })

            with SyncSessionLocal() as session:
                repo = ResearchRepository(session)
                repo.update_job_stage(job_id, "Completed", 9, status="completed")

            await self.broadcast_event(job_id, "complete", {
                "stage_name": "Completed",
                "stage_index": 9,
                "message": "Research analysis, multilingual resources, and personalized roadmap compiled.",
                "status": "completed"
            })

        except Exception as e:
            logger.error(f"Error during graph execution for job {job_id}: {e}", exc_info=True)
            with SyncSessionLocal() as session:
                repo = ResearchRepository(session)
                repo.mark_failed(job_id, str(e))
                
            await self.broadcast_event(job_id, "error", {
                "stage_name": "Failed",
                "message": f"Execution halted: {str(e)}",
                "status": "failed"
            })

research_service = ResearchService()
