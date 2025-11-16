# Schema Specification

## Overview

This document defines the data schemas for all input, intermediate, and output data structures in the Emotion Interpretation Machine system.

## Input Data Schemas

### 1. Transcription Data Schema

**File Format**: JSON  
**Example**: `examples/transcription_love_story.json`

#### Schema Definition

```typescript
interface TranscriptionEntry {
  startTime: string;      // Format: "MM:SS.mmm" (e.g., "00:02.100")
  endTime: string;        // Format: "MM:SS.mmm" (e.g., "00:04.500")
  speaker: string;        // Speaker identifier (e.g., "Elias (Lead)")
  transcript: string;     // Spoken text content
}

type TranscriptionData = TranscriptionEntry[];
```

#### Validation Rules

```javascript
{
  "startTime": {
    "type": "string",
    "pattern": "^\\d{2}:\\d{2}\\.\\d{3}$",
    "required": true,
    "description": "Start timestamp in MM:SS.mmm format"
  },
  "endTime": {
    "type": "string",
    "pattern": "^\\d{2}:\\d{2}\\.\\d{3}$",
    "required": true,
    "description": "End timestamp in MM:SS.mmm format",
    "validation": "Must be after startTime"
  },
  "speaker": {
    "type": "string",
    "minLength": 1,
    "maxLength": 100,
    "required": true,
    "description": "Speaker name or identifier"
  },
  "transcript": {
    "type": "string",
    "minLength": 1,
    "maxLength": 5000,
    "required": true,
    "description": "Spoken content"
  }
}
```

#### Example

```json
[
  {
    "startTime": "00:02.100",
    "endTime": "00:04.500",
    "speaker": "Elias (Lead)",
    "transcript": "Sorry I'm a bit late. The meeting on the 4th floor ran long."
  },
  {
    "startTime": "00:05.000",
    "endTime": "00:08.200",
    "speaker": "Leo (New Hire)",
    "transcript": "Oh, no problem at all. I was just reviewing the onboarding docs."
  }
]
```

### 2. Emotion Detection Data Schema

**File Format**: JSON  
**Example**: `examples/emotion_analysis_love_story.json`

#### Schema Definition

```typescript
interface EmotionEntry {
  timestamp: string;      // Format: "MM:SS.mmm" (e.g., "00:03.000")
  emotion: EmotionType;   // Detected emotion label
}

type EmotionType = 
  | "arms_crossed"
  | "hands_clasped"
  | "chin_rest"
  | "lean_forward"
  | "lean_back"
  | "head_down"
  | "touch_face"
  | "touch_nose"
  | "fix_hair"
  | "fidget_hands";

type EmotionData = EmotionEntry[];
```

#### Validation Rules

```javascript
{
  "timestamp": {
    "type": "string",
    "pattern": "^\\d{2}:\\d{2}\\.\\d{3}$",
    "required": true,
    "description": "Emotion detection timestamp in MM:SS.mmm format"
  },
  "emotion": {
    "type": "string",
    "enum": [
      "arms_crossed", "hands_clasped", "chin_rest", "lean_forward", "lean_back",
      "head_down", "touch_face", "touch_nose", "fix_hair", "fidget_hands"
    ],
    "required": true,
    "description": "Detected emotion category"
  }
}
```

#### Example

```json
[
  {
    "timestamp": "00:03.000",
    "emotion": "arms_crossed"
  },
  {
    "timestamp": "00:09.200",
    "emotion": "lean_forward"
  },
  {
    "timestamp": "00:09.300",
    "emotion": "touch_face"
  }
]
```

#### Emotion Detection Characteristics

- **Temporal Resolution**: 100ms intervals (typical)
- **Multiple Detections**: Can have multiple emotion entries within a single transcription window
- **Micro-expressions**: Rapid emotional changes (e.g., Surprise → Joy → Neutral in 200ms)
- **Baseline Emotions**: Long periods of Neutral or Concentration

## Intermediate Data Schemas

### 3. Aligned Event Schema

After temporal alignment, transcription and emotion data are merged:

