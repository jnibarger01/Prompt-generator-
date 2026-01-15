#!/bin/bash
# Deployment and Testing Script for Prompt Generator

set -e

echo "🚀 Prompt Generator - Deployment Test Script"
echo "============================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "\n${BLUE}Step 1: Installing Dependencies${NC}"
cd backend
pip install -q -r requirements.txt --break-system-packages
cd ..

echo -e "\n${GREEN}✓ Dependencies installed${NC}"

echo -e "\n${BLUE}Step 2: Testing Backend Import${NC}"
cd backend
python3 << EOF
from main import app, engine, PromptTypeEnum, SpecificityLevel

# Test generate
print("Testing generate...")
prompts = engine.generate(PromptTypeEnum.IMAGE, 2, SpecificityLevel.HIGH)
print(f"✓ Generated {len(prompts)} prompts")
print(f"  Example: {prompts[0][:100]}...")

# Test optimize
print("\nTesting optimize...")
optimized, detected = engine.optimize("Give me a bowl cut", "Using the uploaded photo")
print(f"✓ Optimized prompt (detected type: {detected})")
print(f"  Length: {len(optimized)} characters")
print(f"  Preview: {optimized[:100]}...")

print("\n✓ All engine tests passed!")
EOF
cd ..

echo -e "\n${GREEN}✓ Backend tests passed${NC}"

echo -e "\n${BLUE}Step 3: Docker Build Test${NC}"
if command -v docker &> /dev/null; then
    echo "Building Docker image..."
    docker build -t prompt-generator:latest . -q
    echo -e "${GREEN}✓ Docker image built successfully${NC}"
else
    echo "⚠ Docker not found, skipping"
fi

echo -e "\n${GREEN}============================================${NC}"
echo -e "${GREEN}✓ All tests passed!${NC}"
echo -e "\n${BLUE}Deployment Options:${NC}"
echo "  1. Render:  Deploy backend/ as a Web Service"
echo "  2. Netlify: Deploy frontend/ as a Static Site"
echo "  3. Docker:  docker-compose up"
echo "  4. Local:   cd backend && uvicorn main:app --reload"
echo ""
echo "See README.md for detailed deployment instructions"
