# Architecture Specification

## Overview

This document describes the detailed system architecture for the Emotion Interpretation Machine, including all components, their interactions, technology choices, and design rationale.

## System Architecture

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                          Client Layer                                 │
│  ┌────────────────┐                                                  │
│  │  Web Client    │                                                  │
│  │  (React)       │                                                  │
│  └────────────────┘                                                  │
└────────────────────────────┬─────────────────────────────────────────┘
                             │ HTTPS/REST API
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                          API Gateway Layer                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  API Gateway (Express.js / FastAPI)                          │  │
│  │  - Request validation                                        │  │
│  │  - Authentication & Authorization                            │  │
│  │  - Rate limiting                                             │  │
│  │  - Request routing                                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      Application Services Layer                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │  Session         │  │  Data Upload     │  │  Export         │  │
│  │  Manager         │  │  Service         │  │  Service        │  │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │  Validation      │  │  Temporal        │  │  Report         │  │
│  │  Service         │  │  Alignment       │  │  Generator      │  │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘  │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      AI Agent Layer (Core)                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Interpretation Agent (LangGraph)                            │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────┐    │  │
│  │  │  Pattern   │  │  Reasoner  │  │  Narrator          │    │  │
│  │  │  Analyzer  │  │  Node      │  │  (Output Formatter)│    │  │
│  │  └────────────┘  └────────────┘  └────────────────────┘    │  │
│  │                                                               │  │
│  │  Tools:                                                       │  │
│  │  - TemporalAlignmentTool                                     │  │
│  │  - EmotionPatternDetectorTool                                │  │
│  │  - AnomalyDetectorTool                                       │  │
│  │  - NarrativeGeneratorTool                                    │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      LLM Provider Layer                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Holistic AI Bedrock Proxy                                   │  │
│  │  - Claude 3.5 Sonnet (primary)                              │  │
│  │  - Llama 3.2 (fallback)                                     │  │
│  │  - Amazon Nova (alternative)                                │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      Observability Layer                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  LangSmith - Complete Observability Platform                 │  │
│  │  - Execution tracing and visualization                       │  │
│  │  - Performance metrics and analytics                         │  │
│  │  - Token usage tracking and cost monitoring                  │  │
│  │  - Error tracking and debugging                              │  │
│  │  - Decision logging and audit trails                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      Data Persistence Layer                           │
│  ┌────────────────┐  ┌─────────────────┐                           │
│  │  SQLite        │  │  Local File     │                           │
│  │  (Database)    │  │  Storage        │                           │
│  │  (Sessions,    │  │  (Reports,      │                           │
│  │   Reports,     │  │   Exports,      │                           │
│  │   Events)      │  │   Uploads)      │                           │
│  └────────────────┘  └─────────────────┘                           │
└──────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. API Gateway Layer

**Technology**: FastAPI (Python)

**Responsibilities**:
- HTTP request handling
- Request/response validation
- Authentication (JWT tokens)
- Rate limiting (100 req/min)
- CORS configuration
- Request logging
- Error handling

**Key Files**:
```
api/
├── main.py
├── routes/
│   ├── sessions.py
│   ├── upload.py
│   ├── analysis.py
│   └── reports.py
├── middleware/
│   ├── auth.py
│   ├── validation.py
│   └── rateLimit.py
└── config/
    └── api_config.py
```

**Dependencies**:
- FastAPI 0.100+
- Pydantic
- slowapi
- python-jose (JWT)
- python-multipart

### 2. Application Services Layer

#### Session Manager Service

**Purpose**: Manage analysis sessions lifecycle

**Operations**:
- Create new session
- Update session status
- Retrieve session details
- Delete session (with cascade)

**Interface**:
```typescript
interface SessionManager {
  createSession(params: SessionCreateParams): Promise<Session>;
  getSession(sessionId: string): Promise<Session>;
  updateSession(sessionId: string, updates: Partial<Session>): Promise<Session>;
  deleteSession(sessionId: string): Promise<void>;
  listSessions(filters: SessionFilters): Promise<Session[]>;
}
```

