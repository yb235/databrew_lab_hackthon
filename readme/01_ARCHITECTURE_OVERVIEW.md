# 🏛️ System Architecture Overview

This document provides a comprehensive overview of DataBrew Lab's architecture, explaining how all components work together.

## 📋 Table of Contents
- [System Layers](#system-layers)
- [Component Interaction](#component-interaction)
- [Technology Stack](#technology-stack)
- [Architectural Patterns](#architectural-patterns)
- [Data Flow](#data-flow)
- [Deployment Architecture](#deployment-architecture)

## 🎯 Big Picture

DataBrew Lab follows a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                 PRESENTATION LAYER                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  React 19 Frontend (Port 5000)                      │   │
│  │  - UI Components (shadcn/ui)                        │   │
│  │  - State Management (React Hooks)                   │   │
│  │  - Real-time Updates (Socket.IO Client)            │   │
│  │  - Client-side Routing                             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                         ↕ HTTP REST API / WebSocket
┌─────────────────────────────────────────────────────────────┐
│                 APPLICATION LAYER                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Node.js/Express Backend (Port 3001)                │   │
│  │  - REST API Endpoints                               │   │
│  │  - Business Logic Services                          │   │
│  │  - WebSocket Server (Socket.IO)                     │   │
│  │  - Authentication & Authorization                   │   │
│  │  - File Processing & Upload                         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                         ↕ SQL Queries / File I/O
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
│  ┌────────────────┬────────────────┬─────────────────┐     │
│  │ PostgreSQL/    │  Vector DB     │  File Storage   │     │
│  │ SQLite         │  (Embeddings)  │  (Local/Cloud)  │     │
│  │ - User data    │  - Semantic    │  - Documents    │     │
│  │ - Documents    │    search      │  - Audio files  │     │
│  │ - Metadata     │  - Similarity  │  - Transcripts  │     │
│  └────────────────┴────────────────┴─────────────────┘     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Redis Cache (Cloud mode)                           │   │
│  │  - Session storage                                  │   │
│  │  - Temporary data                                   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                         ↕ API Calls
┌─────────────────────────────────────────────────────────────┐
│                 EXTERNAL SERVICES                            │
│  ┌────────────────┬────────────────┬─────────────────┐     │
│  │ AI Services    │  Meeting APIs  │  Podcast APIs   │     │
│  │ - Gemini 2.5   │  - Google Meet │  - Apple        │     │
│  │ - OpenAI GPT-4 │  - Zoom        │  - Spotify      │     │
│  │ - Whisper API  │  - Teams       │  - RSS Feeds    │     │
│  └────────────────┴────────────────┴─────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 System Layers Explained

### 1. Presentation Layer (Frontend)

**Location**: `/src`  
**Technology**: React 19 + TypeScript + Vite  
**Port**: 5000

**Responsibilities**:
- Render user interface
- Handle user interactions
- Manage client-side state
- Communicate with backend via API
- Real-time updates via WebSocket
- Client-side validation

**Key Components**:
```
src/
├── components/          # Reusable UI components
│   ├── ui/             # Base shadcn/ui components
│   ├── Sidebar.tsx     # Navigation sidebar
│   ├── MainContent.tsx # Main content area
│   ├── LiveTranscription.tsx  # Audio transcription
│   └── [other features]
├── hooks/              # Custom React hooks
│   ├── useSupabase.ts  # Database connection
│   └── useMeetstreamSocket.ts  # WebSocket singleton
├── lib/
│   ├── api.ts          # ⚠️ Centralized API client
│   └── utils.ts        # Helper functions
└── App.tsx             # Root component
```

### 2. Application Layer (Backend)

**Location**: `/backend/src`  
**Technology**: Node.js + Express + Socket.IO  
**Port**: 3001

**Responsibilities**:
- Handle HTTP requests
- Implement business logic
- Manage authentication
- Process files and data
- Real-time communication
- Orchestrate external services

**Key Components**:
```
backend/src/
├── routes/              # API endpoint definitions
│   ├── auth.ts         # Authentication
│   ├── dataIngestion.ts # File uploads
│   ├── analytics.ts    # Data analysis
│   ├── meetstream.ts   # Meeting bots
│   ├── brain.ts        # AI chat
│   └── [16 total routes]
├── services/           # Business logic layer
│   ├── aiService.ts    # AI integration
│   ├── providers/      # AI provider implementations
│   ├── brainService.ts # Brain chat logic
│   ├── searchService.ts # Search implementation
│   └── [20+ services]
├── middleware/         # Express middleware
│   ├── errorHandler.ts
│   └── rateLimiter.ts
├── config/             # Configuration
│   ├── database.ts     # DB connection
│   └── desktop.ts      # Desktop mode config
└── index.ts           # Server entry point
```

### 3. Data Layer

**Databases**:

**a) Relational Database**
- **Cloud Mode**: PostgreSQL
- **Desktop Mode**: SQLite
- **Purpose**: Store user data, documents, metadata

**b) Vector Database**
- **Technology**: Custom local vector search
- **Purpose**: Semantic search, similarity matching

**c) Cache Layer**
- **Cloud Mode**: Redis
- **Desktop Mode**: Filesystem cache
- **Purpose**: Session storage, temporary data

**d) File Storage**
- **Cloud Mode**: Cloud storage buckets
- **Desktop Mode**: Local filesystem
- **Purpose**: Documents, audio, transcripts

### 4. External Services Layer

**AI Services**:
- **Gemini 2.5-pro**: Content analysis, summarization
- **OpenAI GPT-4**: Alternative AI provider
- **OpenAI Whisper**: Audio transcription

**Meeting Integration**:
- Google Meet, Zoom, Microsoft Teams
- Bot creation and management

**Podcast Services**:
- Apple Podcasts, Spotify, RSS feeds
- Episode fetching and processing

## 🔗 Component Interaction

### Request Flow Example: User Uploads a Document

```
┌─────────────┐
│   User      │
│   Browser   │
└──────┬──────┘
       │ 1. Select file and click upload
       ↓
┌─────────────────────────────────────────┐
│  Frontend (LiveTranscription.tsx)      │
│  - Validate file                        │
│  - Show upload progress                 │
└──────┬──────────────────────────────────┘
       │ 2. POST /api/v1/data-ingestion/upload
       │    (with file in multipart/form-data)
       ↓
┌─────────────────────────────────────────┐
│  Backend (dataIngestion.ts route)      │
│  - Authenticate user                    │
│  - Validate file type/size              │
└──────┬──────────────────────────────────┘
       │ 3. Call documentProcessor service
       ↓
┌─────────────────────────────────────────┐
│  documentProcessor.ts service          │
│  - Extract text from file               │
│  - Generate metadata                    │
└──────┬──────────────────────────────────┘
       │ 4. Save to database
       ↓
┌─────────────────────────────────────────┐
│  Database (PostgreSQL/SQLite)          │
│  - INSERT document record               │
│  - Store file metadata                  │
└──────┬──────────────────────────────────┘
       │ 5. Generate embeddings
       ↓
┌─────────────────────────────────────────┐
│  AI Service (Gemini/OpenAI)            │
│  - Generate text embeddings             │
│  - Store in vector database             │
└──────┬──────────────────────────────────┘
       │ 6. Return success response
       ↓
┌─────────────────────────────────────────┐
│  Frontend receives response             │
│  - Update UI                            │
│  - Show success notification            │
└─────────────────────────────────────────┘
```

### Real-time Communication Flow: Live Transcription

```
┌─────────────┐                    ┌──────────────┐
│  Frontend   │ ←─── WebSocket ───→│   Backend    │
│  (Browser)  │                    │  (Socket.IO) │
└──────┬──────┘                    └──────┬───────┘
       │                                  │
       │ 1. Start recording              │
       │ ────────────────────────────→   │
       │                                  │
       │ 2. Send audio chunks             │
       │ ────────────────────────────→   │
       │                                  │ 3. Process with Whisper
       │                                  │ ────────────────→ AI
       │                                  │                  Service
       │                                  │ ←───────────────
       │ 4. Emit transcript event         │
       │ ←────────────────────────────   │
       │                                  │
       │ 5. Update UI in real-time       │
       │                                  │
```

## 🏗️ Architectural Patterns

### 1. **API Client Pattern** (Critical!)

**Problem**: Desktop dev mode runs frontend (port 5000) and backend (port 3001) separately.

**Solution**: Centralized API client with configurable base URL.

**Implementation**:
```typescript
// src/lib/api.ts
export const API_BASE_URL = 
  import.meta.env.VITE_API_URL || 'http://localhost:3001/api/v1';

// All API calls use this:
const response = await fetch(`${API_BASE_URL}/endpoint`, {...});
```

**Why it matters**: Enables the same code to work in:
- Desktop dev mode (separate ports)
- Cloud deployment (same domain)
- Electron app (localhost)

### 2. **Service Layer Pattern**

**Problem**: Business logic mixed with route handlers makes code hard to test and maintain.

**Solution**: Separate business logic into service files.

**Example**:
```typescript
// ✅ Good: Thin route handler
router.post('/analyze', asyncHandler(async (req, res) => {
  const result = await analyticsService.analyze(req.body);
  res.json(result);
}));

// Service contains the logic
export const analyticsService = {
  async analyze(data) {
    // Complex business logic here
    const processed = await processData(data);
    const insights = await generateInsights(processed);
    return insights;
  }
};
```

### 3. **Dual-Mode Database Pattern**

**Problem**: Need to support both PostgreSQL (cloud) and SQLite (desktop).

**Solution**: Abstraction layer that detects mode and uses appropriate implementation.

**Example**:
```typescript
// config/database.ts
export async function query(sql: string, params: any[]) {
  if (isDesktopMode()) {
    return desktopDb.run(sql, params);  // SQLite
  } else {
    return pool.query(sql, params);      // PostgreSQL
  }
}
```

### 4. **Singleton Socket Pattern**

**Problem**: Multiple components creating separate WebSocket connections causes state desync.

**Solution**: Single shared socket instance via custom hook.

**Implementation**:
```typescript
// hooks/useMeetstreamSocket.ts
let socketInstance: Socket | null = null;  // Singleton

export function useMeetstreamSocket() {
  if (!socketInstance) {
    socketInstance = io(SOCKET_URL);
  }
  return { socket: socketInstance, ... };
}
```

### 5. **Factory Pattern for AI Providers**

**Problem**: Support multiple AI providers (Gemini, OpenAI, etc.) with different APIs.

**Solution**: Factory pattern with common interface.

**Example**:
```typescript
// services/providers/aiProviderFactory.ts
export function getAIProvider(model?: string): AIProvider {
  if (model?.startsWith('gemini')) {
    return new GeminiProvider();
  } else if (model?.startsWith('gpt')) {
    return new OpenAIProvider();
  }
  return new MockProvider();
}

// All providers implement same interface
interface AIProvider {
  generateCompletion(prompt: string): Promise<string>;
  generateEmbedding(text: string): Promise<number[]>;
}
```

## 📦 Technology Stack Details

### Frontend Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| React | UI framework | 19.0.0 |
| TypeScript | Type safety | 5.7.2 |
| Vite | Build tool | 6.3.5 |
| Tailwind CSS | Styling | 4.1.11 |
| shadcn/ui | UI components | Latest |
| Socket.IO Client | WebSocket | 4.8.1 |
| React Hook Form | Forms | 7.54.2 |
| Recharts | Charts | 2.15.1 |
| Framer Motion | Animations | 12.6.2 |

### Backend Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| Node.js | Runtime | 18+ |
| Express | Web framework | 4.18.2 |
| TypeScript | Type safety | 5.3.3 |
| Socket.IO | WebSocket | 4.7.5 |
| PostgreSQL | Cloud database | Latest |
| SQLite | Desktop database | 3.x |
| Redis | Caching | 4.6.12 |
| Bull | Job queue | 4.12.2 |
| Winston | Logging | 3.11.0 |

### AI & ML Technologies

| Service | Purpose | Model |
|---------|---------|-------|
| Gemini | Analysis, chat | 2.5-pro |
| OpenAI | Alternative AI | GPT-4o |
| Whisper | Transcription | whisper-1 |
| Custom | Vector search | Local |

## 🔐 Security Architecture

### Authentication Flow

```
┌──────────┐     1. Login        ┌──────────┐
│ Frontend │ ─────────────────→  │ Backend  │
└──────────┘                      └────┬─────┘
                                       │ 2. Verify credentials
     ↑                                 ↓
     │                           ┌──────────┐
     │                           │ Database │
     │                           └────┬─────┘
     │ 4. Store token                 │ 3. Generate JWT
     │    in localStorage              ↓
┌──────────┐     ← Token ←      ┌──────────┐
│ Frontend │                     │ Backend  │
└──────────┘                     └──────────┘

All subsequent requests include:
Authorization: Bearer <token>
```

### Security Layers

1. **Helmet**: HTTP security headers
2. **CORS**: Cross-origin request protection
3. **Rate Limiting**: Prevent abuse
4. **JWT**: Token-based authentication
5. **Input Validation**: Joi/Zod schemas
6. **SQL Parameterization**: Prevent injection
7. **File Upload Validation**: Type and size checks

## 🚀 Deployment Architecture

### Cloud Deployment

```
┌─────────────────────────────────────────┐
│         CDN (Vercel/Netlify)            │
│         - Frontend static files         │
│         - Edge caching                  │
└────────────────┬────────────────────────┘
                 │
                 ↓ HTTPS
┌─────────────────────────────────────────┐
│       Load Balancer                     │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        ↓                 ↓
┌──────────────┐  ┌──────────────┐
│  Backend     │  │  Backend     │
│  Instance 1  │  │  Instance 2  │
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬────────┘
                ↓
┌─────────────────────────────────────────┐
│     Managed PostgreSQL                  │
│     Managed Redis                       │
│     Cloud Storage (S3/GCS)              │
└─────────────────────────────────────────┘
```

### Desktop Deployment

```
┌─────────────────────────────────────────┐
│         Electron Application            │
│  ┌────────────┐      ┌───────────────┐ │
│  │  Frontend  │ ──→  │  Backend      │ │
│  │  (Bundled) │ IPC  │  (Embedded)   │ │
│  └────────────┘      └───────┬───────┘ │
└─────────────────────────────┬───────────┘
                              │
                              ↓
         ┌─────────────────────────────────┐
         │    Local File System            │
         │  - SQLite database              │
         │  - Document storage             │
         │  - Cache files                  │
         └─────────────────────────────────┘
```

## 🔄 State Management

### Frontend State

```
┌─────────────────────────────────────────┐
│          Component State                 │
│          (useState, useReducer)         │
└─────────────────────────────────────────┘
                 ↕
┌─────────────────────────────────────────┐
│          Custom Hooks                    │
│  - useMeetstreamSocket (WebSocket)      │
│  - useSupabase (Database)               │
└─────────────────────────────────────────┘
                 ↕
┌─────────────────────────────────────────┐
│          API Client                      │
│          (src/lib/api.ts)               │
└─────────────────────────────────────────┘
                 ↕ HTTP
┌─────────────────────────────────────────┐
│          Backend State                   │
│  - Database (persistent)                │
│  - Redis (temporary)                    │
│  - Memory (session)                     │
└─────────────────────────────────────────┘
```

## 📊 Performance Considerations

### Frontend Optimization
- Code splitting with React.lazy
- Memoization with React.memo, useMemo, useCallback
- Virtual scrolling for large lists
- Debouncing for search inputs
- Image lazy loading

### Backend Optimization
- Database connection pooling
- Redis caching for expensive queries
- Async processing with Bull queues
- Compression middleware
- Response streaming for large files

### Database Optimization
- Proper indexing on frequently queried columns
- Query optimization and EXPLAIN analysis
- Connection pooling
- Prepared statements
- Batch operations

## 🎯 Key Takeaways

1. **Layered Architecture**: Clear separation between presentation, application, and data layers
2. **Dual-Mode Support**: Same codebase works for cloud and desktop deployments
3. **Service Layer**: Business logic separated from route handlers
4. **API Client Pattern**: Centralized API calls support multiple deployment modes
5. **Real-time Communication**: WebSocket for live updates
6. **AI Integration**: Multiple AI providers through factory pattern
7. **Security**: Multiple layers of protection
8. **Scalability**: Designed to scale horizontally

## 📚 Next Steps

Now that you understand the architecture, explore:

- **[Quick Start Guide](./02_QUICK_START.md)** - Set up your development environment
- **[Key Concepts](./03_KEY_CONCEPTS.md)** - Learn core terminology
- **[Frontend Documentation](./04_FRONTEND.md)** - Deep dive into React components
- **[Backend Documentation](./05_BACKEND.md)** - Understand API routes and services

---

**Related Documentation**:
- `/docs/architecture/COMPREHENSIVE_ARCHITECTURE.md` - Even more detailed architecture
- `/docs/architecture/CODE_ARCHITECTURE.md` - Code-level architecture details
- `/agent.md` - Development guidelines for AI agents
