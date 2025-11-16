"""Agent nodes for the emotion interpretation agent."""

from typing import Dict, Any
from src.core.alignment import align_emotion_with_transcript, compute_emotion_pattern
from src.core.agent.state import AgentState


def perform_temporal_alignment(state: AgentState) -> Dict[str, Any]:
    """
    Node 1: Perform temporal alignment of emotions with transcription.
    
    Uses the alignment algorithm from Phase 1 to match emotions with transcript segments.
    """
    transcription = state.get("transcription_entries", [])
    emotions = state.get("emotion_detections", [])
    
    # Perform alignment using the algorithm from Phase 1
    aligned_events = align_emotion_with_transcript(transcription, emotions, window_ms=100)
    
    steps = state.get("steps_completed", [])
    steps.append("temporal_alignment")
    
    return {
        "aligned_events": aligned_events,
        "steps_completed": steps
    }


def analyze_emotion_patterns(state: AgentState) -> Dict[str, Any]:
    """
    Node 2: Analyze emotion patterns across the conversation.
    
    Identifies:
    - Dominant emotions per speaker
    - Emotional transitions
    - Emotion consistency/inconsistency
    """
    aligned_events = state.get("aligned_events", [])
    
    # Group events by speaker
    speaker_emotions = {}
    for event in aligned_events:
        speaker = event["speaker"]
        if speaker not in speaker_emotions:
            speaker_emotions[speaker] = []
        speaker_emotions[speaker].extend(event["emotions"])
    
    # Compute patterns for each speaker
    emotion_patterns = {}
    for speaker, emotions in speaker_emotions.items():
        # Add timestamp if missing (for backward compatibility)
        emotions_with_timestamps = []
        for e in emotions:
            if "timestamp" not in e:
                e["timestamp"] = f"{e['timestamp_ms'] // 60000:02d}:{(e['timestamp_ms'] % 60000) // 1000:02d}.{e['timestamp_ms'] % 1000:03d}"
            emotions_with_timestamps.append(e)
        
        pattern = compute_emotion_pattern(emotions_with_timestamps)
        emotion_patterns[speaker] = pattern
    
    # Detect emotional transitions (shifts between segments)
    transitions = []
    for i in range(1, len(aligned_events)):
        prev_event = aligned_events[i-1]
        curr_event = aligned_events[i]
        
        if prev_event["emotions"] and curr_event["emotions"]:
            prev_emotions = set(e["emotion"] for e in prev_event["emotions"])
            curr_emotions = set(e["emotion"] for e in curr_event["emotions"])
            
            # If emotions changed significantly
            if not prev_emotions.intersection(curr_emotions):
                transitions.append({
                    "from_time_ms": prev_event["end_time_ms"],
                    "to_time_ms": curr_event["start_time_ms"],
                    "speaker": curr_event["speaker"],
                    "from_emotions": list(prev_emotions),
                    "to_emotions": list(curr_emotions)
                })
    
    steps = state.get("steps_completed", [])
    steps.append("emotion_pattern_analysis")
    
    return {
        "emotion_patterns": {
            "by_speaker": emotion_patterns,
            "transitions": transitions
        },
        "steps_completed": steps
    }


def detect_anomalies(state: AgentState) -> Dict[str, Any]:
    """
    Node 3: Detect emotional anomalies and incongruities.
    
    Identifies moments where:
    - Emotion doesn't match content (e.g., fear during casual statement)
    - Unexpected emotional spikes
    - Suppressed or absent emotions where expected
    """
    aligned_events = state.get("aligned_events", [])
    emotion_patterns = state.get("emotion_patterns", {})
    
    anomalies = []
    
    # Get baseline emotions for each speaker
    speaker_baselines = {}
    if "by_speaker" in emotion_patterns:
        for speaker, pattern in emotion_patterns["by_speaker"].items():
            speaker_baselines[speaker] = pattern.get("dominantEmotion", "Neutral")
    
    # Detect anomalies
    for event in aligned_events:
        speaker = event["speaker"]
        emotions = event["emotions"]
        
        if not emotions:
            continue
        
        # Look for strong emotional signals (Surprise, Fear, Anxiety, Anger)
        strong_emotions = ["Surprise", "Fear", "Anxiety", "Anger", "Disgust", "Sadness"]
        
        for emotion_data in emotions:
            emotion = emotion_data["emotion"]
            
            # Check if this is a strong emotion
            if emotion in strong_emotions:
                # Check if it deviates from speaker's baseline
                baseline = speaker_baselines.get(speaker, "Neutral")
                if emotion != baseline:
                    anomalies.append({
                        "timestamp_ms": emotion_data["timestamp_ms"],
                        "speaker": speaker,
                        "emotion": emotion,
                        "baseline": baseline,
                        "transcript": event["transcript"],
                        "severity": "high" if emotion in ["Fear", "Surprise", "Anxiety"] else "medium"
                    })
    
    steps = state.get("steps_completed", [])
    steps.append("anomaly_detection")
    
    return {
        "anomalies": anomalies,
        "steps_completed": steps
    }


