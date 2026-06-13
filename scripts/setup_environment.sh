#!/usr/bin/env bash
# ============================================================
# Chicago City Workforce Analytics
# setup_environment.sh — One-time environment setup
# ============================================================

set -e  # Exit immediately on error

echo "============================================================"
echo "  Chicago Workforce Analytics — Environment Setup"
echo "============================================================"

# ── Python version check ──────────────────────────────────
echo ""
echo "[1] Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required="3.9"
echo "    Found: Python $python_version"

if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)"; then
    echo "    ✓ Python version OK (>= 3.9 required)"
else
    echo "    ✗ ERROR: Python 3.9+ required. Current: $python_version"
    exit 1
fi

# ── Create virtual environment ────────────────────────────
echo ""
echo "[2] Creating virtual environment (.venv)..."
if [ -d ".venv" ]; then
    echo "    ⚠ .venv already exists — skipping creation"
else
    python3 -m venv .venv
    echo "    ✓ Virtual environment created at .venv/"
fi

# ── Activate virtual environment ──────────────────────────
echo ""
echo "[3] Activating virtual environment..."
source .venv/bin/activate
echo "    ✓ Activated: $(which python)"

# ── Upgrade pip ───────────────────────────────────────────
echo ""
echo "[4] Upgrading pip..."
pip install --upgrade pip --quiet
echo "    ✓ pip upgraded to $(pip --version | awk '{print $2}')"

# ── Install dependencies ──────────────────────────────────
echo ""
echo "[5] Installing project dependencies from requirements.txt..."
pip install -r requirements.txt --quiet
echo "    ✓ Dependencies installed"

# ── Verify key imports ────────────────────────────────────
echo ""
echo "[6] Verifying key package imports..."
python3 -c "
import pandas as pd; print(f'    ✓ pandas {pd.__version__}')
import numpy as np; print(f'    ✓ numpy {np.__version__}')
import matplotlib; print(f'    ✓ matplotlib {matplotlib.__version__}')
import seaborn as sns; print(f'    ✓ seaborn {sns.__version__}')
import scipy; print(f'    ✓ scipy {scipy.__version__}')
import openpyxl; print(f'    ✓ openpyxl {openpyxl.__version__}')
"

# ── Create directory structure ────────────────────────────
echo ""
echo "[7] Verifying directory structure..."
dirs=(
    "data/raw"
    "data/processed"
    "data/sql"
    "python_analysis"
    "notebooks"
    "sql_analysis"
    "excel"
    "powerbi/dashboard_screenshots"
    "visualizations"
    "ai_insights"
    "reports"
    "docs"
    "scripts"
)
for dir in "${dirs[@]}"; do
    mkdir -p "$dir"
    echo "    ✓ $dir"
done

# ── Check raw data file ───────────────────────────────────
echo ""
echo "[8] Checking raw data file..."
RAW_FILE="data/raw/Current_Employee_Names__Salaries__and_Position_Titles.csv"
if [ -f "$RAW_FILE" ]; then
    row_count=$(wc -l < "$RAW_FILE")
    echo "    ✓ Raw data found: $RAW_FILE ($row_count lines)"
else
    echo "    ⚠ Raw data NOT found at: $RAW_FILE"
    echo "    → Download from: https://data.cityofchicago.org/Administration-Finance/"
    echo "      Current-Employee-Names-Salaries-and-Position-Title/xzkq-xp2w"
    echo "    → Place the CSV in: data/raw/"
fi

# ── Done ──────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "  ✅ Environment setup complete!"
echo "============================================================"
echo ""
echo "  To activate the environment in future sessions:"
echo "    source .venv/bin/activate"
echo ""
echo "  To run the full analysis pipeline:"
echo "    bash scripts/run_full_pipeline.sh"
echo ""
echo "  To open the Jupyter notebook:"
echo "    jupyter notebook notebooks/Chicago_Workforce_Analytics_Full.ipynb"
echo "============================================================"
