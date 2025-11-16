# API Specification

## Overview

This document defines the REST API endpoints for the Emotion Interpretation Machine system. The API follows RESTful principles and returns JSON responses.

## Base Configuration

```yaml
Base URL: /api/v1
Content-Type: application/json
Authentication: Bearer token (for production)
Rate Limiting: 100 requests/minute per client
```

## API Endpoints

### 1. Session Management

#### Create Analysis Session

Creates a new analysis session for processing emotion and transcription data.

**Endpoint**: `POST /api/v1/sessions`

**Request Body**:
```json
{
  "name": "Holmes Interview Analysis",
  "description": "Analysis of Lord Alistair interrogation",
  "metadata": {
    "source": "video",
    "duration": "01:26.000",
    "participants": ["Holmes", "Lord Alistair"]
  }
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "sessionId": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Holmes Interview Analysis",
    "status": "created",
    "createdAt": "2025-11-16T10:30:00Z"
  },
  "metadata": {
    "requestId": "req_abc123",
    "timestamp": "2025-11-16T10:30:00Z",
    "version": "1.0",
    "processingTime": 45
  }
}
```

#### Get Session

Retrieve session details and status.

**Endpoint**: `GET /api/v1/sessions/{sessionId}`

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "sessionId": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Holmes Interview Analysis",
    "status": "completed",
    "createdAt": "2025-11-16T10:30:00Z",
    "completedAt": "2025-11-16T10:32:15Z",
    "metadata": {
      "source": "video",
      "duration": "01:26.000",
      "participants": ["Holmes", "Lord Alistair"]
    },
    "statistics": {
      "transcriptionEntries": 18,
      "emotionDetections": 45,
      "alignedEvents": 18,
      "keyMoments": 7
    }
  },
  "metadata": {
    "requestId": "req_def456",
    "timestamp": "2025-11-16T10:35:00Z",
    "version": "1.0",
    "processingTime": 12
  }
}
```

### 2. Data Upload

#### Upload Transcription Data

Upload transcription JSON data for a session.

**Endpoint**: `POST /api/v1/sessions/{sessionId}/transcription`

**Request Body**:
```json
{
  "data": [
    {
      "startTime": "00:03.400",
      "endTime": "00:07.800",
      "speaker": "Holmes",
      "transcript": "Lord Alistair, thank you for clarifying..."
    }
  ],
  "source": "whisper-api",
  "sourceMetadata": {
    "model": "whisper-large-v3",
    "language": "en"
  }
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "uploadId": "upload_trans_123",
    "sessionId": "550e8400-e29b-41d4-a716-446655440000",
    "entriesCount": 18,
    "validationStatus": "passed",
    "warnings": []
  },
  "metadata": {
    "requestId": "req_ghi789",
    "timestamp": "2025-11-16T10:30:30Z",
    "version": "1.0",
    "processingTime": 234
  }
}
```

#### Upload Emotion Data

Upload emotion detection JSON data for a session.

**Endpoint**: `POST /api/v1/sessions/{sessionId}/emotions`

**Request Body**:
```json
{
  "data": [
    {
      "timestamp": "00:05.100",
      "emotion": "Neutral"
    },
    {
      "timestamp": "00:10.200",
      "emotion": "Concentration"
    }
  ],
  "source": "facial-recognition",
  "sourceMetadata": {
    "model": "emotion-detection-v2",
    "confidence_threshold": 0.7
  }
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "uploadId": "upload_emot_456",
    "sessionId": "550e8400-e29b-41d4-a716-446655440000",
    "entriesCount": 45,
    "validationStatus": "passed",
    "warnings": [
      {
        "type": "timestamp_gap",
        "message": "Gap of 5 seconds detected between 00:30.000 and 00:35.000"
      }
    ]
  },
  "metadata": {
    "requestId": "req_jkl012",
    "timestamp": "2025-11-16T10:30:45Z",
    "version": "1.0",
    "processingTime": 189
  }
}
```

### 3. Analysis Execution

#### Start Interpretation Analysis

Trigger the AI agent to analyze and interpret the uploaded data.

**Endpoint**: `POST /api/v1/sessions/{sessionId}/analyze`

**Request Body**:
```json
{
  "analysisType": "comprehensive",
  "options": {
    "focusAreas": ["deception_detection", "emotional_patterns"],
    "detailLevel": "high",
    "includeTimeline": true,
    "includeSpeakerProfiles": true
  },
  "agentConfig": {
    "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "temperature": 0.3,
    "maxIterations": 10
  }
}
```

**Response** (202 Accepted):
```json
{
  "success": true,
  "data": {
    "analysisId": "analysis_789",
    "sessionId": "550e8400-e29b-41d4-a716-446655440000",
    "status": "processing",
    "estimatedCompletionTime": "2025-11-16T10:32:00Z",
    "statusUrl": "/api/v1/sessions/550e8400-e29b-41d4-a716-446655440000/analysis/analysis_789/status"
  },
  "metadata": {
    "requestId": "req_mno345",
    "timestamp": "2025-11-16T10:31:00Z",
    "version": "1.0",
    "processingTime": 78
  }
}
```

#### Get Analysis Status

Check the status of an ongoing analysis.

**Endpoint**: `GET /api/v1/sessions/{sessionId}/analysis/{analysisId}/status`

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "analysisId": "analysis_789",
    "status": "processing",
    "progress": {
      "stage": "interpretation",
      "percentage": 65,
      "currentStep": "Analyzing key emotional moments",
      "completedSteps": ["alignment", "pattern_detection"],
      "remainingSteps": ["narrative_generation", "report_compilation"]
    },
    "startedAt": "2025-11-16T10:31:05Z",
    "estimatedCompletionTime": "2025-11-16T10:32:00Z"
  },
  "metadata": {
    "requestId": "req_pqr678",
    "timestamp": "2025-11-16T10:31:40Z",
    "version": "1.0",
    "processingTime": 15
  }
}
```

