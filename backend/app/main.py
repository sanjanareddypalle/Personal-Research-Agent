import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.session import init_db
from app.api.routes_research import router as research_router
from app.api.routes_documents import router as documents_router
from app.api.routes_settings import router as settings_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("researchflow")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database schema on startup...")
    init_db()
    logger.info("Database schema initialized.")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Personal Research-to-Action Agent API powered by LangGraph",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(research_router, prefix=settings.API_V1_STR)
app.include_router(documents_router, prefix=settings.API_V1_STR)
app.include_router(settings_router, prefix=settings.API_V1_STR)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0"
    }


from fastapi.responses import FileResponse

@app.get("/api/download-zip")
def download_project_zip():
    target_zip = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ResearchFlow_AI.zip"))
    if not os.path.exists(target_zip):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Zip file not generated yet")
    return FileResponse(
        target_zip,
        media_type="application/zip",
        filename="ResearchFlow_AI.zip"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
