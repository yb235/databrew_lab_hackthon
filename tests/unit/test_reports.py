"""Tests for report generation."""

import json
import pytest
from src.core.reports import generate_json_report, generate_markdown_report


class TestReportGeneration:
    """Test report generation in different formats."""
    
    def test_generate_json_report_basic(self):
        """Test basic JSON report generation."""
        report_data = {
            "summary": "Test summary",
            "critical_moments": [
                {
                    "timestamp_formatted": "01:30.500",
                    "timestamp_ms": 90500,
                    "speaker": "Alice",
                    "transcript": "I didn't do it",
                    "emotions": [{"emotion": "Fear", "confidence": 0.85}],
                    "reason": "Fear spike during denial"
                }
            ],
            "speaker_profiles": {
                "Alice": {
                    "baseline_emotions": {
                        "Neutral": {"count": 10, "avg_confidence": 0.75}
                    },
                    "patterns": ["Generally neutral"]
                }
            },
            "behavioral_insights": ["High stress during questioning"],
            "anomalies": []
        }
        
        json_report = generate_json_report(report_data, "Test Session")
        
        # Parse to verify it's valid JSON
        parsed = json.loads(json_report)
        
        assert parsed["metadata"]["session_name"] == "Test Session"
        assert parsed["summary"] == "Test summary"
        assert len(parsed["key_moments"]) == 1
        assert parsed["key_moments"][0]["speaker"] == "Alice"
        assert "Alice" in parsed["speaker_profiles"]
    
    def test_generate_json_report_empty(self):
        """Test JSON report generation with empty data."""
        report_data = {}
        
        json_report = generate_json_report(report_data)
        parsed = json.loads(json_report)
        
        assert parsed["summary"] == "No summary available"
        assert parsed["key_moments"] == []
        assert parsed["speaker_profiles"] == {}
    
    def test_generate_markdown_report_basic(self):
        """Test basic Markdown report generation."""
        report_data = {
            "summary": "Test conversation analysis",
            "critical_moments": [
                {
                    "timestamp_formatted": "01:30.500",
                    "timestamp_ms": 90500,
                    "speaker": "Bob",
                    "transcript": "Yes, I was there",
                    "emotions": [{"emotion": "Surprise", "confidence": 0.90}],
                    "reason": "Unexpected surprise during admission"
                }
            ],
            "speaker_profiles": {
                "Bob": {
                    "baseline_emotions": {
                        "Neutral": {"count": 8, "avg_confidence": 0.80}
                    },
                    "patterns": ["Calm demeanor"]
                }
            },
            "emotion_patterns": {
                "Bob": {
                    "transition_count": 3,
                    "emotion_sequence": ["Neutral", "Surprise", "Fear"]
                }
            },
            "anomalies": [
                {
                    "timestamp_formatted": "02:00.000",
                    "timestamp_ms": 120000,
                    "speaker": "Bob",
                    "description": "Sudden fear spike"
                }
            ],
            "behavioral_insights": ["Shows signs of stress"]
        }
        
        md_report = generate_markdown_report(report_data, "Test Session")
        
        # Verify structure
        assert "# Emotion Interpretation Report: Test Session" in md_report
        assert "## Executive Summary" in md_report
        assert "Test conversation analysis" in md_report
        assert "## Critical Moments" in md_report
        assert "Bob" in md_report
        assert "## Speaker Profiles" in md_report
        assert "## Emotion Patterns" in md_report
        assert "## Behavioral Anomalies" in md_report
        assert "## Behavioral Insights" in md_report
        assert "## Timeline" in md_report
    
    def test_generate_markdown_report_empty(self):
        """Test Markdown report generation with empty data."""
        report_data = {}
        
        md_report = generate_markdown_report(report_data)
        
        assert "# Emotion Interpretation Report" in md_report
        assert "No summary available" in md_report
    
    def test_markdown_report_limits_timeline(self):
        """Test that Markdown report limits timeline to first 20 events."""
        # Create many critical moments
        critical_moments = [
            {
                "timestamp_formatted": f"00:{i:02d}.000",
                "timestamp_ms": i * 1000,
                "speaker": "Test",
                "transcript": f"Moment {i}",
                "emotions": [{"emotion": "Neutral", "confidence": 0.5}],
                "reason": f"Reason {i}"
            }
            for i in range(25)
        ]
        
        report_data = {
            "summary": "Test",
            "critical_moments": critical_moments
        }
        
        md_report = generate_markdown_report(report_data)
        
        # Should mention truncation
        assert "and 5 more events" in md_report
    
    def test_json_report_timeline_ordering(self):
        """Test that timeline events are ordered by timestamp."""
        report_data = {
            "summary": "Test",
            "critical_moments": [
                {
                    "timestamp_formatted": "02:00.000",
                    "timestamp_ms": 120000,
                    "speaker": "A",
                    "reason": "Second moment"
                },
                {
                    "timestamp_formatted": "01:00.000",
                    "timestamp_ms": 60000,
                    "speaker": "B",
                    "reason": "First moment"
                }
            ],
            "anomalies": [
                {
                    "timestamp_formatted": "01:30.000",
                    "timestamp_ms": 90000,
                    "speaker": "C",
                    "description": "Middle anomaly"
                }
            ]
        }
        
        json_report = generate_json_report(report_data)
        parsed = json.loads(json_report)
        
        timeline = parsed["timeline"]
        assert len(timeline) == 3
        # Verify chronological order
        assert timeline[0]["timestamp_ms"] == 60000  # First
        assert timeline[1]["timestamp_ms"] == 90000  # Middle
        assert timeline[2]["timestamp_ms"] == 120000  # Last