**Status Values**:
- `pending`: Queued, not yet started
- `processing`: Analysis in progress
- `completed`: Successfully completed
- `failed`: Analysis failed
- `cancelled`: User cancelled

### 4. Results Retrieval

#### Get Interpretation Report

Retrieve the complete interpretation report.

**Endpoint**: `GET /api/v1/sessions/{sessionId}/report`

**Query Parameters**:
- `format`: Response format (`json`, `markdown`, `html`). Default: `json`
- `includeRaw`: Include raw aligned data. Default: `false`

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "metadata": {
      "reportId": "report_abc123",
      "generatedAt": "2025-11-16T10:32:15Z",
      "version": "1.0",
      "inputFiles": {
        "transcription": "upload_trans_123",
        "emotion": "upload_emot_456"
      },
      "processingDuration": 75000,
      "agentVersion": "1.0.0"
    },
    "summary": {
      "title": "The Case of the Stolen Attestation",
      "description": "Analysis reveals Lord Alistair's deception through emotional tells during Holmes's interrogation.",
      "overallTone": "Investigative with underlying tension",
      "confidence": 0.92,
      "mainThemes": ["deception", "anxiety_suppression", "billiards_connection"]
    },
    "keyMoments": [
      {
        "timestamp": 61300,
        "timestampFormatted": "01:01.300",
        "speaker": "Lord Alistair",
        "transcript": "I... what? No. I haven't played in years.",
        "emotionDetected": "Fear",
        "interpretation": "Lord Alistair experiences a 0.4-second cascade of emotions (Surprise → Fear → forced Neutral) when Holmes mentions billiards. This rapid emotional sequence betrays his attempt to maintain composure.",
        "significance": "critical",
        "context": "Holmes strategically changes subject to billiards, a seemingly random topic that triggers the suspect's anxiety.",
        "reasoning": "The emotion spike at this moment is anomalous compared to Lord Alistair's controlled baseline. The rapid transition from Fear to Neutral indicates conscious emotional suppression.",
        "relatedMoments": ["moment_1", "moment_5"]
      }
    ],
    "speakerProfiles": [
      {
        "speaker": "Lord Alistair",
        "emotionalBaseline": "Concentration",
        "emotionalRange": ["Neutral", "Concentration", "Contempt", "Surprise", "Fear", "Anger"],
        "behavioralPatterns": [
          "Maintains controlled baseline with Concentration and Contempt",
          "Shows anomalous Fear spike at 01:01.300",
          "Rapid emotional suppression indicates practiced deception"
        ],
        "credibility": 0.23,
        "keyCharacteristics": [
          "Skilled liar with emotional control",
          "Vulnerable to unexpected questions",
          "Billiards connection triggers anxiety"
        ]
      }
    ],
    "insights": [
      {
        "type": "deceptive",
        "insight": "Subject demonstrates classic deception pattern: maintained emotional control broken by specific trigger word ('billiards')",
        "evidence": ["moment_4", "moment_5"],
        "confidence": 0.89
      }
    ],
    "timeline": [
      {
        "timestamp": 5100,
        "timestampFormatted": "00:05.100",
        "type": "speech",
        "description": "Holmes begins questioning with neutral tone",
        "importance": 0.4
      },
      {
        "timestamp": 61300,
        "timestampFormatted": "01:01.300",
        "type": "emotion_spike",
        "description": "Critical: Fear spike on billiards question",
        "importance": 1.0
      }
    ],
    "observability": {
      "traceId": "trace_langsmith_xyz789",
      "totalEvents": 18,
      "processedEvents": 18,
      "emotionEntries": 45,
      "transcriptionEntries": 18,
      "alignedEvents": 18,
      "agentIterations": 7,
      "llmCalls": 12,
      "totalTokens": 15234,
      "processingTime": {
        "alignment": 2340,
        "analysis": 45670,
        "interpretation": 26990,
        "total": 75000
      }
    }
  },
  "metadata": {
    "requestId": "req_stu901",
    "timestamp": "2025-11-16T10:33:00Z",
    "version": "1.0",
    "processingTime": 234
  }
}
```

#### Get Key Moments

Retrieve only the key interpreted moments.

**Endpoint**: `GET /api/v1/sessions/{sessionId}/key-moments`

**Query Parameters**:
- `minSignificance`: Minimum significance level (`critical`, `high`, `medium`, `low`). Default: `medium`
- `limit`: Maximum number of moments to return. Default: 10

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "moments": [
      {
        "timestamp": 61300,
        "timestampFormatted": "01:01.300",
        "speaker": "Lord Alistair",
        "transcript": "I... what? No. I haven't played in years.",
        "emotionDetected": "Fear",
        "interpretation": "Critical deception tell...",
        "significance": "critical"
      }
    ],
    "count": 7,
    "filtered": 3
  },
  "metadata": {
    "requestId": "req_vwx234",
    "timestamp": "2025-11-16T10:34:00Z",
    "version": "1.0",
    "processingTime": 89
  }
}
```

