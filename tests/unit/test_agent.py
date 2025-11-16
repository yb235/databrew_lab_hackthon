"""Unit tests for agent nodes."""

import pytest
from src.core.agent import (
    perform_temporal_alignment,
    analyze_emotion_patterns,
    detect_anomalies,
    interpret_moments,
    create_speaker_profiles,
    synthesize_report,
    run_interpretation,
)


class TestAgentNodes:
    """Test individual agent nodes."""
    
    def test_temporal_alignment_node(self):
        """Test the temporal alignment node."""
        state = {
            "transcription_entries": [
                {
                    "startTime": "00:03.400",
                    "endTime": "00:07.800",
                    "speaker": "Holmes",
                    "transcript": "Test"
                }
            ],
            "emotion_detections": [
                {"timestamp": "00:05.000", "emotion": "Neutral"}
            ],
            "steps_completed": []
        }
        
        result = perform_temporal_alignment(state)
        
        assert "aligned_events" in result
        assert len(result["aligned_events"]) == 1
        assert "temporal_alignment" in result["steps_completed"]
    
    def test_pattern_analysis_node(self):
        """Test the emotion pattern analysis node."""
        state = {
            "aligned_events": [
                {
                    "speaker": "Holmes",
                    "transcript": "Test",
                    "emotions": [
                        {"emotion": "Neutral", "timestamp_ms": 5000}
                    ],
                    "start_time_ms": 3400,
                    "end_time_ms": 7800
                }
            ],
            "steps_completed": []
        }
        
        result = analyze_emotion_patterns(state)
        
        assert "emotion_patterns" in result
        assert "by_speaker" in result["emotion_patterns"]
        assert "Holmes" in result["emotion_patterns"]["by_speaker"]
        assert "emotion_pattern_analysis" in result["steps_completed"]
    
    def test_anomaly_detection_node(self):
        """Test the anomaly detection node."""
        state = {
            "aligned_events": [
                {
                    "speaker": "Holmes",
                    "transcript": "Test statement",
                    "emotions": [
                        {"emotion": "Fear", "timestamp_ms": 5000}
                    ],
                    "start_time_ms": 3400,
                    "end_time_ms": 7800
                }
            ],
            "emotion_patterns": {
                "by_speaker": {
                    "Holmes": {
                        "dominantEmotion": "Neutral"
                    }
                }
            },
            "steps_completed": []
        }
        
        result = detect_anomalies(state)
        
        assert "anomalies" in result
        # Fear should be detected as anomaly when baseline is Neutral
        assert len(result["anomalies"]) > 0
        assert result["anomalies"][0]["emotion"] == "Fear"
        assert "anomaly_detection" in result["steps_completed"]
    
    def test_speaker_profiling_node(self):
        """Test the speaker profiling node."""
        state = {
            "emotion_patterns": {
                "by_speaker": {
                    "Holmes": {
                        "dominantEmotion": "Neutral",
                        "totalEmotions": 5,
                        "emotionCounts": {"Neutral": 3, "Concentration": 2}
                    }
                }
            },
            "aligned_events": [
                {"speaker": "Holmes", "transcript": "Test 1"},
                {"speaker": "Holmes", "transcript": "Test 2"}
            ],
            "steps_completed": []
        }
        
        result = create_speaker_profiles(state)
        
        assert "speaker_profiles" in result
        assert "Holmes" in result["speaker_profiles"]
        assert result["speaker_profiles"]["Holmes"]["baseline_emotion"] == "Neutral"
        assert "speaker_profiling" in result["steps_completed"]
    
    def test_report_synthesis_node(self):
        """Test the report synthesis node."""
        state = {
            "critical_moments": [
                {
                    "timestamp_ms": 61000,
                    "speaker": "Holmes",
                    "interpretation": "Test interpretation"
                }
            ],
            "speaker_profiles": {
                "Holmes": {
                    "name": "Holmes",
                    "baseline_emotion": "Neutral"
                }
            },
            "emotion_patterns": {},
            "anomalies": [{"severity": "high"}],
            "steps_completed": []
        }
        
        result = synthesize_report(state)
        
        assert "interpretation" in result
        assert "report" in result
        assert "summary" in result["report"]
        assert "report_synthesis" in result["steps_completed"]


class TestFullAgentExecution:
    """Test full agent execution."""
    
    def test_run_interpretation_holmes(self):
        """Test running the full agent on Holmes example data."""
        import json
        import os
        
        # Load Holmes example
        examples_dir = os.path.join(os.path.dirname(__file__), "..", "..", "examples")
        
        with open(os.path.join(examples_dir, "transcription_holmes.json")) as f:
            transcription = json.load(f)
        
        with open(os.path.join(examples_dir, "emotion_analysis_holmes.json")) as f:
            emotions = json.load(f)
        
        # Run agent
        result = run_interpretation(transcription, emotions, session_id=1)
        
        # Verify all steps completed
        assert "steps_completed" in result
        expected_steps = [
            "temporal_alignment",
            "emotion_pattern_analysis",
            "anomaly_detection",
            "moment_interpretation",
            "speaker_profiling",
            "report_synthesis"
        ]
        for step in expected_steps:
            assert step in result["steps_completed"]
        
        # Verify outputs
        assert "aligned_events" in result
        assert "emotion_patterns" in result
        assert "anomalies" in result
        assert "critical_moments" in result
        assert "speaker_profiles" in result
        assert "interpretation" in result
        assert "report" in result
        
        # Verify Holmes and Lord Alistair profiles exist
        assert "Holmes" in result["speaker_profiles"]
        assert "Lord Alistair" in result["speaker_profiles"]
    
    def test_critical_moment_detection(self):
        """Test that critical moments are identified."""
        import json
        import os
        
        examples_dir = os.path.join(os.path.dirname(__file__), "..", "..", "examples")
        
        with open(os.path.join(examples_dir, "transcription_holmes.json")) as f:
            transcription = json.load(f)
        
        with open(os.path.join(examples_dir, "emotion_analysis_holmes.json")) as f:
            emotions = json.load(f)
        
        result = run_interpretation(transcription, emotions)
        
        # Should detect some critical moments
        assert len(result.get("critical_moments", [])) > 0
        
        # Check that 01:01 moment is detected as critical (if it has anomalies)
        # The 01:01 moment is around 61000ms
        moments_near_01_01 = [
            m for m in result.get("critical_moments", [])
            if 59000 <= m["timestamp_ms"] <= 63000
        ]
        
        # Should have at least one critical moment near 01:01
        assert len(moments_near_01_01) > 0
