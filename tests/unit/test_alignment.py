"""Unit tests for temporal alignment algorithm."""

import pytest
from src.core.alignment import (
    timestamp_to_ms,
    ms_to_timestamp,
    align_emotion_with_transcript,
    find_event_at_time,
    compute_emotion_pattern,
)


class TestTimestampConversion:
    """Test timestamp conversion functions."""
    
    def test_timestamp_to_ms_basic(self):
        """Test basic timestamp conversion."""
        assert timestamp_to_ms("00:00.000") == 0
        assert timestamp_to_ms("01:00.000") == 60000
        assert timestamp_to_ms("01:23.456") == 83456
    
    def test_timestamp_to_ms_various_formats(self):
        """Test timestamp conversion with various formats."""
        assert timestamp_to_ms("0:05.100") == 5100
        assert timestamp_to_ms("10:30.500") == 630500
    
    def test_ms_to_timestamp(self):
        """Test milliseconds to timestamp conversion."""
        assert ms_to_timestamp(0) == "00:00.000"
        assert ms_to_timestamp(60000) == "01:00.000"
        assert ms_to_timestamp(83456) == "01:23.456"
        assert ms_to_timestamp(5100) == "00:05.100"


class TestAlignment:
    """Test emotion-transcription alignment."""
    
    def test_basic_alignment(self):
        """Test basic alignment of emotions with transcription."""
        transcription = [
            {
                "startTime": "00:03.400",
                "endTime": "00:07.800",
                "speaker": "Holmes",
                "transcript": "Thank you for clarifying."
            }
        ]
        
        emotions = [
            {"timestamp": "00:05.100", "emotion": "Neutral"}
        ]
        
        aligned = align_emotion_with_transcript(transcription, emotions)
        
        assert len(aligned) == 1
        assert aligned[0]["speaker"] == "Holmes"
        assert len(aligned[0]["emotions"]) == 1
        assert aligned[0]["emotions"][0]["emotion"] == "Neutral"
    
    def test_alignment_with_window(self):
        """Test alignment with tolerance window."""
        transcription = [
            {
                "startTime": "00:03.000",
                "endTime": "00:05.000",
                "speaker": "Speaker",
                "transcript": "Test"
            }
        ]
        
        # Emotion just outside range, but within window
        emotions = [
            {"timestamp": "00:05.050", "emotion": "Happy"}  # 50ms after end
        ]
        
        aligned = align_emotion_with_transcript(transcription, emotions, window_ms=100)
        
        assert len(aligned[0]["emotions"]) == 1
        assert aligned[0]["emotions"][0]["emotion"] == "Happy"
    
    def test_multiple_emotions_per_segment(self):
        """Test multiple emotions matching one transcription segment."""
        transcription = [
            {
                "startTime": "00:08.500",
                "endTime": "00:12.300",
                "speaker": "Lord Alistair",
                "transcript": "Yes, precisely."
            }
        ]
        
        emotions = [
            {"timestamp": "00:10.200", "emotion": "Concentration"},
            {"timestamp": "00:11.000", "emotion": "Neutral"},
        ]
        
        aligned = align_emotion_with_transcript(transcription, emotions)
        
        assert len(aligned) == 1
        assert len(aligned[0]["emotions"]) == 2
        assert aligned[0]["emotions"][0]["emotion"] == "Concentration"
        assert aligned[0]["emotions"][1]["emotion"] == "Neutral"


class TestFindEventAtTime:
    """Test finding events at specific times."""
    
    def test_find_event_at_time(self):
        """Test finding an event at a specific timestamp."""
        aligned_events = [
            {
                "start_time_ms": 3400,
                "end_time_ms": 7800,
                "speaker": "Holmes",
                "transcript": "Test",
                "emotions": [{"emotion": "Neutral"}]
            }
        ]
        
        event = find_event_at_time(aligned_events, "00:05")
        
        assert event is not None
        assert event["speaker"] == "Holmes"
    
    def test_find_event_not_found(self):
        """Test when event is not found at timestamp."""
        aligned_events = [
            {
                "start_time_ms": 3400,
                "end_time_ms": 7800,
                "speaker": "Holmes",
                "transcript": "Test",
                "emotions": []
            }
        ]
        
        event = find_event_at_time(aligned_events, "01:00")
        
        assert event is None


class TestEmotionPattern:
    """Test emotion pattern computation."""
    
    def test_compute_emotion_pattern_empty(self):
        """Test emotion pattern with empty list."""
        pattern = compute_emotion_pattern([])
        
        assert pattern["totalEmotions"] == 0
        assert pattern["dominantEmotion"] is None
    
    def test_compute_emotion_pattern_basic(self):
        """Test basic emotion pattern computation."""
        emotions = [
            {"timestamp": "00:10.000", "emotion": "Surprise"},
            {"timestamp": "00:11.000", "emotion": "Fear"},
            {"timestamp": "00:12.000", "emotion": "Surprise"},
        ]
        
        pattern = compute_emotion_pattern(emotions)
        
        assert pattern["totalEmotions"] == 3
        assert pattern["dominantEmotion"] == "Surprise"
        assert pattern["emotionCounts"]["Surprise"] == 2
        assert pattern["emotionCounts"]["Fear"] == 1
        assert len(pattern["emotionSequence"]) == 3