def interpret_moments(state: AgentState) -> Dict[str, Any]:
    """
    Node 4: Create interpretations for critical moments.
    
    This is a simplified version that creates basic interpretations.
    In full implementation with LLM, this would use Claude 3.5 to generate
    detailed natural language interpretations.
    """
    anomalies = state.get("anomalies", [])
    aligned_events = state.get("aligned_events", [])
    
    # Identify critical moments (anomalies + key transitions)
    critical_moments = []
    
    # Convert anomalies to critical moments
    for anomaly in anomalies:
        if anomaly["severity"] == "high":
            # Find the full event context
            event = next(
                (e for e in aligned_events 
                 if any(em["timestamp_ms"] == anomaly["timestamp_ms"] for em in e.get("emotions", []))),
                None
            )
            
            if event:
                # Simple interpretation based on emotion type
                interpretation = f"{anomaly['speaker']} showed {anomaly['emotion']} when saying: '{event['transcript']}'"
                
                if anomaly["emotion"] == "Surprise":
                    interpretation += " - This unexpected emotional response may indicate they were caught off guard or revealed hidden knowledge."
                elif anomaly["emotion"] == "Fear":
                    interpretation += " - This fear response suggests anxiety about the topic or potential deception."
                elif anomaly["emotion"] == "Anxiety":
                    interpretation += " - This anxiety indicates internal conflict or stress related to their statement."
                
                critical_moments.append({
                    "timestamp_ms": anomaly["timestamp_ms"],
                    "speaker": anomaly["speaker"],
                    "emotion": anomaly["emotion"],
                    "transcript": event["transcript"],
                    "interpretation": interpretation,
                    "significance": "high"
                })
    
    steps = state.get("steps_completed", [])
    steps.append("moment_interpretation")
    
    return {
        "critical_moments": critical_moments,
        "steps_completed": steps
    }


def create_speaker_profiles(state: AgentState) -> Dict[str, Any]:
    """
    Node 5: Create emotional baseline profiles for each speaker.
    
    Provides:
    - Dominant emotional state
    - Emotional range
    - Consistency metrics
    """
    emotion_patterns = state.get("emotion_patterns", {})
    aligned_events = state.get("aligned_events", [])
    
    speaker_profiles = {}
    
    if "by_speaker" in emotion_patterns:
        for speaker, pattern in emotion_patterns["by_speaker"].items():
            # Get all transcripts for this speaker
            speaker_events = [e for e in aligned_events if e["speaker"] == speaker]
            
            profile = {
                "name": speaker,
                "baseline_emotion": pattern.get("dominantEmotion", "Unknown"),
                "total_emotion_detections": pattern.get("totalEmotions", 0),
                "emotion_distribution": pattern.get("emotionCounts", {}),
                "total_utterances": len(speaker_events),
                "emotional_range": len(pattern.get("emotionCounts", {}))
            }
            
            speaker_profiles[speaker] = profile
    
    steps = state.get("steps_completed", [])
    steps.append("speaker_profiling")
    
    return {
        "speaker_profiles": speaker_profiles,
        "steps_completed": steps
    }


def synthesize_report(state: AgentState) -> Dict[str, Any]:
    """
    Node 6: Synthesize final interpretation report.
    
    Combines all analysis into a comprehensive report.
    """
    critical_moments = state.get("critical_moments", [])
    speaker_profiles = state.get("speaker_profiles", {})
    emotion_patterns = state.get("emotion_patterns", {})
    anomalies = state.get("anomalies", [])
    
    # Create summary
    summary = f"Analysis completed with {len(critical_moments)} critical moments identified. "
    summary += f"{len(anomalies)} emotional anomalies detected across {len(speaker_profiles)} speakers."
    
    # Create interpretation text
    interpretation_parts = []
    
    # Add speaker analysis
    interpretation_parts.append("## Speaker Profiles\n")
    for speaker, profile in speaker_profiles.items():
        emotional_range = profile.get('emotional_range', 0)
        total_utterances = profile.get('total_utterances', 0)
        interpretation_parts.append(
            f"- **{speaker}**: Baseline emotion is {profile['baseline_emotion']}. "
            f"Showed {emotional_range} different emotions across {total_utterances} statements.\n"
        )
    
    # Add critical moments
    if critical_moments:
        interpretation_parts.append("\n## Critical Moments\n")
        for moment in sorted(critical_moments, key=lambda x: x["timestamp_ms"]):
            time_str = f"{moment['timestamp_ms'] // 60000:02d}:{(moment['timestamp_ms'] % 60000) // 1000:02d}"
            interpretation_parts.append(
                f"- **{time_str}**: {moment['interpretation']}\n"
            )
    
    interpretation = "\n".join(interpretation_parts)
    
    # Create full report
    report = {
        "summary": summary,
        "critical_moments": critical_moments,
        "speaker_profiles": speaker_profiles,
        "emotion_patterns": emotion_patterns,
        "anomaly_count": len(anomalies),
        "high_severity_anomalies": len([a for a in anomalies if a.get("severity") == "high"])
    }
    
    steps = state.get("steps_completed", [])
    steps.append("report_synthesis")
    
    return {
        "interpretation": interpretation,
        "report": report,
        "steps_completed": steps
    }
