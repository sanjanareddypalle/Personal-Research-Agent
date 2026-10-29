import json
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.database.models import ResearchJobModel, DocumentModel, TaskProgressModel

class ResearchRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_job(
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
    ) -> ResearchJobModel:
        job = ResearchJobModel(
            id=job_id,
            query=query,
            depth=depth,
            constraints=constraints,
            source_preferences=json.dumps(source_preferences),
            status="pending",
            current_stage="Pending",
            stage_index=0,
            is_demo_mode=is_demo,
            language=language,
            skill_level=skill_level,
            study_time_hours_per_week=study_time_hours_per_week
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_job(self, job_id: str) -> Optional[ResearchJobModel]:
        return self.db.query(ResearchJobModel).filter(ResearchJobModel.id == job_id).first()

    def list_jobs(self, limit: int = 50) -> List[ResearchJobModel]:
        return self.db.query(ResearchJobModel).order_by(desc(ResearchJobModel.created_at)).limit(limit).all()

    def update_job_stage(self, job_id: str, stage_name: str, stage_index: int, status: str = "running"):
        job = self.get_job(job_id)
        if job:
            job.current_stage = stage_name
            job.stage_index = stage_index
            job.status = status
            self.db.commit()

    def update_job_payload(self, job_id: str, field_name: str, data: Any):
        job = self.get_job(job_id)
        if job:
            serialized = json.dumps(data, default=str) if not isinstance(data, str) else data
            setattr(job, field_name, serialized)
            self.db.commit()

    def mark_completed(self, job_id: str, report_dict: Dict[str, Any]):
        job = self.get_job(job_id)
        if job:
            job.status = "completed"
            job.current_stage = "Completed"
            job.stage_index = 9
            job.report_json = json.dumps(report_dict, default=str)
            if "learning_resources" in report_dict:
                job.learning_resources_json = json.dumps(report_dict["learning_resources"], default=str)
            self.db.commit()

    def mark_failed(self, job_id: str, error_message: str):
        job = self.get_job(job_id)
        if job:
            job.status = "failed"
            job.current_stage = "Failed"
            job.error_message = error_message
            self.db.commit()

    def delete_job(self, job_id: str) -> bool:
        job = self.get_job(job_id)
        if job:
            self.db.query(TaskProgressModel).filter(TaskProgressModel.research_id == job_id).delete()
            self.db.delete(job)
            self.db.commit()
            return True
        return False

    def update_task_progress(self, research_id: str, phase_number: int, task_id: str, is_completed: bool) -> TaskProgressModel:
        progress_id = f"{research_id}:{task_id}"
        item = self.db.query(TaskProgressModel).filter(TaskProgressModel.id == progress_id).first()
        if not item:
            item = TaskProgressModel(
                id=progress_id,
                research_id=research_id,
                phase_number=phase_number,
                task_id=task_id,
                is_completed=is_completed
            )
            self.db.add(item)
        else:
            item.is_completed = is_completed
        self.db.commit()
        self.db.refresh(item)
        
        job = self.get_job(research_id)
        if job and job.report_json:
            try:
                rep = json.loads(job.report_json)
                if "roadmap" in rep and "phases" in rep["roadmap"]:
                    for phase in rep["roadmap"]["phases"]:
                        for t in phase.get("tasks", []):
                            if t.get("id") == task_id:
                                t["is_completed"] = is_completed
                    job.report_json = json.dumps(rep)
                    if job.roadmap_json:
                        rm = json.loads(job.roadmap_json)
                        for phase in rm.get("phases", []):
                            for t in phase.get("tasks", []):
                                if t.get("id") == task_id:
                                    t["is_completed"] = is_completed
                        job.roadmap_json = json.dumps(rm)
                    self.db.commit()
            except Exception:
                pass
        return item

    def get_task_progress(self, research_id: str) -> Dict[str, bool]:
        items = self.db.query(TaskProgressModel).filter(TaskProgressModel.research_id == research_id).all()
        return {item.task_id: item.is_completed for item in items}


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_document(self, doc_id: str, filename: str, file_type: str, file_size: int, chunk_count: int, file_path: str) -> DocumentModel:
        doc = DocumentModel(
            id=doc_id,
            filename=filename,
            file_type=file_type,
            file_size_bytes=file_size,
            chunk_count=chunk_count,
            file_path=file_path
        )
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def list_documents(self) -> List[DocumentModel]:
        return self.db.query(DocumentModel).order_by(desc(DocumentModel.created_at)).all()

    def get_document(self, doc_id: str) -> Optional[DocumentModel]:
        return self.db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()

    def delete_document(self, doc_id: str) -> bool:
        doc = self.get_document(doc_id)
        if doc:
            self.db.delete(doc)
            self.db.commit()
            return True
        return False
