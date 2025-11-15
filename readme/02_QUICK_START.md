# 🚀 Quick Start Guide

Get DataBrew Lab up and running on your machine in minutes! This guide covers installation, configuration, and your first run.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [First-Time Setup](#first-time-setup)
- [Verification](#verification)
- [Common Issues](#common-issues)

## ✅ Prerequisites

Before you begin, ensure you have:

### Required Software
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **npm** or **yarn** - Comes with Node.js
- **Git** - [Download here](https://git-scm.com/)

### Required API Keys
- **OpenAI API Key** (for AI features and transcription)
  - Sign up at [OpenAI Platform](https://platform.openai.com/)
  - Create an API key in your account settings
  
OR

- **Gemini API Key** (alternative AI provider)
  - Sign up at [Google AI Studio](https://makersuite.google.com/app/apikey)
  - Generate an API key

### Optional (for Cloud Mode)
- **PostgreSQL database** (if not using desktop/SQLite mode)
- **Redis server** (for caching in cloud mode)

### Check Your Setup

```bash
# Verify Node.js installation
node --version
# Should output: v18.x.x or higher

# Verify npm installation
npm --version
# Should output: 9.x.x or higher

# Verify Git installation
git --version
# Should output: git version 2.x.x
```

## 📥 Installation Steps

### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yb235/DataBrew_Lab.git

# Navigate to the project directory
cd DataBrew_Lab
```

### 2. Install Frontend Dependencies

```bash
# Install root/frontend dependencies
npm install

# This will install:
# - React and related libraries
# - UI components (shadcn/ui)
# - Build tools (Vite)
# - And more...
```

### 3. Install Backend Dependencies

```bash
# Navigate to backend directory
cd backend

# Install backend dependencies
npm install

# This will install:
# - Express and middleware
# - Database clients
# - AI service SDKs
# - And more...

# Return to root directory
cd ..
```

## ⚙️ Configuration

### Choose Your Mode

DataBrew Lab supports two main modes:

1. **Desktop Dev Mode** (Recommended for development)
   - SQLite database (no external database needed)
   - Local file storage
   - Best for: Getting started, local development

2. **Cloud Mode**
   - PostgreSQL database required
   - Redis for caching
   - Best for: Production deployment, team collaboration

### Desktop Dev Mode Setup (Recommended)

**Step 1: Create Environment File**

```bash
# Copy the desktop environment template
cp .env.desktop.example .env.desktop
```

**Step 2: Edit `.env.desktop`**

```bash
# Open with your preferred editor
nano .env.desktop
# or
code .env.desktop
# or
vim .env.desktop
```

**Step 3: Configure Required Settings**

```env
# Desktop Mode Configuration
NODE_ENV=desktop
DESKTOP_MODE=true
PORT=3001

# ⚠️ REQUIRED: Add your AI API key
# Option 1: Gemini (Recommended)
GEMINI_API_KEY=your_gemini_api_key_here

# Option 2: OpenAI (Alternative)
OPENAI_API_KEY=sk-your-openai-key-here

# Features (Keep these for desktop mode)
AI_CACHING=true
OFFLINE_MODE=true
VECTOR_SEARCH=true
```

### Cloud Mode Setup (Advanced)

**Step 1: Create Environment File**

```bash
# Copy the environment template
cp .env.example .env
```

**Step 2: Edit `.env`**

```bash
# Open with your preferred editor
nano .env
```

**Step 3: Configure All Settings**

```env
# Server Configuration
NODE_ENV=production
PORT=3001

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/databrew_lab

# Redis Configuration
REDIS_URL=redis://localhost:6379

# AI Services
OPENAI_API_KEY=sk-your-openai-key-here
GEMINI_API_KEY=your_gemini_api_key_here
AI_MODEL=gpt-4o

# Authentication
JWT_SECRET=your-secret-key-here-change-in-production

# Features
AI_CACHING=true
LOG_LEVEL=info
```

**Step 4: Set Up Database**

```bash
# Create PostgreSQL database
createdb databrew_lab

# Run schema (from backend directory)
cd backend
psql databrew_lab < src/models/schema.sql
cd ..
```

## 🏃 Running the Application

### Desktop Dev Mode (3 Terminal Windows)

**Terminal 1: Start Backend**

```bash
cd backend
npm run dev:desktop
```

You should see:
```
🚀 Desktop backend server running on port 3001
✅ Desktop mode initialized
✅ SQLite database initialized
✅ Local vector search ready
```

**Terminal 2: Start Frontend**

```bash
# From root directory
npm run dev
```

You should see:
```
  VITE v6.3.5  ready in 523 ms

  ➜  Local:   http://localhost:5000/
  ➜  Network: use --host to expose
```

**Terminal 3: Start Electron (Optional)**

```bash
# From root directory
npm run electron:dev
```

This opens the desktop application window.

### Cloud Mode (2 Terminal Windows)

**Terminal 1: Start Backend**

```bash
cd backend
npm run dev:cloud
```

**Terminal 2: Start Frontend**

```bash
npm run dev
```

### Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:5000
- **Backend Health Check**: http://localhost:3001/health
- **API Documentation**: http://localhost:3001/api/v1/docs

## 🎯 First-Time Setup

### 1. Verify Backend Connection

The backend should start successfully. Check the logs for:

```
✅ Server initialized successfully
✅ Database connected
✅ Socket.IO server ready
🚀 Server running on port 3001
```

### 2. Verify Frontend Connection

The frontend should display the main interface with:
- Sidebar navigation (left)
- Main content area (center)
- Status indicators (if any connection issues)

### 3. Test Basic Features

**a) Check Database Status**

1. Look for database connection indicator
2. Should show "Connected" status

**b) Upload a Test Document**

1. Navigate to "Data Ingestion" or "Repository"
2. Click "Upload" button
3. Select a text file or PDF
4. Verify successful upload

**c) Test AI Features**

1. Navigate to "Brain Discussion"
2. Type a simple question
3. Verify AI response

## ✅ Verification Checklist

Run through this checklist to ensure everything is working:

- [ ] Backend starts without errors
- [ ] Frontend loads successfully at localhost:5000
- [ ] No console errors in browser developer tools
- [ ] Database connection successful
- [ ] Can navigate between sections in sidebar
- [ ] Can upload a test file
- [ ] AI chat responds to messages
- [ ] WebSocket connection established (check Network tab)

## 🐛 Common Issues

### Issue: "Cannot find module" errors

**Solution**:
```bash
# Delete node_modules and reinstall
rm -rf node_modules
npm install

# Do the same for backend
cd backend
rm -rf node_modules
npm install
cd ..
```

### Issue: Port already in use

**Error**: `EADDRINUSE: address already in use :::3001`

**Solution**:
```bash
# Find and kill process on port 3001
# On Linux/Mac:
lsof -ti:3001 | xargs kill -9

# On Windows:
netstat -ano | findstr :3001
taskkill /PID <PID> /F

# Or change the port in .env.desktop:
PORT=3002
```

### Issue: "OPENAI_API_KEY not found"

**Solution**:
1. Verify `.env.desktop` file exists in root directory
2. Check that `GEMINI_API_KEY` or `OPENAI_API_KEY` is set
3. Restart backend server after adding key

### Issue: "Failed to connect to database"

**Desktop Mode Solution**:
- SQLite should create database automatically
- Check file permissions in user data directory
- Look for database at:
  - Windows: `%APPDATA%\AnalystNexus\database.sqlite`
  - Mac: `~/Library/Application Support/AnalystNexus/database.sqlite`
  - Linux: `~/.config/analyst-nexus/database.sqlite`

**Cloud Mode Solution**:
```bash
# Verify PostgreSQL is running
pg_isready

# Check DATABASE_URL in .env
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT version();"
```

### Issue: Frontend can't connect to backend

**Solution**:
1. Verify backend is running on port 3001
2. Check CORS settings in `backend/src/index.ts`
3. Verify `VITE_API_URL` in frontend (if set)
4. Check browser console for specific error messages

### Issue: Build fails with TypeScript errors

**Solution**:
```bash
# Update TypeScript dependencies
npm update typescript

# In backend
cd backend
npm update typescript
cd ..

# Clear TypeScript cache
rm -rf node_modules/.cache
```

## 📁 Where Data is Stored

### Desktop Mode
- **Database**: `%APPDATA%\AnalystNexus\database.sqlite` (Windows)
- **Documents**: `%APPDATA%\AnalystNexus\documents\`
- **Cache**: `%APPDATA%\AnalystNexus\cache\`
- **Logs**: `%APPDATA%\AnalystNexus\logs\`

### Cloud Mode
- **Database**: PostgreSQL server specified in `DATABASE_URL`
- **Documents**: Local `backend/uploads/` or cloud storage
- **Cache**: Redis server specified in `REDIS_URL`
- **Logs**: `backend/logs/` directory

## 🛠️ Development Commands

### Useful NPM Scripts

**Frontend**:
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run linter
npm test             # Run tests
```

**Backend**:
```bash
npm run dev:desktop  # Desktop mode development
npm run dev:cloud    # Cloud mode development
npm run build        # Build TypeScript
npm run start        # Run built version
npm test             # Run tests
npm run lint         # Run linter
```

**Desktop App**:
```bash
npm run electron:dev     # Run Electron in development
npm run build:desktop    # Build desktop app
npm run dist:win         # Create Windows installer
npm run dist:mac         # Create macOS installer
npm run dist:linux       # Create Linux installer
```

## 🧪 Running Tests

### Frontend Tests
```bash
npm test
```

### Backend Tests
```bash
cd backend
npm test
```

### Integration Tests
```bash
npm run e2e
```

## 📊 Monitoring Your Application

### View Logs

**Backend Logs**:
```bash
# In backend terminal, logs appear automatically
# Or view log files:
cat backend/logs/app.log
```

**Frontend Logs**:
- Open browser Developer Tools (F12)
- Check Console tab for messages

### Health Checks

```bash
# Backend health
curl http://localhost:3001/health

# Desktop info (desktop mode)
curl http://localhost:3001/desktop/info

# API documentation
curl http://localhost:3001/api/v1/docs
```

## 🎓 Next Steps

Now that you have DataBrew Lab running:

1. **Learn Key Concepts**: [Key Concepts Guide](./03_KEY_CONCEPTS.md)
2. **Explore Features**: Try each section in the sidebar
3. **Read API Docs**: [API Reference](./06_API_REFERENCE.md)
4. **Understand Data Flow**: [Data Flow Documentation](./08_DATA_FLOW.md)

## 💡 Tips for Development

1. **Use Desktop Dev Mode** for faster iteration (no external dependencies)
2. **Keep 3 terminals open** (backend, frontend, and one for commands)
3. **Watch backend logs** to understand what's happening
4. **Use browser DevTools** to debug frontend issues
5. **Check the API documentation** at `/api/v1/docs` when backend is running
6. **Read error messages carefully** - they usually point to the solution

## 🆘 Getting Help

If you're still stuck:

1. **Check troubleshooting guide**: [Troubleshooting](./11_TROUBLESHOOTING.md)
2. **Review architecture docs**: [Architecture Overview](./01_ARCHITECTURE_OVERVIEW.md)
3. **Check GitHub issues**: Look for similar problems
4. **Ask for help**: Create a new GitHub issue with:
   - Your environment (OS, Node version)
   - Steps to reproduce
   - Error messages
   - Logs from backend

---

**Congratulations! You should now have DataBrew Lab running on your machine! 🎉**

Next: **[Learn Key Concepts →](./03_KEY_CONCEPTS.md)**
