# 🔄 Data Flow & Workflows

Understanding how data moves through DataBrew Lab from input to output.

## 📋 Table of Contents
- [Document Upload Flow](#document-upload-flow)
- [Search Workflow](#search-workflow)
- [Live Transcription Flow](#live-transcription-flow)
- [AI Chat Workflow](#ai-chat-workflow)
- [Meeting Bot Workflow](#meeting-bot-workflow)
- [Podcast Processing Flow](#podcast-processing-flow)

## 📤 Document Upload Flow

### Step-by-Step Process

```
1. User selects file
   ↓
2. Frontend validates file
   - Check file type (PDF, DOCX, TXT, audio)
   - Check file size (< 50MB)
   - Show upload progress
   ↓
3. Upload to backend
   POST /api/v1/data-ingestion/upload
   - multipart/form-data
   - file + metadata
   ↓
4. Backend processes upload
   - Save file to storage
   - Extract text content
   - Generate metadata
   ↓
5. Text chunking
   - Split into 500-1000 token chunks
   - Add overlap (50-100 tokens)
   - Preserve context
   ↓
6. Generate embeddings
   - Call AI service (Gemini/OpenAI)
   - Get 768-dimensional vectors
   - One embedding per chunk
   ↓
7. Store in database
   - Document record in `documents`
   - Chunks in `document_chunks`
   - Embeddings for semantic search
   ↓
8. Update status → completed
   ↓
9. Frontend refreshes
   - Document appears in list
   - Ready for search
```

### Technical Implementation

```typescript
// Frontend - DataIngestion component
const handleUpload = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('title', title);
  
  const response = await dataIngestionAPI.uploadFile(file, { title });
  console.log('Uploaded:', response.documentId);
};

// Backend - dataIngestion route
router.post('/upload', upload.single('file'), async (req, res) => {
  const { file } = req;
  const userId = req.user.userId;
  
  // Extract text
  const text = await extractText(file.path);
  
  // Process document
  const document = await documentProcessor.process({
    userId,
    filePath: file.path,
    filename: file.originalname,
    text
  });
  
  res.json({ success: true, data: { documentId: document.id } });
});

// Document processor service
async process(data) {
  // 1. Save document record
  const doc = await saveDocument(data);
  
  // 2. Chunk text
  const chunks = await chunkingService.chunk(data.text);
  
  // 3. Generate embeddings
  for (const chunk of chunks) {
    const embedding = await aiService.generateEmbedding(chunk.content);
    await saveChunk(doc.id, chunk, embedding);
  }
  
  // 4. Update status
  await updateDocumentStatus(doc.id, 'completed');
  
  return doc;
}
```

## 🔍 Search Workflow

### Hybrid Search Process

```
1. User enters query
   "customer satisfaction issues"
   ↓
2. Frontend sends search request
   POST /api/v1/search/query
   { query, searchType: 'hybrid' }
   ↓
3. Backend processes query
   ├─ Path A: Keyword Search (BM25)
   │  - Tokenize query
   │  - Match against document text
   │  - Score by term frequency
   │  - Return top 20 results
   │
   └─ Path B: Semantic Search (Vector)
      - Generate query embedding
      - Calculate cosine similarity
      - Find nearest vectors
      - Return top 20 results
   ↓
4. Fusion (RRF - Reciprocal Rank Fusion)
   - Combine both result sets
   - Calculate fused scores
   - Re-rank combined results
   ↓
5. Add context & citations
   - Extract relevant snippets
   - Add document metadata
   - Include relevance scores
   ↓
6. Return to frontend
   { results, totalResults, searchTime }
   ↓
7. Display results
   - Highlighted matches
   - Document previews
   - Relevance indicators
```

### Search Types Comparison

| Type | Method | Best For | Speed |
|------|--------|----------|-------|
| **Keyword** | BM25 | Exact terms, names | Fast |
| **Semantic** | Vector similarity | Concepts, meaning | Medium |
| **Hybrid** | BM25 + Vector + RRF | General search | Medium |

### Implementation

```typescript
// Hybrid search service
async search(query: string, options) {
  // 1. Keyword search
  const keywordResults = await this.keywordSearch(query);
  
  // 2. Semantic search
  const embedding = await aiService.generateEmbedding(query);
  const semanticResults = await this.vectorSearch(embedding);
  
  // 3. RRF fusion
  const fusedResults = this.fuseResults(keywordResults, semanticResults);
  
  // 4. Add context
  return this.addContext(fusedResults);
}
```

## 🎙️ Live Transcription Flow

### Real-Time Audio Processing

```
1. User clicks "Start Recording"
   ↓
2. Browser requests microphone access
   navigator.mediaDevices.getUserMedia({ audio: true })
   ↓
3. Create MediaRecorder
   - Sample rate: 16kHz
   - Format: webm/opus
   - Chunk interval: 1 second
   ↓
4. Start recording
   recorder.start(1000)
   ↓
5. Audio chunks generated
   Every 1 second:
   ├─ ondataavailable event fires
   ├─ Get audio blob
   └─ Send to backend via WebSocket
      socket.emit('audio_chunk', { audio: blob })
   ↓
6. Backend receives chunk
   ├─ Buffer audio data
   ├─ When enough data collected:
   └─ Send to Whisper API
      POST https://api.openai.com/v1/audio/transcriptions
   ↓
7. Whisper returns transcript
   {
     text: "This is what was said",
     language: "en",
     confidence: 0.95
   }
   ↓
8. Backend processes transcript
   ├─ Add timestamp
   ├─ Identify speaker (if diarization on)
   └─ Emit to client
      socket.emit('transcript_update', { text, speaker, timestamp })
   ↓
9. Frontend displays transcript
   - Append to transcript view
   - Highlight speaker
   - Auto-scroll to latest
   ↓
10. User clicks "Stop"
    ├─ Stop recorder
    ├─ Send final chunk
    └─ Save session to database
       POST /api/v1/thought-nuggets/save
```

### WebSocket Events

```typescript
// Client events
socket.emit('start_recording', { sessionId });
socket.emit('audio_chunk', { sessionId, audio });
socket.emit('stop_recording', { sessionId });

// Server events
socket.on('transcript_update', ({ text, speaker, timestamp }));
socket.on('transcription_complete', ({ sessionId, transcript }));
socket.on('transcription_error', ({ error }));
```

## 🧠 AI Chat Workflow

### Brain Discussion Flow

```
1. User types message
   "What are the key findings about customer satisfaction?"
   ↓
2. Frontend sends message
   POST /api/v1/brain/messages
   { content, mode: 'professional', projectId }
   ↓
3. Backend receives message
   ├─ Save to brain_messages table
   └─ Process with brain service
   ↓
4. Search for relevant context
   - Generate query embedding
   - Search document chunks
   - Find top 5 relevant chunks
   ↓
5. Build AI prompt
   System: "You are a research assistant..."
   Context: [relevant document chunks]
   User: "What are the key findings..."
   ↓
6. Call AI service (Gemini/OpenAI)
   - Send prompt with context
   - Receive AI response
   - Extract citations
   ↓
7. Process AI response
   ├─ Parse markdown
   ├─ Extract mentioned documents
   ├─ Add citation links
   └─ Calculate relevance scores
   ↓
8. Save response
   UPDATE brain_messages
   SET response = ?, citations = ?
   WHERE id = ?
   ↓
9. Return to frontend
   {
     response: "Based on the analysis...",
     citations: [{ documentId, snippet, relevance }],
     timestamp
   }
   ↓
10. Display in chat
    - Render markdown
    - Show citations
    - Add to history
```

## 🤖 Meeting Bot Workflow

### Bot Lifecycle

```
1. User creates bot
   POST /api/v1/meetstream/bot
   { meetingUrl, botName, instructions }
   ↓
2. Backend creates bot
   ├─ Generate bot ID
   ├─ Store in database
   └─ Send to meeting service
   ↓
3. Bot joins meeting
   - Connect to meeting platform
   - Authenticate
   - Join as participant
   ├─ Status → joining
   └─ Emit bot_created event
   ↓
4. Bot becomes active
   - Listen to audio
   - Transcribe in real-time
   - Status → active
   ↓
5. User sends command
   socket.emit('agent_message', { message: "Summarize discussion" })
   ↓
6. Bot processes command
   ├─ Get meeting context (transcripts)
   ├─ Call AI with context + command
   └─ Generate response
   ↓
7. Bot responds
   socket.emit('bot_message', {
     botId,
     message: "The main points discussed are..."
   })
   ↓
8. User sees response in UI
   ↓
9. Meeting ends
   - Bot leaves meeting
   - Generate summary
   - Save transcript
   - Status → ended
```

## 📻 Podcast Processing Flow

### End-to-End Process

```
1. User adds podcast
   POST /api/v1/podcast-transcription/add-podcast
   { podcastUrl, episodeLimit: 10 }
   ↓
2. Fetch podcast feed
   - Parse RSS/JSON feed
   - Extract metadata
   - List episodes
   ↓
3. Save podcast & episodes
   INSERT INTO podcasts (...)
   INSERT INTO podcast_episodes (...)
   ↓
4. Queue episodes for transcription
   For each episode:
   └─ Add to processing queue
   ↓
5. Process episode (background job)
   ├─ Download audio file
   ├─ Convert format if needed
   ├─ Send to Whisper API
   └─ Receive transcript
   ↓
6. Save transcript
   UPDATE podcast_episodes
   SET transcript = ?,
       transcription_status = 'completed'
   ↓
7. Analyze content (optional)
   - Extract key points
   - Identify speakers
   - Generate summary
   ↓
8. Make searchable
   - Chunk transcript
   - Generate embeddings
   - Store in search index
   ↓
9. Notify user
   - Status update via WebSocket
   - Email notification (optional)
```

## 🔄 State Management

### Frontend State Flow

```
Component State
    ↕ useState/useReducer
Custom Hooks
    ↕ useEffect
API Client
    ↕ fetch
Backend API
    ↕ routes
Services
    ↕ business logic
Database
```

### Real-Time Updates

```
Event Occurs
    ↓
Backend emits socket event
    ↓
Frontend hook listens
    ↓
State updates
    ↓
Component re-renders
    ↓
UI reflects change
```

## 📊 Performance Optimization

### Caching Strategy

```
Request arrives
    ↓
Check cache
    ├─ Hit → Return cached data
    └─ Miss ↓
         Query database
             ↓
         Store in cache (TTL: 5 min)
             ↓
         Return data
```

### Batch Processing

```
Multiple embeddings needed
    ↓
Collect into batch (max 20)
    ↓
Single API call
    ↓
Process results
    ↓
Save all at once (transaction)
```

## 🎯 Key Takeaways

1. **Upload**: File → Extract → Chunk → Embed → Store
2. **Search**: Query → (BM25 + Vector) → Fuse → Rank → Return
3. **Transcription**: Audio → Chunks → Whisper → Stream → Save
4. **AI Chat**: Message → Context → AI → Citations → Response
5. **Meeting Bot**: Join → Listen → Transcribe → Respond → Summary
6. **Podcast**: Fetch → Download → Transcribe → Analyze → Search

## 📚 Next Steps

- **[AI Integration](./09_AI_INTEGRATION.md)** - Deep dive into AI services
- **[Frontend](./04_FRONTEND.md)** - UI component implementation
- **[Backend](./05_BACKEND.md)** - API implementation details

---

**Understanding data flow helps you:**
- Debug issues more effectively
- Optimize performance bottlenecks
- Design new features properly
- Make architectural decisions
