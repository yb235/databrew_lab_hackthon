# Temporal Alignment Specification

## Overview

Temporal alignment is the core process of matching emotion detection timestamps with transcription segments. This document details the algorithms and considerations for accurate alignment.

## Problem Statement

**Given**:
- Transcription data: Time-ranged segments `[startTime, endTime]` with speaker and text
- Emotion data: Point-in-time detections at specific `timestamp` values

**Goal**: Match emotion detections to their corresponding speech segments

**Challenges**:
- Emotion timestamps are points; transcriptions are ranges
- Multiple emotions can occur within one speech segment (micro-expressions)
- Emotion detection may have gaps or overlap with speech boundaries
- Timestamp precision differences (emotion: 100ms, speech: variable)

## Alignment Algorithm

### Core Algorithm

```python
def align_emotion_with_transcript(
    transcription: List[TranscriptionEntry],
    emotions: List[EmotionEntry],
    tolerance_ms: int = 100
) -> List[AlignedEvent]:
    """
    Aligns emotion detections with transcription segments
    
    Args:
        transcription: List of transcription entries
        emotions: List of emotion detections
        tolerance_ms: Boundary tolerance in milliseconds (default: 100ms)
    
    Returns:
        List of aligned events with matched emotions
    """
    
    # Step 1: Normalize timestamps to milliseconds
    transcription_ms = [
        {
            **entry,
            "startTime_ms": timestamp_to_ms(entry["startTime"]),
            "endTime_ms": timestamp_to_ms(entry["endTime"])
        }
        for entry in transcription
    ]
    
    emotions_ms = [
        {
            **entry,
            "timestamp_ms": timestamp_to_ms(entry["timestamp"])
        }
        for entry in emotions
    ]
    
    # Step 2: Sort both lists by time
    transcription_ms.sort(key=lambda x: x["startTime_ms"])
    emotions_ms.sort(key=lambda x: x["timestamp_ms"])
    
    # Step 3: Align emotions to transcriptions
    aligned_events = []
    emotion_idx = 0
    
    for trans in transcription_ms:
        start = trans["startTime_ms"] - tolerance_ms
        end = trans["endTime_ms"] + tolerance_ms
        
        # Collect all emotions in this window
        window_emotions = []
        
        # Advance to first relevant emotion
        while (emotion_idx < len(emotions_ms) and 
               emotions_ms[emotion_idx]["timestamp_ms"] < start):
            emotion_idx += 1
        
        # Collect emotions in window
        temp_idx = emotion_idx
        while (temp_idx < len(emotions_ms) and 
               emotions_ms[temp_idx]["timestamp_ms"] <= end):
            window_emotions.append(emotions_ms[temp_idx])
            temp_idx += 1
        
        # Create emotion detections with relative position
        emotion_detections = []
        duration = trans["endTime_ms"] - trans["startTime_ms"]
        
        for emot in window_emotions:
            relative_position = (
                (emot["timestamp_ms"] - trans["startTime_ms"]) / duration
                if duration > 0 else 0.5
            )
            
            emotion_detections.append(EmotionDetection(
                timestamp=emot["timestamp_ms"],
                emotion=emot["emotion"],
                relativePosition=max(0.0, min(1.0, relative_position)),
                isAnomaly=False  # Will be set later
            ))
        
        # Analyze emotion pattern
        emotion_pattern = compute_emotion_pattern(emotion_detections)
        
        # Create aligned event
        aligned_event = AlignedEvent(
            id=generate_uuid(),
            startTime=trans["startTime_ms"],
            endTime=trans["endTime_ms"],
            speaker=trans["speaker"],
            transcript=trans["transcript"],
            emotions=emotion_detections,
            emotionalPattern=emotion_pattern,
            durationMs=duration
        )
        
        aligned_events.append(aligned_event)
    
    return aligned_events
```

### Emotion Pattern Analysis

```python
def compute_emotion_pattern(
    emotions: List[EmotionDetection]
) -> EmotionPattern:
    """
    Analyzes sequence of emotions to identify patterns
    """
    
    if not emotions:
        return EmotionPattern(
            dominantEmotion="Neutral",
            emotionSequence=[],
            hasConflict=False,
            transitionCount=0,
            anomalyScore=0.0
        )
    
    # Get emotion sequence
    emotion_sequence = [e.emotion for e in emotions]
    
    # Find dominant emotion (most frequent)
    emotion_counts = Counter(emotion_sequence)
    dominant_emotion = emotion_counts.most_common(1)[0][0]
    
    # Count transitions (emotion changes)
    transitions = 0
    for i in range(1, len(emotion_sequence)):
        if emotion_sequence[i] != emotion_sequence[i-1]:
            transitions += 1
    
    # Compute anomaly score (higher = more unusual)
    anomaly_score = compute_anomaly_score(
        emotions, 
        dominant_emotion, 
        transitions
    )
    
    # Detect conflicts (emotions contradicting typical patterns)
    has_conflict = detect_emotion_conflict(emotion_sequence)
    
    return EmotionPattern(
        dominantEmotion=dominant_emotion,
        emotionSequence=emotion_sequence,
        hasConflict=has_conflict,
        transitionCount=transitions,
        anomalyScore=anomaly_score
    )

def compute_anomaly_score(
    emotions: List[EmotionDetection],
    dominant: str,
    transitions: int
) -> float:
    """
    Computes anomaly score (0.0 to 1.0)
    Higher score = more anomalous
    """
    
    # Base score on transition frequency
    transition_score = min(1.0, transitions / 5.0)
    
    # Check for conflicting emotions
    conflict_emotions = {
        "Joy": ["Sadness", "Anger", "Fear", "Disgust"],
        "Neutral": [],
        "Concentration": [],
        "Anxiety": [],
        "Fear": ["Joy", "Satisfaction"],
        "Anger": ["Joy", "Satisfaction"]
    }
    
    conflict_score = 0.0
    for emotion in emotions:
        if (dominant in conflict_emotions and 
            emotion.emotion in conflict_emotions[dominant]):
            conflict_score += 0.3
    
    conflict_score = min(1.0, conflict_score)
    
    # Weighted combination
    anomaly_score = (0.6 * transition_score) + (0.4 * conflict_score)
    
    return round(anomaly_score, 2)
```

