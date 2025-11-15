# 🖥️ Desktop Application Documentation

Complete guide to the Electron-based desktop application features and architecture.

## 📋 Table of Contents
- [Overview](#overview)
- [Desktop Mode Features](#desktop-mode-features)
- [Architecture](#architecture)
- [Data Storage](#data-storage)
- [Building & Distribution](#building--distribution)
- [Configuration](#configuration)

## 🎯 Overview

DataBrew Lab includes a full-featured desktop application built with Electron, providing:
- **Complete Privacy**: All data stays on your local machine
- **Offline Operation**: Core features work without internet
- **No Cloud Costs**: Zero ongoing subscription fees
- **Cross-Platform**: Windows, macOS, and Linux support

## ✨ Desktop Mode Features

### Local Database (SQLite)
- Lightweight file-based database
- Automatic schema replication from PostgreSQL
- Full CRUD operations
- Transaction support
- No external database server needed

**Location:**
- Windows: `%APPDATA%\AnalystNexus\database.sqlite`
- macOS: `~/Library/Application Support/AnalystNexus/database.sqlite`
- Linux: `~/.config/analyst-nexus/database.sqlite`

### Local File Storage
- Documents stored in user data directory
- Automatic file deduplication
- Organized folder structure
- Efficient disk space usage

**Directory Structure:**
```
AnalystNexus/
├── database.sqlite       # SQLite database
├── documents/            # Uploaded documents
│   ├── pdf/
│   ├── docx/
│   └── txt/
├── audio/                # Audio recordings
├── transcripts/          # Saved transcripts
├── cache/                # Temporary files
└── logs/                 # Application logs
```

### Local Vector Search
- Custom vector similarity implementation
- Fast semantic search on local data
- Embedding storage in SQLite
- No external vector database required

### Filesystem Cache
- AI response caching
- Reduces API calls
- Faster subsequent queries
- Configurable size limits

### Offline Capabilities
- Upload and organize documents (offline)
- Search existing documents (offline)
- View transcripts and notes (offline)
- AI features require internet (API calls)

## 🏗️ Architecture

### Application Structure

```
Electron App
├── Main Process (Node.js)
│   ├── Window management
│   ├── IPC handlers
│   ├── File system access
│   └── Native APIs
│
├── Renderer Process (React)
│   ├── Frontend UI
│   ├── User interactions
│   └── IPC communication
│
└── Backend Server (Express)
    ├── REST API
    ├── SQLite database
    ├── Local storage
    └── AI services
```

### Process Communication

```
┌─────────────────────────────────────┐
│     Renderer (React Frontend)       │
│     Port: 5000                      │
└──────────────┬──────────────────────┘
               │ IPC / HTTP
               ↓
┌─────────────────────────────────────┐
│     Main Process (Electron)         │
│     - Window management             │
│     - File dialogs                  │
│     - System tray                   │
└──────────────┬──────────────────────┘
               │ Child Process
               ↓
┌─────────────────────────────────────┐
│     Backend Server (Express)        │
│     Port: 3001                      │
│     - API endpoints                 │
│     - SQLite database               │
│     - Local storage                 │
└─────────────────────────────────────┘
```

### Key Files

**Main Process:**
```
electron/
├── main.js              # Entry point
├── preload.js           # Secure IPC bridge
└── package.json         # Electron config
```

**Desktop Services:**
```
backend/src/
├── config/
│   └── desktop.ts       # Desktop config
├── services/
│   ├── desktopDatabase.ts    # SQLite wrapper
│   ├── desktopStorageService.ts  # File storage
│   ├── desktopConfigService.ts   # Settings
│   ├── desktopCache.ts           # Caching
│   └── desktopInitService.ts     # Initialization
```

## 💾 Data Storage

### SQLite Database

**Schema Replication:**
All PostgreSQL tables replicated for SQLite:

```sql
-- Documents table (same as PostgreSQL)
CREATE TABLE documents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  title TEXT,
  filename TEXT NOT NULL,
  file_path TEXT NOT NULL,
  mime_type TEXT,
  size_bytes INTEGER,
  status TEXT DEFAULT 'processing',
  metadata TEXT,  -- JSON as TEXT in SQLite
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Key Differences from PostgreSQL:**
- `SERIAL` → `INTEGER PRIMARY KEY AUTOINCREMENT`
- `JSONB` → `TEXT` (parsed as JSON in code)
- `TIMESTAMP` → `DATETIME`
- `VECTOR` → Custom blob storage

### Database Access

```typescript
// backend/src/services/desktopDatabase.ts
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

class DesktopDatabase {
  private db: any;
  
  async initialize() {
    const dbPath = this.getDatabasePath();
    
    this.db = await open({
      filename: dbPath,
      driver: sqlite3.Database
    });
    
    await this.createTables();
  }
  
  async run(sql: string, params: any[] = []) {
    return await this.db.run(sql, params);
  }
  
  async all(sql: string, params: any[] = []) {
    return await this.db.all(sql, params);
  }
  
  async get(sql: string, params: any[] = []) {
    return await this.db.get(sql, params);
  }
  
  async transaction(callback: (db: any) => Promise<void>) {
    await this.db.exec('BEGIN');
    try {
      await callback(this.db);
      await this.db.exec('COMMIT');
    } catch (error) {
      await this.db.exec('ROLLBACK');
      throw error;
    }
  }
}

export const desktopDb = new DesktopDatabase();
```

### File Storage

```typescript
// backend/src/services/desktopStorageService.ts
import path from 'path';
import fs from 'fs';
import { app } from 'electron';

class DesktopStorageService {
  private userDataPath: string;
  
  constructor() {
    this.userDataPath = app.getPath('userData');
  }
  
  getDocumentsPath(): string {
    return path.join(this.userDataPath, 'documents');
  }
  
  getAudioPath(): string {
    return path.join(this.userDataPath, 'audio');
  }
  
  getCachePath(): string {
    return path.join(this.userDataPath, 'cache');
  }
  
  saveFile(buffer: Buffer, relativePath: string): string {
    const fullPath = path.join(this.userDataPath, relativePath);
    fs.mkdirSync(path.dirname(fullPath), { recursive: true });
    fs.writeFileSync(fullPath, buffer);
    return fullPath;
  }
  
  readFile(relativePath: string): Buffer {
    const fullPath = path.join(this.userDataPath, relativePath);
    return fs.readFileSync(fullPath);
  }
  
  deleteFile(relativePath: string): void {
    const fullPath = path.join(this.userDataPath, relativePath);
    if (fs.existsSync(fullPath)) {
      fs.unlinkSync(fullPath);
    }
  }
  
  getDiskUsage(): { used: number, available: number } {
    // Implementation to calculate disk usage
  }
}

export const desktopStorage = new DesktopStorageService();
```

### Vector Storage (SQLite)

```sql
-- Store embeddings as binary blobs
CREATE TABLE document_embeddings (
  chunk_id INTEGER PRIMARY KEY,
  embedding BLOB NOT NULL
);

-- Index for faster lookups
CREATE INDEX idx_embeddings_chunk ON document_embeddings(chunk_id);
```

**Similarity Search:**
```typescript
async function vectorSearch(queryEmbedding: number[], limit: number) {
  // 1. Get all embeddings
  const rows = await desktopDb.all(
    'SELECT chunk_id, embedding FROM document_embeddings'
  );
  
  // 2. Calculate similarities
  const results = rows.map(row => ({
    chunkId: row.chunk_id,
    similarity: cosineSimilarity(
      queryEmbedding,
      bufferToArray(row.embedding)
    )
  }));
  
  // 3. Sort and limit
  return results
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, limit);
}

function cosineSimilarity(a: number[], b: number[]): number {
  const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
  const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
  const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
  return dotProduct / (magnitudeA * magnitudeB);
}
```

## 🔧 Configuration

### Desktop Settings

```typescript
// backend/src/services/desktopConfigService.ts
interface DesktopConfig {
  database: {
    path: string;
    backupEnabled: boolean;
    backupInterval: number; // hours
  };
  storage: {
    maxCacheSize: number; // bytes
    autoCleanup: boolean;
  };
  ai: {
    offlineMode: boolean;
    cacheResponses: boolean;
    cacheDuration: number; // seconds
  };
  sync: {
    enabled: boolean;
    cloudUrl?: string;
    interval: number; // minutes
  };
}

class DesktopConfigService {
  private config: DesktopConfig;
  private configPath: string;
  
  constructor() {
    this.configPath = path.join(app.getPath('userData'), 'config.json');
    this.loadConfig();
  }
  
  loadConfig() {
    if (fs.existsSync(this.configPath)) {
      this.config = JSON.parse(fs.readFileSync(this.configPath, 'utf8'));
    } else {
      this.config = this.getDefaultConfig();
      this.saveConfig();
    }
  }
  
  getDefaultConfig(): DesktopConfig {
    return {
      database: {
        path: 'database.sqlite',
        backupEnabled: true,
        backupInterval: 24
      },
      storage: {
        maxCacheSize: 1024 * 1024 * 1024, // 1GB
        autoCleanup: true
      },
      ai: {
        offlineMode: false,
        cacheResponses: true,
        cacheDuration: 300 // 5 minutes
      },
      sync: {
        enabled: false,
        interval: 30
      }
    };
  }
}
```

### Environment Variables

```env
# .env.desktop
NODE_ENV=desktop
DESKTOP_MODE=true
PORT=3001

# AI Services (still needed for AI features)
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Desktop Features
AI_CACHING=true
OFFLINE_MODE=true
VECTOR_SEARCH=true

# Optional
LOG_LEVEL=info
MAX_CACHE_SIZE=1GB
AUTO_BACKUP=true
```

## 📦 Building & Distribution

### Development Build

```bash
# Start in development mode
npm run electron:dev

# What happens:
# 1. Frontend starts on port 5000
# 2. Backend starts on port 3001  
# 3. Electron window opens
```

### Production Build

```bash
# Build everything
npm run build:desktop

# What happens:
# 1. Frontend builds to dist/
# 2. Backend compiles TypeScript
# 3. Electron builder packages app
```

### Platform-Specific Builds

```bash
# Windows
npm run dist:win
# Creates: dist/DataBrew-Setup-0.0.1.exe

# macOS
npm run dist:mac
# Creates: dist/DataBrew-0.0.1.dmg

# Linux
npm run dist:linux
# Creates: dist/DataBrew-0.0.1.AppImage
```

### electron-builder Configuration

```json
// electron-builder.json
{
  "appId": "com.databrew.analysta-nexus",
  "productName": "DataBrew Lab",
  "directories": {
    "output": "dist",
    "buildResources": "assets"
  },
  "files": [
    "electron/**/*",
    "dist/**/*",
    "backend/dist/**/*",
    "backend/node_modules/**/*"
  ],
  "win": {
    "target": ["nsis"],
    "icon": "assets/icon.ico"
  },
  "mac": {
    "target": ["dmg"],
    "icon": "assets/icon.icns",
    "category": "public.app-category.productivity"
  },
  "linux": {
    "target": ["AppImage", "deb"],
    "icon": "assets/icon.png",
    "category": "Office"
  }
}
```

## 🚀 Running Desktop Mode

### Start Backend in Desktop Mode

```bash
cd backend
npm run dev:desktop
```

**Initialization Steps:**
1. Load desktop environment variables
2. Initialize SQLite database
3. Create user data directories
4. Set up local file storage
5. Initialize vector search
6. Start Express server on port 3001

### Start Electron App

```bash
npm run electron:dev
```

**Window Configuration:**
```typescript
// electron/main.js
const mainWindow = new BrowserWindow({
  width: 1400,
  height: 900,
  webPreferences: {
    nodeIntegration: false,
    contextIsolation: true,
    preload: path.join(__dirname, 'preload.js')
  }
});

// Load frontend
mainWindow.loadURL('http://localhost:5000');
```

## 🔐 Security Considerations

### Secure IPC Communication

```typescript
// electron/preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
  // Expose safe APIs only
  selectFile: () => ipcRenderer.invoke('select-file'),
  saveFile: (data) => ipcRenderer.invoke('save-file', data),
  getAppPath: () => ipcRenderer.invoke('get-app-path')
});
```

### Data Protection
- All data stored locally
- No external database connections
- API keys stored securely in config
- File system permissions properly set

## 📊 Performance

### Optimization Strategies

1. **Database:**
   - Connection pooling
   - Prepared statements
   - Proper indexing
   - Vacuum on schedule

2. **File Storage:**
   - Deduplication
   - Compression
   - Lazy loading
   - Cache management

3. **Vector Search:**
   - Index optimization
   - Batch processing
   - Result caching
   - Parallel computation

## 🎯 Key Takeaways

1. **Complete Privacy**: All data stays local
2. **No Dependencies**: SQLite, no external DB
3. **Cross-Platform**: Windows, macOS, Linux
4. **Offline Capable**: Core features work offline
5. **Easy Distribution**: Single executable installer

## 📚 Next Steps

- **[Quick Start](./02_QUICK_START.md)** - Setup desktop mode
- **[Database Schema](./07_DATABASE_SCHEMA.md)** - SQLite schema
- **[Troubleshooting](./11_TROUBLESHOOTING.md)** - Desktop issues

---

**Desktop Mode Advantages:**
- ✅ Complete data privacy
- ✅ No ongoing cloud costs
- ✅ Works offline for core features
- ✅ Fast local operations
- ✅ Full control over data
