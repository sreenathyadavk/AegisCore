#!/bin/bash

# Navigate to script directory
cd "$(dirname "$0")"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Starting AegisGate System ===${NC}"

# 1. Check Redis
if [ ! "$(docker ps -q -f name=aegis_redis)" ]; then
    if [ "$(docker ps -aq -f name=aegis_redis)" ]; then
        echo "Starting existing Redis container..."
        docker start aegis_redis
    else
        echo "Creating Redis container..."
        docker run --name aegis_redis -d -p 6379:6379 redis:7-alpine
    fi
else
    echo -e "${GREEN}✓ Redis is running${NC}"
fi

# 2. Activate Venv
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install uvicorn
fi

# 3. Kill existing instances
pkill -f "uvicorn app.main:app"
pkill -f "tests/upstream_mock.py"

# 4. Start Mock Upstream
echo "Starting Mock Upstream Service on port 8080..."
python3 tests/upstream_mock.py > /dev/null 2>&1 &
UPSTREAM_PID=$!
echo -e "${GREEN}✓ Upstream running (PID: $UPSTREAM_PID)${NC}"

# 5. Start Firewall
echo -e "${BLUE}Starting Firewall on port 8000...${NC}"
echo "Dashboard will be available at: http://localhost:8000/dashboard"
echo "Press CTRL+C to stop both services."

# Trap to kill upstream when firewall stops
trap "kill $UPSTREAM_PID; exit" INT

uvicorn app.main:app --port 8000 --reload
