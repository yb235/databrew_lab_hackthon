# API Documentation

## Emotion Interpretation Machine API

**Version**: 1.0.0  
**Base URL**: `http://localhost:3001` (default)

---

## Overview

The Emotion Interpretation Machine API provides endpoints for uploading transcription and emotion data, running AI-powered analysis, and retrieving interpretation reports.

### Quick Start

1. Create a session
2. Upload transcription data
3. Upload emotion detection data
4. Check status (ensure READY state)
5. Trigger analysis
6. Download reports

---

## Authentication

Currently, the API does not require authentication. This is suitable for development and testing. For production deployment, implement appropriate authentication mechanisms (JWT, API keys, etc.).

---

## Endpoints

### Health Check

#### `GET /health`

Check API health and database connectivity.

**Response**:
```json
{
  "status": "ok",
  "database": "connected",
  "version": "1.0.0"
}
```

**Status Codes**:
- `200 OK` - Service is healthy

---

### Sessions

#### `POST /api/sessions`

Create a new analysis session.

**Request Body**:
```json
{
  "name": "My Analysis Session"
}
```

**Response**:
```json
{
  "id": 1,
  "name": "My Analysis Session",
  "status": "created",
  "created_at": "2025-11-16T10:00:00.000Z",
  "updated_at": "2025-11-16T10:00:00.000Z"
}
```

**Status Codes**:
- `201 Created` - Session created successfully
- `422 Unprocessable Entity` - Invalid request body

---

#### `GET /api/sessions/{session_id}`

Get details of a specific session.

**URL Parameters**:
- `session_id` (integer, required) - The session ID

**Response**:
```json
{
  "id": 1,
  "name": "My Analysis Session",
  "status": "ready",
  "created_at": "2025-11-16T10:00:00.000Z",
  "updated_at": "2025-11-16T10:00:05.000Z"
}
```

**Status Codes**:
- `200 OK` - Session retrieved successfully
- `404 Not Found` - Session does not exist

---

#### `GET /api/sessions`

List all sessions (ordered by creation date, newest first).

**Response**:
```json
[
  {
    "id": 2,
    "name": "Latest Session",
    "status": "completed",
    "created_at": "2025-11-16T11:00:00.000Z",
    "updated_at": "2025-11-16T11:05:00.000Z"
  },
  {
    "id": 1,
    "name": "First Session",
    "status": "ready",
    "created_at": "2025-11-16T10:00:00.000Z",
    "updated_at": "2025-11-16T10:05:00.000Z"
  }
]
```

**Status Codes**:
- `200 OK` - Sessions retrieved successfully

---

#### `GET /api/sessions/{session_id}/status`

Get detailed status of a session including data counts.

**URL Parameters**:
- `session_id` (integer, required) - The session ID

**Response**:
```json
{
  "session_id": 1,
  "name": "My Analysis Session",
  "status": "ready",
  "created_at": "2025-11-16T10:00:00.000Z",
  "updated_at": "2025-11-16T10:05:00.000Z",
  "data": {
    "transcription_entries": 18,
    "emotion_detections": 47,
    "aligned_events": 18,
    "reports": 0
  }
}
```

**Status Codes**:
- `200 OK` - Status retrieved successfully
- `404 Not Found` - Session does not exist

---

### Data Upload

#### `POST /api/sessions/{session_id}/transcription`

Upload transcription data for a session.

**URL Parameters**:
- `session_id` (integer, required) - The session ID

**Request Body**:
```json
{
  "entries": [
    {
      "startTime": "00:03.400",
      "endTime": "00:07.800",
      "speaker": "Holmes",
      "transcript": "Lord Alistair, thank you for clarifying."
    },
    {
      "startTime": "00:08.500",
      "endTime": "00:12.300",
      "speaker": "Lord Alistair",
      "transcript": "Yes, precisely. I was working on my memoirs."
    }
  ]
}
```

**Time Format**: `MM:SS.mmm` (e.g., `01:23.456` = 1 minute, 23.456 seconds)

