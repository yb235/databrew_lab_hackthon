"""LangGraph agent for emotion interpretation."""

from langgraph.graph import StateGraph, END
from src.core.agent.state import AgentState
from src.core.agent.nodes import (
    perform_temporal_alignment,
    analyze_emotion_patterns,
    detect_anomalies,
    interpret_moments,
    create_speaker_profiles,
    synthesize_report,
)


def create_interpretation_agent():
    """
    Create the LangGraph agent for emotion interpretation.
    
    The agent follows this workflow:
    1. Temporal Alignment: Match emotions with transcription
    2. Pattern Analysis: Identify emotion patterns and transitions
    3. Anomaly Detection: Find emotional incongruities
    4. Moment Interpretation: Interpret critical moments
    5. Speaker Profiling: Create baseline profiles
    6. Report Synthesis: Generate final report
    """
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("temporal_alignment", perform_temporal_alignment)
    workflow.add_node("pattern_analysis", analyze_emotion_patterns)
    workflow.add_node("anomaly_detection", detect_anomalies)
    workflow.add_node("moment_interpretation", interpret_moments)
    workflow.add_node("speaker_profiling", create_speaker_profiles)
    workflow.add_node("report_synthesis", synthesize_report)
    
    # Define the workflow edges (sequential for now)
    workflow.set_entry_point("temporal_alignment")
    workflow.add_edge("temporal_alignment", "pattern_analysis")
    workflow.add_edge("pattern_analysis", "anomaly_detection")
    workflow.add_edge("anomaly_detection", "moment_interpretation")
    workflow.add_edge("moment_interpretation", "speaker_profiling")
    workflow.add_edge("speaker_profiling", "report_synthesis")
    workflow.add_edge("report_synthesis", END)
    
    # Compile the graph
    agent = workflow.compile()
    
    return agent


def run_interpretation(transcription_entries, emotion_detections, session_id=None):
    """
    Run the interpretation agent on transcription and emotion data.
    
    Args:
        transcription_entries: List of transcription entries
        emotion_detections: List of emotion detections
        session_id: Optional session ID for tracking
        
    Returns:
        Final state with interpretation and report
    """
    agent = create_interpretation_agent()
    
    # Prepare initial state
    initial_state = {
        "session_id": session_id,
        "transcription_entries": transcription_entries,
        "emotion_detections": emotion_detections,
        "steps_completed": []
    }
    
    # Run the agent
    final_state = agent.invoke(initial_state)
    
    return final_state
