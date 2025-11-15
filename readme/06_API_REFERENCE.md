# 📡 API Reference

Complete reference for all backend API endpoints in DataBrew Lab.

## 📋 Table of Contents
- [Base URL](#base-url)
- [Authentication](#authentication)
- [Data Ingestion](#data-ingestion)
- [Search & Analytics](#search--analytics)
- [Brain Discussion](#brain-discussion)
- [Meeting & Transcription](#meeting--transcription)
- [Repository Management](#repository-management)
- [Podcast Intelligence](#podcast-intelligence)
- [Real-Time Features](#real-time-features)
- [Response Formats](#response-formats)
- [Error Codes](#error-codes)

## 🌐 Base URL

```
Development: http://localhost:3001/api/v1
Production: https://your-domain.com/api/v1
```

All endpoints are prefixed with `/api/v1`.

## 🔐 Authentication

### POST /auth/register

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "firstName": "John",
  "lastName": "Doe"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "123",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "user",
      "createdAt": "2025-01-15T10:30:00Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### POST /auth/login

Authenticate and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "123",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### GET /auth/me

Get current user profile.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "123",
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "role": "user"
  }
}
```

## 📤 Data Ingestion

### POST /data-ingestion/upload

Upload a document for processing.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body (FormData):**
```
file: <file>
title: "My Document" (optional)
type: "research" (optional)
folderId: "folder-123" (optional)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "documentId": "doc-123",
    "filename": "document.pdf",
    "status": "processing",
    "uploadedAt": "2025-01-15T10:30:00Z"
  }
}
```

**Supported File Types:**
- PDF: `application/pdf`
- Word: `application/msword`, `.docx`
- Text: `text/plain`
- Audio: `audio/mpeg`, `audio/wav`
- Video: `video/mp4`

**Size Limit:** 50MB

### GET /data-ingestion/status/:documentId

Check document processing status.

**Response:**
```json
{
  "success": true,
  "data": {
    "documentId": "doc-123",
    "status": "completed",
    "progress": 100,
    "extractedText": "...",
    "metadata": {
      "pageCount": 10,
      "wordCount": 5000
    }
  }
}
```

**Statuses:**
- `uploading` - File is being uploaded
- `processing` - Extracting text and generating embeddings
- `completed` - Ready for search
- `failed` - Error occurred

### GET /data-ingestion/recent

Get recent uploads.

**Query Parameters:**
- `limit` (optional): Number of results (default: 10)
- `all` (optional): Include all users' uploads if admin (default: false)

**Response:**
```json
{
  "success": true,
  "data": {
    "documents": [
      {
        "id": "doc-123",
        "title": "Research Report",
        "filename": "report.pdf",
        "uploadedAt": "2025-01-15T10:30:00Z",
        "status": "completed"
      }
    ]
  }
}
```

## 🔍 Search & Analytics

### POST /search/query

Perform hybrid search across documents.

**Request Body:**
```json
{
  "query": "customer satisfaction analysis",
  "searchType": "hybrid",
  "limit": 10,
  "filters": {
    "documentTypes": ["research", "interview"],
    "dateRange": {
      "start": "2025-01-01",
      "end": "2025-01-31"
    }
  }
}
```

**Search Types:**
- `hybrid` - Combines BM25 + Vector (recommended)
- `semantic` - Vector similarity only
- `keyword` - BM25 keyword search only

**Response:**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "documentId": "doc-123",
        "title": "Q4 Survey Results",
        "snippet": "...customer satisfaction scores improved by 15%...",
        "score": 0.89,
        "highlights": ["customer satisfaction", "analysis"],
        "metadata": {
          "type": "research",
          "createdAt": "2025-01-10T00:00:00Z"
        }
      }
    ],
    "totalResults": 12,
    "searchTime": 0.052
  }
}
```

### POST /analytics/analyze

Analyze documents with AI.

**Request Body:**
```json
{
  "documentIds": ["doc-123", "doc-456"],
  "analysisType": "summary",
  "options": {
    "language": "en",
    "depth": "detailed"
  }
}
```

**Analysis Types:**
- `summary` - Generate summary
- `entities` - Extract named entities
- `sentiment` - Sentiment analysis
- `themes` - Identify key themes
- `relationships` - Find entity relationships

**Response:**
```json
{
  "success": true,
  "data": {
    "analysis": {
      "summary": "The documents discuss...",
      "keyPoints": [
        "Customer satisfaction improved",
        "Revenue increased by 20%"
      ],
      "confidence": 0.92
    }
  }
}
```

### POST /analytics/extract-entities

Extract named entities from documents.

**Request Body:**
```json
{
  "documentIds": ["doc-123"],
  "entityTypes": ["PERSON", "ORG", "LOCATION"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "entities": [
      {
        "text": "Apple Inc.",
        "type": "ORG",
        "occurrences": 15,
        "confidence": 0.95
      }
    ]
  }
}
```

## 🧠 Brain Discussion

### GET /brain/state

Get current brain discussion state.

**Response:**
```json
{
  "success": true,
  "data": {
    "mode": "professional",
    "conversationHistory": [...],
    "geneticProfile": {...},
    "preferences": {...}
  }
}
```

### POST /brain/messages

Send message to brain AI.

**Request Body:**
```json
{
  "content": "What are the key findings?",
  "mode": "professional",
  "projectId": "proj-123" (optional)
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "response": "Based on the analysis...",
    "citations": [
      {
        "documentId": "doc-123",
        "snippet": "...",
        "relevance": 0.92
      }
    ],
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

### POST /brain/genetic-profile

Upload genetic data for personalized insights.

**Request Body:**
```json
{
  "filename": "genetic_data.txt",
  "traits": {
    "riskTolerance": 75,
    "impulsivity": 40,
    "stressResponse": 60
  }
}
```

## 🎙️ Meeting & Transcription

### POST /meetstream/bot

Create a meeting bot.

**Request Body:**
```json
{
  "meetingUrl": "https://meet.google.com/abc-defg-hij",
  "botName": "Research Assistant",
  "instructions": "Take notes and answer questions"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "botId": "bot-123",
    "status": "created",
    "joinLink": "..."
  }
}
```

### POST /audio-transcription/start

Start live transcription session.

**Request Body:**
```json
{
  "sessionId": "session-123",
  "language": "en",
  "speakerDiarization": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "sessionId": "session-123",
    "status": "active",
    "startedAt": "2025-01-15T10:30:00Z"
  }
}
```

### POST /audio-transcription/chunk

Send audio chunk for transcription.

**Headers:**
```
Content-Type: audio/webm
```

**Request Body:** Binary audio data

**Response:**
```json
{
  "success": true,
  "data": {
    "text": "This is the transcribed text",
    "speaker": "Speaker 1",
    "confidence": 0.95,
    "timestamp": 1234567890
  }
}
```

### POST /thought-nuggets/save

Save a thought nugget session.

**Request Body:**
```json
{
  "title": "Team Meeting Notes",
  "transcript": "...",
  "duration": 3600,
  "speakers": ["Speaker 1", "Speaker 2"]
}
```

## 📚 Repository Management

### GET /repository/folders

List all folders.

**Response:**
```json
{
  "success": true,
  "data": {
    "folders": [
      {
        "id": "folder-123",
        "name": "Research Reports",
        "parentId": null,
        "documentCount": 15
      }
    ]
  }
}
```

### POST /repository/folders

Create new folder.

**Request Body:**
```json
{
  "name": "New Folder",
  "parentId": "folder-123" (optional)
}
```

### GET /repository/documents

List documents in folder.

**Query Parameters:**
- `folderId` (optional): Filter by folder
- `page` (optional): Page number
- `limit` (optional): Results per page

## 📻 Podcast Intelligence

### POST /podcast-transcription/add-podcast

Add podcast for processing.

**Request Body:**
```json
{
  "podcastUrl": "https://podcasts.apple.com/...",
  "episodeLimit": 10
}
```

### GET /podcast-transcription/episodes

List podcast episodes.

**Response:**
```json
{
  "success": true,
  "data": {
    "episodes": [
      {
        "id": "ep-123",
        "title": "Episode Title",
        "description": "...",
        "audioUrl": "...",
        "transcriptionStatus": "completed"
      }
    ]
  }
}
```

## ⚡ Real-Time Features (WebSocket)

### Connection

```javascript
import io from 'socket.io-client';

const socket = io('http://localhost:3001', {
  auth: { token: yourAuthToken }
});
```

### Events

**Client → Server:**

```javascript
// Start recording
socket.emit('start_recording', { sessionId: '123' });

// Send audio chunk
socket.emit('audio_chunk', { sessionId: '123', audio: buffer });

// Stop recording
socket.emit('stop_recording', { sessionId: '123' });
```

**Server → Client:**

```javascript
// Transcript update
socket.on('transcript_update', (data) => {
  console.log('New transcript:', data.text);
});

// Bot message
socket.on('bot_message', (data) => {
  console.log('Bot says:', data.message);
});

// Status update
socket.on('status_update', (data) => {
  console.log('Status:', data.status);
});
```

## 📊 Response Formats

### Success Response

```json
{
  "success": true,
  "data": {
    // Response data
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  }
}
```

## ⚠️ Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `VALIDATION_ERROR` | Invalid request data | 400 |
| `UNAUTHORIZED` | Missing or invalid token | 401 |
| `FORBIDDEN` | Insufficient permissions | 403 |
| `NOT_FOUND` | Resource not found | 404 |
| `CONFLICT` | Resource already exists | 409 |
| `RATE_LIMIT_EXCEEDED` | Too many requests | 429 |
| `INTERNAL_ERROR` | Server error | 500 |
| `SERVICE_UNAVAILABLE` | External service down | 503 |

## 🔒 Rate Limiting

**Limits:**
- Authentication: 5 requests per 15 minutes per IP
- API calls: 100 requests per 15 minutes per user
- File uploads: 10 uploads per hour per user
- Search: 50 requests per minute per user

**Rate limit headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642345678
```

## 🧪 Testing APIs

### Using cURL

```bash
# Register user
curl -X POST http://localhost:3001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","firstName":"Test","lastName":"User"}'

# Upload file
curl -X POST http://localhost:3001/api/v1/data-ingestion/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf" \
  -F "title=My Document"

# Search
curl -X POST http://localhost:3001/api/v1/search/query \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"customer feedback","searchType":"hybrid"}'
```

### Using Postman

1. Import collection from `/postman_collection.json`
2. Set environment variables:
   - `baseUrl`: `http://localhost:3001/api/v1`
   - `token`: Your JWT token
3. Run requests

### API Documentation UI

Visit `http://localhost:3001/api/v1/docs` when backend is running for interactive API documentation.

---

**Related Documentation:**
- [Backend Documentation](./05_BACKEND.md) - Implementation details
- [Data Flow](./08_DATA_FLOW.md) - How data moves through APIs
- [Quick Start](./02_QUICK_START.md) - Setup instructions
