# 📖 DataBrew Lab - Complete Documentation Guide

Welcome to DataBrew Lab (Analyst Nexus Research Desktop)! This documentation is designed to help first-time users understand the entire codebase, architecture, and workflows.

## 🎯 What is DataBrew Lab?

DataBrew Lab is a **comprehensive research intelligence platform** that transforms raw data from interviews, calls, podcasts, and documents into actionable insights through AI-powered analysis and transcription.

Think of it as your **AI-powered research assistant** that can:
- 🎙️ Transcribe audio in real-time
- 📻 Process and analyze podcasts
- 🤖 Join video meetings as an AI agent
- 📊 Search and analyze your research data semantically
- 🧠 Have intelligent conversations about your research
- 📚 Organize and manage your research documents

## 🗺️ Documentation Navigation

This documentation is organized to guide you step-by-step:

### For First-Time Users:
1. **[START HERE](./00_START_HERE.md)** ← You are here
2. **[System Architecture Overview](./01_ARCHITECTURE_OVERVIEW.md)** - Understand how everything fits together
3. **[Quick Start Guide](./02_QUICK_START.md)** - Get up and running in minutes
4. **[Key Concepts](./03_KEY_CONCEPTS.md)** - Core concepts and terminology

### For Developers:
5. **[Frontend Documentation](./04_FRONTEND.md)** - React components, hooks, and structure
6. **[Backend Documentation](./05_BACKEND.md)** - API routes, services, and database
7. **[API Reference](./06_API_REFERENCE.md)** - Complete API endpoint documentation
8. **[Database Schema](./07_DATABASE_SCHEMA.md)** - Database tables and relationships

### For Advanced Users:
9. **[Data Flow & Workflows](./08_DATA_FLOW.md)** - How data moves through the system
10. **[AI Integration](./09_AI_INTEGRATION.md)** - AI models and vector search
11. **[Desktop Application](./10_DESKTOP_APP.md)** - Desktop-specific features
12. **[Troubleshooting](./11_TROUBLESHOOTING.md)** - Common issues and solutions

## 🚀 Quick Links

