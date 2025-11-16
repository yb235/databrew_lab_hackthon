"""Main FastAPI application."""

import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from sqlalchemy.orm import Session
from typing import List
import json

from src.models import (
    SessionCreate,
    SessionResponse,
    TranscriptionUpload,
    EmotionUpload,
    AlignedEventResponse,
    InterpretationReportResponse,
    HealthResponse,
)
from src.models.database import (
    Session as SessionModel,
    SessionStatus,
    TranscriptionEntry,
    EmotionDetection,
    AlignedEvent,
    InterpretationReport,
)
from src.utils.database import get_db_session, init_db
from src.core.alignment import align_emotion_with_transcript, timestamp_to_ms
from src.core.agent import run_interpretation
from src.core.reports import generate_json_report, generate_markdown_report

# Initialize FastAPI app
app = FastAPI(
    title="Emotion Interpretation Machine",
    description="AI agent system for analyzing conversations by combining emotion detection with transcription",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db_session)):
    """Health check endpoint."""
    try:
        # Test database connection
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return HealthResponse(status="ok", database="connected")
    except Exception as e:
        return HealthResponse(status="error", database=f"disconnected: {str(e)}")


@app.post("/api/sessions", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(session_data: SessionCreate, db: Session = Depends(get_db_session)):
    """Create a new analysis session."""
    session = SessionModel(name=session_data.name, status=SessionStatus.CREATED.value)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@app.get("/api/sessions/{session_id}", response_model=SessionResponse)
async def get_session(session_id: int, db: Session = Depends(get_db_session)):
    """Get session details."""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.get("/api/sessions", response_model=List[SessionResponse])
async def list_sessions(db: Session = Depends(get_db_session)):
    """List all sessions."""
    sessions = db.query(SessionModel).order_by(SessionModel.created_at.desc()).all()
    return sessions


@app.post("/api/sessions/{session_id}/transcription", status_code=status.HTTP_201_CREATED)
async def upload_transcription(
    session_id: int,
    data: TranscriptionUpload,
    db: Session = Depends(get_db_session)
):
    """Upload transcription data for a session."""
    # Check if session exists
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Delete existing transcription entries for this session
    db.query(TranscriptionEntry).filter(TranscriptionEntry.session_id == session_id).delete()
    
    # Create new transcription entries
    for entry in data.entries:
        transcription_entry = TranscriptionEntry(
            session_id=session_id,
            start_time_ms=timestamp_to_ms(entry.startTime),
            end_time_ms=timestamp_to_ms(entry.endTime),
            speaker=entry.speaker,
            transcript=entry.transcript,
        )
        db.add(transcription_entry)
    
    # Update session status
    session.status = SessionStatus.UPLOADING.value
    
    db.commit()
    
    return {"message": f"Uploaded {len(data.entries)} transcription entries", "session_id": session_id}


@app.post("/api/sessions/{session_id}/emotions", status_code=status.HTTP_201_CREATED)
async def upload_emotions(
    session_id: int,
    data: EmotionUpload,
    db: Session = Depends(get_db_session)
):
    """Upload emotion detection data for a session."""
    # Check if session exists
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Delete existing emotion detections for this session
    db.query(EmotionDetection).filter(EmotionDetection.session_id == session_id).delete()
    
    # Create new emotion detections
    for detection in data.detections:
        emotion_detection = EmotionDetection(
            session_id=session_id,
            timestamp_ms=timestamp_to_ms(detection.timestamp),
            emotion=detection.emotion,
            confidence=detection.confidence,
        )
        db.add(emotion_detection)
    
    # Update session status to READY if we have both transcription and emotions
    transcription_count = db.query(TranscriptionEntry).filter(
        TranscriptionEntry.session_id == session_id
    ).count()
    
    if transcription_count > 0:
        session.status = SessionStatus.READY.value
    
    db.commit()
    
    return {"message": f"Uploaded {len(data.detections)} emotion detections", "session_id": session_id}


@app.post("/api/sessions/{session_id}/align", status_code=status.HTTP_201_CREATED)
async def align_session_data(session_id: int, db: Session = Depends(get_db_session)):
    """Align transcription and emotion data for a session."""
    # Check if session exists
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get transcription entries
    transcription_entries = db.query(TranscriptionEntry).filter(
        TranscriptionEntry.session_id == session_id
    ).order_by(TranscriptionEntry.start_time_ms).all()
    
    if not transcription_entries:
        raise HTTPException(status_code=400, detail="No transcription data found")
    
    # Get emotion detections
    emotion_detections = db.query(EmotionDetection).filter(
        EmotionDetection.session_id == session_id
    ).order_by(EmotionDetection.timestamp_ms).all()
    
    if not emotion_detections:
        raise HTTPException(status_code=400, detail="No emotion data found")
    
    # Convert to format for alignment algorithm
    transcription_data = [
        {
            "startTime": f"{entry.start_time_ms // 60000:02d}:{(entry.start_time_ms % 60000) // 1000:02d}.{entry.start_time_ms % 1000:03d}",
            "endTime": f"{entry.end_time_ms // 60000:02d}:{(entry.end_time_ms % 60000) // 1000:02d}.{entry.end_time_ms % 1000:03d}",
            "speaker": entry.speaker,
            "transcript": entry.transcript,
        }
        for entry in transcription_entries
    ]
    
    emotion_data = [
        {
            "timestamp": f"{detection.timestamp_ms // 60000:02d}:{(detection.timestamp_ms % 60000) // 1000:02d}.{detection.timestamp_ms % 1000:03d}",
            "emotion": detection.emotion,
            "confidence": detection.confidence,
        }
        for detection in emotion_detections
    ]
    
    # Perform alignment
    window_ms = int(os.getenv("ALIGNMENT_WINDOW_MS", "100"))
    aligned_events = align_emotion_with_transcript(transcription_data, emotion_data, window_ms)
    
    # Delete existing aligned events
    db.query(AlignedEvent).filter(AlignedEvent.session_id == session_id).delete()
    
    # Save aligned events
    for event in aligned_events:
        aligned_event = AlignedEvent(
            session_id=session_id,
            start_time_ms=event["start_time_ms"],
            end_time_ms=event["end_time_ms"],
            speaker=event["speaker"],
            transcript=event["transcript"],
            emotions=event["emotions"],
        )
        db.add(aligned_event)
    
    # Update session status
    session.status = SessionStatus.READY.value
    
    db.commit()
    
    return {
        "message": f"Aligned {len(aligned_events)} events",
        "session_id": session_id,
        "aligned_events_count": len(aligned_events)
    }


@app.get("/api/sessions/{session_id}/aligned-events", response_model=List[AlignedEventResponse])
async def get_aligned_events(session_id: int, db: Session = Depends(get_db_session)):
    """Get aligned events for a session."""
    # Check if session exists
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get aligned events
    aligned_events = db.query(AlignedEvent).filter(
        AlignedEvent.session_id == session_id
    ).order_by(AlignedEvent.start_time_ms).all()
    
    return aligned_events


@app.post("/api/sessions/{session_id}/analyze", status_code=status.HTTP_201_CREATED)
async def analyze_session(session_id: int, db: Session = Depends(get_db_session)):
    """Run AI agent analysis on a session."""
    # Check if session exists
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get transcription entries
    transcription_entries = db.query(TranscriptionEntry).filter(
        TranscriptionEntry.session_id == session_id
    ).order_by(TranscriptionEntry.start_time_ms).all()
    
    if not transcription_entries:
        raise HTTPException(status_code=400, detail="No transcription data found")
    
    # Get emotion detections
    emotion_detections = db.query(EmotionDetection).filter(
        EmotionDetection.session_id == session_id
    ).order_by(EmotionDetection.timestamp_ms).all()
    
    if not emotion_detections:
        raise HTTPException(status_code=400, detail="No emotion data found")
    
    # Convert to format for agent
    transcription_data = [
        {
            "startTime": f"{entry.start_time_ms // 60000:02d}:{(entry.start_time_ms % 60000) // 1000:02d}.{entry.start_time_ms % 1000:03d}",
            "endTime": f"{entry.end_time_ms // 60000:02d}:{(entry.end_time_ms % 60000) // 1000:02d}.{entry.end_time_ms % 1000:03d}",
            "speaker": entry.speaker,
            "transcript": entry.transcript,
        }
        for entry in transcription_entries
    ]
    
    emotion_data = [
        {
            "timestamp": f"{detection.timestamp_ms // 60000:02d}:{(detection.timestamp_ms % 60000) // 1000:02d}.{detection.timestamp_ms % 1000:03d}",
            "emotion": detection.emotion,
            "confidence": detection.confidence,
        }
        for detection in emotion_detections
    ]
    
    # Update session status
    session.status = SessionStatus.ANALYZING.value
    db.commit()
    
    # Run agent analysis
    try:
        result = run_interpretation(transcription_data, emotion_data, session_id=session_id)
        
        # Save interpretation report
        report = InterpretationReport(
            session_id=session_id,
            report_data=result.get("report", {}),
            summary=result.get("report", {}).get("summary"),
            key_moments=result.get("critical_moments", []),
            speaker_profiles=result.get("speaker_profiles", {}),
        )
        db.add(report)
        
        # Update session status
        session.status = SessionStatus.COMPLETED.value
        db.commit()
        
        return {
            "message": "Analysis completed successfully",
            "session_id": session_id,
            "report_id": report.id,
            "critical_moments_found": len(result.get("critical_moments", [])),
            "steps_completed": result.get("steps_completed", [])
        }
    except Exception as e:
        session.status = SessionStatus.FAILED.value
        db.commit()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/api/sessions/{session_id}/report", response_model=InterpretationReportResponse)
async def get_interpretation_report(session_id: int, db: Session = Depends(get_db_session)):
    """Get the interpretation report for a session."""
    # Check if session exists
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get the most recent report
    report = db.query(InterpretationReport).filter(
        InterpretationReport.session_id == session_id
    ).order_by(InterpretationReport.created_at.desc()).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="No report found for this session")
    
    return report


