"""Temporal alignment algorithm for matching emotions with transcription."""

from typing import List, Dict, Any, Tuple
import re


def timestamp_to_ms(timestamp: str) -> int:
    """
    Convert timestamp string (MM:SS.mmm) to milliseconds.
    
    Args:
        timestamp: Time string in format "MM:SS.mmm" or "M:SS.mmm"
        
    Returns:
        Time in milliseconds
    """
    # Handle format: MM:SS.mmm or M:SS.mmm
    pattern = r"(\d+):(\d+)\.(\d+)"
    match = re.match(pattern, timestamp)
    
    if not match:
        raise ValueError(f"Invalid timestamp format: {timestamp}. Expected MM:SS.mmm")
    
    minutes = int(match.group(1))
    seconds = int(match.group(2))
    milliseconds = int(match.group(3))
    
    total_ms = (minutes * 60 * 1000) + (seconds * 1000) + milliseconds
    return total_ms


def ms_to_timestamp(ms: int) -> str:
    """
    Convert milliseconds to timestamp string (MM:SS.mmm).
    
    Args:
        ms: Time in milliseconds
        
    Returns:
        Timestamp string in format "MM:SS.mmm"
    """
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    milliseconds = ms % 1000
    
    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def align_emotion_with_transcript(
    transcription_entries: List[Dict[str, Any]],
    emotion_detections: List[Dict[str, Any]],
    window_ms: int = 100
) -> List[Dict[str, Any]]:
    """
    Align emotion detections with transcription entries using temporal matching.
    
    The algorithm matches emotions to transcript segments based on timestamps:
    - For each transcription entry, find all emotions within its time range
    - Use a tolerance window (default ±100ms) for matching
    
    Args:
        transcription_entries: List of transcription entries with startTime, endTime, speaker, transcript
        emotion_detections: List of emotion detections with timestamp, emotion
        window_ms: Tolerance window in milliseconds for matching (default: 100)
        
    Returns:
        List of aligned events combining transcription and emotions
    """
    aligned_events = []
    
    for entry in transcription_entries:
        # Convert timestamps to milliseconds
        start_time_ms = timestamp_to_ms(entry["startTime"])
        end_time_ms = timestamp_to_ms(entry["endTime"])
        
        # Find emotions within this time range (with tolerance window)
        matched_emotions = []
        for detection in emotion_detections:
            emotion_time_ms = timestamp_to_ms(detection["timestamp"])
            
            # Check if emotion falls within transcription time range (with window)
            if (start_time_ms - window_ms) <= emotion_time_ms <= (end_time_ms + window_ms):
                matched_emotions.append({
                    "timestamp_ms": emotion_time_ms,
                    "timestamp": detection["timestamp"],
                    "emotion": detection["emotion"],
                    "confidence": detection.get("confidence")
                })
        
        # Create aligned event
        aligned_event = {
            "start_time_ms": start_time_ms,
            "end_time_ms": end_time_ms,
            "speaker": entry["speaker"],
            "transcript": entry["transcript"],
            "emotions": matched_emotions
        }
        
        aligned_events.append(aligned_event)
    
    return aligned_events


def find_event_at_time(aligned_events: List[Dict[str, Any]], target_time: str) -> Dict[str, Any]:
    """
    Find the aligned event at a specific time.
    
    Args:
        aligned_events: List of aligned events
        target_time: Target timestamp in format "MM:SS.mmm" or "MM:SS"
        
    Returns:
        Aligned event at that time, or None if not found
    """
    # Handle format without milliseconds
    if "." not in target_time:
        target_time = target_time + ".000"
    
    target_ms = timestamp_to_ms(target_time)
    
    for event in aligned_events:
        if event["start_time_ms"] <= target_ms <= event["end_time_ms"]:
            return event
    
    return None


def get_emotion_sequence(aligned_events: List[Dict[str, Any]]) -> List[Tuple[str, str, List[str]]]:
    """
    Get a simplified sequence of (speaker, transcript, emotions) for analysis.
    
    Args:
        aligned_events: List of aligned events
        
    Returns:
        List of tuples (speaker, transcript, emotion_list)
    """
    sequence = []
    for event in aligned_events:
        emotions = [e["emotion"] for e in event["emotions"]]
        sequence.append((event["speaker"], event["transcript"], emotions))
    
    return sequence


def compute_emotion_pattern(emotions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute emotion patterns from a list of emotion detections.
    
    Args:
        emotions: List of emotion detections with timestamp and emotion
        
    Returns:
        Dictionary with emotion pattern statistics
    """
    if not emotions:
        return {
            "totalEmotions": 0,
            "dominantEmotion": None,
            "emotionCounts": {},
            "emotionSequence": []
        }
    
    # Count emotions
    emotion_counts = {}
    emotion_sequence = []
    
    for detection in emotions:
        emotion = detection["emotion"]
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        emotion_sequence.append({
            "timestamp": detection["timestamp"],
            "emotion": emotion
        })
    
    # Find dominant emotion
    dominant_emotion = max(emotion_counts, key=emotion_counts.get)
    
    return {
        "totalEmotions": len(emotions),
        "dominantEmotion": dominant_emotion,
        "emotionCounts": emotion_counts,
        "emotionSequence": emotion_sequence
    }