#### Get Timeline

Retrieve the complete timeline of events.

**Endpoint**: `GET /api/v1/sessions/{sessionId}/timeline`

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "timeline": [
      {
        "timestamp": 5100,
        "timestampFormatted": "00:05.100",
        "type": "speech",
        "description": "Holmes begins questioning",
        "importance": 0.4
      }
    ],
    "duration": 86000,
    "eventCount": 45
  },
  "metadata": {
    "requestId": "req_yz567",
    "timestamp": "2025-11-16T10:35:00Z",
    "version": "1.0",
    "processingTime": 67
  }
}
```

### 5. Observability

#### Get Trace Information

Retrieve LangSmith trace details for transparency.

**Endpoint**: `GET /api/v1/sessions/{sessionId}/trace`

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "traceId": "trace_langsmith_xyz789",
    "traceUrl": "https://smith.langchain.com/traces/xyz789",
    "agentRuns": [
      {
        "runId": "run_1",
        "type": "agent",
        "startTime": "2025-11-16T10:31:05Z",
        "endTime": "2025-11-16T10:31:12Z",
        "status": "success",
        "input": "Analyze temporal alignment...",
        "output": "Identified 18 aligned events...",
        "toolCalls": [
          {
            "tool": "temporal_aligner",
            "input": {...},
            "output": {...}
          }
        ]
      }
    ],
    "metrics": {
      "totalRunTime": 75000,
      "llmCalls": 12,
      "totalTokens": 15234,
      "costEstimate": 0.234
    }
  },
  "metadata": {
    "requestId": "req_abc890",
    "timestamp": "2025-11-16T10:36:00Z",
    "version": "1.0",
    "processingTime": 45
  }
}
```

### 6. Export

#### Export Report

Export the interpretation report in various formats.

**Endpoint**: `GET /api/v1/sessions/{sessionId}/export`

**Query Parameters**:
- `format`: Export format (`json`, `pdf`, `markdown`, `html`). Required.

**Response** (200 OK):
- For JSON: Returns JSON data
- For PDF/HTML/Markdown: Returns file download

### 7. Batch Operations

#### Batch Analysis

Analyze multiple sessions in batch.

**Endpoint**: `POST /api/v1/batch/analyze`

**Request Body**:
```json
{
  "sessionIds": [
    "550e8400-e29b-41d4-a716-446655440000",
    "660e8400-e29b-41d4-a716-446655440001"
  ],
  "options": {
    "analysisType": "comprehensive"
  }
}
```

