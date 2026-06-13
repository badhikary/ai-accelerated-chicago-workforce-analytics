# Analytical Methodology
## Chicago City Workforce Analytics

---

## Overview

This document describes the full analytical methodology used in this project — from raw data acquisition through statistical testing, visualization, and AI-augmented insight generation. It is intended to make the project fully reproducible and to demonstrate senior-level analytical rigor.

---

## 1. Data Acquisition

- **Source**: [City of Chicago Open Data Portal](https://data.cityofchicago.org) via [data.gov](https://data.gov)
- **Access Method**: Direct CSV download (no API key required — public domain dataset)
- **File Format**: Comma-separated values (.csv)
- **Encoding**: UTF-8
- **Row Count**: 31,984 employee records
- **Column Count**: 8 original columns

No scraping, API calls, or proprietary data sources were used. The dataset is fully reproducible by downloading the same file from the public portal.

---

## 2. Data Profiling

Before any cleaning, a systematic data profile was generated covering:

| Profiling Dimension | Method |
|--------------------|--------|
| Row/column counts | `df.shape` |
| Data types | `df.dtypes` |
| Null counts and percentages | `df.isnull().sum()` |
| Unique value counts | `df.nunique()` |
| Numeric descriptive stats | `df.describe()` |
| Top categorical values | `df.value_counts().head(5)` |

Profile output saved to `data/processed/data_profile_report.json` for reproducibility and audit trail.

**Key profiling findings**:
- `Typical Hours`: 78.3% null — expected (NULL for salaried workers by design)
- `Annual Salary`: 21.7% null — expected (NULL for hourly workers by design)
- `Hourly Rate`: 78.3% null — expected (NULL for salaried workers by design)
- All string columns: 0 nulls
- No unexpected missing data patterns detected

---

## 3. Data Cleaning & Transformation

All cleaning steps are documented in `python_analysis/01_data_ingestion_cleaning.py`.

### 3.1 Column Standardization
Original column names were converted to snake_case for programmatic consistency:
```
Name                 → employee_name
Job Titles           → job_title
Department           → department
Full or Part-Time    → employment_type
Salary or Hourly     → pay_type
Typical Hours        → typical_hours
Annual Salary        → annual_salary
Hourly Rate          → hourly_rate
```

### 3.2 String Normalization
All string columns were `.strip().upper()`-transformed to eliminate whitespace inconsistencies and ensure consistent grouping.

### 3.3 Annual Equivalent Compensation (Key Derived Column)

The dataset contains two different compensation structures that are not directly comparable. A normalized `annual_equivalent` column was created:

```
IF pay_type == 'SALARY':
    annual_equivalent = annual_salary

IF pay_type == 'HOURLY':
    annual_equivalent = hourly_rate × typical_hours × 52
```

**Assumptions**:
- 52 working weeks per year (no deduction for holidays/PTO — gross annualization)
- `typical_hours` represents contracted weekly hours, not actual hours worked
- This produces a gross annual compensation equivalent for comparison purposes

**Limitation**: Overtime, bonuses, pension contributions, and benefits are not included. This analysis covers base compensation only.

### 3.4 Compensation Tier Bands

Custom compensation tiers were defined to segment the workforce:

| Tier Code | Label | Range |
|----------|-------|-------|
| 1_Under_50K | Under $50K | $0 – $49,999 |
| 2_50K-75K | $50K–$75K | $50,000 – $74,999 |
| 3_75K-100K | $75K–$100K | $75,000 – $99,999 |
| 4_100K-125K | $100K–$125K | $100,000 – $124,999 |
| 5_125K-150K | $125K–$150K | $125,000 – $149,999 |
| 6_150K_Plus | $150K+ | $150,000 and above |

These bands were designed to align with common public sector salary grade boundaries and provide meaningful segmentation of this specific dataset's distribution.

### 3.5 Feature Engineering

| Derived Column | Logic | Purpose |
|---------------|-------|---------|
| `annual_equivalent` | See 3.3 | Normalize all compensation to annual basis |
| `compensation_tier` | See 3.4 | Segment analysis |
| `comp_quartile` | `pd.qcut(annual_equivalent, 4)` | Quartile membership |
| `is_public_safety` | 1 if CPD/CFD/OEMC, else 0 | Public safety vs. civilian split |
| `is_fulltime` | 1 if F, else 0 | Employment type binary |
| `dept_short` | Lookup dict of abbreviations | Chart label readability |
| `is_outlier_low` | 1 if below Q1–1.5×IQR | Outlier flag |
| `is_outlier_high` | 1 if above Q3+1.5×IQR | Outlier flag |

### 3.6 Validation Checks
Post-cleaning assertions confirmed:
- Row count preserved (31,984 = 31,984) ✓
- `annual_equivalent` coverage: 100.0% ✓
- All `pay_type` values in {SALARY, HOURLY} ✓
- All `employment_type` values in {F, P} ✓
- Zero unexpected nulls ✓

---

## 4. Exploratory Data Analysis (EDA)

EDA covered the following dimensions:

### 4.1 Univariate Analysis
- Distribution of `annual_equivalent` (histogram, 80 bins)
- Frequency distributions of `department`, `job_title`, `pay_type`, `employment_type`
- Percentile ladder (P1 through P99)

### 4.2 Bivariate Analysis
- Compensation by pay type (SALARY vs HOURLY): distribution overlay + boxplot
- Compensation by employment type (F vs P): boxplot
- Compensation by public safety segment: boxplot
- Department headcount vs. total payroll: bar charts

### 4.3 Multivariate Analysis
- Heatmap: department × employment type → median compensation
- Top 15 departments: compensation boxplot (sorted by median)
- Compensation tier breakdown: count vs. payroll share

---

## 5. Statistical Testing

### 5.1 Normality Assessment
**D'Agostino K² test** (n=5,000 random sample):
- Statistic: 276.57 | p-value: 8.76×10⁻⁶¹
- **Conclusion**: Compensation is NOT normally distributed → non-parametric tests required

### 5.2 Two-Group Comparison: Salaried vs. Hourly
**Primary test**: Mann-Whitney U (non-parametric, appropriate for non-normal data)
- H₀: No difference in median compensation between salaried and hourly workers
- Result: U = 116,300,697.5, p < 1×10⁻³⁰⁰ → **Reject H₀**
- Effect size: Cohen's d = 0.674 → **Large effect**

**Secondary test**: Independent t-test (parametric, for comparison)
- t = 52.41, p < 1×10⁻³⁰⁰ → Consistent with Mann-Whitney result

### 5.3 Multi-Group Comparison: Departments
**Primary test**: Kruskal-Wallis H (non-parametric ANOVA alternative)
- H₀: Median compensation is equal across all departments
- Result: H = 6,243.81, p < 1×10⁻³⁰⁰ → **Reject H₀**
- Effect size: Eta-squared (η²) = 0.266 → **Large effect** (department explains 26.6% of variance)

**Secondary test**: One-way ANOVA
- F = 1,120.9, p < 1×10⁻³⁰⁰ → Consistent result

### 5.4 Full-Time vs. Part-Time Equity
**Test**: Mann-Whitney U (two-sided)
- Result: U = 27,541,439, p < 1×10⁻³⁰⁰
- Effect size: Cohen's d = 4.41 → **Very large**
- Note: Gap is hours-driven, not rate-driven. Part-time workers work 10–20 hrs/week

### 5.5 Effect Size Interpretation Standards

| Cohen's d | Interpretation |
|-----------|---------------|
| 0.0 – 0.2 | Negligible |
| 0.2 – 0.5 | Small |
| 0.5 – 0.8 | Medium |
| > 0.8 | Large |

| Eta-squared (η²) | Interpretation |
|-----------------|---------------|
| < 0.01 | Negligible |
| 0.01 – 0.06 | Small |
| 0.06 – 0.14 | Medium |
| > 0.14 | Large |

---

## 6. Outlier Detection

**Method**: Tukey's IQR Fence Method

```
Q1 = 25th percentile = $97,488
Q3 = 75th percentile = $127,146
IQR = Q3 - Q1 = $29,658
Lower fence = Q1 - 1.5 × IQR = $53,001
Upper fence = Q3 + 1.5 × IQR = $171,633
```

**Results**:
- High outliers (> $171,633): 729 employees (2.3%) — predominantly senior executives and specialized roles
- Low outliers (< $53,001): 1,321 employees (4.1%) — predominantly part-time workers and stipend/elected roles

All outliers were **retained** in aggregate analysis with appropriate flagging. They represent valid, real-world compensation levels, not data entry errors.

---

## 7. Visualization Design Principles

All charts follow these corporate visualization standards:

- **Primary color**: Navy Blue (#003087) — authority, trust
- **Accent colors**: Red (#E63946) for alerts/highlights; Teal (#2A9D8F) for secondary series; Amber (#F4A261) for tertiary
- **Typography**: DejaVu Sans (open-source, clean)
- **Resolution**: 150 DPI (suitable for presentations and print)
- **Source citation**: Every chart includes "Source: City of Chicago / data.gov"
- **Non-interactive backend**: Matplotlib Agg (server-safe, reproducible)
- **Chart types selected** to match data shape:
  - Histogram → continuous distribution
  - Boxplot → spread and outliers by category
  - Heatmap → two-dimensional cross-tab
  - Horizontal bar → ranked categories with long labels
  - Violin → distribution shape comparison
  - Q-Q plot → normality assessment

---

## 8. SQL Architecture

The SQL layer uses **SQLite** for maximum portability — no server required. All queries are also PostgreSQL-compatible (minor syntax differences noted in comments).

**Database objects created**:
- `workforce_raw` — mirrors CSV 1:1 (raw ingestion table)
- `workforce_clean` — transformed production table with derived columns
- `vw_dept_summary` — department-level summary view
- `vw_compensation_bands` — compensation tier distribution view
- `vw_payroll_liability` — annual/monthly/weekly payroll by department
- 6 indexes on high-cardinality analytical columns

**Query modules** cover: schema/load, workforce KPIs, department analysis, compensation analysis, pay equity, executive dashboard metrics.

---

## 9. Excel Workbook Architecture

The Excel workbook (`excel/Chicago_Workforce_Analytics.xlsx`) was programmatically generated using `openpyxl` to ensure reproducibility. Six tabs:

| Tab | Content | Audience |
|-----|---------|---------|
| 📊 Overview Dashboard | KPI cards + full department table | Executive/Manager |
| 💰 Compensation Analysis | Salary bands, pay type comparison, percentiles | HR/Finance |
| 🏆 Top Job Titles | Top 50 titles by compensation (min 10 employees) | HR |
| 👑 Top 50 Earners | Individual top earner table | Leadership/Audit |
| ⚖️ Pay Equity | Statistical test results + dept equity ratios | HR/Legal |
| 📋 Methodology | Data dictionary + key findings + methods | All |

Professional formatting includes: conditional color scales, data bars, alternating row fills, frozen header rows, and number formatting.

---

## 10. AI Integration Methodology

AI tools were used in three ways:

1. **Generative Narrative**: GPT-4/Claude prompts convert structured statistics into executive prose. Prompts are documented and reusable (see `ai_insights/ai_analysis_prompts.md`).

2. **Anomaly Classification**: A rule-based Python module mirrors the output a production LLM call would return — classifying compensation outliers into business-meaningful categories without requiring an API key for portfolio demonstration.

3. **Data Quality Scoring**: A structured 6-dimension DQ scorecard (Completeness, Validity, Consistency, Uniqueness, Accuracy, Timeliness) generates an objective A–D grade with actionable detail per dimension.

**AI Ethics Compliance**:
- No PII sent to external API services
- All AI outputs reviewed and validated
- AI use clearly disclosed in all deliverables
- Rule-based fallbacks ensure reproducibility without API keys

---

## 11. Reproducibility

To fully reproduce this project from scratch:

```bash
# 1. Clone repo
git clone https://github.com/YOUR_USERNAME/chicago-workforce-analytics.git
cd chicago-workforce-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place raw data file
# Copy CSV to: data/raw/Current_Employee_Names__Salaries__and_Position_Titles.csv

# 4. Run pipeline
python python_analysis/01_data_ingestion_cleaning.py
python python_analysis/02_exploratory_data_analysis.py
python python_analysis/03_statistical_analysis.py
python python_analysis/04_compensation_benchmarking.py
python python_analysis/05_visualization_export.py
python ai_insights/ai_accelerated_pipeline.py

# 5. For SQL analysis
sqlite3 data/sql/chicago_workforce.db < sql_analysis/01_schema_and_load.sql
# (Then manually import CSV via .import command — see script header)
```

Expected runtime: ~2–3 minutes on a standard laptop.

---

*Methodology document prepared as part of the Chicago City Workforce Analytics Senior Data Analyst Portfolio Project.*
