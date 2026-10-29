import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import init_db

@pytest.fixture(autouse=True)
def setup_database():
    init_db()

def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

def test_settings_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/settings")
        assert response.status_code == 200
        data = response.json()
        assert "llm_provider" in data
        assert "search_provider" in data

def test_research_submission_and_lifecycle():
    with TestClient(app) as client:
        # 1. Create Research
        payload = {
            "query": "What GenAI skills should I learn to become an AI engineer in 2027?",
            "depth": "standard",
            "constraints": "Production engineering focus",
            "source_preferences": ["documentation", "research_papers"]
        }
        create_res = client.post("/api/research", json=payload)
        assert create_res.status_code == 200
        job_id = create_res.json()["id"]
        assert len(job_id) > 10

        # 2. Get Detail
        detail_res = client.get(f"/api/research/{job_id}")
        assert detail_res.status_code == 200
        detail = detail_res.json()
        assert detail["id"] == job_id
        assert detail["query"] == payload["query"]

        # 3. List
        list_res = client.get("/api/research")
        assert list_res.status_code == 200
        items = list_res.json()
        assert any(i["id"] == job_id for i in items)

        # 4. Task progress update
        task_res = client.patch(f"/api/research/{job_id}/tasks/task_1_1", json={"is_completed": True})
        assert task_res.status_code == 200
        assert task_res.json()["is_completed"] is True