**Response** (202 Accepted):
```json
{
  "success": true,
  "data": {
    "batchId": "batch_123",
    "sessionCount": 2,
    "status": "processing",
    "statusUrl": "/api/v1/batch/batch_123/status"
  },
  "metadata": {
    "requestId": "req_batch_1",
    "timestamp": "2025-11-16T10:40:00Z",
    "version": "1.0",
    "processingTime": 123
  }
}
```

## Error Responses

### Error Schema

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional context"
    },
    "timestamp": "2025-11-16T10:30:00Z"
  },
  "metadata": {
    "requestId": "req_error_1",
    "timestamp": "2025-11-16T10:30:00Z",
    "version": "1.0",
    "processingTime": 12
  }
}
```

### Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `SESSION_NOT_FOUND` | 404 | Session ID does not exist |
| `INVALID_SCHEMA` | 400 | Input data fails schema validation |
| `MISSING_DATA` | 400 | Required transcription or emotion data not uploaded |
| `TIMESTAMP_MISMATCH` | 400 | Timestamp formats or ranges incompatible |
| `ANALYSIS_IN_PROGRESS` | 409 | Cannot start new analysis while one is running |
| `ANALYSIS_FAILED` | 500 | Agent analysis encountered an error |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

### Example Error Response

```json
{
  "success": false,
  "error": {
    "code": "INVALID_SCHEMA",
    "message": "Transcription data failed validation",
    "details": {
      "errors": [
        {
          "field": "data[2].startTime",
          "message": "Invalid timestamp format: expected MM:SS.mmm"
        },
        {
          "field": "data[5].speaker",
          "message": "Speaker field cannot be empty"
        }
      ]
    },
    "timestamp": "2025-11-16T10:30:15Z"
  },
  "metadata": {
    "requestId": "req_error_123",
    "timestamp": "2025-11-16T10:30:15Z",
    "version": "1.0",
    "processingTime": 34
  }
}
```

## Rate Limiting

```
Rate Limit: 100 requests per minute per client
Headers:
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1637067600
```

## Webhook Support (Optional)

Register webhooks for asynchronous notifications:

**Endpoint**: `POST /api/v1/webhooks`

**Request Body**:
```json
{
  "url": "https://your-app.com/webhooks/emotion-analysis",
  "events": ["analysis.completed", "analysis.failed"],
  "secret": "webhook_secret_key"
}
```

**Webhook Payload**:
```json
{
  "event": "analysis.completed",
  "sessionId": "550e8400-e29b-41d4-a716-446655440000",
  "analysisId": "analysis_789",
  "timestamp": "2025-11-16T10:32:15Z",
  "data": {
    "reportUrl": "/api/v1/sessions/550e8400-e29b-41d4-a716-446655440000/report"
  }
}
```

## Authentication (Production)

```http
Authorization: Bearer <access_token>
```

OAuth 2.0 flow for production deployment:
1. Obtain access token from auth endpoint
2. Include in all API requests
3. Token expires after 1 hour
4. Refresh using refresh token

## SDK Examples

### Python SDK

```python
from emotion_interpreter import Client

# Initialize client
client = Client(api_key="your_api_key")

# Create session
session = client.create_session(
    name="Holmes Analysis",
    description="Interrogation analysis"
)

# Upload data
client.upload_transcription(
    session_id=session.id,
    data=transcription_json
)

client.upload_emotions(
    session_id=session.id,
    data=emotion_json
)

# Start analysis
analysis = client.analyze(
    session_id=session.id,
    options={"detailLevel": "high"}
)

# Wait for completion
report = client.wait_for_report(
    session_id=session.id,
    analysis_id=analysis.id
)

# Access results
for moment in report.key_moments:
    print(f"{moment.timestamp}: {moment.interpretation}")
```

### JavaScript SDK

```javascript
import { EmotionInterpreter } from 'emotion-interpreter-js';

const client = new EmotionInterpreter({ apiKey: 'your_api_key' });

// Create session
const session = await client.createSession({
  name: 'Holmes Analysis',
  description: 'Interrogation analysis'
});

// Upload data
await client.uploadTranscription(session.id, transcriptionData);
await client.uploadEmotions(session.id, emotionData);

// Start analysis
const analysis = await client.analyze(session.id, {
  detailLevel: 'high'
});

// Poll for completion
const report = await client.waitForReport(session.id, analysis.id);

// Access results
report.keyMoments.forEach(moment => {
  console.log(`${moment.timestamp}: ${moment.interpretation}`);
});
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 2025 | Initial API specification |

## Next Steps

See [03_ARCHITECTURE.md](./03_ARCHITECTURE.md) for system design and [04_AGENT_DESIGN.md](./04_AGENT_DESIGN.md) for agent implementation details.