#### Data Upload Service

**Purpose**: Handle transcription and emotion data uploads

**Operations**:
- Validate input schema
- Store raw data
- Normalize timestamps
- Trigger validation pipeline

**Validation Pipeline**:
```
Raw JSON → Schema Validation → Timestamp Normalization → 
Data Cleaning → Storage → Return Upload ID
```

#### Validation Service

**Purpose**: Validate and sanitize input data

**Checks**:
- JSON schema compliance
- Timestamp format validation
- Timestamp ordering (startTime < endTime)
- Required field presence
- Data type validation
- Range checks (e.g., emotion enum values)

**Example Validator**:
```python
from pydantic import BaseModel, validator

class TranscriptionEntry(BaseModel):
    startTime: str
    endTime: str
    speaker: str
    transcript: str
    
    @validator('startTime', 'endTime')
    def validate_timestamp(cls, v):
        pattern = r'^\d{2}:\d{2}\.\d{3}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid timestamp format')
        return v
    
    @validator('endTime')
    def validate_end_after_start(cls, v, values):
        if 'startTime' in values:
            start_ms = timestamp_to_ms(values['startTime'])
            end_ms = timestamp_to_ms(v)
            if end_ms <= start_ms:
                raise ValueError('endTime must be after startTime')
        return v
```

#### Temporal Alignment Service

**Purpose**: Match emotion detections with transcription segments

**Algorithm**:
```python
def align_emotion_with_transcript(
    transcription: List[TranscriptionEntry],
    emotions: List[EmotionEntry]
) -> List[AlignedEvent]:
    """
    Temporal alignment algorithm:
    1. Convert all timestamps to milliseconds
    2. For each transcription segment [start, end]:
       - Find all emotion detections within the time window
       - Handle boundary cases (±100ms tolerance)
       - Compute emotion pattern (sequence, dominant, transitions)
       - Detect anomalies (unexpected emotions)
    3. Create aligned event objects
    4. Return sorted by timestamp
    """
    aligned_events = []
    
    for trans in transcription:
        start_ms = timestamp_to_ms(trans.startTime)
        end_ms = timestamp_to_ms(trans.endTime)
        
        # Find emotions in window (with tolerance)
        window_emotions = [
            e for e in emotions
            if start_ms - 100 <= timestamp_to_ms(e.timestamp) <= end_ms + 100
        ]
        
        # Analyze emotion pattern
        emotion_pattern = analyze_emotion_pattern(window_emotions)
        
        # Create aligned event
        event = AlignedEvent(
            startTime=start_ms,
            endTime=end_ms,
            speaker=trans.speaker,
            transcript=trans.transcript,
            emotions=window_emotions,
            emotionPattern=emotion_pattern
        )
        
        aligned_events.append(event)
    
    return sorted(aligned_events, key=lambda e: e.startTime)
```

**Edge Cases**:
- No emotion data for a transcription segment (mark as "no_data")
- Multiple rapid emotions (micro-expressions)
- Timestamp gaps (large pauses)
- Overlapping transcriptions (concurrent speakers)

#### Report Generator Service

**Purpose**: Format and compile interpretation reports

**Output Formats**:
- JSON (structured data)
- Markdown (human-readable)
- HTML (web display)
- PDF (download/print)

### 3. AI Agent Layer (Core)

**Technology**: LangGraph + LangChain + Holistic AI Bedrock

#### Agent Architecture

