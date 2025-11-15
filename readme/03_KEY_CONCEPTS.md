# 🧠 Key Concepts

Understanding these core concepts will help you navigate and work with DataBrew Lab effectively.

## 📋 Table of Contents
- [Core Terminology](#core-terminology)
- [Feature Concepts](#feature-concepts)
- [Technical Concepts](#technical-concepts)
- [Workflow Concepts](#workflow-concepts)

## 🎯 Core Terminology

### What is DataBrew Lab?

**DataBrew Lab** (also known as Analyst Nexus Research Desktop) is a research intelligence platform that helps you:
- Capture information (documents, audio, meetings, podcasts)
- Process it with AI
- Search and analyze it semantically
- Generate insights and summaries

Think of it as your **AI-powered research workspace**.

### Key Terms

#### Document
Any piece of content you upload:
- PDF files
- Word documents
- Text files
- Audio recordings
- Transcripts

#### Repository
A collection of organized documents with:
- Hierarchical folder structure
- Tags and metadata
- Search capabilities
- Version tracking

#### Thought Nugget
A live audio transcription session that:
- Records audio in real-time
- Transcribes with AI (Whisper)
- Identifies speakers
- Saves for later analysis

#### Brain Discussion
An AI chat interface that:
- Understands your research context
- Answers questions about your documents
- Provides personalized insights
- Maintains conversation history

#### Meeting Bot
An AI agent that:
- Joins video calls (Meet, Zoom, Teams)
- Listens to conversations
- Provides real-time assistance
- Generates meeting summaries

#### Podcast Intelligence
A feature that:
- Fetches podcast episodes
- Transcribes content
- Analyzes themes and insights
- Integrates with research data

## 🔍 Feature Concepts

### 1. Data Ingestion

**What**: The process of getting data into the system.

**How it works**:
```
User uploads file → Backend validates → Extract text → 
Generate embeddings → Store in database → Ready for search
```

**Supported formats**:
- Documents: PDF, DOCX, TXT
- Audio: MP3, WAV, M4A
- Video: MP4 (extracts audio)

### 2. Semantic Search

**What**: Search based on meaning, not just keywords.

**Example**:
- Query: "customer satisfaction issues"
- Matches documents about:
  - "unhappy clients"
  - "user complaints"
  - "feedback problems"

**How it works**:
```
Query → Generate embedding → Find similar vectors → 
Rank by similarity → Return relevant documents
```

### 3. Hybrid Search

**What**: Combines two search methods for better results.

**Components**:
1. **BM25 (Keyword)**: Traditional keyword search
2. **Vector (Semantic)**: Meaning-based search
3. **RRF Fusion**: Intelligently combines both results

**When to use**:
- Keyword search: Exact terms, names, dates
- Semantic search: Concepts, themes, ideas
- Hybrid: Best of both worlds (recommended)

### 4. Embeddings

**What**: Mathematical representations of text that capture meaning.

**Example**:
```
Text: "The cat sat on the mat"
Embedding: [0.23, -0.15, 0.87, ..., 0.42]  (768 dimensions)
```

**Why important**:
- Similar text has similar embeddings
- Enables semantic search
- Powers AI understanding

### 5. Vector Database

**What**: Special database for storing and searching embeddings.

**Features**:
- Fast similarity search
- Handles high-dimensional data
- Supports nearest neighbor queries

**In DataBrew Lab**:
- Local vector search in desktop mode
- Integrated with SQLite/PostgreSQL

### 6. Chunking

**What**: Breaking documents into smaller, manageable pieces.

**Why necessary**:
- AI models have token limits
- Improves search accuracy
- Better context retrieval

**How it works**:
```
Large document (10,000 words) →
Split into chunks (500 words each) →
20 chunks with overlap →
Each chunk gets embedding →
Stored separately
```

**Chunk strategy**:
- Size: ~500-1000 tokens
- Overlap: 50-100 tokens
- Preserves context at boundaries

### 7. Transcription

**What**: Converting speech to text using AI.

**Technology**: OpenAI Whisper API

**Features**:
- Real-time transcription
- Speaker identification (diarization)
- Multiple language support
- High accuracy

**Use cases**:
- Recording meetings
- Transcribing interviews
- Processing podcasts
- Live note-taking

### 8. Agent Communication

**What**: Real-time interaction with AI agents during sessions.

**How it works**:
```
User starts recording → Agent bot created → 
Bot joins context → User asks question → 
Agent uses session data → Responds with insight
```

**Commands**:
- "Summarize what was just said"
- "What are the key points?"
- "Find inconsistencies"

## 🛠️ Technical Concepts

### API Base URL

**What**: The root URL for all backend API calls.

**Why important**: Supports multiple deployment modes.

**Pattern**:
```typescript
const API_BASE_URL = 
  import.meta.env.VITE_API_URL || 'http://localhost:3001/api/v1';

// All API calls use this
fetch(`${API_BASE_URL}/endpoint`)
```

**Modes**:
- Desktop dev: `http://localhost:3001/api/v1`
- Cloud: `https://api.yourdomain.com/api/v1`
- Electron: `http://localhost:3001/api/v1`

### WebSocket (Socket.IO)

**What**: Real-time bidirectional communication.

**vs HTTP**:
- HTTP: Request → Response (one-way)
- WebSocket: Persistent connection (two-way)

**Used for**:
- Live transcription updates
- Meeting bot messages
- Real-time notifications
- Chat messages

**Example**:
```typescript
// Frontend emits event
socket.emit('start_recording', { sessionId: '123' });

// Backend sends update
socket.on('transcript_update', (data) => {
  console.log('New transcript:', data.text);
});
```

### Service Layer

**What**: Business logic separated from API routes.

**Why important**:
- Code reusability
- Easier testing
- Better organization
- Clearer responsibilities

**Example**:
```typescript
// ❌ Bad: Logic in route
router.post('/analyze', (req, res) => {
  const text = req.body.text;
  const words = text.split(' ').length;
  const sentences = text.split('.').length;
  // ... more logic ...
});

// ✅ Good: Logic in service
router.post('/analyze', (req, res) => {
  const result = analyticsService.analyze(req.body);
  res.json(result);
});
```

### Middleware

**What**: Functions that run before your route handlers.

**Purpose**:
- Authentication
- Logging
- Error handling
- Request validation
- Rate limiting

**Example**:
```typescript
// Middleware checks authentication
app.use('/api/v1/protected', authenticateToken);

// Now all /api/v1/protected/* routes are protected
```

### Environment Variables

**What**: Configuration values stored outside code.

**Why important**:
- Security (no API keys in code)
- Flexibility (different per environment)
- Safety (no accidental commits)

**Files**:
- `.env.desktop` - Desktop mode config
- `.env` - Cloud mode config
- `.env.example` - Template for others

### Desktop vs Cloud Mode

**Desktop Mode**:
- SQLite database (local file)
- No external dependencies
- Offline capable
- Best for: Development, privacy

**Cloud Mode**:
- PostgreSQL database (server)
- Redis for caching
- Requires internet
- Best for: Production, teams

**How to detect**:
```typescript
const isDesktop = 
  process.env.NODE_ENV === 'desktop' || 
  process.env.DESKTOP_MODE === 'true';
```

## 🔄 Workflow Concepts

### Document Processing Workflow

```
1. Upload
   ↓
2. Validate (type, size)
   ↓
3. Extract text
   ↓
4. Chunk into pieces
   ↓
5. Generate embeddings
   ↓
6. Store in database
   ↓
7. Ready for search
```

### Search Workflow

```
1. User enters query
   ↓
2. Generate query embedding
   ↓
3. Search database (hybrid or semantic)
   ↓
4. Rank results by relevance
   ↓
5. Return with citations
```

### Live Transcription Workflow

```
1. User clicks "Start Recording"
   ↓
2. Browser captures audio
   ↓
3. Audio chunks sent to backend
   ↓
4. Backend sends to Whisper API
   ↓
5. Transcript returned
   ↓
6. Saved to database
   ↓
7. Frontend updates in real-time
```

### AI Chat Workflow

```
1. User types message
   ↓
2. Search relevant documents
   ↓
3. Build context with search results
   ↓
4. Send to AI (Gemini/OpenAI)
   ↓
5. AI generates response
   ↓
6. Return with citations
```

### Meeting Bot Workflow

```
1. User creates bot for meeting
   ↓
2. Bot joins video call
   ↓
3. Bot listens to conversation
   ↓
4. Transcription happens in background
   ↓
5. User asks bot questions
   ↓
6. Bot responds using meeting context
   ↓
7. Meeting summary generated
```

## 🎓 Learning Tips

### Understand Data Flow

Follow data through the system:
```
User Input → Frontend → API → Service → Database → Response
```

### Read the Logs

Logs tell you what's happening:
```
[INFO] Document uploaded: doc-123
[DEBUG] Generating embedding for chunk 5/20
[INFO] Search query: "customer feedback"
[INFO] Found 12 relevant documents
```

### Use Developer Tools

Browser DevTools are your friend:
- Console: See frontend logs
- Network: Monitor API calls
- Sources: Debug code

### Experiment Safely

Desktop mode is risk-free:
- Uses local database
- Easy to reset
- Fast iteration

## 🔑 Key Takeaways

1. **Semantic Search**: Search by meaning, not just keywords
2. **Embeddings**: Mathematical representations of text meaning
3. **Chunking**: Breaking documents into searchable pieces
4. **WebSocket**: Real-time bidirectional communication
5. **Service Layer**: Business logic separated from routes
6. **Desktop vs Cloud**: Two deployment modes with different trade-offs
7. **API Base URL**: Centralized pattern for all backend calls

## 📚 Next Steps

Now that you understand key concepts:

- **[Frontend Documentation](./04_FRONTEND.md)** - Learn about React components
- **[Backend Documentation](./05_BACKEND.md)** - Understand API routes
- **[Data Flow](./08_DATA_FLOW.md)** - See how data moves through system
- **[API Reference](./06_API_REFERENCE.md)** - Complete API documentation

---

**Tip**: Keep this document handy as a reference when exploring the codebase!