@app.get("/api/sessions/{session_id}/report.json")
async def download_report_json(session_id: int, db: Session = Depends(get_db_session)):
    """Download the interpretation report as JSON."""
    # Check if session exists
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get the most recent report
    report = db.query(InterpretationReport).filter(
        InterpretationReport.session_id == session_id
    ).order_by(InterpretationReport.created_at.desc()).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="No report found for this session")
    
    # Generate JSON report
    json_report = generate_json_report(report.report_data, session.name)
    
    return Response(
        content=json_report,
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=report_{session_id}.json"
        }
    )


@app.get("/api/sessions/{session_id}/report.md")
async def download_report_markdown(session_id: int, db: Session = Depends(get_db_session)):
    """Download the interpretation report as Markdown."""
    # Check if session exists
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get the most recent report
    report = db.query(InterpretationReport).filter(
        InterpretationReport.session_id == session_id
    ).order_by(InterpretationReport.created_at.desc()).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="No report found for this session")
    
    # Generate Markdown report
    md_report = generate_markdown_report(report.report_data, session.name)
    
    return Response(
        content=md_report,
        media_type="text/markdown",
        headers={
            "Content-Disposition": f"attachment; filename=report_{session_id}.md"
        }
    )


@app.get("/api/sessions/{session_id}/status")
async def get_session_status(session_id: int, db: Session = Depends(get_db_session)):
    """Get the current status of a session."""
    # Check if session exists
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Count data
    transcription_count = db.query(TranscriptionEntry).filter(
        TranscriptionEntry.session_id == session_id
    ).count()
    
    emotion_count = db.query(EmotionDetection).filter(
        EmotionDetection.session_id == session_id
    ).count()
    
    aligned_count = db.query(AlignedEvent).filter(
        AlignedEvent.session_id == session_id
    ).count()
    
    report_count = db.query(InterpretationReport).filter(
        InterpretationReport.session_id == session_id
    ).count()
    
    return {
        "session_id": session_id,
        "name": session.name,
        "status": session.status,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "data": {
            "transcription_entries": transcription_count,
            "emotion_detections": emotion_count,
            "aligned_events": aligned_count,
            "reports": report_count
        }
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "3001"))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)
