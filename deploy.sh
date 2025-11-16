#!/bin/bash

# Emotion Interpretation Machine - Deployment Script
# This script helps deploy the application to a VPS or local server

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Emotion Interpretation Machine Deployer${NC}"
echo -e "${GREEN}========================================${NC}"
echo

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}Error: Python 3.10+ is required. Found: $PYTHON_VERSION${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python version: $PYTHON_VERSION${NC}"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
fi
echo

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ .env file created${NC}"
        echo -e "${YELLOW}⚠ Please edit .env file with your configuration${NC}"
    else
        echo -e "${RED}Error: .env.example not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi
echo

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
python -m pytest tests/ -q
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed${NC}"
else
    echo -e "${RED}✗ Tests failed${NC}"
    echo -e "${YELLOW}Continue anyway? (y/n)${NC}"
    read -r response
    if [ "$response" != "y" ]; then
        exit 1
    fi
fi
echo

# Ask deployment type
echo -e "${YELLOW}Select deployment type:${NC}"
echo "1) Development (foreground)"
echo "2) Production (with systemd)"
echo "3) Docker"
echo -n "Enter choice [1-3]: "
read -r choice

case $choice in
    1)
        echo -e "${GREEN}Starting development server...${NC}"
        python src/main.py
        ;;
    2)
        echo -e "${YELLOW}Setting up systemd service...${NC}"
        
        # Get current directory
        CURRENT_DIR=$(pwd)
        CURRENT_USER=$(whoami)
        
        # Create systemd service file
        SERVICE_FILE="/tmp/emotion-interpreter.service"
        cat > $SERVICE_FILE << EOF
[Unit]
Description=Emotion Interpretation Machine
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$CURRENT_DIR
Environment="PATH=$CURRENT_DIR/venv/bin"
ExecStart=$CURRENT_DIR/venv/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

        echo -e "${YELLOW}Service file created at $SERVICE_FILE${NC}"
        echo -e "${YELLOW}To install, run:${NC}"
        echo "  sudo cp $SERVICE_FILE /etc/systemd/system/"
        echo "  sudo systemctl daemon-reload"
        echo "  sudo systemctl enable emotion-interpreter"
        echo "  sudo systemctl start emotion-interpreter"
        echo "  sudo systemctl status emotion-interpreter"
        echo
        echo -e "${YELLOW}Install now? (requires sudo) (y/n)${NC}"
        read -r install_response
        
        if [ "$install_response" = "y" ]; then
            sudo cp $SERVICE_FILE /etc/systemd/system/
            sudo systemctl daemon-reload
            sudo systemctl enable emotion-interpreter
            sudo systemctl start emotion-interpreter
            
            echo
            echo -e "${GREEN}✓ Service installed and started${NC}"
            echo -e "${YELLOW}Check status with: sudo systemctl status emotion-interpreter${NC}"
            echo -e "${YELLOW}View logs with: sudo journalctl -u emotion-interpreter -f${NC}"
        fi
        ;;
    3)
        echo -e "${YELLOW}Building Docker image...${NC}"
        
        if ! command -v docker &> /dev/null; then
            echo -e "${RED}Error: Docker is not installed${NC}"
            exit 1
        fi
        
        docker build -t emotion-interpreter:latest .
        
        echo -e "${GREEN}✓ Docker image built${NC}"
        echo
        echo -e "${YELLOW}Start container? (y/n)${NC}"
        read -r docker_response
        
        if [ "$docker_response" = "y" ]; then
            echo -e "${YELLOW}Starting Docker container...${NC}"
            
            # Create data directory
            mkdir -p data
            
            docker run -d \
                --name emotion-interpreter \
                -p 3001:3001 \
                -v $(pwd)/data:/app/data \
                --env-file .env \
                emotion-interpreter:latest
            
            echo -e "${GREEN}✓ Container started${NC}"
            echo -e "${YELLOW}View logs with: docker logs -f emotion-interpreter${NC}"
            echo -e "${YELLOW}Stop with: docker stop emotion-interpreter${NC}"
        else
            echo -e "${YELLOW}To start the container manually, run:${NC}"
            echo "  docker run -d --name emotion-interpreter -p 3001:3001 -v \$(pwd)/data:/app/data --env-file .env emotion-interpreter:latest"
        fi
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo
echo -e "${YELLOW}API available at: http://localhost:3001${NC}"
echo -e "${YELLOW}Health check: curl http://localhost:3001/health${NC}"
echo