## Edge Cases

### 1. No Emotion Data for Segment

```python
# When no emotions detected in window
if not window_emotions:
    emotion_pattern = EmotionPattern(
        dominantEmotion="No Data",
        emotionSequence=[],
        hasConflict=False,
        transitionCount=0,
        anomalyScore=0.0
    )
```

### 2. Overlapping Transcriptions

```python
def handle_overlapping_transcriptions(
    transcription: List[TranscriptionEntry]
) -> List[TranscriptionEntry]:
    """
    Handles cases where multiple speakers talk simultaneously
    """
    # Sort by start time
    sorted_trans = sorted(transcription, key=lambda x: x["startTime"])
    
    # Detect overlaps
    overlaps = []
    for i in range(len(sorted_trans) - 1):
        if sorted_trans[i]["endTime"] > sorted_trans[i+1]["startTime"]:
            overlaps.append((i, i+1))
    
    # For overlaps, split emotions proportionally or assign to primary speaker
    # Implementation depends on requirements
    
    return sorted_trans
```

### 3. Timestamp Gaps

```python
def detect_timestamp_gaps(
    emotions: List[EmotionEntry],
    max_gap_ms: int = 5000
) -> List[Gap]:
    """
    Identifies significant gaps in emotion detection
    """
    gaps = []
    emotions_sorted = sorted(emotions, key=lambda x: x["timestamp"])
    
    for i in range(len(emotions_sorted) - 1):
        t1 = timestamp_to_ms(emotions_sorted[i]["timestamp"])
        t2 = timestamp_to_ms(emotions_sorted[i+1]["timestamp"])
        gap = t2 - t1
        
        if gap > max_gap_ms:
            gaps.append(Gap(
                startTime=t1,
                endTime=t2,
                duration=gap,
                reason="emotion_detection_gap"
            ))
    
    return gaps
```

## Boundary Handling

### Tolerance Window

The tolerance window (`tolerance_ms`) handles:
- Timing imprecision in emotion detection
- Slight misalignment between emotion and speech timestamps
- Emotions detected just before/after speech starts/ends

**Default**: 100ms tolerance

```
Transcription: [00:02.100 ──────────── 00:04.500]
Tolerance:     [00:02.000 ═══════════════ 00:04.600]
                    ↑ -100ms              +100ms ↑

Emotions at 00:02.000, 00:02.050, 00:04.550 all match
```

### Relative Position Calculation

```python
def calculate_relative_position(
    emotion_time: int,
    segment_start: int,
    segment_end: int
) -> float:
    """
    Calculates where in the segment (0.0 to 1.0) the emotion occurred
    
    0.0 = start of speech
    0.5 = middle
    1.0 = end of speech
    """
    duration = segment_end - segment_start
    if duration == 0:
        return 0.5  # Single point
    
    position = (emotion_time - segment_start) / duration
    
    # Clamp to [0.0, 1.0]
    return max(0.0, min(1.0, position))
```

## Micro-Expression Detection

```python
def detect_micro_expressions(
    emotions: List[EmotionDetection],
    window_ms: int = 500
) -> List[MicroExpression]:
    """
    Identifies rapid emotion changes (micro-expressions)
    
    Micro-expression: 2+ emotion changes within 500ms
    """
    micro_expressions = []
    
    i = 0
    while i < len(emotions):
        # Look ahead for rapid changes
        window_end = emotions[i].timestamp + window_ms
        window_emotions = []
        
        j = i
        while j < len(emotions) and emotions[j].timestamp <= window_end:
            window_emotions.append(emotions[j])
            j += 1
        
        # Check for micro-expression (3+ different emotions)
        unique_emotions = set(e.emotion for e in window_emotions)
        if len(unique_emotions) >= 3:
            micro_expressions.append(MicroExpression(
                startTime=emotions[i].timestamp,
                endTime=emotions[j-1].timestamp,
                emotions=window_emotions,
                interpretation="Rapid emotional transition"
            ))
        
        i = j if j > i else i + 1
    
    return micro_expressions
```

