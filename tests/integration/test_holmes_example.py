"""Integration test for Holmes example - verifying the critical 01:01 moment."""

import pytest
import json
import os
from src.core.alignment import align_emotion_with_transcript, find_event_at_time


def load_example_file(filename: str):
    """Load an example JSON file."""
    examples_dir = os.path.join(os.path.dirname(__file__), "..", "..", "examples")
    filepath = os.path.join(examples_dir, filename)
    
    with open(filepath, "r") as f:
        return json.load(f)


class TestHolmesExample:
    """Test the Holmes interview example."""
    
    def test_holmes_alignment(self):
        """Test that Holmes example aligns correctly."""
        # Load example data
        transcription = load_example_file("transcription_holmes.json")
        emotions = load_example_file("emotion_analysis_holmes.json")
        
        # Perform alignment
        aligned_events = align_emotion_with_transcript(transcription, emotions)
        
        # Verify we have aligned events
        assert len(aligned_events) > 0
        
        # Verify structure
        assert all("speaker" in event for event in aligned_events)
        assert all("transcript" in event for event in aligned_events)
        assert all("emotions" in event for event in aligned_events)
    
    def test_holmes_01_01_moment(self):
        """Test the critical 01:01 moment in Holmes example.
        
        This is a key test case mentioned in the implementation tracker.
        At 01:01, there should be a significant emotional shift that indicates
        potential deception.
        """
        # Load example data
        transcription = load_example_file("transcription_holmes.json")
        emotions = load_example_file("emotion_analysis_holmes.json")
        
        # Perform alignment
        aligned_events = align_emotion_with_transcript(transcription, emotions)
        
        # Find the event at 01:01
        event_01_01 = find_event_at_time(aligned_events, "01:01")
        
        # Verify event exists
        assert event_01_01 is not None, "Event at 01:01 should exist"
        
        # Verify it has emotions
        assert len(event_01_01["emotions"]) > 0, "Event at 01:01 should have emotions"
        
        # Extract emotion types at this moment
        emotions_at_moment = [e["emotion"] for e in event_01_01["emotions"]]
        
        # The 01:01 moment should show emotional changes (Surprise, Fear, etc.)
        # This is a key indicator of deception in the Holmes example
        assert any(emotion in emotions_at_moment for emotion in ["Surprise", "Fear", "Anxiety"]), \
            f"Expected emotional shift at 01:01, but found: {emotions_at_moment}"
    
    def test_holmes_speaker_distribution(self):
        """Test that we have proper speaker distribution."""
        transcription = load_example_file("transcription_holmes.json")
        emotions = load_example_file("emotion_analysis_holmes.json")
        
        aligned_events = align_emotion_with_transcript(transcription, emotions)
        
        # Get unique speakers
        speakers = set(event["speaker"] for event in aligned_events)
        
        # Holmes example should have both Holmes and Lord Alistair
        assert "Holmes" in speakers
        assert "Lord Alistair" in speakers
    
    def test_holmes_temporal_coverage(self):
        """Test that emotions are properly distributed across the timeline."""
        transcription = load_example_file("transcription_holmes.json")
        emotions = load_example_file("emotion_analysis_holmes.json")
        
        aligned_events = align_emotion_with_transcript(transcription, emotions)
        
        # Count events with emotions
        events_with_emotions = sum(1 for event in aligned_events if len(event["emotions"]) > 0)
        
        # Most events should have matched emotions
        assert events_with_emotions > len(aligned_events) * 0.5, \
            "At least 50% of transcript segments should have matched emotions"


class TestAllExamples:
    """Test that all example files can be processed."""
    
    @pytest.mark.parametrize("example_name", [
        "holmes",
        "20min_lie",
        "double_agent",
        # Note: love_story and office_lovers have JSON format issues in the example files
        # These would need to be fixed in the data files themselves
    ])
    def test_example_alignment(self, example_name):
        """Test that each example can be aligned successfully."""
        # Load files
        transcription = load_example_file(f"transcription_{example_name}.json")
        emotions = load_example_file(f"emotion_analysis_{example_name}.json")
        
        # Perform alignment
        aligned_events = align_emotion_with_transcript(transcription, emotions)
        
        # Verify we got results
        assert len(aligned_events) > 0, f"Example {example_name} should produce aligned events"
        
        # Verify structure
        for event in aligned_events:
            assert "speaker" in event
            assert "transcript" in event
            assert "emotions" in event
            assert "start_time_ms" in event
            assert "end_time_ms" in event
