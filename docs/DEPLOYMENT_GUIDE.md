# Deployment Guide

## Emotion Interpretation Machine - Simple Deployment

This guide provides step-by-step instructions for deploying the Emotion Interpretation Machine to production.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment Options](#production-deployment-options)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Running the Application](#running-the-application)
7. [Monitoring and Observability](#monitoring-and-observability)
8. [Security Considerations](#security-considerations)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git
- 512 MB RAM minimum (1 GB recommended)
- 1 GB disk space

### External Services (Optional but Recommended)

- **Holistic AI Bedrock Proxy** - For LLM-powered interpretation (requires API key)
- **LangSmith** - For observability and tracing (free tier available)

---

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/yb235/emotion-interpretation-machine.git
cd emotion-interpretation-machine
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and configure:

```bash
# Server Configuration
HOST=0.0.0.0
PORT=3001

# Database (SQLite - auto-created)
DATABASE_URL=sqlite:///./emotion_interpretation.db

# LangChain/LangSmith (optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key_here

# Holistic AI Bedrock Proxy (optional)
HOLISTIC_AI_TEAM_ID=your_team_id
HOLISTIC_AI_API_TOKEN=your_api_token

# Alignment Configuration
ALIGNMENT_WINDOW_MS=100
```

### 5. Initialize Database

The database will be automatically created when you first run the application.

### 6. Run Tests

```bash
pytest tests/
```

### 7. Start Development Server

```bash
python src/main.py
```

The API will be available at `http://localhost:3001`

---

## Production Deployment Options

### Option 1: Simple VPS (Recommended)

Deploy to a simple VPS provider like DigitalOcean, Linode, or Hetzner.

**Advantages**:
- Simple and cost-effective ($5-12/month)
- Full control over environment
- Easy to maintain

**Steps**:

1. **Provision VPS** (Ubuntu 20.04 or later recommended)

2. **SSH into VPS**:
```bash
ssh user@your-vps-ip
```

3. **Install Python and Dependencies**:
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip git -y
```

4. **Clone Repository**:
```bash
git clone https://github.com/yb235/emotion-interpretation-machine.git
cd emotion-interpretation-machine
```

5. **Setup Application**:
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Configure Environment**:
```bash
cp .env.example .env
nano .env  # Edit with your values
```

7. **Create Systemd Service** (for auto-restart):

Create `/etc/systemd/system/emotion-interpreter.service`:

```ini
[Unit]
Description=Emotion Interpretation Machine
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/emotion-interpretation-machine
Environment="PATH=/home/your-username/emotion-interpretation-machine/venv/bin"
ExecStart=/home/your-username/emotion-interpretation-machine/venv/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

8. **Start Service**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable emotion-interpreter
sudo systemctl start emotion-interpreter
sudo systemctl status emotion-interpreter
```

9. **Setup Nginx Reverse Proxy** (optional but recommended):

Install Nginx:
```bash
sudo apt install nginx -y
```

Create `/etc/nginx/sites-available/emotion-interpreter`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/emotion-interpreter /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

10. **Setup SSL with Let's Encrypt** (optional):
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

### Option 2: Docker Container

**Prerequisites**: Docker installed on your machine

1. **Create Dockerfile**:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directory for SQLite database
RUN mkdir -p /app/data

# Expose port
EXPOSE 3001

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=3001
ENV DATABASE_URL=sqlite:////app/data/emotion_interpretation.db

# Run application
CMD ["python", "src/main.py"]
```

2. **Build Image**:
```bash
docker build -t emotion-interpreter:latest .
```

3. **Run Container**:
```bash
docker run -d \
  --name emotion-interpreter \
  -p 3001:3001 \
  -v $(pwd)/data:/app/data \
  -e LANGCHAIN_API_KEY=your_key \
  -e HOLISTIC_AI_TEAM_ID=your_id \
  -e HOLISTIC_AI_API_TOKEN=your_token \
  emotion-interpreter:latest
```

4. **Check Logs**:
```bash
docker logs -f emotion-interpreter
```

---

### Option 3: Platform-as-a-Service (Railway, Render, Fly.io)

These platforms provide simple one-click deployments.

**Railway Example**:

1. Connect GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push

**Render Example**:

1. Create `render.yaml`:

```yaml
services:
  - type: web
    name: emotion-interpreter
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python src/main.py
    envVars:
      - key: HOST
        value: 0.0.0.0
      - key: PORT
        value: 10000
```

2. Connect repository and deploy

---

## Environment Configuration

### Required Variables

```bash
# Server
HOST=0.0.0.0
PORT=3001

# Database (SQLite)
DATABASE_URL=sqlite:///./emotion_interpretation.db
```

### Optional Variables (for full functionality)

```bash
# LangSmith (observability)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key

# Holistic AI Bedrock Proxy (LLM)
HOLISTIC_AI_TEAM_ID=your_team_id
HOLISTIC_AI_API_TOKEN=your_api_token

# Alignment configuration
ALIGNMENT_WINDOW_MS=100
```

---

## Database Setup

The application uses SQLite which requires no separate database server.

**Database Location**: By default, the database file is created at `./emotion_interpretation.db`

**Backup**: Simply copy the database file to back up all data:

```bash
# Backup
cp emotion_interpretation.db emotion_interpretation_backup_$(date +%Y%m%d).db

# Restore
cp emotion_interpretation_backup_20251116.db emotion_interpretation.db
```

**Migration**: To use a different database location, update `DATABASE_URL` in `.env`

---

## Running the Application

### Development Mode

```bash
python src/main.py
```

### Production Mode (with Gunicorn)

1. **Install Gunicorn**:
```bash
pip install gunicorn
```

2. **Run with Gunicorn**:
```bash
gunicorn src.main:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:3001 \
  --access-logfile - \
  --error-logfile -
```

---

## Monitoring and Observability

### LangSmith Integration

If configured, all agent runs are automatically traced in LangSmith.

**View Traces**:
1. Go to https://smith.langchain.com/
2. Select your project
3. View traces for all analysis runs

### Application Logs

**View logs** (if using systemd):
```bash
sudo journalctl -u emotion-interpreter -f
```

**View logs** (if using Docker):
```bash
docker logs -f emotion-interpreter
```

### Health Check

```bash
curl http://localhost:3001/health
```

Expected response:
```json
{
  "status": "ok",
  "database": "connected",
  "version": "1.0.0"
}
```

---

## Security Considerations

### 1. Environment Variables

- Never commit `.env` file to version control
- Use secrets management in production (e.g., AWS Secrets Manager, HashiCorp Vault)

### 2. CORS Configuration

By default, CORS allows all origins (`*`). For production, restrict to specific domains:

```python
# In src/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Change this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. HTTPS

Always use HTTPS in production:
- Use Let's Encrypt for free SSL certificates
- Configure Nginx as reverse proxy with SSL

### 4. Firewall

Configure firewall to only allow necessary ports:
```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### 5. Rate Limiting

Consider adding rate limiting middleware for production (e.g., `slowapi`):

```bash
pip install slowapi
```

### 6. Authentication

The API currently has no authentication. For production:
- Implement JWT tokens
- Use API keys
- Add OAuth 2.0

---

## Troubleshooting

### Application Won't Start

1. **Check Python version**:
```bash
python --version  # Should be 3.10+
```

2. **Check dependencies installed**:
```bash
pip list | grep fastapi
```

3. **Check port availability**:
```bash
lsof -i :3001
```

### Database Errors

1. **Check database file permissions**:
```bash
ls -l emotion_interpretation.db
```

2. **Reset database** (WARNING: deletes all data):
```bash
rm emotion_interpretation.db
python src/main.py  # Will recreate
```

### Analysis Fails

1. **Check LLM API keys** (if using Holistic AI):
```bash
env | grep HOLISTIC_AI
```

2. **Check LangSmith tracing** (if enabled):
```bash
env | grep LANGCHAIN
```

3. **Review logs** for error details

### Performance Issues

1. **Check system resources**:
```bash
free -h  # Memory
df -h    # Disk space
```

2. **Monitor process**:
```bash
htop
```

3. **Consider upgrading VPS** if consistently high load

---

## Backup and Recovery

### Backup Strategy

1. **Database Backup** (daily recommended):
```bash
#!/bin/bash
# backup.sh
cp emotion_interpretation.db backups/db_$(date +%Y%m%d_%H%M%S).db
# Keep only last 7 days
find backups/ -name "db_*.db" -mtime +7 -delete
```

2. **Automated Backups** (cron):
```bash
# Add to crontab
crontab -e

# Run backup daily at 2 AM
0 2 * * * /home/user/emotion-interpretation-machine/backup.sh
```

### Recovery

1. **Stop application**:
```bash
sudo systemctl stop emotion-interpreter
```

2. **Restore database**:
```bash
cp backups/db_20251116_020000.db emotion_interpretation.db
```

3. **Start application**:
```bash
sudo systemctl start emotion-interpreter
```

---

## Updating the Application

### Pull Latest Changes

```bash
cd emotion-interpretation-machine
git pull origin main
```

### Restart Application

**Systemd**:
```bash
sudo systemctl restart emotion-interpreter
```

**Docker**:
```bash
docker restart emotion-interpreter
```

---

## Support

For issues or questions:
- Check logs for error details
- Review API documentation
- Create an issue on GitHub

---

**Version**: 1.0.0  
**Last Updated**: November 16, 2025