### I want to...
- **Understand the big picture** → [Architecture Overview](./01_ARCHITECTURE_OVERVIEW.md)
- **Start developing** → [Quick Start Guide](./02_QUICK_START.md)
- **Add a new API endpoint** → [Backend Documentation](./05_BACKEND.md#adding-new-endpoints)
- **Create a new component** → [Frontend Documentation](./04_FRONTEND.md#creating-components)
- **Understand how search works** → [Data Flow Documentation](./08_DATA_FLOW.md#search-workflow)
- **Fix a bug** → [Troubleshooting Guide](./11_TROUBLESHOOTING.md)

## 📊 Technology Stack at a Glance

```
┌─────────────────────────────────────────────┐
│           Frontend (Port 5000)              │
│  React 19 + TypeScript + Vite              │
│  Tailwind CSS + shadcn/ui                  │
└─────────────────────────────────────────────┘
                    ↕ HTTP/WebSocket
┌─────────────────────────────────────────────┐
│           Backend (Port 3001)               │
│  Node.js + Express + Socket.IO             │
│  PostgreSQL/SQLite + Redis                 │
└─────────────────────────────────────────────┘
                    ↕ API Calls
┌─────────────────────────────────────────────┐
│          AI Services                        │
│  Gemini 2.5-pro / OpenAI GPT-4             │
│  OpenAI Whisper (Transcription)            │
└─────────────────────────────────────────────┘
```

## 🎓 Learning Path

### Beginner (New to the project)
1. Read this page (START HERE)
2. Review [Architecture Overview](./01_ARCHITECTURE_OVERVIEW.md)
3. Follow [Quick Start Guide](./02_QUICK_START.md)
4. Understand [Key Concepts](./03_KEY_CONCEPTS.md)

### Intermediate (Ready to develop)
1. Study [Frontend Documentation](./04_FRONTEND.md)
2. Study [Backend Documentation](./05_BACKEND.md)
3. Review [API Reference](./06_API_REFERENCE.md)
4. Check [Database Schema](./07_DATABASE_SCHEMA.md)

### Advanced (System-level understanding)
1. Master [Data Flow & Workflows](./08_DATA_FLOW.md)
2. Deep dive into [AI Integration](./09_AI_INTEGRATION.md)
3. Explore [Desktop Application](./10_DESKTOP_APP.md)
4. Reference [Troubleshooting](./11_TROUBLESHOOTING.md)

## 🔑 Key Features Overview

### 1. 🎙️ Live Audio Transcription (Thought Nuggets)
Real-time speech-to-text using OpenAI Whisper with speaker identification and auto-save.

### 2. 📻 Podcast Intelligence
Multi-platform podcast processing with automatic transcription and AI-powered analysis.

### 3. 🤖 AI Meeting Agents
Intelligent bots that join video calls for real-time assistance, fact-checking, and insights.

### 4. 📊 Data Playground
Advanced analytics with hybrid search (BM25 + Vector), entity extraction, and visualization.

### 5. 🧠 Brain Discussion
Personalized AI conversations with cognitive profile integration and context awareness.

### 6. 📚 Repository Management
Organized document storage with intelligent categorization and semantic search.

### 7. 🖥️ Desktop Application
Full offline capability with local data storage using SQLite and Electron.

## 🏗️ Project Structure

```
DataBrew_Lab/
├── src/                    # Frontend React application
│   ├── components/         # UI components
│   ├── hooks/             # React hooks
│   └── lib/               # Utilities and API client
│
├── backend/               # Backend Node.js API
│   └── src/
│       ├── routes/        # API route definitions
│       ├── services/      # Business logic
│       ├── config/        # Configuration
│       └── models/        # Database models
│
├── docs/                  # Original documentation
├── readme/               # This comprehensive guide
├── electron/             # Desktop app configuration
└── testing/              # Test scripts and reports
```

## ⚙️ Deployment Modes

DataBrew Lab supports **three deployment modes**:

### 1. Cloud Mode (Production)
- Frontend and backend deployed on cloud platforms
- PostgreSQL database
- Redis for caching
- Best for: Teams and cloud-based workflows

### 2. Desktop Dev Mode (Development)
- Frontend: `localhost:5000`
- Backend: `localhost:3001`
- SQLite database
- Best for: Local development and testing

### 3. Desktop App Mode (Electron)
- Packaged desktop application
- Offline-first architecture
- Local data storage
- Best for: Privacy-focused users and offline work

## 🎯 Core Principles

### 1. **Architecture-First Thinking**
Understand the system architecture before making changes. Always review the architecture documentation first.

### 2. **API Client Pattern**
All backend API calls MUST use the centralized API client from `/src/lib/api.ts` to support multiple deployment modes.

### 3. **Dual-Mode Support**
Code works in both desktop (SQLite) and cloud (PostgreSQL) modes through abstraction layers.

### 4. **Service Layer Pattern**
Business logic is separated from route handlers for maintainability and testability.

## 📝 Important Files to Know

| File | Purpose | When to Use |
|------|---------|-------------|
| `/src/lib/api.ts` | Centralized API client | Making backend API calls |
| `/backend/src/index.ts` | Backend entry point | Understanding server setup |
| `/src/App.tsx` | Frontend root component | Understanding UI structure |
| `/backend/src/routes/` | API endpoint definitions | Adding/modifying APIs |
| `/backend/src/services/` | Business logic | Implementing features |
| `.env.example` | Environment variables | Configuration setup |
| `package.json` | Dependencies and scripts | Running commands |

## 🚦 Getting Started Commands

```bash
# Install dependencies
npm install
cd backend && npm install && cd ..

# Start development (Desktop Dev Mode)
# Terminal 1: Backend
cd backend && npm run dev:desktop

# Terminal 2: Frontend
npm run dev

# Run tests
npm test
cd backend && npm test

# Build for production
npm run build
cd backend && npm run build
```

## 🆘 Need Help?

- **Architecture questions**: See [Architecture Overview](./01_ARCHITECTURE_OVERVIEW.md)
- **Setup issues**: Check [Quick Start Guide](./02_QUICK_START.md)
- **API questions**: Review [API Reference](./06_API_REFERENCE.md)
- **Bugs**: Consult [Troubleshooting Guide](./11_TROUBLESHOOTING.md)
- **Contributing**: Read `/CONTRIBUTING.md` in the root directory

## 📚 Additional Resources

- **Main README**: `/README.md` - Project overview
- **Developer Guide**: `/docs/DEVELOPER_GUIDE.md` - Detailed development guide
- **Agent Guide**: `/agent.md` - AI agent development instructions
- **Architecture Docs**: `/docs/architecture/` - Deep dive into architecture
- **API Documentation**: Available at `http://localhost:3001/api/v1/docs` when running

## 🎉 Ready to Dive In?

Now that you have an overview, proceed to:

👉 **[Architecture Overview](./01_ARCHITECTURE_OVERVIEW.md)** - Understand how everything works together

Or jump directly to:

👉 **[Quick Start Guide](./02_QUICK_START.md)** - Start developing immediately

---

**Last Updated**: January 2025  
**Documentation Version**: 1.0  
**Project Version**: 0.01

*This documentation is maintained to help developers understand and contribute to DataBrew Lab. If you find any errors or have suggestions, please contribute!*
