# Project Charter
## Chicago City Workforce Compensation Analytics

---

**Project Title**: Chicago City Workforce Compensation Analytics — End-to-End Senior Data Analyst Portfolio Project  
**Project Sponsor**: Portfolio / Personal Professional Development  
**Data Source**: City of Chicago / data.gov (Public Domain)  
**Project Type**: Workforce Analytics | Compensation Intelligence | Public Sector  
**Date Initiated**: 2025  
**Status**: Complete

---

## 1. Executive Summary

This project delivers a comprehensive workforce analytics solution for the City of Chicago employee compensation dataset. It is designed to mirror the rigor, methodology, and deliverables expected of a **Senior Data Analyst** at a U.S. Fortune 500 company, consulting firm, or public sector analytics team.

The project spans the full analytics lifecycle: raw data ingestion, data quality assessment, SQL querying, Python-based statistical analysis, Excel-based reporting, Power BI dashboard development, and AI-enabled narrative generation.

---

## 2. Business Objectives

| Objective | Success Criteria |
|-----------|----------------|
| Understand workforce composition by department | Headcount table + visual by department |
| Analyze compensation distribution across city | Salary histogram, percentile analysis |
| Identify pay equity patterns | Statistical test (ANOVA/t-test) between groups |
| Build executive KPI dashboard | Power BI dashboard with 5+ pages |
| Quantify total payroll liability | Aggregated annual payroll by department |
| Surface anomalies and outliers | Flagged records + commentary |
| Demonstrate AI-accelerated workflows | Prompt library + AI-generated report sections |

---

## 3. Scope

**In Scope**:
- Data profiling and quality assessment
- Data cleaning and transformation (Python + SQL)
- Exploratory data analysis (EDA)
- Descriptive and inferential statistical analysis
- Salary benchmarking and quartile analysis
- Department-level compensation comparison
- Full/part-time and salary/hourly compensation analysis
- Power BI interactive dashboard
- Excel workbook with pivot tables and charts
- AI-enabled insights and prompt library
- Executive summary report
- GitHub-ready documentation

**Out of Scope**:
- Predictive modeling (salary prediction ML model)
- PII redaction or re-identification
- Real-time data pipeline (batch analysis only)
- Integration with other HR systems

---

## 4. Deliverables

| Deliverable | Format | Audience |
|------------|--------|---------|
| Cleaned Dataset | CSV + Parquet | Technical |
| SQLite Database | .db file | Technical |
| Python Analysis Scripts | .py files | Technical |
| Jupyter Notebook | .ipynb | Technical / Reviewers |
| SQL Queries | .sql files | Technical |
| Excel Workbook | .xlsx | Business |
| Power BI Dashboard | .pbix | Executive / Business |
| AI Insights Report | Markdown | Business |
| Executive Report | Markdown / PDF | Executive |
| README + Documentation | Markdown | All |

---

## 5. Analytical Methodology

```
Raw Data (CSV)
    │
    ▼
[1] Data Ingestion & Profiling
    - Load via pandas
    - Shape, dtypes, null counts
    - Value distributions
    │
    ▼
[2] Data Cleaning & Transformation
    - Standardize column names
    - Derive Annual_Equivalent
    - Handle nulls (by design)
    - Encode categorical flags
    - Export cleaned CSV + Parquet
    │
    ▼
[3] SQL Analysis
    - Load to SQLite
    - Run 6 query modules
    - Export result sets
    │
    ▼
[4] Statistical Analysis (Python)
    - Descriptive stats
    - Compensation percentiles
    - ANOVA: salary by department
    - T-test: salary vs hourly annualized
    - Outlier detection (IQR + Z-score)
    │
    ▼
[5] Visualization
    - matplotlib / seaborn / plotly
    - 12+ charts exported as PNG
    │
    ▼
[6] Excel Workbook
    - 6 tabs: Summary, By Dept, By Job Title,
      Pay Equity, Distribution, Charts
    │
    ▼
[7] Power BI Dashboard
    - 5 pages: Overview, Departments,
      Compensation, Pay Equity, Top Earners
    │
    ▼
[8] AI-Enabled Insights
    - Anomaly detection pipeline
    - LLM-generated narratives
    - Reusable prompt library
    │
    ▼
[9] Executive Report
    - Key findings
    - Recommendations
    - Methodology summary
```

---

## 6. Tools & Technologies

| Tool | Version | Role |
|------|---------|------|
| Python | 3.11 | Core analysis language |
| pandas | 2.x | Data manipulation |
| numpy | 1.x | Numerical operations |
| matplotlib | 3.x | Static visualization |
| seaborn | 0.x | Statistical visualization |
| plotly | 5.x | Interactive charts |
| scipy | 1.x | Statistical tests |
| sqlite3 | Built-in | SQL database |
| openpyxl | 3.x | Excel generation |
| Jupyter | Latest | Notebook environment |
| Power BI Desktop | Latest | BI dashboard |
| Excel | 365/2021 | Reporting |
| Git | Latest | Version control |
| GitHub | N/A | Portfolio hosting |

---

## 7. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Dataset has no unique employee ID | High | Medium | Use name as proxy; document limitation |
| Hourly vs salary comparison not apples-to-apples | High | High | Annualize all compensation using formula |
| Outliers skew averages | Medium | Medium | Report median alongside mean; flag extremes |
| Department name inconsistency | Low | Low | Standardize with strip/upper during cleaning |

---

## 8. Success Metrics

- ✅ 100% of columns profiled and documented
- ✅ Zero untransformed nulls in analytical outputs
- ✅ All 8 business questions answered with data evidence
- ✅ Power BI dashboard with minimum 5 interactive pages
- ✅ At least 12 charts generated programmatically
- ✅ AI prompt library with minimum 10 reusable prompts
- ✅ Executive report suitable for C-suite presentation
- ✅ Full GitHub repository with proper README and documentation
