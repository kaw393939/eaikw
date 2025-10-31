#!/bin/bash
# Setup script for LLM Quality Gate

set -e

echo "🚀 Setting up LLM Quality Gate..."

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION found"

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
if [ ! -d "qa_agents/venv" ]; then
    python3 -m venv qa_agents/venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
source qa_agents/venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -e references/openai-agents-python/ > /dev/null 2>&1
pip install -r qa_agents/requirements.txt > /dev/null 2>&1
echo "✅ Dependencies installed"

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    echo "📝 Please create .env file with OPENAI_API_KEY"
    echo ""
    echo "Example:"
    echo "  OPENAI_API_KEY=sk-..."
    echo "  LLM_MODEL=gpt-4o-mini"
    echo ""
    exit 1
fi

# Check for OPENAI_API_KEY
source .env
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY not found in .env file"
    exit 1
fi
echo "✅ OpenAI API key configured"

# Make quality gate executable
chmod +x qa_agents/quality_gate.py
echo "✅ Quality gate script is executable"

# Update pre-commit hook
echo "🔗 Updating git pre-commit hook..."
cat > .husky/pre-commit << 'EOF'
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run lint-staged first (fast auto-fixes)
npx lint-staged

# Run LLM quality gate
echo ""
echo "Running LLM Quality Gate..."
cd /Users/kwilliams/Desktop/117_site
qa_agents/venv/bin/python3 qa_agents/quality_gate.py
EOF

chmod +x .husky/pre-commit
echo "✅ Pre-commit hook updated"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Test the quality gate: qa_agents/venv/bin/python3 qa_agents/quality_gate.py"
echo "2. Make a commit to see it in action"
echo ""
echo "💡 The quality gate will:"
echo "   - Run all linters (ESLint, Stylelint, Markdownlint)"
echo "   - Analyze issues with LLM"
echo "   - Attempt automatic fixes"
echo "   - Block commit if critical issues remain"
echo ""
echo "💰 Cost: ~\$0.15-0.30 per commit with gpt-4o-mini"
