import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ResearchFlow AI"
    API_V1_STR: str = "/api"
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    UPLOAD_DIR: Path = DATA_DIR / "uploads"
    VECTOR_INDEX_DIR: Path = DATA_DIR / "faiss_index"
    
    # Database
    DATABASE_URL: str = f"sqlite+aiosqlite:///{DATA_DIR}/researchflow.db"
    SYNC_DATABASE_URL: str = f"sqlite:///{DATA_DIR}/researchflow.db"
    
    # LLM Settings
    LLM_PROVIDER: str = "gemini"  # "gemini", "openai", "demo"
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gemini-2.5-flash"
    
    # Search Provider
    SEARCH_PROVIDER: str = "duckduckgo"  # "duckduckgo", "tavily", "demo"
    TAVILY_API_KEY: str = ""
    
    # Embeddings
    EMBEDDING_PROVIDER: str = "local"  # "local", "gemini", "openai"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Demo Mode
    DEMO_MODE: bool = False
    
    # CORS
    FRONTEND_ORIGIN: str = "http://localhost:3005"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.VECTOR_INDEX_DIR.mkdir(parents=True, exist_ok=True)