```python
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated

# State definition
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    aligned_events: List[AlignedEvent]
    context_windows: List[ContextWindow]
    interpretations: List[InterpretedMoment]
    insights: List[Insight]
    speaker_profiles: Dict[str, SpeakerProfile]
    is_last_step: bool

# Create graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("analyze_patterns", analyze_emotion_patterns)
graph.add_node("detect_anomalies", detect_emotional_anomalies)
graph.add_node("build_context", build_conversation_context)
graph.add_node("interpret_moments", interpret_key_moments)
graph.add_node("generate_insights", generate_behavioral_insights)
graph.add_node("create_profiles", create_speaker_profiles)
graph.add_node("synthesize_report", synthesize_final_report)

# Define edges
graph.add_edge(START, "analyze_patterns")
graph.add_edge("analyze_patterns", "detect_anomalies")
graph.add_edge("detect_anomalies", "build_context")
graph.add_edge("build_context", "interpret_moments")
graph.add_edge("interpret_moments", "generate_insights")
graph.add_edge("generate_insights", "create_profiles")
graph.add_edge("create_profiles", "synthesize_report")
graph.add_edge("synthesize_report", END)

# Compile
agent = graph.compile()
```

#### Agent Nodes

**1. Pattern Analyzer Node**
- Analyzes emotion sequences for each aligned event
- Identifies emotional patterns (baseline, spikes, suppressions)
- Computes pattern metrics (volatility, intensity, transitions)

**2. Anomaly Detector Node**
- Detects unexpected emotional responses
- Compares against speaker baseline
- Flags emotion-speech conflicts

**3. Context Builder Node**
- Groups events into conversation windows
- Identifies conversation flow stages
- Tracks emotional trajectory

**4. Interpreter Node**
- Generates natural language interpretations
- Explains significance of key moments
- Provides reasoning chains

**5. Insight Generator Node**
- Synthesizes cross-event patterns
- Identifies behavioral themes
- Assesses deception/authenticity

**6. Profile Creator Node**
- Builds speaker-specific profiles
- Determines emotional baselines
- Identifies behavioral patterns

**7. Report Synthesizer Node**
- Compiles all analysis into report structure
- Generates summary and timeline
- Formats for output

#### Agent Tools

```python
from langchain.tools import BaseTool

class TemporalAlignmentTool(BaseTool):
    name = "temporal_aligner"
    description = "Aligns emotion data with transcription segments"
    
    def _run(self, transcription: List, emotions: List) -> List[AlignedEvent]:
        return align_emotion_with_transcript(transcription, emotions)

class EmotionPatternDetectorTool(BaseTool):
    name = "emotion_pattern_detector"
    description = "Detects patterns in emotion sequences"
    
    def _run(self, aligned_events: List[AlignedEvent]) -> List[EmotionPattern]:
        return detect_emotion_patterns(aligned_events)

class AnomalyDetectorTool(BaseTool):
    name = "anomaly_detector"
    description = "Identifies anomalous emotional responses"
    
    def _run(self, events: List[AlignedEvent]) -> List[Anomaly]:
        return detect_anomalies(events)

class NarrativeGeneratorTool(BaseTool):
    name = "narrative_generator"
    description = "Generates natural language interpretations"
    
    def _run(self, moment: InterpretedMoment, context: str) -> str:
        return generate_interpretation_narrative(moment, context)
```

### 4. LLM Provider Layer

**Primary**: Holistic AI Bedrock Proxy

**Configuration**:
```python
from core.react_agent.holistic_ai_bedrock import HolisticAIBedrockChat
from langchain_core.prompts import ChatPromptTemplate

# Initialize model
model = HolisticAIBedrockChat(
    team_id=os.getenv("HOLISTIC_AI_TEAM_ID"),
    api_token=SecretStr(os.getenv("HOLISTIC_AI_API_TOKEN")),
    model="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    temperature=0.3,
    max_tokens=4096
)

# Bind tools
model_with_tools = model.bind_tools(tools)
```

**Model Selection Criteria**:
- **Claude 3.5 Sonnet**: Best for complex reasoning and interpretation (primary)
- **Llama 3.2**: Cost-effective alternative for pattern detection
- **Amazon Nova**: Balanced performance for mixed tasks

