from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime
from app.database.session import Base

class ResearchJobModel(Base):
    __tablename__ = "research_jobs"

    id = Column(String, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    depth = Column(String, default="standard")
    constraints = Column(Text, nullable=True)
    source_preferences = Column(Text, nullable=True)  # JSON serialized list
    status = Column(String, default="pending", index=True)  # pending, running, completed, failed
    current_stage = Column(String, default="Pending")
    stage_index = Column(Integer, default=0)
    is_demo_mode = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)

    # Personalized & Multilingual Learning Extensions
    language = Column(String, default="en")
    skill_level = Column(String, default="beginner")
    study_time_hours_per_week = Column(String, default="10-15")
    
    # Structured Stage JSON Payloads
    goal_json = Column(Text, nullable=True)
    plan_json = Column(Text, nullable=True)
    sources_json = Column(Text, nullable=True)
    claims_json = Column(Text, nullable=True)
    comparisons_json = Column(Text, nullable=True)
    verifications_json = Column(Text, nullable=True)
    findings_json = Column(Text, nullable=True)
    roadmap_json = Column(Text, nullable=True)
    learning_resources_json = Column(Text, nullable=True)
    report_json = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size_bytes = Column(Integer, default=0)
    chunk_count = Column(Integer, default=0)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class TaskProgressModel(Base):
    __tablename__ = "task_progress"

    id = Column(String, primary_key=True, index=True)  # research_id:task_id
    research_id = Column(String, index=True, nullable=False)
    phase_number = Column(Integer, nullable=False)
    task_id = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
