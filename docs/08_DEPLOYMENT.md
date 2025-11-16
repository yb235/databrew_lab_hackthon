# Deployment Specification

## Overview

This document outlines the simplified deployment strategy for the Emotion Interpretation Machine. The system uses a **single, straightforward deployment approach** with minimal dependencies.

## Infrastructure Requirements

### Compute
- **Development**: Local machine (8GB RAM, 4 cores minimum)
- **Production**: Simple VPS (DigitalOcean, Linode, Hetzner): 4GB RAM, 2 vCPU

### Database
- **All Environments**: SQLite (file-based, no setup required)

### Cache
- **All Environments**: In-memory caching (Python `lru_cache`)

### Storage
- **All Environments**: Local file system (persistent disk)

### Observability
- **LangSmith**: Cloud-hosted (only external service required besides LLM)
  - Complete tracing, metrics, and monitoring
  - No additional observability services needed

## Deployment Architecture

### Single Server Deployment

```yaml
Architecture:
  Nginx (optional) → FastAPI Server → SQLite Database + Local Storage
  
Single Server Setup:
  - FastAPI application (Python)
  - SQLite database (file-based)
  - Local file storage (./storage/)
  - LangSmith tracing (cloud)
  - React web client (served as static files)
  
Benefits:
  - Very low cost ($5-12/month)
  - Simple to manage
  - No vendor lock-in
  - Full control
  - Easy to understand
  
Best for: All deployments - startups, small to medium projects
```

## Deployment Steps

### 1. Development Setup (Local)

```bash
# Clone repository
git clone https://github.com/your-org/emotion-interpretation-machine
cd emotion-interpretation-machine

# Install Python dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your keys:
# - HOLISTIC_AI_TEAM_ID
# - HOLISTIC_AI_API_TOKEN  
# - LANGCHAIN_API_KEY
# - DATABASE_URL=sqlite:///./emotion_db.sqlite

# Initialize SQLite database
python scripts/init_db.py

# Start API server
uvicorn api.main:app --reload --port 8000

# In another terminal, start web client
cd web-client
npm install
npm run dev

# Access at:
# - API: http://localhost:8000
# - Web Client: http://localhost:5000
```

### 2. VPS Deployment (Production)

```bash
# On your VPS (Ubuntu/Debian example)

# Install dependencies
sudo apt update
sudo apt install python3.11 python3-pip nginx git -y

# Clone and setup
cd /opt
sudo git clone https://github.com/your-org/emotion-interpretation-machine
cd emotion-interpretation-machine
sudo pip3 install -r requirements.txt

# Build web client
cd web-client
npm install
npm run build
cd ..

# Configure environment
sudo cp .env.example .env
sudo nano .env  # Edit with your credentials

# Initialize database
sudo python3 scripts/init_db.py

# Setup systemd service
sudo nano /etc/systemd/system/emotion-api.service
```

**systemd service file** (`/etc/systemd/system/emotion-api.service`):
```ini
[Unit]
Description=Emotion Interpretation Machine API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/emotion-interpretation-machine
Environment="PATH=/usr/bin"
ExecStart=/usr/bin/python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl daemon-reload
sudo systemctl enable emotion-api
sudo systemctl start emotion-api
sudo systemctl status emotion-api

# Setup Nginx reverse proxy
sudo nano /etc/nginx/sites-available/emotion-api
```