**Response**:
```json
{
  "message": "Uploaded 2 transcription entries",
  "session_id": 1
}
```

**Status Codes**:
- `201 Created` - Transcription uploaded successfully
- `404 Not Found` - Session does not exist
- `422 Unprocessable Entity` - Invalid request body

**Notes**:
- Uploading new transcription data will replace existing data for the session
- Updates session status to `uploading`

---

#### `POST /api/sessions/{session_id}/emotions`

Upload emotion detection data for a session.

**URL Parameters**:
- `session_id` (integer, required) - The session ID

**Request Body**:
```json
{
  "detections": [
    {
      "timestamp": "00:03.500",
      "emotion": "Neutral",
      "confidence": 0.85
    },
    {
      "timestamp": "00:08.600",
      "emotion": "Fear",
      "confidence": 0.72
    }
  ]
}
```

**Time Format**: `MM:SS.mmm`

**Response**:
```json
{
  "message": "Uploaded 2 emotion detections",
  "session_id": 1
}
```

**Status Codes**:
- `201 Created` - Emotions uploaded successfully
- `404 Not Found` - Session does not exist
- `422 Unprocessable Entity` - Invalid request body

**Notes**:
- Uploading new emotion data will replace existing data for the session
- If both transcription and emotion data exist, updates session status to `ready`

---

### Analysis

#### `POST /api/sessions/{session_id}/align`

Manually trigger alignment of transcription and emotion data (optional - analysis will auto-align if needed).

**URL Parameters**:
- `session_id` (integer, required) - The session ID

**Response**:
```json
{
  "message": "Aligned 18 events",
  "session_id": 1,
  "aligned_events_count": 18
}
```

**Status Codes**:
- `201 Created` - Alignment completed successfully
- `400 Bad Request` - Missing transcription or emotion data
- `404 Not Found` - Session does not exist

---

#### `POST /api/sessions/{session_id}/analyze`

Run AI agent analysis on a session.

**URL Parameters**:
- `session_id` (integer, required) - The session ID

**Response**:
```json
{
  "message": "Analysis completed successfully",
  "session_id": 1,
  "report_id": 5,
  "critical_moments_found": 3,
  "steps_completed": [
    "temporal_alignment",
    "emotion_pattern_analysis",
    "anomaly_detection",
    "moment_interpretation",
    "speaker_profiling",
    "report_synthesis"
  ]
}
```

**Status Codes**:
- `201 Created` - Analysis completed successfully
- `400 Bad Request` - Missing transcription or emotion data
- `404 Not Found` - Session does not exist
- `500 Internal Server Error` - Analysis failed (check error details)

**Notes**:
- Session status changes to `analyzing` during analysis
- Session status changes to `completed` on success or `failed` on error
- Analysis typically takes 10-30 seconds depending on data size

---

### Reports

#### `GET /api/sessions/{session_id}/report`

Get the interpretation report (JSON format with full data structure).

**URL Parameters**:
- `session_id` (integer, required) - The session ID

**Response**:
```json
{
  "id": 5,
  "session_id": 1,
  "report_data": {
    "summary": "Analysis reveals...",
    "critical_moments": [...],
    "speaker_profiles": {...},
    "emotion_patterns": {...},
    "anomalies": [...]
  },
  "summary": "Analysis reveals...",
  "key_moments": [...],
  "speaker_profiles": {...},
  "created_at": "2025-11-16T10:10:00.000Z"
}
```

**Status Codes**:
- `200 OK` - Report retrieved successfully
- `404 Not Found` - Session or report does not exist

---

#### `GET /api/sessions/{session_id}/report.json`

Download structured JSON report.

**URL Parameters**:
- `session_id` (integer, required) - The session ID

