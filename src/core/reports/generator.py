"""Report generation logic for different formats."""

import json
from datetime import datetime, timezone
from typing import Dict, Any, List


def format_timestamp(ms: int) -> str:
    """Convert milliseconds to MM:SS.mmm format."""
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    milliseconds = ms % 1000
    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def generate_json_report(report_data: Dict[str, Any], session_name: str = None) -> str:
    """
    Generate a structured JSON report from agent output.
    
    Args:
        report_data: The report data from the agent
        session_name: Optional session name
        
    Returns:
        JSON string of the structured report
    """
    # Build structured report
    structured_report = {
        "metadata": {
            "session_name": session_name or "Unknown",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0"
        },
        "summary": report_data.get("summary", "No summary available"),
        "key_moments": report_data.get("critical_moments", []),
        "speaker_profiles": report_data.get("speaker_profiles", {}),
        "behavioral_insights": report_data.get("behavioral_insights", []),
        "emotion_patterns": report_data.get("emotion_patterns", {}),
        "anomalies": report_data.get("anomalies", []),
        "timeline": _build_timeline(report_data)
    }
    
    return json.dumps(structured_report, indent=2)


def generate_markdown_report(report_data: Dict[str, Any], session_name: str = None) -> str:
    """
    Generate a human-readable Markdown report from agent output.
    
    Args:
        report_data: The report data from the agent
        session_name: Optional session name
        
    Returns:
        Markdown formatted report string
    """
    session_name = session_name or "Unknown Session"
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Build Markdown report
    md = []
    
    # Header
    md.append(f"# Emotion Interpretation Report: {session_name}\n")
    md.append(f"**Generated:** {timestamp}\n")
    md.append("---\n")
    
    # Executive Summary
    md.append("## Executive Summary\n")
    summary = report_data.get("summary", "No summary available")
    md.append(f"{summary}\n")
    md.append("")
    
    # Key Moments
    critical_moments = report_data.get("critical_moments", [])
    if critical_moments:
        md.append("## Critical Moments\n")
        md.append(f"Found {len(critical_moments)} significant moment(s) requiring attention:\n")
        for i, moment in enumerate(critical_moments, 1):
            timestamp_str = moment.get("timestamp_formatted", moment.get("timestamp", "Unknown"))
            speaker = moment.get("speaker", "Unknown")
            reason = moment.get("reason", "No reason provided")
            transcript = moment.get("transcript", "")
            emotions = moment.get("emotions", [])
            
            md.append(f"### {i}. {timestamp_str} - {speaker}\n")
            if transcript:
                md.append(f"**Quote:** \"{transcript}\"\n")
            if emotions:
                emotion_str = ", ".join([f"{e.get('emotion', 'Unknown')} ({e.get('confidence', 0):.2f})" for e in emotions])
                md.append(f"**Emotions:** {emotion_str}\n")
            md.append(f"**Analysis:** {reason}\n")
            md.append("")
    
    # Speaker Profiles
    speaker_profiles = report_data.get("speaker_profiles", {})
    if speaker_profiles:
        md.append("## Speaker Profiles\n")
        for speaker, profile in speaker_profiles.items():
            md.append(f"### {speaker}\n")
            
            baseline = profile.get("baseline_emotions", {})
            if baseline:
                md.append("**Baseline Emotions:**\n")
                for emotion, data in baseline.items():
                    count = data.get("count", 0)
                    avg_conf = data.get("avg_confidence", 0)
                    md.append(f"- {emotion}: {count} occurrences (avg confidence: {avg_conf:.2f})\n")
                md.append("")
            
            patterns = profile.get("patterns", [])
            if patterns:
                md.append("**Patterns:**\n")
                for pattern in patterns:
                    md.append(f"- {pattern}\n")
                md.append("")
    
    # Emotional Patterns
    emotion_patterns = report_data.get("emotion_patterns", {})
    if emotion_patterns:
        md.append("## Emotion Patterns\n")
        
        # Handle both flat dict and nested dict with "by_speaker"
        patterns_by_speaker = emotion_patterns.get("by_speaker", emotion_patterns) if isinstance(emotion_patterns, dict) else {}
        
        for speaker, pattern_data in patterns_by_speaker.items():
            if not isinstance(pattern_data, dict):
                continue
                
            md.append(f"### {speaker}\n")
            
            transitions = pattern_data.get("transition_count", 0)
            md.append(f"**Emotion Transitions:** {transitions}\n")
            
            sequence = pattern_data.get("emotion_sequence", [])
            if sequence:
                md.append(f"**Emotion Sequence:** {' → '.join(sequence[:10])}{'...' if len(sequence) > 10 else ''}\n")
            
            md.append("")
    
    # Anomalies
    anomalies = report_data.get("anomalies", [])
    if anomalies:
        md.append("## Behavioral Anomalies\n")
        md.append(f"Detected {len(anomalies)} anomalous behavior(s):\n")
        for i, anomaly in enumerate(anomalies, 1):
            timestamp_str = anomaly.get("timestamp_formatted", anomaly.get("timestamp", "Unknown"))
            speaker = anomaly.get("speaker", "Unknown")
            description = anomaly.get("description", "No description provided")
            
            md.append(f"{i}. **{timestamp_str} - {speaker}:** {description}\n")
        md.append("")
    
    # Behavioral Insights
    behavioral_insights = report_data.get("behavioral_insights", [])
    if behavioral_insights:
        md.append("## Behavioral Insights\n")
        for insight in behavioral_insights:
            md.append(f"- {insight}\n")
        md.append("")
    
    # Timeline
    md.append("## Timeline\n")
    timeline = _build_timeline(report_data)
    if timeline:
        md.append("| Time | Speaker | Event | Emotions |\n")
        md.append("|------|---------|-------|----------|\n")
        for event in timeline[:20]:  # Limit to first 20 events
            time = event.get("timestamp_formatted", "")
            speaker = event.get("speaker", "")
            description = event.get("event", "")[:50]  # Truncate long descriptions
            emotions = ", ".join([e.get("emotion", "") for e in event.get("emotions", [])][:3])
            md.append(f"| {time} | {speaker} | {description} | {emotions} |\n")
        if len(timeline) > 20:
            md.append(f"\n*... and {len(timeline) - 20} more events*\n")
    else:
        md.append("No timeline data available.\n")
    
    md.append("")
    md.append("---\n")
    md.append("*Report generated by Emotion Interpretation Machine v1.0*\n")
    
    return "\n".join(md)


def _build_timeline(report_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Build a timeline of events from report data.
    
    Args:
        report_data: The report data from the agent
        
    Returns:
        List of timeline events
    """
    timeline = []
    
    # Add critical moments to timeline
    critical_moments = report_data.get("critical_moments", [])
    for moment in critical_moments:
        timeline.append({
            "timestamp_ms": moment.get("timestamp_ms", 0),
            "timestamp_formatted": moment.get("timestamp_formatted", ""),
            "speaker": moment.get("speaker", ""),
            "event": f"CRITICAL: {moment.get('reason', '')}",
            "emotions": moment.get("emotions", []),
            "type": "critical"
        })
    
    # Add anomalies to timeline
    anomalies = report_data.get("anomalies", [])
    for anomaly in anomalies:
        timeline.append({
            "timestamp_ms": anomaly.get("timestamp_ms", 0),
            "timestamp_formatted": anomaly.get("timestamp_formatted", ""),
            "speaker": anomaly.get("speaker", ""),
            "event": f"ANOMALY: {anomaly.get('description', '')}",
            "emotions": anomaly.get("emotions", []),
            "type": "anomaly"
        })
    
    # Sort by timestamp
    timeline.sort(key=lambda x: x.get("timestamp_ms", 0))
    
    return timeline
