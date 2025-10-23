#!/bin/bash

# Quick Start Script for Network Intelligence Crawler

echo "============================================"
echo "Network Intelligence Crawler - Setup"
echo "============================================"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Create directories
mkdir -p data exports reports

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found. Creating from example..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your GitHub token!"
    echo "   Get token at: https://github.com/settings/tokens/new"
    echo ""
    read -p "Press Enter to continue (or Ctrl+C to exit and setup .env first)..."
fi

# Run the analysis
echo ""
echo "============================================"
echo "Running Analysis..."
echo "============================================"
echo ""

# Quick analysis (no deep scan)
python main.py --all

echo ""
echo "============================================"
echo "✓ Setup and Analysis Complete!"
echo "============================================"
echo ""
echo "Output files:"
echo "  - Database: data/network_intel.db"
echo "  - LinkedIn: exports/connections_enriched.xlsx"
echo "  - GitHub:   exports/github_portfolio.md"
echo ""
echo "To run again:"
echo "  source venv/bin/activate"
echo "  python main.py --all"
echo ""
echo "For help:"
echo "  python main.py --help"
echo ""
