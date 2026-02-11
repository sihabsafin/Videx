#!/bin/bash

# Content Intelligence Platform - Quick Setup Script

echo "=========================================="
echo " Content Intelligence Platform Setup"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.9"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)" 2>/dev/null; then
    echo -e "${GREEN}✅ Python $python_version${NC}"
else
    echo -e "${RED}❌ Python $python_version (need 3.9+)${NC}"
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
if pip3 install -r requirements.txt > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  Installing with verbose output...${NC}"
    pip3 install -r requirements.txt
fi

# Setup .env
echo ""
echo "🔑 Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env file${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env and add your API keys${NC}"
else
    echo -e "${GREEN}✅ .env file exists${NC}"
fi

# Create .gitignore if missing
if [ ! -f .gitignore ]; then
    echo ".env" > .gitignore
    echo "__pycache__/" >> .gitignore
    echo "*.pyc" >> .gitignore
    echo -e "${GREEN}✅ Created .gitignore${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Edit .env file and add your API key:"
echo "   - Get Groq key: https://console.groq.com/keys"
echo "   - OR Get Gemini key: https://makersuite.google.com/app/apikey"
echo ""
echo "2. Run the app:"
echo "   streamlit run app.py"
echo ""
echo "3. Open browser:"
echo "   http://localhost:8501"
echo ""
echo "=========================================="
