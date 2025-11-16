# Data Flow Specification

## Overview

This document describes the end-to-end data flow through the Emotion Interpretation Machine system.

## Complete Data Flow Diagram

```
[User Upload] → [API Gateway] → [Validation] → [Storage] → [Temporal Alignment] 
    → [Agent Processing] → [Report Generation] → [User Retrieval]
```

## Detailed Flow

### 1. Data Ingestion Phase

**Step 1: Create Session**
```
POST /api/v1/sessions
→ Generate session_id
→ Store in SQLite sessions table
→ Return session_id to client
```

**Step 2: Upload Transcription**
```
POST /api/v1/sessions/{id}/transcription
→ Validate JSON schema
→ Normalize timestamps to milliseconds
→ Store in transcription_entries table
→ Return upload_id
```

**Step 3: Upload Emotions**
```
POST /api/v1/sessions/{id}/emotions
→ Validate JSON schema
→ Normalize timestamps
→ Store in emotion_detections table
→ Return upload_id
```

### 2. Analysis Phase

**Step 4: Trigger Analysis**
```
POST /api/v1/sessions/{id}/analyze
→ Create analysis_job record (status: pending)
→ Add job to in-memory queue
→ Return analysis_id (202 Accepted)
```

**Step 5: Background Processing**
```
Worker Process:
1. Fetch job from queue
2. Update status to 'processing'
3. Load transcription and emotion data
4. Run temporal alignment
5. Run agent analysis
6. Generate report
7. Store report
8. Update status to 'completed'
9. Send webhook notification (if configured)
```

### 3. Report Generation Phase

**Step 6: Agent Execution Flow**
```
Agent Graph:
├── validate_input
│   └── Check schemas, timestamps
├── temporal_alignment
│   └── Match emotions to transcripts
├── pattern_analysis
│   └── Compute emotion patterns
├── anomaly_detection
│   └── Find unusual responses
├── context_building
│   └── Group into windows
├── interpret_moments
│   └── LLM generates interpretations
├── speaker_profiling
│   └── Build speaker profiles
├── insight_generation
│   └── Generate behavioral insights
└── report_synthesis
    └── Compile final report
```

**Step 7: Report Storage**
```
Report compilation:
→ Store JSON in interpretation_reports table
→ Save markdown/HTML to local storage
→ Store trace_id from LangSmith
→ Cache report in memory (1 hour TTL)
```

### 4. Retrieval Phase

**Step 8: Fetch Report**
```
GET /api/v1/sessions/{id}/report
→ Check in-memory cache (hit: return cached)
→ Miss: Query SQLite
→ Transform to requested format
→ Return to client
```

## State Transitions

### Session States
```
created → uploading → ready → analyzing → completed
                                       → failed
                                       → cancelled
```

### Analysis Job States
```
pending → processing → completed
                    → failed
```

## Caching Strategy

```python
# In-memory cache using lru_cache
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_session(session_id: str):
    """Cache session data"""
    return fetch_session(session_id)

@lru_cache(maxsize=500)
def get_cached_report(session_id: str):
    """Cache report data"""
    return fetch_report(session_id)
```

## Data Retention

| Data Type | Retention | Storage |
|-----------|-----------|---------|
| Raw uploads | 30 days | SQLite Database |
| Aligned events | 90 days | SQLite Database |
| Reports | 1 year | SQLite Database + Local Files |
| Traces | 30 days | LangSmith |
| Logs | 90 days | LangSmith (via tracing) |
| Cache | In-memory | Python lru_cache |

## Next Steps

See:
- [08_DEPLOYMENT.md](./08_DEPLOYMENT.md) - Infrastructure deployment
- [09_IMPLEMENTATION_GUIDE.md](./09_IMPLEMENTATION_GUIDE.md) - Development guide