**Nginx configuration**:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Serve web client static files
    location / {
        root /opt/emotion-interpretation-machine/web-client/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # Proxy API requests
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Enable site and restart Nginx
sudo ln -s /etc/nginx/sites-available/emotion-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL with Let's Encrypt (optional)
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### 3. Docker Deployment (Optional)

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - HOLISTIC_AI_TEAM_ID=${HOLISTIC_AI_TEAM_ID}
      - HOLISTIC_AI_API_TOKEN=${HOLISTIC_AI_API_TOKEN}
      - LANGCHAIN_API_KEY=${LANGCHAIN_API_KEY}
      - LANGCHAIN_TRACING_V2=true
      - LANGCHAIN_PROJECT=emotion-interpretation-machine
      - DATABASE_URL=sqlite:////app/data/emotion_db.sqlite
      - STORAGE_DIR=/app/storage
    volumes:
      - ./data:/app/data
      - ./storage:/app/storage
    restart: always

volumes:
  data:
  storage:
```

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Build web client
RUN cd web-client && npm install && npm run build

# Create directories
RUN mkdir -p /app/data /app/storage

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Deploy
docker-compose up -d

# View logs
docker-compose logs -f api
```


## Environment Variables

```bash
# Required - Holistic AI Bedrock (LLM Access)
HOLISTIC_AI_TEAM_ID=your-team-id
HOLISTIC_AI_API_TOKEN=your-api-token

# Required - LangSmith (Observability)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=emotion-interpretation-machine
LANGCHAIN_API_KEY=your-langsmith-api-key
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

# Database (SQLite only)
DATABASE_URL=sqlite:///./emotion_db.sqlite

# Storage
STORAGE_DIR=./storage  # Local file storage path

# API Configuration
API_PORT=8000
API_HOST=0.0.0.0
CORS_ORIGINS=http://localhost:5000,https://yourdomain.com
RATE_LIMIT_PER_MINUTE=100

# Application Settings
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE_MB=50
SESSION_TIMEOUT_MINUTES=60
```

## Scaling Strategy

### Vertical Scaling (Performance)
- Upgrade VPS resources (more RAM, CPUs)
- Optimize database with better indexes
- SQLite performance is excellent for most workloads

### Performance Optimization
- In-memory caching (`lru_cache`) for frequent queries
- Database indexing (already defined in schema)
- Async processing with FastAPI BackgroundTasks

## Monitoring

### LangSmith Monitoring (Complete Solution)

All monitoring is handled by LangSmith:
- ✅ Execution traces and debugging
- ✅ Performance metrics and analytics  
- ✅ Error tracking and alerting
- ✅ Cost monitoring and budget alerts
- ✅ Usage statistics and trends

**Setup monitoring alerts in LangSmith**:
1. Go to LangSmith Dashboard → Project Settings
2. Configure Monitors for:
   - High error rate (> 5%)
   - Slow execution (> 2 minutes)
   - High daily cost (> budget threshold)
3. Set alert destinations (email, Slack, webhook)

### Application Logs

**For VPS**:
```bash
# View application logs
sudo journalctl -u emotion-api -f

# Or if using log files
tail -f /var/log/emotion-api/application.log
```

**For Docker**:
```bash
# View container logs
docker-compose logs -f api

# Or specific container
docker logs -f <container-id>
```

### Health Checks

**Implement health endpoint** (`/health`):
```python
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Check database connection
    db_ok = await check_database()
    
    # Check LangSmith connection  
    langsmith_ok = check_langsmith()
    
    # Check Holistic AI connection
    llm_ok = await check_llm_connection()
    
    status = "healthy" if all([db_ok, langsmith_ok, llm_ok]) else "degraded"
    
    return {
        "status": status,
        "components": {
            "database": "up" if db_ok else "down",
            "langsmith": "up" if langsmith_ok else "down",
            "llm": "up" if llm_ok else "down"
        },
        "timestamp": datetime.utcnow().isoformat()
    }
```

**Configure monitoring**:
```bash
# Add health check monitoring (cron or monitoring service)
# Example with curl:
*/5 * * * * curl -f http://localhost:3001/health || echo "Health check failed"

# Or use monitoring services like:
# - UptimeRobot (free tier available)
# - Healthchecks.io (open source)
# - Better Uptime
```

## Security

### API Security
- JWT authentication (implement token-based auth)
- Rate limiting (prevent abuse)
- Input validation (sanitize all inputs)
- CORS configuration (restrict origins)

### Data Security
- **TLS/HTTPS**: Use SSL certificates (Let's Encrypt free)
- **Database encryption**: Enable at-rest encryption
- **File permissions**: Restrict access to storage directories
- **Environment variables**: Never commit secrets to git

### Secrets Management

**Option 1: Environment Variables** (simple):
```bash
# .env file (never commit this)
HOLISTIC_AI_API_TOKEN=secret-token
LANGCHAIN_API_KEY=secret-key
```

**Option 2: Docker Secrets** (Docker Swarm):
```yaml
secrets:
  holistic_ai_token:
    external: true
  langchain_key:
    external: true
    
services:
  api:
    secrets:
      - holistic_ai_token
      - langchain_key
```

**Option 3: Cloud Secrets Manager** (optional):
- AWS Secrets Manager
- GCP Secret Manager
- Azure Key Vault
- HashiCorp Vault

## Cost Estimation

### Single Server Deployment (Monthly Costs)

**VPS Option (Recommended)**:
- VPS (4GB RAM, 2 vCPU): $5-12 (DigitalOcean, Hetzner, Linode)
- Domain: $1/month (or free with some providers)
- SSL: Free (Let's Encrypt)
- LangSmith: $0-49 (free tier available, $49/mo for team)
- Holistic AI Bedrock: Pay-per-token (varies by usage)

**Total Infrastructure: $5-12/month** (excluding LLM token costs)

### LLM Token Costs (Variable)

**Claude 3.5 Sonnet** (via Holistic AI Bedrock):
- Input: ~$3 per 1M tokens
- Output: ~$15 per 1M tokens

**Example usage**:
- 100 analyses/day × 10K tokens avg = 1M tokens/10 days
- Estimated: $15-25/month for moderate usage
- Higher volume: $50-500+/month depending on scale

**Total Estimated Monthly Cost: $20-40/month**

**Simplified Architecture Savings**:
- No PostgreSQL hosting: Save $15-50/month
- No Redis hosting: Save $15-30/month
- No additional cloud services: Save $20-40/month
- Single deployment model: Reduced complexity and maintenance

**Total Savings: $50-120/month** 🎉

## Backup and Disaster Recovery

### Database Backups

**SQLite**:
```bash
# Simple file copy
cp emotion_db.sqlite emotion_db.backup-$(date +%Y%m%d).sqlite

# Automated daily backups
echo "0 2 * * * cp /path/to/emotion_db.sqlite /backups/emotion_db.backup-\$(date +\%Y\%m\%d).sqlite" | crontab -
```

**PostgreSQL**:
```bash
# Manual backup
pg_dump emotion_db > backup-$(date +%Y%m%d).sql

# Automated daily backups
echo "0 2 * * * pg_dump emotion_db > /backups/emotion_db-\$(date +\%Y\%m\%d).sql" | crontab -

# Keep last 7 days
find /backups -name "emotion_db-*.sql" -mtime +7 -delete
```

### Storage Backups

```bash
# Backup storage directory
tar -czf storage-backup-$(date +%Y%m%d).tar.gz storage/

# Sync to remote location (optional)
rsync -avz storage/ remote-server:/backups/emotion-storage/
```

### Restore Procedures

**SQLite**:
```bash
# Stop application
sudo systemctl stop emotion-api

# Restore from backup
cp backup-20240115.sqlite emotion_db.sqlite

# Start application  
sudo systemctl start emotion-api
```

**PostgreSQL**:
```bash
# Stop application
sudo systemctl stop emotion-api

# Restore database
cp backup-20240115.sqlite emotion_db.sqlite

# Start application
sudo systemctl start emotion-api
```

## Maintenance

### Regular Tasks

**Weekly**:
- Review LangSmith traces for errors
- Check disk space usage
- Review application logs
- Monitor costs and token usage

**Monthly**:
- Update dependencies (security patches)
- Review and optimize database indexes
- Clean up old data/logs
- Test backup restore procedures

**Quarterly**:
- Review and optimize LLM prompts based on traces
- Analyze performance trends
- Update documentation
- Security audit

### Updates and Upgrades

```bash
# Update application code
cd /opt/emotion-interpretation-machine
sudo git pull origin main

# Update dependencies
sudo pip3 install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart emotion-api

# Verify deployment
curl http://localhost:3001/health
```

## Troubleshooting

### Common Issues

**1. Application won't start**:
```bash
# Check logs
sudo journalctl -u emotion-api -n 50

# Check environment variables
sudo cat /opt/emotion-interpretation-machine/.env

# Test manually
cd /opt/emotion-interpretation-machine
python3 api/server.py
```

**2. Database connection failed**:
```bash
# Check database file exists and permissions
ls -la /opt/emotion-interpretation-machine/emotion_db.sqlite

# Check file permissions
sudo chmod 644 /opt/emotion-interpretation-machine/emotion_db.sqlite

# Verify DATABASE_URL in .env
```

**3. LangSmith tracing not working**:
```bash
# Verify environment variables
echo $LANGCHAIN_TRACING_V2
echo $LANGCHAIN_API_KEY

# Test API key
curl -H "Authorization: Bearer $LANGCHAIN_API_KEY" https://api.smith.langchain.com/
```

**4. High latency**:
- Check LangSmith traces for bottlenecks
- Monitor database query performance
- Check network latency to Holistic AI
- Consider upgrading resources

## Next Steps

After deployment:
1. **Test with example data** from `/examples` folder
2. **Configure LangSmith monitoring alerts**
3. **Setup automated backups**
4. **Document your specific deployment configuration**
5. **Monitor initial performance and costs**
6. **Iterate and optimize based on LangSmith insights**

See:
- [09_IMPLEMENTATION_GUIDE.md](./09_IMPLEMENTATION_GUIDE.md) - Implementation steps
- [06_OBSERVABILITY.md](./06_OBSERVABILITY.md) - LangSmith monitoring details
- [03_ARCHITECTURE.md](./03_ARCHITECTURE.md) - Architecture overview
