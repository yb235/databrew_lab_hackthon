"""End-to-end tests for the complete workflow."""

import pytest
import json
from pathlib import Path
from fastapi.testclient import TestClient
from src.main import app
from src.utils.database import init_db


# Initialize test client
client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    """Initialize database for tests."""
    init_db()
    yield


class TestCompleteWorkflow:
    """Test the complete workflow from upload to report download."""
    
    def test_full_workflow_holmes(self, setup_database):
        """Test complete workflow with Holmes example."""
        # Load example data
        examples_dir = Path(__file__).parent.parent.parent / "examples"
        
        with open(examples_dir / "transcription_holmes.json") as f:
            transcription_data = json.load(f)
        
        with open(examples_dir / "emotion_analysis_holmes.json") as f:
            emotion_data = json.load(f)
        
        # Step 1: Create session
        response = client.post(
            "/api/sessions",
            json={"name": "Holmes E2E Test"}
        )
        assert response.status_code == 201
        session = response.json()
        session_id = session["id"]
        
        # Step 2: Upload transcription
        response = client.post(
            f"/api/sessions/{session_id}/transcription",
            json={"entries": transcription_data}
        )
        assert response.status_code == 201
        
        # Step 3: Upload emotions
        response = client.post(
            f"/api/sessions/{session_id}/emotions",
            json={"detections": emotion_data}
        )
        assert response.status_code == 201
        
        # Step 4: Check status
        response = client.get(f"/api/sessions/{session_id}/status")
        assert response.status_code == 200
        status_data = response.json()
        assert status_data["status"].upper() == "READY"
        assert status_data["data"]["transcription_entries"] > 0
        assert status_data["data"]["emotion_detections"] > 0
        
        # Step 5: Run analysis
        response = client.post(f"/api/sessions/{session_id}/analyze")
        assert response.status_code == 201
        analysis_result = response.json()
        assert "report_id" in analysis_result
        
        # Step 6: Get report
        response = client.get(f"/api/sessions/{session_id}/report")
        assert response.status_code == 200
        report = response.json()
        assert report["session_id"] == session_id
        assert report["summary"] is not None
        
        # Step 7: Download JSON report
        response = client.get(f"/api/sessions/{session_id}/report.json")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        json_report = json.loads(response.content)
        assert "metadata" in json_report
        assert json_report["metadata"]["session_name"] == "Holmes E2E Test"
        
        # Step 8: Download Markdown report
        response = client.get(f"/api/sessions/{session_id}/report.md")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/markdown; charset=utf-8"
        md_report = response.content.decode("utf-8")
        assert "# Emotion Interpretation Report" in md_report
        assert "Holmes E2E Test" in md_report
    
    def test_error_handling_no_data(self, setup_database):
        """Test error handling when trying to analyze without data."""
        # Create session
        response = client.post(
            "/api/sessions",
            json={"name": "Empty Session"}
        )
        assert response.status_code == 201
        session_id = response.json()["id"]
        
        # Try to analyze without data
        response = client.post(f"/api/sessions/{session_id}/analyze")
        assert response.status_code == 400
        assert "No transcription data found" in response.json()["detail"]
    
    def test_error_handling_missing_session(self):
        """Test error handling for non-existent session."""
        response = client.get("/api/sessions/99999/status")
        assert response.status_code == 404
        assert "Session not found" in response.json()["detail"]
    
    def test_error_handling_no_report(self, setup_database):
        """Test error handling when requesting report before analysis."""
        # Create session
        response = client.post(
            "/api/sessions",
            json={"name": "No Report Session"}
        )
        assert response.status_code == 201
        session_id = response.json()["id"]
        
        # Try to get report
        response = client.get(f"/api/sessions/{session_id}/report.json")
        assert response.status_code == 404
        assert "No report found" in response.json()["detail"]


class TestAPIEndpoints:
    """Test individual API endpoints."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["database"] == "connected"
    
    def test_list_sessions(self, setup_database):
        """Test listing sessions."""
        response = client.get("/api/sessions")
        assert response.status_code == 200
        sessions = response.json()
        assert isinstance(sessions, list)
    
    def test_create_and_get_session(self, setup_database):
        """Test creating and retrieving a session."""
        # Create
        response = client.post(
            "/api/sessions",
            json={"name": "Test Session"}
        )
        assert response.status_code == 201
        session = response.json()
        assert session["name"] == "Test Session"
        assert "id" in session
        
        # Get
        response = client.get(f"/api/sessions/{session['id']}")
        assert response.status_code == 200
        retrieved = response.json()
        assert retrieved["id"] == session["id"]
        assert retrieved["name"] == "Test Session"


class TestPerformance:
    """Test performance targets."""
    
    def test_alignment_performance(self, setup_database):
        """Test that alignment completes within 5 seconds."""
        import time
        
        # Load example data
        examples_dir = Path(__file__).parent.parent.parent / "examples"
        
        with open(examples_dir / "transcription_holmes.json") as f:
            transcription_data = json.load(f)
        
        with open(examples_dir / "emotion_analysis_holmes.json") as f:
            emotion_data = json.load(f)
        
        # Create session and upload data
        response = client.post("/api/sessions", json={"name": "Perf Test"})
        session_id = response.json()["id"]
        
        client.post(f"/api/sessions/{session_id}/transcription", json={"entries": transcription_data})
        client.post(f"/api/sessions/{session_id}/emotions", json={"detections": emotion_data})
        
        # Test alignment performance
        start_time = time.time()
        response = client.post(f"/api/sessions/{session_id}/align")
        elapsed_time = time.time() - start_time
        
        assert response.status_code == 201
        assert elapsed_time < 5.0, f"Alignment took {elapsed_time:.2f}s, should be < 5s"
