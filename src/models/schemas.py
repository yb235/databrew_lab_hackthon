"""Pydantic schemas for API request/response models."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TranscriptionEntryInput(BaseModel):
    """Input model for transcription entry."""
    startTime: str = Field(..., description="Start time in format MM:SS.mmm")
    endTime: str = Field(..., description="End time in format MM:SS.mmm")
    speaker: str = Field(..., description="Speaker name")
    transcript: str = Field(..., description="Transcription text")


class EmotionDetectionInput(BaseModel):
    """Input model for emotion detection."""
    timestamp: str = Field(..., description="Timestamp in format MM:SS.mmm")
    emotion: str = Field(..., description="Detected emotion")
    confidence: Optional[float] = Field(None, description="Confidence score (0-1)")


class TranscriptionUpload(BaseModel):
    """Model for uploading transcription data."""
    entries: List[TranscriptionEntryInput]


class EmotionUpload(BaseModel):
    """Model for uploading emotion data."""
    detections: List[EmotionDetectionInput]


class SessionCreate(BaseModel):
    """Model for creating a new session."""
    name: str = Field(..., description="Session name", min_length=1, max_length=255)


class SessionResponse(BaseModel):
    """Response model for session."""
    id: int
    name: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AlignedEventResponse(BaseModel):
    """Response model for aligned event."""
    id: int
    start_time_ms: int
    end_time_ms: int
    speaker: str
    transcript: str
    emotions: List[Dict[str, Any]]

    class Config:
        from_attributes = True


class InterpretationReportResponse(BaseModel):
    """Response model for interpretation report."""
    id: int
    session_id: int
    report_data: Dict[str, Any]
    summary: Optional[str]
    key_moments: Optional[List[Dict[str, Any]]]
    speaker_profiles: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    database: str
    version: str = "1.0.0"
