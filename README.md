# Emotion Interpretation Machine

**AI Agent System for Analyzing Conversations through Emotion Detection and Transcription**

![Status](https://img.shields.io/badge/status-phase_3_complete-green)
![Phase](https://img.shields.io/badge/phase-3_of_4_complete-blue)
![Tests](https://img.shields.io/badge/tests-38_passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen)

## 📖 Overview

The Emotion Interpretation Machine is an AI agent system that combines emotion detection data with speech transcription to provide deep insights about conversations, interviews, and interactions. By matching temporal emotion signals with spoken content, the system reveals hidden meanings, deception, underlying feelings, and relationship dynamics.

## 🎯 Key Features

- **Temporal Alignment**: Window-based matching of emotions with transcription segments (±100ms tolerance)
- **Pattern Analysis**: Identifies dominant emotions, transitions, and emotional consistency
- **Anomaly Detection**: Flags unexpected emotional responses and incongruities
- **Critical Moments**: Highlights key moments where emotions and content diverge
- **Speaker Profiling**: Creates emotional baseline profiles for each speaker
- **Interpretation Reports**: Generates structured analysis with evidence-based insights
- **Multi-Format Reports**: Download reports in JSON (structured) or Markdown (readable) formats
- **REST API**: Complete API for data upload, analysis, and report generation
- **LangSmith Integration**: Full observability and tracing for all agent operations

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Git

### Option 1: Standard Installation

```bash
# Clone repository
git clone https://github.com/yb235/emotion-interpretation-machine.git
cd emotion-interpretation-machine

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys (optional for basic functionality)
```

### Option 2: One-Command Deployment

```bash
# Use the deployment script
./deploy.sh
```

This interactive script will:
- Check prerequisites
- Set up virtual environment
- Install dependencies
- Run tests
- Choose deployment type (dev/systemd/Docker)

### Option 3: Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t emotion-interpreter:latest .
docker run -d -p 3001:3001 -v $(pwd)/data:/app/data emotion-interpreter:latest
```

### Running the Server

```bash
# Start FastAPI server
python src/main.py

# Server will run on http://localhost:3001
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

## 📊 API Endpoints

### Sessions
- `POST /api/sessions` - Create a new analysis session
- `GET /api/sessions/:id` - Get session details
- `GET /api/sessions` - List all sessions
- `GET /api/sessions/:id/status` - Get session status with data counts

### Data Upload
- `POST /api/sessions/:id/transcription` - Upload transcription data
- `POST /api/sessions/:id/emotions` - Upload emotion detection data

### Analysis
- `POST /api/sessions/:id/align` - Perform temporal alignment
- `GET /api/sessions/:id/aligned-events` - Get aligned events
- `POST /api/sessions/:id/analyze` - Run AI agent analysis
- `GET /api/sessions/:id/report` - Get interpretation report (JSON)
- `GET /api/sessions/:id/report.json` - Download JSON report
- `GET /api/sessions/:id/report.md` - Download Markdown report

### Health
- `GET /health` - Health check endpoint

**📚 See [API Documentation](docs/API_DOCUMENTATION.md) for complete details**

## 🔬 Example Usage

```bash
# 1. Create a session
curl -X POST http://localhost:3001/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"name": "Holmes Interview"}'

# 2. Upload transcription data
curl -X POST http://localhost:3001/api/sessions/1/transcription \
  -H "Content-Type: application/json" \
  -d '{"entries": [...]}'

# 3. Upload emotion data
curl -X POST http://localhost:3001/api/sessions/1/emotions \
  -H "Content-Type: application/json" \
  -d '{"detections": [...]}'

# 4. Run analysis
curl -X POST http://localhost:3001/api/sessions/1/analyze

# 5. Download report
curl http://localhost:3001/api/sessions/1/report.json -o report.json
curl http://localhost:3001/api/sessions/1/report.md -o report.md
```

**📚 See [User Guide](docs/USER_GUIDE.md) for detailed examples**

## 🧪 Test Examples

The repository includes 5 example scenarios in the `examples/` directory:

1. **Holmes Interview** - Deception detection (01:01 critical moment)
2. **20-Minute Lie** - Extended lie detection
3. **Double Agent** - Internal conflict analysis
4. **Love Story** - Relationship dynamics
5. **Office Lovers** - Hidden affection

## 🏗️ Architecture

### Phase 1: Foundation + Alignment ✅
- SQLite database with 5 models
- FastAPI REST API with 13 endpoints
- Temporal alignment algorithm (±100ms window)
- Pydantic validation
- Comprehensive testing (24 tests)

### Phase 2: Agent + Observability ✅
- LangGraph agent with 6 nodes:
  1. Temporal Alignment
  2. Pattern Analysis
  3. Anomaly Detection
  4. Moment Interpretation
  5. Speaker Profiling
  6. Report Synthesis
- LangSmith tracing configuration (requires API keys)
- Holistic AI Bedrock integration ready

### Phase 3: Reports + Testing ✅
- JSON and Markdown report generation
- Complete end-to-end testing (38 tests total)
- 92% test coverage
- Performance validation (<5s alignment)

### Phase 4: Polish + Deploy (In Progress)
- Comprehensive documentation
- Docker deployment support
- Deployment script
- Production-ready configuration

## 📈 Implementation Status

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 1: Foundation + Alignment | ✅ Complete | 100% |
| Phase 2: Agent + Observability | ✅ Complete | 100% |
| Phase 3: Reports + Testing | ✅ Complete | 100% |
| Phase 4: Polish + Deploy | 🟡 In Progress | 75% |

**Overall Progress**: 93% (3.75/4 phases)

## 🧬 Project Structure

```
emotion-interpretation-machine/
├── src/                      # Source code
│   ├── main.py              # FastAPI application
│   ├── core/                # Core logic
│   │   ├── alignment/       # Temporal alignment
│   │   ├── agent/           # LangGraph agent
│   │   └── reports/         # Report generation
│   ├── models/              # Database models & schemas
│   └── utils/               # Utilities
├── tests/                   # Test suite
│   ├── unit/               # Unit tests (30)
│   ├── integration/        # Integration tests (7)
│   └── e2e/                # End-to-end tests (8)
├── examples/               # Example data files
├── docs/                   # Technical documentation
│   ├── API_DOCUMENTATION.md
│   ├── DEPLOYMENT_GUIDE.md
│   └── USER_GUIDE.md
├── project-management/     # Project management docs
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
└── deploy.sh               # Deployment script
```

## 🧪 Testing

- **Total Tests**: 38 (all passing ✅)
- **Unit Tests**: 30
- **Integration Tests**: 7
- **E2E Tests**: 8
- **Coverage**: 92% overall
- **Holmes 01:01 Verification**: ✅ Passed
- **Performance**: Alignment <5s ✅

## 📚 Documentation

### User Documentation
- **[User Guide](docs/USER_GUIDE.md)** - Complete usage guide with examples
- **[API Documentation](docs/API_DOCUMENTATION.md)** - Full API reference
- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Production deployment instructions

### Project Management
- [Project Planning](project-management/PROJECT_PLANNING.md) - Overview and timeline
- [Implementation Tracker](project-management/IMPLEMENTATION_TRACKER.md) - Detailed task tracking
- [Testing Strategy](project-management/TESTING_STRATEGY.md) - Testing approach
- [Development Setup](project-management/DEVELOPMENT_SETUP.md) - Setup guide

### Technical Documentation
- [Architecture](docs/03_ARCHITECTURE.md) - System architecture
- [Agent Design](docs/04_AGENT_DESIGN.md) - LangGraph agent details
- [Temporal Alignment](docs/05_TEMPORAL_ALIGNMENT.md) - Alignment algorithm
- [Observability](docs/06_OBSERVABILITY.md) - LangSmith integration

## 🔧 Technology Stack

- **AI Framework**: LangGraph, LangChain
- **LLM Provider**: Holistic AI Bedrock (Claude 3.5 Sonnet)
- **Observability**: LangSmith
- **Backend**: Python 3.10+, FastAPI
- **Database**: SQLite
- **Testing**: pytest, pytest-cov, pytest-asyncio
- **Containerization**: Docker, Docker Compose
- **Code Quality**: black, flake8, isort, mypy

## 🎓 Key Achievements

### Holmes Example Analysis
The agent successfully identifies the critical 01:01 moment in the Holmes interview:
- **Timestamp**: 61000-61500ms (01:01)
- **Speaker**: Lord Alistair
- **Statement**: "I... what? No. I haven't played in years."
- **Emotions Detected**: Surprise + Fear
- **Interpretation**: Unexpected emotional response indicating potential deception

### Speaker Profiling
- **Holmes**: Neutral baseline, 2 emotion types, consistent behavior
- **Lord Alistair**: High emotional variance (7 emotion types), suggesting internal conflict

## 🔐 Security

- ✅ CodeQL security scanning passed (0 alerts)
- ✅ No hardcoded credentials
- ✅ Environment variable configuration
- ✅ Input validation with Pydantic
- ✅ SQL injection protection via SQLAlchemy ORM

## 🤝 Contributing

This is a project implementation for the Holistic AI Hackathon - Track B (Glass Box).

## 📄 License

This project is part of the Holistic AI Hackathon.

## 🙏 Acknowledgments

- Holistic AI for Bedrock proxy access
- LangChain/LangGraph for agent framework
- LangSmith for observability platform

## 📞 Support

For questions or issues:
- Review the [documentation](docs/)
- Check the [implementation tracker](project-management/IMPLEMENTATION_TRACKER.md)
- Review [example analyses](examples/)

---

**Created**: November 16, 2025  
**Status**: Phase 2 Complete (50% overall)  
**Next Phase**: Reports + Testing
