# 🤖 AI Integration Documentation

Complete guide to AI and machine learning integration in DataBrew Lab.

## 📋 Table of Contents
- [Overview](#overview)
- [AI Providers](#ai-providers)
- [Embeddings & Vector Search](#embeddings--vector-search)
- [Text Generation](#text-generation)
- [Audio Transcription](#audio-transcription)
- [Prompt Engineering](#prompt-engineering)
- [Performance & Caching](#performance--caching)

## 🎯 Overview

DataBrew Lab integrates multiple AI services:
- **Gemini 2.5-pro** - Text analysis, chat, embeddings
- **OpenAI GPT-4** - Alternative text model
- **OpenAI Whisper** - Audio transcription
- **Local Vector Database** - Semantic search

### AI Architecture

```
Application Layer
      ↓
AI Service (aiService.ts)
      ↓
Provider Factory (aiProviderFactory.ts)
      ↓
   ┌──────┴──────┐
   ↓             ↓
Gemini        OpenAI
Provider      Provider
   ↓             ↓
External APIs
```

## 🔌 AI Providers

### Provider Factory Pattern

Supports multiple AI providers through a common interface.

```typescript
// backend/src/services/providers/aiProviderFactory.ts
export interface AIProvider {
  generateCompletion(prompt: string, options?: any): Promise<string>;
  generateEmbedding(text: string): Promise<number[]>;
}

export function getAIProvider(model?: string): AIProvider {
  const selectedModel = model || process.env.AI_MODEL || 'gemini-2.0-flash-exp';
  
  if (selectedModel.startsWith('gemini')) {
    return new GeminiProvider();
  } else if (selectedModel.startsWith('gpt')) {
    return new OpenAIProvider();
  }
  
  throw new Error(`Unsupported model: ${selectedModel}`);
}
```

### Gemini Provider

**Models:**
- `gemini-2.5-pro` - Advanced reasoning and analysis
- `gemini-2.0-flash-exp` - Fast generation
- `text-embedding-004` - 768-dimensional embeddings

**Implementation:**
```typescript
// backend/src/services/providers/geminiProvider.ts
import { GoogleGenerativeAI } from '@google/generative-ai';

export class GeminiProvider implements AIProvider {
  private genAI: GoogleGenerativeAI;
  private model: string;
  
  constructor() {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) throw new Error('GEMINI_API_KEY required');
    
    this.genAI = new GoogleGenerativeAI(apiKey);
    this.model = 'gemini-2.5-pro';
  }
  
  async generateCompletion(prompt: string, options = {}): Promise<string> {
    const model = this.genAI.getGenerativeModel({ model: this.model });
    const result = await model.generateContent(prompt);
    return result.response.text();
  }
  
  async generateEmbedding(text: string): Promise<number[]> {
    const model = this.genAI.getGenerativeModel({ 
      model: 'text-embedding-004' 
    });
    const result = await model.embedContent(text);
    return result.embedding.values;
  }
}
```

**Features:**
- Context caching (saves on API costs)
- JSON mode for structured output
- Function calling for tools
- Long context window (up to 2M tokens)

### OpenAI Provider

**Models:**
- `gpt-4o` - Most capable model
- `gpt-4-turbo` - Fast and capable
- `text-embedding-3-small` - Efficient embeddings

**Implementation:**
```typescript
// backend/src/services/providers/openaiProvider.ts
import OpenAI from 'openai';

export class OpenAIProvider implements AIProvider {
  private client: OpenAI;
  
  constructor() {
    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) throw new Error('OPENAI_API_KEY required');
    
    this.client = new OpenAI({ apiKey });
  }
  
  async generateCompletion(prompt: string, options = {}): Promise<string> {
    const response = await this.client.chat.completions.create({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: prompt }],
      temperature: options.temperature || 0.7,
      max_tokens: options.maxTokens || 2000
    });
    
    return response.choices[0].message.content || '';
  }
  
  async generateEmbedding(text: string): Promise<number[]> {
    const response = await this.client.embeddings.create({
      model: 'text-embedding-3-small',
      input: text
    });
    
    return response.data[0].embedding;
  }
}
```

## 🔍 Embeddings & Vector Search

### What are Embeddings?

Embeddings convert text into numerical vectors that capture semantic meaning.

**Example:**
```
Text: "customer satisfaction"
Embedding: [0.23, -0.15, 0.87, ..., 0.42]  (768 numbers)

Similar text has similar vectors:
"client happiness" → [0.21, -0.14, 0.85, ..., 0.40]
```

### Generating Embeddings

```typescript
// Generate embedding for text
const embedding = await aiService.generateEmbedding(
  "The customer is very satisfied with the product"
);
// Returns: number[] (768 dimensions)

// Generate embedding for search query
const queryEmbedding = await aiService.generateEmbedding(
  "customer feedback"
);
```

### Storing Embeddings

**PostgreSQL (with pgvector):**
```sql
CREATE TABLE document_chunks (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding VECTOR(768)
);

-- Create index for fast similarity search
CREATE INDEX idx_embedding ON document_chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

**SQLite (Desktop Mode):**
```sql
-- Store as blob
CREATE TABLE document_embeddings (
  chunk_id INTEGER PRIMARY KEY,
  embedding BLOB
);

-- Custom similarity calculation in JavaScript
```

### Vector Search

**Cosine Similarity Search:**
```typescript
// Find similar documents
async function vectorSearch(queryEmbedding: number[], limit: number = 10) {
  if (isPostgreSQL()) {
    return await query(`
      SELECT 
        id,
        content,
        1 - (embedding <=> $1) as similarity
      FROM document_chunks
      WHERE 1 - (embedding <=> $1) > 0.7
      ORDER BY embedding <=> $1
      LIMIT $2
    `, [queryEmbedding, limit]);
  } else {
    // SQLite: calculate similarity in code
    const chunks = await getAllChunks();
    return chunks
      .map(chunk => ({
        ...chunk,
        similarity: cosineSimilarity(queryEmbedding, chunk.embedding)
      }))
      .filter(c => c.similarity > 0.7)
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, limit);
  }
}
```

**Distance Metrics:**
- `<=>` Cosine distance (PostgreSQL)
- `<#>` Dot product (PostgreSQL)
- `<->` Euclidean distance (PostgreSQL)

### Hybrid Search

Combines keyword (BM25) and semantic (vector) search.

```typescript
async function hybridSearch(query: string) {
  // 1. Keyword search
  const keywordResults = await keywordSearch(query);
  // Returns: [{ id: 'doc1', score: 0.8 }, ...]
  
  // 2. Semantic search
  const queryEmbedding = await generateEmbedding(query);
  const semanticResults = await vectorSearch(queryEmbedding);
  // Returns: [{ id: 'doc2', similarity: 0.9 }, ...]
  
  // 3. RRF Fusion (Reciprocal Rank Fusion)
  const fused = fuseResults(keywordResults, semanticResults);
  // Combines rankings intelligently
  
  return fused;
}
```

**RRF Formula:**
```
score = Σ 1 / (k + rank_i)
where:
  k = 60 (constant)
  rank_i = position in result list i
```

## 💬 Text Generation

### Basic Completion

```typescript
const response = await aiService.generateCompletion(
  "Summarize this document: " + documentText
);
```

### With Context

```typescript
const prompt = `
You are a research assistant. Use the following context to answer the question.

Context:
${relevantChunks.map(c => c.content).join('\n\n')}

Question: ${userQuestion}

Answer:`;

const response = await aiService.generateCompletion(prompt);
```

### Streaming Responses

```typescript
const stream = await aiService.generateCompletionStream(prompt);

for await (const chunk of stream) {
  process.stdout.write(chunk);
  // Send to frontend via WebSocket
  socket.emit('ai_chunk', { text: chunk });
}
```

### Structured Output (JSON Mode)

```typescript
const prompt = `
Extract entities from this text: "${text}"

Return JSON in this format:
{
  "people": ["name1", "name2"],
  "organizations": ["org1", "org2"],
  "locations": ["loc1", "loc2"]
}
`;

const response = await aiService.generateCompletion(prompt, {
  responseFormat: 'json'
});

const entities = JSON.parse(response);
```

## 🎙️ Audio Transcription

### Whisper API Integration

**Models:**
- `whisper-1` - Optimized for transcription

**Features:**
- Multi-language support (98+ languages)
- Speaker diarization
- Timestamps
- High accuracy

### Implementation

```typescript
// backend/src/services/audioTranscriptionService.ts
import OpenAI from 'openai';
import FormData from 'form-data';
import fs from 'fs';

async function transcribeAudio(audioPath: string, options = {}) {
  const client = new OpenAI({ 
    apiKey: process.env.OPENAI_API_KEY 
  });
  
  const transcription = await client.audio.transcriptions.create({
    file: fs.createReadStream(audioPath),
    model: 'whisper-1',
    language: options.language || 'en',
    response_format: 'verbose_json', // Include timestamps
    timestamp_granularities: ['word', 'segment']
  });
  
  return {
    text: transcription.text,
    language: transcription.language,
    duration: transcription.duration,
    segments: transcription.segments
  };
}
```

### Real-Time Transcription

```typescript
// Stream audio chunks to Whisper
async function transcribeChunk(audioBlob: Blob) {
  // 1. Buffer chunks until min size (to reduce API calls)
  audioBuffer.push(audioBlob);
  
  if (audioBuffer.length >= 10) { // 10 seconds worth
    const combinedAudio = combineAudioBlobs(audioBuffer);
    
    // 2. Send to Whisper
    const result = await transcribeAudio(combinedAudio);
    
    // 3. Return transcript
    return result.text;
  }
}
```

## 📝 Prompt Engineering

### Best Practices

**1. Clear Instructions:**
```typescript
// ❌ Vague
"Analyze this"

// ✅ Specific
"Analyze this research document and identify:
1. Main findings
2. Methodology used
3. Key statistics
4. Conclusions"
```

**2. Provide Context:**
```typescript
const prompt = `
Role: You are an expert financial analyst.

Context: The user is analyzing quarterly reports.

Task: Summarize the key financial metrics from this report.

Format: Return a bulleted list.

Report: ${documentText}
`;
```

**3. Few-Shot Examples:**
```typescript
const prompt = `
Extract company names from text.

Example 1:
Input: "Apple and Microsoft announced a partnership"
Output: ["Apple", "Microsoft"]

Example 2:
Input: "Tesla's stock rose after the announcement"
Output: ["Tesla"]

Now extract from:
Input: "${userText}"
Output:`;
```

**4. Constrain Output:**
```typescript
// Limit length
const prompt = `Summarize in exactly 3 sentences: ${text}`;

// Force format
const prompt = `Answer with only "yes" or "no": ${question}`;

// Request JSON
const prompt = `Return as JSON: { "summary": "...", "score": 0-100 }`;
```

### Brain Discussion Prompts

```typescript
function buildBrainPrompt(userMessage: string, mode: string, context: Chunk[]) {
  const personality = {
    professional: "You are a professional research assistant...",
    creative: "You are a creative brainstorming partner...",
    analytical: "You are a data-driven analyst..."
  };
  
  return `
${personality[mode]}

Relevant Research Context:
${context.map((c, i) => `
[${i + 1}] From "${c.documentTitle}":
${c.content}
`).join('\n')}

User Question: ${userMessage}

Instructions:
- Use the provided context to answer
- Cite sources using [1], [2], etc.
- If context doesn't contain the answer, say so
- Be concise but thorough

Answer:`;
}
```

## ⚡ Performance & Caching

### Response Caching

```typescript
// Simple in-memory cache
const cache = new Map<string, { data: any, expires: number }>();

async function getCachedCompletion(prompt: string) {
  const cacheKey = hashPrompt(prompt);
  const cached = cache.get(cacheKey);
  
  if (cached && cached.expires > Date.now()) {
    return cached.data;
  }
  
  const response = await aiService.generateCompletion(prompt);
  
  cache.set(cacheKey, {
    data: response,
    expires: Date.now() + (5 * 60 * 1000) // 5 minutes
  });
  
  return response;
}
```

### Batch Processing

```typescript
// Process multiple embeddings at once
async function generateEmbeddingsBatch(texts: string[]) {
  const BATCH_SIZE = 20;
  const results: number[][] = [];
  
  for (let i = 0; i < texts.length; i += BATCH_SIZE) {
    const batch = texts.slice(i, i + BATCH_SIZE);
    const embeddings = await Promise.all(
      batch.map(text => aiService.generateEmbedding(text))
    );
    results.push(...embeddings);
  }
  
  return results;
}
```

### Rate Limiting

```typescript
// Throttle API calls
class RateLimiter {
  private queue: Promise<any>[] = [];
  private requestsPerMinute = 50;
  
  async throttle<T>(fn: () => Promise<T>): Promise<T> {
    // Wait if queue is full
    if (this.queue.length >= this.requestsPerMinute) {
      await this.queue[0];
    }
    
    const promise = fn();
    this.queue.push(promise);
    
    // Remove after 1 minute
    setTimeout(() => {
      const index = this.queue.indexOf(promise);
      if (index > -1) this.queue.splice(index, 1);
    }, 60000);
    
    return promise;
  }
}
```

### Cost Optimization

**Tips:**
1. Cache embeddings (only generate once per text)
2. Use cheaper models for simple tasks
3. Limit max tokens in completions
4. Batch API calls when possible
5. Implement request deduplication
6. Use context caching (Gemini)

**Model Costs (approximate):**
- Gemini 2.5-pro: $0.00125 per 1K tokens
- GPT-4o: $0.005 per 1K input tokens
- Whisper: $0.006 per minute
- Embeddings: Very cheap (~$0.0001 per 1K tokens)

## 🎯 Key Takeaways

1. **Factory Pattern**: Easily switch between AI providers
2. **Embeddings**: Power semantic search and recommendations
3. **Hybrid Search**: Combine keyword + semantic for best results
4. **Prompt Engineering**: Clear instructions = better results
5. **Caching**: Reduce costs and improve speed
6. **Batch Processing**: Handle large volumes efficiently

## 📚 Next Steps

- **[Data Flow](./08_DATA_FLOW.md)** - See AI in action
- **[Backend](./05_BACKEND.md)** - Service implementation
- **[Troubleshooting](./11_TROUBLESHOOTING.md)** - Common AI issues

---

**Key Resources:**
- [Gemini API Docs](https://ai.google.dev/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [pgvector Guide](https://github.com/pgvector/pgvector)