**Response**: JSON file download with structure:
```json
{
  "metadata": {
    "session_name": "My Analysis Session",
    "generated_at": "2025-11-16T10:10:00.000Z",
    "version": "1.0.0"
  },
  "summary": "Executive summary of findings...",
  "key_moments": [
    {
      "timestamp_formatted": "01:01.500",
      "timestamp_ms": 61500,
      "speaker": "Lord Alistair",
      "transcript": "I... I never left the room.",
      "emotions": [
        {"emotion": "Fear", "confidence": 0.85}
      ],
      "reason": "Fear spike during denial - potential deception indicator"
    }
  ],
  "speaker_profiles": {
    "Holmes": {
      "baseline_emotions": {...},
      "patterns": [...]
    }
  },
  "behavioral_insights": [...],
  "emotion_patterns": {...},
  "anomalies": [...],
  "timeline": [...]
}
```

**Headers**:
- `Content-Type`: `application/json`
- `Content-Disposition`: `attachment; filename=report_{session_id}.json`

**Status Codes**:
- `200 OK` - Report downloaded successfully
- `404 Not Found` - Session or report does not exist

---

#### `GET /api/sessions/{session_id}/report.md`

Download human-readable Markdown report.

**URL Parameters**:
- `session_id` (integer, required) - The session ID

**Response**: Markdown file download with formatted report.

**Headers**:
- `Content-Type`: `text/markdown`
- `Content-Disposition`: `attachment; filename=report_{session_id}.md`

**Status Codes**:
- `200 OK` - Report downloaded successfully
- `404 Not Found` - Session or report does not exist

---

#### `GET /api/sessions/{session_id}/aligned-events`

Get aligned events (transcription segments with matched emotions).

**URL Parameters**:
- `session_id` (integer, required) - The session ID

**Response**:
```json
[
  {
    "id": 1,
    "start_time_ms": 3400,
    "end_time_ms": 7800,
    "speaker": "Holmes",
    "transcript": "Lord Alistair, thank you for clarifying.",
    "emotions": [
      {"emotion": "Neutral", "confidence": 0.85, "timestamp_ms": 3500}
    ]
  }
]
```

**Status Codes**:
- `200 OK` - Aligned events retrieved successfully
- `404 Not Found` - Session does not exist

---

## Session Status Values

- `created` - Session created, awaiting data upload
- `uploading` - Data upload in progress
- `ready` - Both transcription and emotion data uploaded, ready for analysis
- `analyzing` - Analysis in progress
- `completed` - Analysis completed successfully
- `failed` - Analysis failed (see error logs)

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common error codes:
- `400 Bad Request` - Invalid request or missing required data
- `404 Not Found` - Resource (session, report) does not exist
- `422 Unprocessable Entity` - Request body validation failed
- `500 Internal Server Error` - Server error during processing

---

## Rate Limiting

Currently, no rate limiting is implemented. For production deployment, consider implementing rate limiting to prevent abuse.

---

## Examples

### Complete Workflow Example

```python
import requests

BASE_URL = "http://localhost:3001"

# 1. Create session
response = requests.post(f"{BASE_URL}/api/sessions", json={"name": "Holmes Interview"})
session_id = response.json()["id"]

# 2. Upload transcription
transcription_data = {
    "entries": [
        {
            "startTime": "00:03.400",
            "endTime": "00:07.800",
            "speaker": "Holmes",
            "transcript": "Lord Alistair, thank you for clarifying."
        }
    ]
}
requests.post(f"{BASE_URL}/api/sessions/{session_id}/transcription", json=transcription_data)

# 3. Upload emotions
emotion_data = {
    "detections": [
        {"timestamp": "00:03.500", "emotion": "Neutral", "confidence": 0.85}
    ]
}
requests.post(f"{BASE_URL}/api/sessions/{session_id}/emotions", json=emotion_data)

# 4. Check status
status = requests.get(f"{BASE_URL}/api/sessions/{session_id}/status").json()
print(f"Status: {status['status']}")

# 5. Run analysis
requests.post(f"{BASE_URL}/api/sessions/{session_id}/analyze")

# 6. Download report
report_json = requests.get(f"{BASE_URL}/api/sessions/{session_id}/report.json")
with open("report.json", "wb") as f:
    f.write(report_json.content)
```

---

## Support

For issues or questions, please refer to the project documentation or create an issue in the GitHub repository.

**Version**: 1.0.0  
**Last Updated**: November 16, 2025