**Prompts**:
```python
SYSTEM_PROMPT = """You are an expert behavioral analyst specializing in 
emotion-speech correlation analysis. Your task is to interpret temporal 
alignment between facial emotion detection and speech transcription.

You analyze:
- Emotional authenticity vs. deception
- Micro-expressions and suppressed emotions
- Critical moments where emotions diverge from speech
- Relationship dynamics and interpersonal signals

Provide clear, evidence-based interpretations with specific timestamp 
references. Explain your reasoning step-by-step."""

INTERPRETATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """Analyze this aligned event:

Timestamp: {timestamp}
Speaker: {speaker}
Transcript: "{transcript}"
Emotions detected: {emotions}
Emotion pattern: {pattern}

Context (previous events): {context}

Provide:
1. Interpretation of emotional signals
2. Significance level (critical/high/medium/low)
3. Reasoning for your interpretation
4. Related moments or patterns""")
])
```

### 5. Observability Layer

#### LangSmith Integration (Complete Observability)

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "emotion-interpretation-machine"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"

# Automatic tracing enabled
# All agent runs, tool calls, and LLM interactions are traced
```

**Complete Trace Information Captured**:
- Agent execution graph and flow visualization
- Node inputs/outputs at each step
- Tool calls and results
- LLM prompts and responses
- Timing information and performance metrics
- Token usage and cost tracking
- Error traces and debugging information
- Custom metadata and decision logging

**LangSmith Features Used**:
- **Tracing**: Complete execution visibility
- **Metrics**: Performance and cost analytics
- **Monitoring**: Real-time execution tracking
- **Debugging**: Error analysis and root cause identification
- **Analytics**: Usage patterns and optimization insights

**Custom Decision Logging**:
```python
from langsmith import traceable

@traceable(run_type="chain", name="decision_point")
def log_decision(stage: str, input_data: dict, reasoning: str):
    """Log critical decision points with reasoning"""
    return {
        'stage': stage,
        'input': input_data,
        'reasoning': reasoning,
        'timestamp': datetime.utcnow().isoformat()
    }

# Usage in agent
log_decision(
    stage='anomaly_detection',
    input_data={'event_id': event.id, 'emotions': event.emotions},
    reasoning='Detected Fear spike at 01:01.300, deviates from Neutral baseline'
)
```

**Performance Tracking**:
```python
import time
from contextlib import contextmanager

@contextmanager
def track_performance(operation_name: str):
    """Track performance metrics in LangSmith"""
    start = time.time()
    try:
        yield
    finally:
        duration = (time.time() - start) * 1000
        # Automatically captured in LangSmith trace
        print(f"{operation_name}: {duration:.2f}ms")

# Usage
with track_performance('temporal_alignment'):
    aligned_events = align_emotion_with_transcript(transcription, emotions)
```

### 6. Data Persistence Layer

#### Database

**All Environments**: SQLite
```python
# Simple file-based database
DATABASE_URL = "sqlite:///./emotion_interpretation.db"
```

#### SQLite Schema

```sql
-- Sessions table
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'created',
    metadata TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    completed_at TEXT
);
CREATE INDEX idx_status ON sessions(status);
CREATE INDEX idx_created ON sessions(created_at);