```typescript
interface AlignedEvent {
  id: string;                      // Unique event identifier
  startTime: number;               // Normalized timestamp (milliseconds)
  endTime: number;                 // Normalized timestamp (milliseconds)
  speaker: string;                 // Speaker identifier
  transcript: string;              // Spoken content
  emotions: EmotionDetection[];    // All emotions detected during this speech
  emotionalPattern: EmotionPattern; // Analysis of emotion sequence
  durationMs: number;              // Event duration in milliseconds
}

interface EmotionDetection {
  timestamp: number;               // Normalized timestamp (milliseconds)
  emotion: EmotionType;           // Detected emotion
  relativePosition: number;       // Position within speech (0.0 to 1.0)
  isAnomaly: boolean;             // Flags unexpected emotional spikes
}

interface EmotionPattern {
  dominantEmotion: EmotionType;   // Most frequent emotion
  emotionSequence: EmotionType[]; // Temporal sequence
  hasConflict: boolean;           // True if emotion contradicts speech
  transitionCount: number;        // Number of emotion changes
  anomalyScore: number;           // 0.0 to 1.0, higher = more unusual
}
```

### 4. Context Window Schema

For agent reasoning, events are grouped into context windows:

```typescript
interface ContextWindow {
  id: string;                      // Window identifier
  startTime: number;               // Window start (milliseconds)
  endTime: number;                 // Window end (milliseconds)
  events: AlignedEvent[];          // Events in this window
  conversationFlow: string;        // "initiation" | "development" | "climax" | "resolution"
  speakers: string[];              // Unique speakers in window
  emotionalTrend: EmotionalTrend;  // Overall emotional trajectory
}

interface EmotionalTrend {
  direction: "escalating" | "de-escalating" | "stable" | "volatile";
  intensity: number;               // 0.0 to 1.0
  volatility: number;              // 0.0 to 1.0, higher = more changes
  keyMoments: KeyMoment[];         // Critical emotional events
}

interface KeyMoment {
  timestamp: number;               // When it occurred
  eventId: string;                 // Reference to aligned event
  significance: number;            // 0.0 to 1.0, importance score
  reason: string;                  // Why it's significant
  emotionBefore: EmotionType;      // Emotion before the moment
  emotionAfter: EmotionType;       // Emotion after the moment
}
```

## Output Data Schemas

### 5. Interpretation Report Schema

Final output from the agent:

```typescript
interface InterpretationReport {
  metadata: ReportMetadata;
  summary: Summary;
  keyMoments: InterpretedMoment[];
  speakerProfiles: SpeakerProfile[];
  insights: Insight[];
  timeline: TimelineEvent[];
  observability: ObservabilityMetrics;
}

interface ReportMetadata {
  reportId: string;
  generatedAt: string;             // ISO 8601 timestamp
  version: string;                 // Schema version
  inputFiles: {
    transcription: string;
    emotion: string;
  };
  processingDuration: number;      // milliseconds
  agentVersion: string;
}

interface Summary {
  title: string;                   // Brief title of the interaction
  description: string;             // 2-3 sentence overview
  overallTone: string;             // Emotional tone (e.g., "Romantic tension")
  confidence: number;              // 0.0 to 1.0
  mainThemes: string[];            // Key themes identified
}

interface InterpretedMoment {
  timestamp: number;               // When it occurred (milliseconds)
  timestampFormatted: string;      // Human-readable (e.g., "00:09.200")
  speaker: string;
  transcript: string;
  emotionDetected: EmotionType;
  interpretation: string;          // Natural language explanation
  significance: "critical" | "high" | "medium" | "low";
  context: string;                 // Surrounding context
  reasoning: string;               // Agent's reasoning process
  relatedMoments: string[];        // IDs of related moments
}

interface SpeakerProfile {
  speaker: string;
  emotionalBaseline: EmotionType;  // Typical emotion state
  emotionalRange: EmotionType[];   // All emotions displayed
  behavioralPatterns: string[];    // Observed patterns
  credibility: number;             // 0.0 to 1.0 (for deception analysis)
  keyCharacteristics: string[];    // Notable traits
}

interface Insight {
  type: "behavioral" | "emotional" | "relational" | "deceptive";
  insight: string;                 // The insight itself
  evidence: string[];              // Supporting evidence (moment IDs)
  confidence: number;              // 0.0 to 1.0
}

interface TimelineEvent {
  timestamp: number;
  timestampFormatted: string;
  type: "speech" | "emotion_spike" | "pattern_change" | "key_moment";
  description: string;
  importance: number;              // 0.0 to 1.0
}

interface ObservabilityMetrics {
  traceId: string;                 // LangSmith trace ID
  totalEvents: number;
  processedEvents: number;
  emotionEntries: number;
  transcriptionEntries: number;
  alignedEvents: number;
  agentIterations: number;
  llmCalls: number;
  totalTokens: number;
  processingTime: {
    alignment: number;             // milliseconds
    analysis: number;
    interpretation: number;
    total: number;
  };
}
```

