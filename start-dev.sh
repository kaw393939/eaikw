#!/bin/bash
# Development Environment Startup Script
# Usage: ./start-dev.sh

set -e  # Exit on error

echo "🚀 Starting Development Environment..."
echo ""

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Loaded .env file"
else
    echo "⚠️  Warning: .env file not found"
fi

# Set development mode
export ELEVENTY_ENV=development
echo "✅ Set ELEVENTY_ENV=development"

# Check if port 8080 is already in use
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 8080 is already in use. Killing existing process..."
    kill $(lsof -t -i:8080) 2>/dev/null || true
    sleep 2
fi

# Clean and build
echo ""
echo "🏗️  Building site..."
npm run clean
npm run build

# Check if build was successful
if [ ! -d "_site" ]; then
    echo "❌ Build failed - _site directory not created"
    exit 1
fi

# Verify CSS was built
if [ ! -f "_site/assets/css/main.css" ]; then
    echo "❌ CSS file not found at _site/assets/css/main.css"
    exit 1
fi

echo "✅ Build successful"
echo ""
echo "🌐 Starting development server..."
echo "   URL: http://localhost:8080/"
echo "   Press Ctrl+C to stop"
echo ""

# Start the server
npm start
