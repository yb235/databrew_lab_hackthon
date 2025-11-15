# 🔧 Backend Documentation

Complete guide to the Node.js/Express backend architecture, services, and development patterns.

## 📋 Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Routes & Endpoints](#routes--endpoints)
- [Services Layer](#services-layer)
- [Database Layer](#database-layer)
- [Middleware](#middleware)
- [AI Integration](#ai-integration)
- [Development Patterns](#development-patterns)

## 🎯 Overview

The backend is built with:
- **Node.js 18+** - JavaScript runtime
- **Express** - Web framework
- **TypeScript** - Type safety
- **Socket.IO** - Real-time communication
- **PostgreSQL/SQLite** - Databases
- **Redis** - Caching (cloud mode)

**Port:** 3001  
**API Prefix:** `/api/v1`  
**Package Manager:** npm

## 📁 Project Structure

```
backend/src/
├── routes/              # API endpoint definitions
│   ├── auth.ts         # Authentication
│   ├── dataIngestion.ts # File uploads
│   ├── analytics.ts    # Data analysis
│   ├── search.ts       # Search functionality
│   ├── brain.ts        # AI chat
│   ├── meetstream.ts   # Meeting bots
│   ├── thoughtNuggets.ts # Transcription
│   └── [16 total routes]
├── services/           # Business logic layer
│   ├── aiService.ts    # AI integration
│   ├── providers/      # AI provider implementations
│   │   ├── geminiProvider.ts
│   │   ├── openaiProvider.ts
│   │   └── aiProviderFactory.ts
│   ├── brainService.ts
│   ├── searchService.ts
│   ├── hybridSearchService.ts
│   ├── documentProcessor.ts
│   └── [25+ services]
├── middleware/         # Express middleware
│   ├── errorHandler.ts
│   ├── auth.ts
│   └── rateLimiter.ts
├── config/             # Configuration
│   ├── database.ts     # Database connection
│   ├── desktop.ts      # Desktop mode config
│   └── redis.ts        # Redis connection
├── models/             # Database models/schema
│   ├── schema.sql
│   └── migrations/
├── utils/              # Utilities
│   ├── logger.ts
│   └── validators.ts
├── types/              # TypeScript types
│   ├── index.ts
│   └── brain.ts
└── index.ts           # Server entry point
```

## 🛣️ Routes & Endpoints

### Route Structure

Each route file exports an Express Router:

```typescript
// backend/src/routes/myRoute.ts
import express from 'express';
import { asyncHandler } from '@/middleware/errorHandler';
import { authenticateToken } from '@/middleware/auth';
import { myService } from '@/services/myService';

const router = express.Router();

// Public endpoint
router.get('/public', asyncHandler(async (req, res) => {
  const data = await myService.getPublicData();
  res.json({ success: true, data });
}));

// Protected endpoint
router.post('/protected', authenticateToken, asyncHandler(async (req, res) => {
  const userId = (req as any).user.userId;
  const result = await myService.processData(userId, req.body);
  res.json({ success: true, data: result });
}));

export default router;
```

### Key Routes

**Authentication (`/auth`)**
- `POST /register` - User registration
- `POST /login` - User login
- `GET /me` - Get current user
- `POST /refresh` - Refresh token

**Data Ingestion (`/data-ingestion`)**
- `POST /upload` - Upload file
- `GET /status/:id` - Check processing status
- `GET /recent` - Get recent uploads
- `DELETE /:id` - Delete document

**Search (`/search`)**
- `POST /query` - Search documents
- `POST /semantic` - Semantic search
- `POST /hybrid` - Hybrid search

**Analytics (`/analytics`)**
- `POST /analyze` - Analyze documents
- `POST /extract-entities` - Extract entities
- `POST /sentiment` - Sentiment analysis

**Brain (`/brain`)**
- `GET /state` - Get brain state
- `POST /messages` - Send message
- `POST /genetic-profile` - Upload genetic data

**Meeting (`/meetstream`)**
- `POST /bot` - Create meeting bot
- `GET /bots` - List active bots
- `DELETE /bot/:id` - Remove bot

**Audio Transcription (`/audio-transcription`)**
- `POST /start` - Start session
- `POST /chunk` - Send audio chunk
- `POST /stop` - End session

**Thought Nuggets (`/thought-nuggets`)**
- `POST /save` - Save nugget
- `GET /list` - List nuggets
- `GET /:id` - Get nugget
- `DELETE /:id` - Delete nugget

## 🔧 Services Layer

Services contain the business logic, separated from route handlers.

### Service Pattern

```typescript
// backend/src/services/myService.ts
import { query } from '@/config/database';
import { logger } from '@/utils/logger';
import { getAIProvider } from './providers/aiProviderFactory';

export const myService = {
  async processData(userId: string, data: any) {
    logger.info('Processing data', { userId });
    
    try {
      // 1. Validate input
      if (!data.content) {
        throw new Error('Content is required');
      }
      
      // 2. Process with AI
      const aiProvider = getAIProvider();
      const analysis = await aiProvider.generateCompletion(
        `Analyze this: ${data.content}`
      );
      
      // 3. Save to database
      await query(
        'INSERT INTO processed_data (user_id, content, analysis) VALUES ($1, $2, $3)',
        [userId, data.content, analysis]
      );
      
      // 4. Return result
      return {
        analysis,
        processedAt: new Date()
      };
    } catch (error) {
      logger.error('Failed to process data', { error, userId });
      throw error;
    }
  },
  
  async getData(userId: string, filters: any) {
    const result = await query(
      'SELECT * FROM processed_data WHERE user_id = $1',
      [userId]
    );
    return result.rows;
  }
};
```

### Key Services

**aiService.ts** - AI integration
```typescript
export const aiService = {
  async generateCompletion(prompt: string, options?: any): Promise<string>
  async generateEmbedding(text: string): Promise<number[]>
  async analyzeContent(content: string): Promise<Analysis>
}
```

**brainService.ts** - Brain discussion
```typescript
export const brainService = {
  async handleMessage(userId: string, message: BrainMessageInput): Promise<BrainResponse>
  async getState(userId: string): Promise<BrainState>
  async updateGeneticProfile(userId: string, profile: GeneticProfile): Promise<void>
}
```

**searchService.ts** - Search functionality
```typescript
export const searchService = {
  async keywordSearch(query: string, filters?: SearchFilters): Promise<SearchResult[]>
  async semanticSearch(query: string, limit?: number): Promise<SearchResult[]>
}
```

**hybridSearchService.ts** - Advanced search
```typescript
export const hybridSearchService = {
  async search(query: string, options?: HybridSearchOptions): Promise<HybridSearchResult>
  // Combines BM25 + Vector search with RRF fusion
}
```

**documentProcessor.ts** - File processing
```typescript
export const documentProcessor = {
  async process(filePath: string, metadata: DocumentMetadata): Promise<ProcessedDocument>
  async extractText(filePath: string): Promise<string>
  async generateEmbeddings(text: string): Promise<number[]>
  async chunkDocument(text: string): Promise<Chunk[]>
}
```

## 🗄️ Database Layer

### Database Configuration

**Dual-mode support:**

```typescript
// backend/src/config/database.ts
import { Pool } from 'pg';
import { desktopDb } from '../services/desktopDatabase';

const isDesktopMode = () => {
  return process.env.NODE_ENV === 'desktop' || 
         process.env.DESKTOP_MODE === 'true';
};

// PostgreSQL pool (cloud mode)
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000
});

// Query function - automatically uses correct database
export async function query(sql: string, params: any[] = []) {
  if (isDesktopMode()) {
    return desktopDb.run(sql, params);  // SQLite
  } else {
    return pool.query(sql, params);      // PostgreSQL
  }
}

export async function transaction<T>(callback: (client: any) => Promise<T>): Promise<T> {
  if (isDesktopMode()) {
    return desktopDb.transaction(callback);
  } else {
    const client = await pool.connect();
    try {
      await client.query('BEGIN');
      const result = await callback(client);
      await client.query('COMMIT');
      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }
}
```

### Database Schema

**Key Tables:**

```sql
-- Users
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  role VARCHAR(50) DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Documents
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title VARCHAR(255),
  filename VARCHAR(255),
  file_path TEXT,
  mime_type VARCHAR(100),
  size_bytes INTEGER,
  status VARCHAR(50) DEFAULT 'processing',
  metadata JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Document Chunks
CREATE TABLE document_chunks (
  id SERIAL PRIMARY KEY,
  document_id INTEGER REFERENCES documents(id),
  chunk_index INTEGER,
  content TEXT,
  embedding VECTOR(768),  -- PostgreSQL with pgvector
  metadata JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Thought Nuggets
CREATE TABLE thought_nuggets (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title VARCHAR(255),
  transcript TEXT,
  duration_seconds INTEGER,
  speakers JSONB,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Brain Messages
CREATE TABLE brain_messages (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  content TEXT,
  response TEXT,
  mode VARCHAR(50),
  citations JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Query Patterns

**Best Practices:**

```typescript
// ✅ Good: Parameterized queries
await query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);

// ❌ Bad: String concatenation (SQL injection risk!)
await query(
  `SELECT * FROM users WHERE email = '${email}'`
);

// ✅ Good: Transactions for related operations
await transaction(async (client) => {
  const user = await client.query('INSERT INTO users ... RETURNING id');
  await client.query('INSERT INTO profiles (user_id, ...) VALUES ($1, ...)', [user.rows[0].id]);
});

// ✅ Good: Proper indexing
CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_chunks_document_id ON document_chunks(document_id);
```

## 🛡️ Middleware

### Error Handler

```typescript
// backend/src/middleware/errorHandler.ts
export const asyncHandler = (fn: Function) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

export const errorHandler = (
  err: any,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  logger.error('Request error', { 
    error: err.message,
    stack: err.stack,
    path: req.path
  });

  const status = err.status || 500;
  const message = err.message || 'Internal server error';

  res.status(status).json({
    success: false,
    error: {
      message,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    }
  });
};
```

### Authentication

```typescript
// backend/src/middleware/auth.ts
import jwt from 'jsonwebtoken';

export const authenticateToken = (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ 
      success: false, 
      error: 'Access token required' 
    });
  }

  try {
    const user = jwt.verify(token, process.env.JWT_SECRET!);
    (req as any).user = user;
    next();
  } catch (error) {
    return res.status(403).json({ 
      success: false, 
      error: 'Invalid token' 
    });
  }
};
```

### Rate Limiting

```typescript
// backend/src/middleware/rateLimiter.ts
import rateLimit from 'express-rate-limit';

export const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP'
});

