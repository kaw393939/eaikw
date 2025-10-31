"""Configuration for LLM Quality Agents"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
SITE_DIR = PROJECT_ROOT / "_site"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Model configuration
# Use gpt-4o-mini for cost efficiency (~$0.15 per 1M tokens vs $10 for gpt-4)
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# Quality thresholds
QUALITY_THRESHOLDS = {
    "max_critical_issues": 0,
    "max_warnings": 5,
    "min_lighthouse_score": 95,
    "max_auto_fix_attempts": 3,
}

# Cost tracking
ENABLE_COST_TRACKING = True
COST_PER_1M_INPUT_TOKENS = 0.15  # USD for gpt-4o-mini
COST_PER_1M_OUTPUT_TOKENS = 0.60  # USD for gpt-4o-mini
