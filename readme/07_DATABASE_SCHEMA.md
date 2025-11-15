# 🗄️ Database Schema Documentation

Complete reference for the database schema, tables, relationships, and data models.

## 📋 Table of Contents
- [Overview](#overview)
- [Database Modes](#database-modes)
- [Core Tables](#core-tables)
- [Relationships](#relationships)
- [Indexes](#indexes)
- [Data Types](#data-types)

## 🎯 Overview

DataBrew Lab uses a relational database schema designed for:
- User management and authentication
- Document storage and processing
- Semantic search with embeddings
- Real-time transcription sessions
- AI conversation history
- Meeting bot management

**Databases:**
- **Cloud Mode**: PostgreSQL with pgvector extension
- **Desktop Mode**: SQLite with custom vector storage

## 🔄 Database Modes

### PostgreSQL (Cloud)
- Full-featured relational database
- pgvector extension for vector operations
- Supports advanced indexing
- Connection pooling
- Transactions with ACID guarantees

### SQLite (Desktop)
- Lightweight file-based database
- Located in user data directory
- Custom vector search implementation
- Full schema replication
- Offline-first design

## 📊 Core Tables

### users
User accounts and authentication.

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  role VARCHAR(50) DEFAULT 'user',
  is_active BOOLEAN DEFAULT true,
  last_login TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

**Columns:**
- `id` - Primary key
- `email` - Unique email address
- `password` - Bcrypt hashed password
- `first_name`, `last_name` - User names
- `role` - User role (user, admin, etc.)
- `is_active` - Account status
- `last_login` - Last login timestamp
- `created_at`, `updated_at` - Audit timestamps

### documents
Uploaded documents and files.

```sql
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255),
  filename VARCHAR(255) NOT NULL,
  file_path TEXT NOT NULL,
  mime_type VARCHAR(100),
  size_bytes INTEGER,
  status VARCHAR(50) DEFAULT 'processing',
  folder_id INTEGER REFERENCES folders(id),
  metadata JSONB DEFAULT '{}',
  processed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_folder_id ON documents(folder_id);
CREATE INDEX idx_documents_created_at ON documents(created_at DESC);
```

**Status Values:**
- `uploading` - File upload in progress
- `processing` - Text extraction and embedding generation
- `completed` - Ready for search
- `failed` - Processing error

### document_chunks
Document text chunks with embeddings.

```sql
CREATE TABLE document_chunks (
  id SERIAL PRIMARY KEY,
  document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  chunk_index INTEGER NOT NULL,
  content TEXT NOT NULL,
  embedding VECTOR(768),  -- PostgreSQL with pgvector
  token_count INTEGER,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chunks_document_id ON document_chunks(document_id);
CREATE INDEX idx_chunks_embedding ON document_chunks USING ivfflat (embedding vector_cosine_ops);
```

**Note:** SQLite uses a separate `document_embeddings` table with blob storage.

### folders
Hierarchical folder structure for organization.

```sql
CREATE TABLE folders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  parent_id INTEGER REFERENCES folders(id) ON DELETE CASCADE,
  path TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_folders_user_id ON folders(user_id);
CREATE INDEX idx_folders_parent_id ON folders(parent_id);
CREATE INDEX idx_folders_path ON folders(path);
```

### thought_nuggets
Transcription sessions and audio recordings.

```sql
CREATE TABLE thought_nuggets (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255),
  transcript TEXT,
  duration_seconds INTEGER,
  speakers JSONB DEFAULT '[]',
  audio_file_path TEXT,
  session_id VARCHAR(100) UNIQUE,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_nuggets_user_id ON thought_nuggets(user_id);
CREATE INDEX idx_nuggets_session_id ON thought_nuggets(session_id);
CREATE INDEX idx_nuggets_created_at ON thought_nuggets(created_at DESC);
```

**Speakers JSONB Format:**
```json
[
  {
    "id": "speaker_1",
    "name": "John Doe",
    "segments": [
      { "start": 0, "end": 15.5, "text": "Hello..." }
    ]
  }
]
```

### brain_messages
AI conversation history.

```sql
CREATE TABLE brain_messages (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  response TEXT NOT NULL,
  mode VARCHAR(50) DEFAULT 'professional',
  project_id VARCHAR(100),
  citations JSONB DEFAULT '[]',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_brain_user_id ON brain_messages(user_id);
CREATE INDEX idx_brain_project_id ON brain_messages(project_id);
CREATE INDEX idx_brain_created_at ON brain_messages(created_at DESC);
```

**Citations JSONB Format:**
```json
[
  {
    "documentId": "doc-123",
    "documentTitle": "Research Report",
    "snippet": "Relevant text...",
    "relevance": 0.92
  }
]
```

### brain_genetic_profiles
User genetic data for personalized insights.

```sql
CREATE TABLE brain_genetic_profiles (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  filename VARCHAR(255),
  file_size INTEGER,
  traits JSONB NOT NULL,
  summary TEXT,
  source VARCHAR(50) DEFAULT 'upload',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_genetic_user_id ON brain_genetic_profiles(user_id);
```

**Traits JSONB Format:**
```json
{
  "riskTolerance": 75,
  "impulsivity": 40,
  "stressResponse": 60,
  "noveltySeeking": 65,
  "lossAversion": 55,
  "dispositionEffect": 50,
  "overconfidenceBias": 45,
  "errorCorrection": 70
}
```

### meeting_bots
Active meeting bots and their status.

```sql
CREATE TABLE meeting_bots (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  bot_id VARCHAR(100) UNIQUE NOT NULL,
  meeting_url TEXT NOT NULL,
  bot_name VARCHAR(255),
  instructions TEXT,
  status VARCHAR(50) DEFAULT 'created',
  join_at TIMESTAMP,
  leave_at TIMESTAMP,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_bots_user_id ON meeting_bots(user_id);
CREATE INDEX idx_bots_bot_id ON meeting_bots(bot_id);
CREATE INDEX idx_bots_status ON meeting_bots(status);
```

**Status Values:**
- `created` - Bot created but not joined
- `joining` - Attempting to join meeting
- `active` - In meeting
- `leaving` - Exiting meeting
- `ended` - Session complete
- `failed` - Error occurred

### podcasts
Podcast shows and metadata.

```sql
CREATE TABLE podcasts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  feed_url TEXT,
  platform VARCHAR(50),
  author VARCHAR(255),
  artwork_url TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_podcasts_user_id ON podcasts(user_id);
CREATE INDEX idx_podcasts_feed_url ON podcasts(feed_url);
```

### podcast_episodes
Individual podcast episodes.

```sql
CREATE TABLE podcast_episodes (
  id SERIAL PRIMARY KEY,
  podcast_id INTEGER NOT NULL REFERENCES podcasts(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  audio_url TEXT NOT NULL,
  duration_seconds INTEGER,
  published_at TIMESTAMP,
  transcript TEXT,
  transcription_status VARCHAR(50) DEFAULT 'pending',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_episodes_podcast_id ON podcast_episodes(podcast_id);
CREATE INDEX idx_episodes_status ON podcast_episodes(transcription_status);
CREATE INDEX idx_episodes_published ON podcast_episodes(published_at DESC);
```

### projects
Project organization for documents and analysis.

```sql
CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  color VARCHAR(20) DEFAULT '#3B82F6',
  icon VARCHAR(50) DEFAULT 'folder',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_user_id ON projects(user_id);
```

### relationships
Entity relationships for knowledge graph.

```sql
CREATE TABLE relationships (
  id SERIAL PRIMARY KEY,
  source_entity VARCHAR(255) NOT NULL,
  relationship_type VARCHAR(100) NOT NULL,
  target_entity VARCHAR(255) NOT NULL,
  confidence FLOAT DEFAULT 0.0,
  document_ids INTEGER[] DEFAULT '{}',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_relationships_source ON relationships(source_entity);
CREATE INDEX idx_relationships_target ON relationships(target_entity);
CREATE INDEX idx_relationships_type ON relationships(relationship_type);
```

## 🔗 Relationships

### Entity Relationship Diagram

```
users
  ├─── documents (1:N)
  │      └─── document_chunks (1:N)
  ├─── folders (1:N)
  ├─── thought_nuggets (1:N)
  ├─── brain_messages (1:N)
  ├─── brain_genetic_profiles (1:1)
  ├─── meeting_bots (1:N)
  ├─── podcasts (1:N)
  └─── projects (1:N)

podcasts
  └─── podcast_episodes (1:N)

folders
  ├─── documents (1:N)
  └─── folders (1:N) -- self-referential
```

## 🔍 Indexes

### Performance Indexes

**Foreign Key Indexes:**
- All foreign keys have corresponding indexes
- Improves JOIN performance
- Speeds up cascade operations

**Search Indexes:**
- `documents.status` - Filter by processing status
- `documents.created_at DESC` - Recent documents first
- `brain_messages.created_at DESC` - Conversation history
- `thought_nuggets.created_at DESC` - Recent sessions

**Vector Indexes (PostgreSQL):**
```sql
CREATE INDEX idx_chunks_embedding 
ON document_chunks 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

**Full-Text Search (PostgreSQL):**
```sql
CREATE INDEX idx_documents_fts 
ON documents 
USING GIN (to_tsvector('english', title || ' ' || COALESCE(metadata->>'description', '')));
```

## 📊 Data Types

### JSONB Fields

**Advantages:**
- Flexible schema
- Query support
- Index support
- Efficient storage

**Common Uses:**
- `metadata` - Additional properties
- `speakers` - Complex nested data
- `citations` - References with scores
- `traits` - Numerical mappings

**Query Examples:**
```sql
-- Query JSONB field
SELECT * FROM documents WHERE metadata->>'type' = 'research';

-- Update JSONB field
UPDATE documents SET metadata = metadata || '{"reviewed": true}' WHERE id = 123;

-- Index JSONB field
CREATE INDEX idx_docs_type ON documents ((metadata->>'type'));
```

### Vector Type (PostgreSQL)

Used for semantic search embeddings.

```sql
-- Column definition
embedding VECTOR(768)

-- Cosine similarity search
SELECT * FROM document_chunks
ORDER BY embedding <=> query_embedding
LIMIT 10;

-- Dot product
SELECT * FROM document_chunks
ORDER BY embedding <#> query_embedding
LIMIT 10;
```

## 🔄 Migrations

### Schema Version Control

Migrations track database changes over time.

```sql
CREATE TABLE schema_migrations (
  version VARCHAR(50) PRIMARY KEY,
  applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Migration Example:**
```sql
-- migrations/001_add_projects.sql
BEGIN;

CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO schema_migrations (version) VALUES ('001');

COMMIT;
```

## 🛡️ Security Considerations

1. **Password Hashing**: Always use bcrypt with salt rounds ≥ 12
2. **Parameterized Queries**: Never concatenate user input
3. **Cascade Deletes**: Automatically clean up related data
4. **Row-Level Security**: Consider RLS for multi-tenant scenarios
5. **Audit Logging**: Track sensitive operations

## 📚 Next Steps

- **[Backend Documentation](./05_BACKEND.md)** - How to query database
- **[API Reference](./06_API_REFERENCE.md)** - API endpoints
- **[Data Flow](./08_DATA_FLOW.md)** - How data moves through system

---

**Key Takeaways:**
1. Schema supports both PostgreSQL and SQLite
2. JSONB for flexible metadata storage
3. Proper indexing for performance
4. Foreign keys enforce referential integrity
5. Cascade deletes for data cleanup
