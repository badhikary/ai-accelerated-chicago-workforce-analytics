# 🏙️ Chicago City Workforce Analytics
### End-to-End Senior Data Analyst Project | City of Chicago | data.gov


[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![SQL](https://img.shields.io/badge/SQL-SQLite%2FPostgreSQL-orange?logo=postgresql)](https://postgresql.org)
[![Excel](https://img.shields.io/badge/Excel-Advanced-green?logo=microsoftexcel)](https://microsoft.com/excel)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi)](https://powerbi.microsoft.com)
[![AI](https://img.shields.io/badge/AI-Accelerated%20Analytics-purple?logo=openai)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

> **AI-Accelerated, Human-Validated Analytics Workflow:** This project demonstrates how AI was used to accelerate documentation, SQL/DAX drafting, dashboard planning, and business communication. Final outputs were structured, reviewed, and validated by the analyst using repeatable Python, SQL, Excel, and Power BI analysis steps.

---

## 📋 Project Overview

This is an **end-to-end workforce analytics portfolio project** built on publicly available City of Chicago employee compensation data sourced from data.gov. The project demonstrates senior-level data analyst competencies across the full analytics lifecycle — from raw data ingestion, data cleaning, SQL analysis, Excel reporting, and Power BI dashboard planning to AI-accelerated, human-validated business communication.

> **Dataset**: City of Chicago — Current Employee Names, Salaries, and Position Titles  
> **Source**: [data.gov / City of Chicago Open Data Portal](https://data.cityofchicago.org)  
> **Records**: 31,984 employees | 39 departments | 8 columns  
> **Scope**: Compensation, workforce composition, pay equity, departmental benchmarking

---

## 🎯 Business Questions Answered

| # | Business Question | Tool Used |
|---|------------------|-----------|
| 1 | What is the total annual payroll liability by department? | SQL + Python |
| 2 | Is there evidence of pay disparity by employment type (salary vs hourly)? | Python / Stats |
| 3 | Which departments have the highest and lowest compensation bands? | Power BI Dashboard |
| 4 | What is the salary distribution across the entire workforce? | Python / Excel |
| 5 | Are part-time employees compensated fairly relative to full-time? | SQL + Python |
| 6 | What are the top-paying job titles in the city government? | SQL |
| 7 | How does the compensation structure differ across police, fire, and civilian roles? | Python / Excel |
| 8 | What workforce optimization opportunities exist? | AI-Accelerated Insights |

---

## 📁 Project Structure

```
chicago_workforce_analytics/
│
├── 📂 data/
│   ├── raw/                    # Original data.gov dataset (untouched)
│   ├── processed/              # Cleaned, transformed datasets (CSV + Parquet)
│   └── sql/                    # SQLite database file
│
├── 📂 python_analysis/
│   ├── 01_data_ingestion_cleaning.py
│   ├── 02_exploratory_data_analysis.py
│   ├── 03_statistical_analysis.py
│   ├── 04_compensation_benchmarking.py
│   └── 05_visualization_export.py
│
├── 📂 notebooks/
│   └── Chicago_Workforce_Analytics_Full.ipynb   # Full Jupyter Notebook
│
├── 📂 sql_analysis/
│   ├── 01_schema_and_load.sql
│   ├── 02_workforce_summary.sql
│   ├── 03_department_analysis.sql
│   ├── 04_compensation_analysis.sql
│   ├── 05_pay_equity_analysis.sql
│   └── 06_executive_kpi_queries.sql
│
├── 📂 excel/
│   ├── Chicago_Workforce_Analytics.xlsx        # Multi-tab Excel workbook
│   └── excel_instructions.md                   # How to use the Excel file
│
├── 📂 powerbi/
│   ├── Chicago_Workforce_Dashboard.pbix        # Power BI dashboard file
│   ├── powerbi_setup_guide.md                  # DAX measures + setup steps
│   └── dashboard_screenshots/                  # PNG exports of all pages
│
├── 📂 ai_insights/
│   ├── ai_analysis_prompts.md                  # Reusable AI prompt library
│   ├── gpt_workforce_insights.md               # AI-Accelerated narrative insights
│   └── ai_accelerated_pipeline.py              # AI-Accelerated anomaly detection
│
├── 📂 visualizations/
│   └── (exported PNG charts from Python)
│
├── 📂 reports/
│   └── Chicago_Workforce_Executive_Report.md   # Final executive summary report
│
├── 📂 docs/
│   ├── data_dictionary.md
│   ├── methodology.md
│   └── project_charter.md
│
├── 📂 scripts/
│   ├── setup_environment.sh
│   └── run_full_pipeline.sh
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧰 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Data Ingestion** | Python (pandas, numpy) | ETL, cleaning, transformation |
| **Database** | SQLite (portable) / PostgreSQL-compatible SQL | Querying, aggregations |
| **Statistical Analysis** | scipy, statsmodels | Pay equity tests, distributions |
| **Visualization** | matplotlib, seaborn, plotly | Charts, heatmaps, distributions |
| **Spreadsheet** | Microsoft Excel (openpyxl) | Pivot tables, dashboards |
| **BI Dashboard** | Power BI | Executive-level interactive dashboard |
| **AI / LLM** | OpenAI GPT-4 API / Claude API | Narrative insights, anomaly flags |
| **Version Control** | Git + GitHub | Source control, portfolio hosting |
| **Environment** | Python 3.11, Jupyter Notebook | Development environment |

---

## 📊 Key Findings (Executive Summary)

- 🔵 **31,984 city employees** with a total estimated annual payroll of **~$3.6 billion**
- 🔴 The **Chicago Police Department** is the largest employer (12,315 employees, 38.5% of workforce)
- 🟢 Median annual salary: **$115,158** — 48% higher than the U.S. median household income
- 🟡 **Hourly employees** average **$46.30/hr** (annualized ~$96,300) vs salaried **$115,240**
- 🟠 Top 10 departments account for **92%** of the total workforce
- 🔵 **Part-time workers** (2.8% of workforce) are concentrated in Chicago Public Library and Parks

---

## 🚀 How to Run This Project

### 1. Clone the Repository
```bash
git clone https://github.com/badhikary/ai_accelerated_human_validated_analytics_workflow_chicago_workforce_project.git
cd ai_accelerated_human_validated_analytics_workflow_chicago_workforce_project
```

### 2. Set Up Environment
```bash
bash scripts/setup_environment.sh
# OR manually:
pip install -r requirements.txt
```

### 3. Run the Full Pipeline
```bash
bash scripts/run_full_pipeline.sh
# OR step-by-step:
python python_analysis/01_data_ingestion_cleaning.py
python python_analysis/02_exploratory_data_analysis.py
python python_analysis/03_statistical_analysis.py
python python_analysis/04_compensation_benchmarking.py
python python_analysis/05_visualization_export.py
```

### 4. Explore in Jupyter
```bash
jupyter notebook notebooks/Chicago_Workforce_Analytics_Full.ipynb
```

### 5. SQL Analysis
```bash
# Load SQLite DB and run queries:
sqlite3 data/sql/chicago_workforce.db < sql_analysis/01_schema_and_load.sql
sqlite3 data/sql/chicago_workforce.db < sql_analysis/02_workforce_summary.sql
```

---

## 📈 Sample Visualizations

> All charts are auto-generated by the Python pipeline and saved to `/visualizations/`

- Salary Distribution Histogram (full workforce)
- Department Headcount Bar Chart
- Compensation Boxplot by Department (Top 15)
- Salary vs Hourly Comparison
- Payroll Heatmap by Department × Employment Type
- Top 20 Job Titles by Average Compensation

---

## 🤖 AI-Accelerated Features

This project incorporates AI at multiple stages:

| Stage | AI Tool | Use Case |
|-------|---------|----------|
| **Data Cleaning** | GPT-4 prompt | Flag anomalous salary entries |
| **Insight Generation** | Claude API | Narrative business summaries |
| **Anomaly Detection** | Python + LLM | Detect outliers, mislabeled roles |
| **Executive Narrative** | GPT-4 | Auto-draft report sections |
| **Prompt Library** | Reusable prompts | Analyst toolkit for AI-Accelerated EDA |

---

## 📜 Data Source & License

- **Source**: [City of Chicago Data Portal](https://data.cityofchicago.org/Administration-Finance/Current-Employee-Names-Salaries-and-Position-Title/xzkq-xp2w)
- **Aggregator**: [data.gov](https://data.gov)
- **Data License**: Public Domain / Open Data Commons
- **Project Code License**: MIT

---

## 👤 Author

**Biplab Adhikary**  
Senior Data Analyst  

🔗 [LinkedIn](https://www.linkedin.com/in/biplab-adhikary/) | [GitHub](https://github.com/badhikary)

---

*Built as a portfolio demonstration of end-to-end senior data analyst capabilities using real U.S. municipal government open data.*