-- Transcription data
CREATE TABLE transcription_entries (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    upload_id TEXT,
    start_time_ms INTEGER NOT NULL,
    end_time_ms INTEGER NOT NULL,
    speaker TEXT NOT NULL,
    transcript TEXT NOT NULL,
    source_metadata TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_session_time ON transcription_entries(session_id, start_time_ms);

-- Emotion data
CREATE TABLE emotion_detections (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    upload_id TEXT,
    timestamp_ms INTEGER NOT NULL,
    emotion TEXT NOT NULL,
    confidence REAL,
    source_metadata TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_emotion_session_time ON emotion_detections(session_id, timestamp_ms);

-- Aligned events
CREATE TABLE aligned_events (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    start_time_ms INTEGER NOT NULL,
    end_time_ms INTEGER NOT NULL,
    speaker TEXT NOT NULL,
    transcript TEXT NOT NULL,
    emotion_pattern TEXT NOT NULL,
    emotions TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_aligned_session_time ON aligned_events(session_id, start_time_ms);

-- Interpretation reports
CREATE TABLE interpretation_reports (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    report_data TEXT NOT NULL,
    trace_id TEXT,
    observability_metrics TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_report_session ON interpretation_reports(session_id);
CREATE INDEX idx_trace ON interpretation_reports(trace_id);

-- Analysis jobs (for tracking async processing)
CREATE TABLE analysis_jobs (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'pending',
    progress TEXT,
    started_at TEXT,
    completed_at TEXT,
    error_message TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_job_session_status ON analysis_jobs(session_id, status);
```

#### In-Memory Caching

**Default and Only Caching**:
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_session_data(session_id: str):
    """Cached session data retrieval"""
    return fetch_from_database(session_id)
```

#### File Storage

**Local File System**:
```python
import os
import json

STORAGE_DIR = os.getenv("STORAGE_DIR", "./storage")

# Storage structure
# storage/
# ├── reports/
# │   └── {session_id}/
# │       ├── report.json
# │       ├── report.md
# │       └── report.html
# ├── uploads/
# │   └── {session_id}/
# │       ├── transcription_raw.json
# │       └── emotion_raw.json
# └── exports/
#     └── {export_id}/
#         └── export.zip

def save_report(session_id: str, report: dict, format: str = 'json'):
    """Save report to local file system"""
    report_dir = os.path.join(STORAGE_DIR, 'reports', session_id)
    os.makedirs(report_dir, exist_ok=True)
    
    if format == 'json':
        filepath = os.path.join(report_dir, 'report.json')
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
    elif format == 'md':
        filepath = os.path.join(report_dir, 'report.md')
        with open(filepath, 'w') as f:
            f.write(generate_markdown_report(report))
    
    return filepath
```

## Technology Stack Summary

### Frontend
- **Client**: React web application

### Backend
- **API**: FastAPI (Python)
- **Agent Framework**: LangGraph 0.2+, LangChain Core 0.3+
- **LLM**: Holistic AI Bedrock Proxy (Claude 3.5, Llama 3.2, Nova)

### Data
- **Database**: SQLite (file-based, all environments)
- **Cache**: In-memory (Python `lru_cache`)
- **Storage**: Local file system

### Observability
- **Complete Platform**: LangSmith (tracing, metrics, monitoring, debugging, analytics)

### Infrastructure
- **Compute**: Simple server deployment
- **Container**: Docker (optional)
- **Deployment**: VPS or any basic hosting platform

## Deployment Architecture

### Development
```
Local Machine:
- SQLite database (./emotion_interpretation.db)
- API Server (localhost:8000)
- Web Client (localhost:5000)
- LangSmith tracing (cloud)
- Local file storage (./storage/)
```

### Production
```
Single Server Deployment:
- SQLite database (persistent disk)
- FastAPI application
- React web client (static files served by API)
- Local file storage (persistent disk)
- LangSmith tracing (cloud)
- Nginx (reverse proxy, optional)
```

## Security Considerations

1. **Authentication**: JWT tokens with configurable expiry
2. **Authorization**: Role-based access control (RBAC)
3. **Data Encryption**: TLS in transit, database encryption at rest
4. **API Security**: Rate limiting, input validation, CORS
5. **Secrets Management**: Environment variables or secrets manager
6. **Audit Logging**: All API calls and decisions logged via LangSmith

## Scalability

### Vertical Scaling
- Increase server resources (CPU, RAM) as needed
- SQLite handles thousands of concurrent reads efficiently

### Performance Optimization
- In-memory response caching (`lru_cache`)
- Database indexing (defined in schema)
- SQLite connection pooling
- Async processing with FastAPI BackgroundTasks

## Next Steps

See:
- [04_AGENT_DESIGN.md](./04_AGENT_DESIGN.md) - Detailed agent implementation
- [05_TEMPORAL_ALIGNMENT.md](./05_TEMPORAL_ALIGNMENT.md) - Alignment algorithms
- [06_OBSERVABILITY.md](./06_OBSERVABILITY.md) - Monitoring and tracing