### 6. API Response Schema

Standard API response wrapper:

```typescript
interface APIResponse<T> {
  success: boolean;
  data?: T;
  error?: APIError;
  metadata: ResponseMetadata;
}

interface APIError {
  code: string;                    // Error code (e.g., "INVALID_SCHEMA")
  message: string;                 // Human-readable error
  details?: Record<string, any>;   // Additional error context
  timestamp: string;               // ISO 8601
}

interface ResponseMetadata {
  requestId: string;
  timestamp: string;               // ISO 8601
  version: string;                 // API version
  processingTime: number;          // milliseconds
}
```

## Data Validation

### Timestamp Validation

```python
import re
from datetime import datetime

def validate_timestamp(timestamp: str) -> bool:
    """Validate timestamp format MM:SS.mmm"""
    pattern = r'^\d{2}:\d{2}\.\d{3}$'
    if not re.match(pattern, timestamp):
        return False
    
    # Parse and validate ranges
    parts = timestamp.split(':')
    seconds_parts = parts[1].split('.')
    
    minutes = int(parts[0])
    seconds = int(seconds_parts[0])
    milliseconds = int(seconds_parts[1])
    
    return (0 <= minutes <= 59 and 
            0 <= seconds <= 59 and 
            0 <= milliseconds <= 999)

def timestamp_to_milliseconds(timestamp: str) -> int:
    """Convert MM:SS.mmm to total milliseconds"""
    parts = timestamp.split(':')
    minutes = int(parts[0])
    seconds_parts = parts[1].split('.')
    seconds = int(seconds_parts[0])
    milliseconds = int(seconds_parts[1])
    
    return (minutes * 60 * 1000) + (seconds * 1000) + milliseconds

def milliseconds_to_timestamp(ms: int) -> str:
    """Convert milliseconds to MM:SS.mmm format"""
    minutes = ms // (60 * 1000)
    remaining = ms % (60 * 1000)
    seconds = remaining // 1000
    milliseconds = remaining % 1000
    
    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
```

### Schema Validation (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Transcription Data",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["startTime", "endTime", "speaker", "transcript"],
    "properties": {
      "startTime": {
        "type": "string",
        "pattern": "^\\d{2}:\\d{2}\\.\\d{3}$"
      },
      "endTime": {
        "type": "string",
        "pattern": "^\\d{2}:\\d{2}\\.\\d{3}$"
      },
      "speaker": {
        "type": "string",
        "minLength": 1,
        "maxLength": 100
      },
      "transcript": {
        "type": "string",
        "minLength": 1
      }
    }
  }
}
```

## Data Storage Considerations

### Database Schema (SQLite)

```sql
-- Transcription entries
CREATE TABLE transcriptions (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    start_time_ms INTEGER NOT NULL,
    end_time_ms INTEGER NOT NULL,
    speaker TEXT NOT NULL,
    transcript TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_trans_session_time ON transcriptions(session_id, start_time_ms);

-- Emotion detections
CREATE TABLE emotion_detections (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    timestamp_ms INTEGER NOT NULL,
    emotion TEXT NOT NULL,
    confidence REAL,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_emotion_session_time ON emotion_detections(session_id, timestamp_ms);

-- Aligned events
CREATE TABLE aligned_events (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    transcription_id TEXT REFERENCES transcriptions(id),
    start_time_ms INTEGER NOT NULL,
    end_time_ms INTEGER NOT NULL,
    speaker TEXT NOT NULL,
    transcript TEXT NOT NULL,
    emotion_pattern TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_aligned_session_time ON aligned_events(session_id, start_time_ms);

-- Interpretation reports
CREATE TABLE interpretation_reports (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    report_data TEXT NOT NULL,
    trace_id TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_report_session ON interpretation_reports(session_id);
CREATE INDEX idx_report_trace ON interpretation_reports(trace_id);
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 2025 | Initial schema specification |

## Next Steps

See [02_API_SPECIFICATION.md](./02_API_SPECIFICATION.md) for API endpoints that consume and produce these schemas.
