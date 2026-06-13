#!/usr/bin/env bash
# ============================================================
# Chicago City Workforce Analytics
# run_full_pipeline.sh — Execute complete analysis pipeline
# ============================================================

set -e

START_TIME=$(date +%s)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo "  CHICAGO WORKFORCE ANALYTICS — FULL PIPELINE RUN"
echo "  Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"

cd "$PROJECT_ROOT"

# ── Pre-flight check ──────────────────────────────────────
echo ""
echo "[PRE-FLIGHT] Checking prerequisites..."

RAW_FILE="data/raw/Current_Employee_Names__Salaries__and_Position_Titles.csv"
if [ ! -f "$RAW_FILE" ]; then
    echo "  ✗ ERROR: Raw data file not found: $RAW_FILE"
    echo "    Download from: https://data.cityofchicago.org"
    exit 1
fi
echo "  ✓ Raw data file found"

python3 -c "import pandas, numpy, matplotlib, seaborn, scipy, openpyxl" 2>/dev/null \
    && echo "  ✓ All Python dependencies available" \
    || { echo "  ✗ Missing dependencies — run: bash scripts/setup_environment.sh"; exit 1; }

mkdir -p data/processed data/sql visualizations ai_insights

# ── Step 1: Data Ingestion & Cleaning ─────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 1/5 — Data Ingestion & Cleaning"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 python_analysis/01_data_ingestion_cleaning.py
echo "  ✅ Step 1 complete"

# ── Step 2: Exploratory Data Analysis ─────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 2/5 — Exploratory Data Analysis"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 python_analysis/02_exploratory_data_analysis.py
echo "  ✅ Step 2 complete"

# ── Step 3: Statistical Analysis ──────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 3/5 — Statistical Analysis"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 python_analysis/03_statistical_analysis.py
echo "  ✅ Step 3 complete"

# ── Step 4: Compensation Benchmarking ─────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 4/5 — Compensation Benchmarking"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 python_analysis/04_compensation_benchmarking.py
echo "  ✅ Step 4 complete"

# ── Step 5: Visualization Export & Dashboard ──────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 5/5 — Visualization Export & Executive Dashboard"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 python_analysis/05_visualization_export.py
echo "  ✅ Step 5 complete"

# ── AI Pipeline ───────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  BONUS — AI-Accelerated Analytics Pipeline"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 ai_insights/ai_accelerated_pipeline.py
echo "  ✅ AI pipeline complete"

# ── Summary ───────────────────────────────────────────────
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
MINUTES=$((ELAPSED / 60))
SECONDS=$((ELAPSED % 60))

echo ""
echo "============================================================"
echo "  ✅ FULL PIPELINE COMPLETE"
echo "  Total runtime: ${MINUTES}m ${SECONDS}s"
echo "  Finished: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo ""
echo "  Outputs generated:"

VIZ_COUNT=$(ls visualizations/*.png 2>/dev/null | wc -l)
CSV_COUNT=$(ls data/processed/*.csv 2>/dev/null | wc -l)
echo "    📊 Visualizations:   $VIZ_COUNT PNG charts  → visualizations/"
echo "    📁 Processed data:   $CSV_COUNT CSV files    → data/processed/"
echo "    📓 Jupyter notebook:              → notebooks/"
echo "    🗄️  SQL database:                  → data/sql/"
echo "    📊 Excel workbook:                → excel/Chicago_Workforce_Analytics.xlsx"
echo "    🤖 AI insights:                   → ai_insights/"
echo "    📋 Executive report:              → reports/Chicago_Workforce_Executive_Report.md"
echo ""
echo "  Next steps:"
echo "    → Open Power BI:  powerbi/Chicago_Workforce_Dashboard.pbix"
echo "    → Open notebook:  jupyter notebook notebooks/Chicago_Workforce_Analytics_Full.ipynb"
echo "    → View report:    cat reports/Chicago_Workforce_Executive_Report.md"
echo "============================================================"
