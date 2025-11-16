"""Agent state definition for LangGraph."""

from typing import List, Dict, Any, Optional, TypedDict


class AgentState(TypedDict, total=False):
    """State for the emotion interpretation agent."""
    
    # Input data
    session_id: int
    transcription_entries: List[Dict[str, Any]]
    emotion_detections: List[Dict[str, Any]]
    
    # Alignment results
    aligned_events: List[Dict[str, Any]]
    
    # Analysis results
    emotion_patterns: Dict[str, Any]
    anomalies: List[Dict[str, Any]]
    critical_moments: List[Dict[str, Any]]
    speaker_profiles: Dict[str, Any]
    
    # Final output
    interpretation: str
    report: Dict[str, Any]
    
    # Metadata
    error: Optional[str]
    steps_completed: List[str]
