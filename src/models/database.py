"""Database models for the Emotion Interpretation Machine."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class SessionStatus(str, Enum):
    """Status of an analysis session."""
    CREATED = "created"
    UPLOADING = "uploading"
    READY = "ready"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"


class Session(Base):
    """Analysis session model."""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    status = Column(String(50), default=SessionStatus.CREATED.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transcription_entries = relationship("TranscriptionEntry", back_populates="session", cascade="all, delete-orphan")
    emotion_detections = relationship("EmotionDetection", back_populates="session", cascade="all, delete-orphan")
    aligned_events = relationship("AlignedEvent", back_populates="session", cascade="all, delete-orphan")
    interpretation_reports = relationship("InterpretationReport", back_populates="session", cascade="all, delete-orphan")


class TranscriptionEntry(Base):
    """Transcription data entry model."""
    __tablename__ = "transcription_entries"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    start_time_ms = Column(Integer, nullable=False)  # Milliseconds
    end_time_ms = Column(Integer, nullable=False)    # Milliseconds
    speaker = Column(String(255), nullable=False)
    transcript = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    session = relationship("Session", back_populates="transcription_entries")


class EmotionDetection(Base):
    """Emotion detection data model."""
    __tablename__ = "emotion_detections"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    timestamp_ms = Column(Integer, nullable=False)  # Milliseconds
    emotion = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=True)  # Optional confidence score
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    session = relationship("Session", back_populates="emotion_detections")


class AlignedEvent(Base):
    """Aligned emotion-transcription event model."""
    __tablename__ = "aligned_events"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    transcription_entry_id = Column(Integer, ForeignKey("transcription_entries.id", ondelete="CASCADE"), nullable=True)
    start_time_ms = Column(Integer, nullable=False)
    end_time_ms = Column(Integer, nullable=False)
    speaker = Column(String(255), nullable=False)
    transcript = Column(Text, nullable=False)
    emotions = Column(JSON, nullable=False)  # List of emotions with timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    session = relationship("Session", back_populates="aligned_events")


class InterpretationReport(Base):
    """AI-generated interpretation report model."""
    __tablename__ = "interpretation_reports"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    report_data = Column(JSON, nullable=False)  # Full report as JSON
    summary = Column(Text, nullable=True)
    key_moments = Column(JSON, nullable=True)  # List of critical moments
    speaker_profiles = Column(JSON, nullable=True)  # Speaker emotion profiles
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    session = relationship("Session", back_populates="interpretation_reports")
