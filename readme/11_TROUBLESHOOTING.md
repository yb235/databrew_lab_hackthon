# 🔧 Troubleshooting Guide

Solutions to common problems when working with DataBrew Lab.

## 📋 Table of Contents
- [Installation & Setup](#installation--setup)
- [Backend Issues](#backend-issues)
- [Frontend Issues](#frontend-issues)
- [Database Problems](#database-problems)
- [API & Network Issues](#api--network-issues)
- [Desktop Mode Issues](#desktop-mode-issues)
- [AI Service Issues](#ai-service-issues)
- [Performance Issues](#performance-issues)

## 🔧 Installation & Setup

### "Cannot find module" errors

**Problem**: Missing dependencies after cloning.

**Solution**:
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install

# Also clean backend
cd backend
rm -rf node_modules package-lock.json
npm install
cd ..
```

### "EACCES: permission denied"

**Problem**: Insufficient permissions for npm install.

**Solution**:
```bash
# Don't use sudo! Fix npm permissions instead
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### Version conflicts

**Problem**: "Peer dependency not satisfied" warnings.

**Solution**:
```bash
# Use specific npm version
npm install --legacy-peer-deps

# Or update to latest compatible versions
npm update
```

## 🖥️ Backend Issues

### Port already in use

**Error**: `EADDRINUSE: address already in use :::3001`

**Solution**:
```bash
# Find process on port 3001
# Linux/Mac:
lsof -ti:3001 | xargs kill -9

# Windows:
netstat -ano | findstr :3001
taskkill /PID <PID_NUMBER> /F

# Or use different port
# In .env.desktop:
PORT=3002
```

### "OPENAI_API_KEY not found"

**Error**: AI features not working.

**Solution**:
```bash
# 1. Check .env.desktop exists
ls -la .env.desktop

# 2. Verify key is set
cat .env.desktop | grep API_KEY

# 3. Add key if missing
echo "GEMINI_API_KEY=your_key_here" >> .env.desktop
# OR
echo "OPENAI_API_KEY=sk-your_key_here" >> .env.desktop

# 4. Restart backend
cd backend
npm run dev:desktop
```

### Backend won't start

**Error**: Various startup errors.

**Diagnostic steps**:
```bash
# Check Node version
node --version
# Should be 18+

# Check environment
cd backend
cat .env.desktop

# Check logs
npm run dev:desktop 2>&1 | tee backend.log

# Common issues:
# - Missing API keys
# - Wrong NODE_ENV
# - Database connection issues
# - Port conflicts
```

## 💻 Frontend Issues

### "Failed to fetch" errors

**Problem**: Frontend can't connect to backend.

**Solution**:
```bash
# 1. Verify backend is running
curl http://localhost:3001/health

# 2. Check API_BASE_URL in frontend
# src/lib/api.ts should have:
export const API_BASE_URL = 'http://localhost:3001/api/v1';

# 3. Check CORS settings
# backend/src/index.ts should include localhost:5000 in allowedOrigins

# 4. Clear browser cache
# Open DevTools → Network → Disable cache
```

### White screen / blank page

**Problem**: Frontend loads but shows nothing.

**Solution**:
```typescript
// 1. Check browser console (F12)
// Look for JavaScript errors

// 2. Check if Vite server is running
npm run dev
// Should show: Local: http://localhost:5000

// 3. Clear browser cache and reload
Ctrl + Shift + R (Windows/Linux)
Cmd + Shift + R (Mac)

// 4. Check for build errors
npm run build
```

### Hot reload not working

**Problem**: Changes don't reflect in browser.

**Solution**:
```bash
# 1. Restart Vite dev server
Ctrl + C
npm run dev

# 2. Check file watchers limit (Linux)
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# 3. Hard reload browser
Ctrl + Shift + R
```

## 🗄️ Database Problems

### "Database connection failed"

**Cloud Mode**:
```bash
# Check PostgreSQL is running
pg_isready

# Verify DATABASE_URL
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Common issues:
# - PostgreSQL not running
# - Wrong credentials
# - Firewall blocking connection
# - Database doesn't exist
```

**Desktop Mode**:
```bash
# Check SQLite database path
# Windows: %APPDATA%\AnalystNexus\database.sqlite
# Mac: ~/Library/Application Support/AnalystNexus/database.sqlite
# Linux: ~/.config/analyst-nexus/database.sqlite

# Verify file exists
ls -l <database_path>

# Test SQLite
sqlite3 <database_path> ".tables"

# If corrupted, delete and restart
rm <database_path>
# Backend will recreate it
```

### "Table does not exist"

**Problem**: Missing database tables.

**Solution**:
```sql
-- Cloud mode: Run schema
cd backend
psql databrew_lab < src/models/schema.sql

-- Desktop mode: Delete database
# It will be auto-created with all tables
rm ~/.config/analyst-nexus/database.sqlite
# Restart backend
```

### Migration errors

**Problem**: Schema version conflicts.

**Solution**:
```sql
-- Check current version
SELECT * FROM schema_migrations;

-- Manually run missing migrations
-- backend/src/models/migrations/XXX_migration.sql

-- Or reset database (CAUTION: data loss!)
DROP DATABASE databrew_lab;
CREATE DATABASE databrew_lab;
-- Run schema again
```

## 🌐 API & Network Issues

### 401 Unauthorized

**Problem**: Token invalid or missing.

**Solution**:
```typescript
// 1. Check if token exists
console.log(localStorage.getItem('auth_token'));

// 2. Login again to get fresh token
POST /api/v1/auth/login

// 3. Verify token in requests
// Should have header:
Authorization: Bearer <token>

// 4. Check token expiration
// JWT tokens expire (default: 24h)
```

### 429 Rate Limit Exceeded

**Problem**: Too many requests.

**Solution**:
```typescript
// Wait before retrying
await new Promise(resolve => setTimeout(resolve, 60000)); // 1 minute

// Implement exponential backoff
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 429 && i < maxRetries - 1) {
        await new Promise(resolve => 
          setTimeout(resolve, Math.pow(2, i) * 1000)
        );
      } else {
        throw error;
      }
    }
  }
}
```

### CORS errors

**Problem**: Cross-origin requests blocked.

**Solution**:
```typescript
// backend/src/index.ts
const allowedOrigins = [
  'http://localhost:5000',
  'http://localhost:5001',
  'http://localhost:5173',
  // Add your domain
];

app.use(cors({
  origin: allowedOrigins,
  credentials: true
}));
```

## 🖥️ Desktop Mode Issues

### Database file not found

**Problem**: Can't locate SQLite database.

**Solution**:
```bash
# Print user data path
node -e "console.log(require('electron').app.getPath('userData'))"

# Manually create directory
mkdir -p "$HOME/Library/Application Support/AnalystNexus"  # Mac
mkdir -p "$HOME/.config/analyst-nexus"  # Linux
mkdir "%APPDATA%\AnalystNexus"  # Windows

# Restart app
```

### File upload fails

**Problem**: Can't save uploaded files.

**Solution**:
```bash
# Check permissions
ls -ld ~/.config/analyst-nexus

# Should be: drwxr-xr-x (755)
chmod 755 ~/.config/analyst-nexus

# Check disk space
df -h

# Check file size limits
# Max: 50MB per file
```

### Electron app won't start

**Problem**: Desktop app fails to launch.

**Solution**:
```bash
# Check Electron is installed
cd electron
npm list electron

# Reinstall Electron
npm install electron --save-dev

# Check for conflicting processes
ps aux | grep electron
kill <PID>

# Clear Electron cache
rm -rf ~/Library/Application Support/DataBrew Lab  # Mac
rm -rf ~/.config/DataBrew Lab  # Linux
rd /s "%APPDATA%\DataBrew Lab"  # Windows
```

## 🤖 AI Service Issues

### "API key invalid"

**Problem**: AI services return 401 errors.

**Solution**:
```bash
# Verify key is correct
echo $GEMINI_API_KEY
echo $OPENAI_API_KEY

# Test key directly
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# Regenerate key if needed
# OpenAI: https://platform.openai.com/api-keys
# Gemini: https://makersuite.google.com/app/apikey
```

### Transcription fails

**Problem**: Whisper API errors.

**Solution**:
```bash
# Check audio format
# Supported: mp3, mp4, mpeg, mpga, m4a, wav, webm

# Check file size
# Max: 25MB

# Check audio quality
# Recommended: 16kHz sample rate, mono

# Test with small file first
```

### Slow AI responses

**Problem**: Long wait times for AI.

**Solution**:
```typescript
// Enable caching
AI_CACHING=true

// Reduce max tokens
const response = await aiService.generateCompletion(prompt, {
  maxTokens: 500  // Instead of 2000
});

// Use faster models
AI_MODEL=gemini-2.0-flash-exp  // Instead of gemini-2.5-pro

// Batch requests
const results = await Promise.all(
  prompts.map(p => aiService.generateCompletion(p))
);
```

### Embedding generation fails

**Problem**: Vector search not working.

**Solution**:
```typescript
// Check embedding dimensions
// Should be 768 for most models

// Verify embeddings are saved
const chunks = await query(
  'SELECT COUNT(*) FROM document_chunks WHERE embedding IS NOT NULL'
);

// Regenerate if needed
for (const chunk of allChunks) {
  const embedding = await aiService.generateEmbedding(chunk.content);
  await saveEmbedding(chunk.id, embedding);
}
```

## ⚡ Performance Issues

### Slow search

**Problem**: Search takes too long.

**Solution**:
```sql
-- Add indexes
CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_chunks_document_id ON document_chunks(document_id);

-- For PostgreSQL with pgvector
CREATE INDEX idx_embedding ON document_chunks 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Limit results
SELECT * FROM documents LIMIT 10;

-- Use pagination
SELECT * FROM documents LIMIT 10 OFFSET 20;
```

### High memory usage

**Problem**: Application using too much RAM.

**Solution**:
```typescript
// Limit concurrent operations
const BATCH_SIZE = 10;
for (let i = 0; i < items.length; i += BATCH_SIZE) {
  const batch = items.slice(i, i + BATCH_SIZE);
  await Promise.all(batch.map(processItem));
}

// Clear cache periodically
setInterval(() => {
  cache.clear();
}, 30 * 60 * 1000); // Every 30 minutes

// Use streams for large files
const stream = fs.createReadStream(filePath);
stream.pipe(processor);
```

### Slow document upload

**Problem**: File processing takes too long.

**Solution**:
```typescript
// Process in background
queue.add('process-document', { documentId });

// Chunk in parallel
const chunks = await chunkingService.chunk(text);
await Promise.all(chunks.map(async (chunk) => {
  const embedding = await generateEmbedding(chunk.content);
  await saveChunk(chunk, embedding);
}));

// Show progress
socket.emit('upload-progress', { 
  documentId, 
  progress: Math.round((processed / total) * 100) 
});
```

## 🔍 Debugging Tips

### Enable Debug Logging

```bash
# Backend
LOG_LEVEL=debug npm run dev:desktop

# Frontend
// In browser console
localStorage.setItem('debug', '*');
```

### Check Logs

```bash
# Backend logs
tail -f backend/logs/app.log

# Desktop app logs
# Mac: ~/Library/Logs/DataBrew Lab/
# Linux: ~/.config/DataBrew Lab/logs/
# Windows: %APPDATA%\DataBrew Lab\logs\
```

### Network Debugging

```bash
# Monitor API calls
# Chrome DevTools → Network tab
# Filter by "XHR" or "Fetch"

# Check WebSocket connection
# Look for "ws://" connections
# Status should be 101 Switching Protocols
```

## 🆘 Getting More Help

### Information to Include

When asking for help, provide:

1. **Environment**:
   - OS and version
   - Node.js version (`node --version`)
   - npm version (`npm --version`)
   
2. **Mode**:
   - Desktop or cloud
   - Development or production
   
3. **Error Messages**:
   - Full error text
   - Stack traces
   - Console logs
   
4. **Steps to Reproduce**:
   - What you did
   - What you expected
   - What actually happened
   
5. **Logs**:
   - Backend logs
   - Browser console
   - Network activity

### Where to Get Help

- **GitHub Issues**: [Create an issue](https://github.com/yb235/DataBrew_Lab/issues)
- **Documentation**: Check other docs in `/readme`
- **Architecture Docs**: See `/docs/architecture`

## 🎯 Quick Fixes Checklist

Before asking for help, try:

- [ ] Restart backend server
- [ ] Clear browser cache and reload
- [ ] Check all environment variables are set
- [ ] Verify API keys are valid
- [ ] Check database connection
- [ ] Look at error messages carefully
- [ ] Search existing GitHub issues
- [ ] Check logs for details

---

**Remember**: Most issues are configuration-related. Double-check your `.env.desktop` file and verify all services are running!