## Baseline Computation

```python
def compute_speaker_baseline(
    speaker_events: List[AlignedEvent]
) -> EmotionBaseline:
    """
    Computes emotional baseline for a speaker
    """
    
    # Collect all emotions
    all_emotions = []
    for event in speaker_events:
        all_emotions.extend([e.emotion for e in event.emotions])
    
    # Count frequencies
    emotion_counts = Counter(all_emotions)
    total = len(all_emotions)
    
    # Dominant emotion (most frequent)
    dominant = emotion_counts.most_common(1)[0][0] if all_emotions else "Neutral"
    
    # Compute distribution
    distribution = {
        emotion: count / total
        for emotion, count in emotion_counts.items()
    }
    
    # Compute volatility (average transitions per event)
    total_transitions = sum(
        event.emotionalPattern.transitionCount 
        for event in speaker_events
    )
    avg_volatility = total_transitions / len(speaker_events) if speaker_events else 0
    
    return EmotionBaseline(
        dominantEmotion=dominant,
        distribution=distribution,
        volatility=avg_volatility,
        sampleSize=len(speaker_events)
    )
```

## Anomaly Detection

```python
def detect_anomalies(
    event: AlignedEvent,
    baseline: EmotionBaseline,
    threshold: float = 0.7
) -> List[Anomaly]:
    """
    Detects anomalous emotions relative to baseline
    """
    anomalies = []
    
    for emotion_det in event.emotions:
        # Check if emotion is rare for this speaker
        expected_freq = baseline.distribution.get(emotion_det.emotion, 0.0)
        
        # Emotion is anomalous if:
        # 1. Very rare for this speaker (< 10% frequency)
        # 2. Conflicts with dominant baseline
        if expected_freq < 0.1 or is_conflicting_emotion(
            emotion_det.emotion, 
            baseline.dominantEmotion
        ):
            anomalies.append(Anomaly(
                timestamp=emotion_det.timestamp,
                emotion=emotion_det.emotion,
                expected=baseline.dominantEmotion,
                severity=compute_severity(expected_freq),
                confidence=1.0 - expected_freq
            ))
    
    return anomalies

def is_conflicting_emotion(emotion: str, baseline: str) -> bool:
    """Check if emotion conflicts with baseline"""
    conflicts = {
        ("Joy", "Fear"), ("Joy", "Sadness"), ("Joy", "Anger"),
        ("Fear", "Satisfaction"), ("Fear", "Joy"),
        ("Anger", "Joy"), ("Anger", "Satisfaction"),
        ("Neutral", "Fear"), ("Neutral", "Anger"),
        ("Concentration", "Anxiety"), ("Concentration", "Surprise")
    }
    
    return (emotion, baseline) in conflicts or (baseline, emotion) in conflicts
```

## Performance Optimization

```python
def optimize_alignment_with_indexing(
    transcription: List[TranscriptionEntry],
    emotions: List[EmotionEntry]
) -> List[AlignedEvent]:
    """
    Optimized version using binary search for large datasets
    """
    
    # Build index for emotions by timestamp
    emotion_index = build_timestamp_index(emotions)
    
    aligned_events = []
    
    for trans in transcription:
        start_ms = timestamp_to_ms(trans["startTime"]) - 100
        end_ms = timestamp_to_ms(trans["endTime"]) + 100
        
        # Binary search for emotions in range
        start_idx = bisect_left(emotion_index, start_ms)
        end_idx = bisect_right(emotion_index, end_ms)
        
        window_emotions = emotions[start_idx:end_idx]
        
        # Process as before
        aligned_event = create_aligned_event(trans, window_emotions)
        aligned_events.append(aligned_event)
    
    return aligned_events
```

## Testing

```python
def test_alignment():
    """Test alignment with example data"""
    
    transcription = [
        {
            "startTime": "00:02.100",
            "endTime": "00:04.500",
            "speaker": "Holmes",
            "transcript": "Thank you for clarifying."
        }
    ]
    
    emotions = [
        {"timestamp": "00:02.000", "emotion": "Neutral"},
        {"timestamp": "00:03.000", "emotion": "Concentration"},
        {"timestamp": "00:04.000", "emotion": "Neutral"},
        {"timestamp": "00:05.000", "emotion": "Joy"}  # Outside window
    ]
    
    aligned = align_emotion_with_transcript(transcription, emotions)
    
    # Should have 1 aligned event
    assert len(aligned) == 1
    
    # Should include first 3 emotions (within tolerance)
    assert len(aligned[0].emotions) == 3
    
    # Fourth emotion should be excluded (outside window + tolerance)
    emotion_list = [e.emotion for e in aligned[0].emotions]
    assert "Joy" not in emotion_list
```

## Next Steps

See:
- [04_AGENT_DESIGN.md](./04_AGENT_DESIGN.md) - How agent uses aligned data
- [06_OBSERVABILITY.md](./06_OBSERVABILITY.md) - Monitoring alignment process