export const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // Only 5 login attempts per 15 minutes
  message: 'Too many login attempts'
});
```

## 🤖 AI Integration

### Provider Factory Pattern

```typescript
// backend/src/services/providers/aiProviderFactory.ts
import { GeminiProvider } from './geminiProvider';
import { OpenAIProvider } from './openaiProvider';

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
  
  throw new Error(`Unsupported AI model: ${selectedModel}`);
}
```

### Gemini Provider

```typescript
// backend/src/services/providers/geminiProvider.ts
import { GoogleGenerativeAI } from '@google/generative-ai';

export class GeminiProvider implements AIProvider {
  private genAI: GoogleGenerativeAI;
  
  constructor() {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) throw new Error('GEMINI_API_KEY not configured');
    this.genAI = new GoogleGenerativeAI(apiKey);
  }
  
  async generateCompletion(prompt: string, options?: any): Promise<string> {
    const model = this.genAI.getGenerativeModel({ 
      model: 'gemini-2.5-pro' 
    });
    
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

## 📝 Development Patterns

### Adding New Endpoint

**Step 1: Create Route**
```typescript
// backend/src/routes/myFeature.ts
import express from 'express';
import { asyncHandler } from '@/middleware/errorHandler';
import { myService } from '@/services/myService';

const router = express.Router();

router.post('/process', asyncHandler(async (req, res) => {
  const result = await myService.process(req.body);
  res.json({ success: true, data: result });
}));

export default router;
```

**Step 2: Create Service**
```typescript
// backend/src/services/myService.ts
export const myService = {
  async process(data: any) {
    // Business logic here
    return { processed: true };
  }
};
```

**Step 3: Register Route**
```typescript
// backend/src/index.ts
import myFeatureRoutes from './routes/myFeature';

app.use(`/api/${API_VERSION}/my-feature`, myFeatureRoutes);
```

### Logging Best Practices

```typescript
import { logger } from '@/utils/logger';

// Different log levels
logger.debug('Detailed debug info', { data });
logger.info('General information', { userId });
logger.warn('Warning condition', { issue });
logger.error('Error occurred', { error, context });

// Structured logging
logger.info('User action', {
  userId: user.id,
  action: 'upload',
  resource: 'document',
  duration: 1234
});
```

## 🧪 Testing

```typescript
// backend/src/__tests__/myService.test.ts
import { myService } from '../services/myService';

describe('MyService', () => {
  test('should process data', async () => {
    const result = await myService.process({ content: 'test' });
    expect(result.processed).toBe(true);
  });
  
  test('should handle errors', async () => {
    await expect(
      myService.process({})
    ).rejects.toThrow('Content is required');
  });
});
```

## 🚀 Running the Backend

```bash
# Development (Cloud mode)
cd backend
npm run dev:cloud

# Development (Desktop mode)
npm run dev:desktop

# Production
npm run build
npm run start
```

## 📚 Next Steps

- **[API Reference](./06_API_REFERENCE.md)** - Complete endpoint docs
- **[Database Schema](./07_DATABASE_SCHEMA.md)** - Database details
- **[Data Flow](./08_DATA_FLOW.md)** - How data moves
- **[AI Integration](./09_AI_INTEGRATION.md)** - AI details

---

**Key Takeaways:**
1. Service layer separates business logic from routes
2. Dual-mode database support (PostgreSQL/SQLite)
3. Factory pattern for AI providers
4. Always use parameterized queries
5. Comprehensive error handling and logging
