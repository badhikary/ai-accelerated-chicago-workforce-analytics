# City of Chicago Workforce Analytics
## Executive Summary Report

**Prepared by**: Senior Data Analyst  
**Data Source**: City of Chicago / data.gov (Public Domain)  
**Analysis Date**: 2025  
**Dataset**: Current Employee Names, Salaries, and Position Titles  
**Records Analyzed**: 31,984 employees | 39 departments

---

## 1. Executive Summary

The City of Chicago operates one of the largest municipal workforces in the United States, employing **31,984 individuals** across 39 departments with an estimated total annual payroll of **$3.54 billion**. This report presents a comprehensive data-driven analysis of workforce composition, compensation structure, and pay equity — designed to support strategic decision-making by city leadership, the Office of Budget and Management, and the Chicago City Council Finance Committee.

### Key Findings at a Glance

| Metric | Value | Context |
|--------|-------|---------|
| Total Employees | 31,984 | 6th largest U.S. city government |
| Total Annual Payroll | $3.54 Billion | FY estimate |
| Median Compensation | $111,252 | 75% above U.S. median worker |
| Average Compensation | $110,575 | Includes annualized hourly workers |
| Largest Department | Chicago Police Dept. | 12,315 employees (38.5%) |
| Full-Time Rate | 97.2% | 31,097 of 31,984 employees |
| Salaried Rate | 78.3% | 25,042 employees on fixed salary |
| Public Safety Share | 56.2% | CPD + CFD + OEMC combined |
| Data Quality Score | 97/100 (Grade A) | IQR-validated, DQ-assessed |

---

## 2. Workforce Composition Analysis

### 2.1 Departmental Distribution

The city's workforce is **highly concentrated** in a small number of large departments. The top 5 departments account for **75.9% of total payroll expenditure**:

| Rank | Department | Employees | % of Total | Annual Payroll |
|------|-----------|-----------|-----------|----------------|
| 1 | Chicago Police Department | 12,315 | 38.5% | $1.45B |
| 2 | Chicago Fire Department | 4,806 | 15.0% | $584M |
| 3 | Department of Water Management | 2,048 | 6.4% | $225M |
| 4 | Department of Streets and Sanitation | 2,008 | 6.3% | $200M |
| 5 | Chicago Department of Aviation | 1,985 | 6.2% | $195M |

**Key Insight**: The Chicago Police Department alone employs more staff than the next three departments combined. Any CPD contract negotiation, overtime policy change, or staffing reduction has an outsized fiscal impact on the total payroll budget.

### 2.2 Employment Type

- **Full-Time (F)**: 31,097 employees (97.2%) — near-universal full-time employment
- **Part-Time (P)**: 887 employees (2.8%) — concentrated in Chicago Public Library and cultural/parks roles

The extremely low part-time rate (2.8%) is characteristic of a heavily unionized municipal workforce where collective bargaining agreements typically define full-time status for benefits eligibility.

### 2.3 Pay Structure

- **Salaried employees**: 25,042 (78.3%) — receive fixed annual compensation
- **Hourly employees**: 6,942 (21.7%) — compensated at an hourly rate with defined weekly hours

Hourly workers are most prevalent in the Departments of Streets & Sanitation, Aviation, and Water Management — roles with variable operational demands.

---

## 3. Compensation Analysis

### 3.1 Salary Distribution

The compensation distribution across the city's workforce shows a **slightly left-skewed, approximately normal curve** centered around $111,252 (median).

**Compensation Percentile Ladder**:

| Percentile | Annual Compensation |
|-----------|-------------------|
| P10 | $68,670 |
| P25 (Q1) | $97,488 |
| P50 (Median) | $111,252 |
| P75 (Q3) | $127,146 |
| P90 | $146,448 |
| P95 | $157,212 |
| P99 | $196,140 |
| Maximum | $350,000 |

The **interquartile range (IQR) of $29,658** is relatively narrow, indicating that the bulk of the workforce sits within a compressed central compensation band — consistent with union-negotiated step schedules that limit wide variation within job classifications.

### 3.2 Compensation Tier Distribution

| Band | Employees | % of Workforce | Total Payroll | % of Payroll |
|------|-----------|---------------|---------------|-------------|
| Under $50K | 1,539 | 4.8% | $51.2M | 1.4% |
| $50K – $75K | 1,614 | 5.0% | $105.8M | 3.0% |
| $75K – $100K | 5,671 | 17.7% | $498.6M | 14.1% |
| $100K – $125K | 14,423 | 45.1% | $1.63B | 46.1% |
| $125K – $150K | 6,174 | 19.3% | $834.7M | 23.6% |
| $150K+ | 2,563 | 8.0% | $428.7M | 12.1% |

**The $100K–$125K band is the largest tier**, containing 45% of the workforce. This reflects standardized salary schedules for police officers, firefighters, and mid-level civil servants.

### 3.3 Salaried vs. Hourly (Annualized) Comparison

| Metric | Salaried | Hourly (Annualized) | Gap |
|--------|---------|---------------------|-----|
| Median | $115,158 | $101,358 | $13,800 (13.6%) |
| Mean | $115,240 | $93,745 | $21,495 (22.9%) |
| Count | 25,042 | 6,942 | — |

**Statistical Finding**: Mann-Whitney U test confirms the compensation difference between salaried and hourly workers is statistically significant (p < 1×10⁻³⁰⁰) with a **large effect size (Cohen's d = 0.674)**. This is not random variation — it is a structural feature of the compensation system.

---

## 4. Department-Level Benchmarking

### 4.1 Highest and Lowest Compensating Departments

**Top 5 Departments by Median Compensation**:
| Department | Median Comp | vs. City Median |
|-----------|------------|-----------------|
| Department of Buildings | $133,432 | +19.9% |
| Chicago Fire Department | $122,376 | +10.0% |
| Department of Fleet & Facility Mgmt | $120,120 | +8.0% |
| Chicago Police Department | $115,158 | +3.5% |
| Department of Water Management | $109,200 | -1.8% |

**Bottom 5 Departments by Median Compensation**:
| Department | Median Comp | vs. City Median |
|-----------|------------|-----------------|
| Department of Family & Support Services | $76,464 | -31.3% |
| Chicago Public Library | $76,464 | -31.3% |
| Office of Budget and Management | $83,616 | -24.8% |
| Chicago Animal Care and Control | $85,956 | -22.8% |
| Department of Public Health | $88,296 | -20.6% |

### 4.2 Equity Ratios

Departments with equity ratios **above 1.15** (well above city average) may indicate:
- Strong union contract terms (CFD, CPD)
- Specialized license/certification requirements (Buildings)
- Competitive market rates for technical skills

Departments below 0.85 (well below average) should be reviewed for:
- Retention risk in competitive labor markets
- Whether current pay scales attract and retain qualified staff
- Potential reclassification opportunities

---

## 5. Pay Equity Analysis

### 5.1 Statistical Tests Summary

All compensation differences were validated through rigorous non-parametric testing (required because the D'Agostino K² normality test confirmed the distribution is non-normal at p < 8.76×10⁻⁶¹).

| Comparison | Test | p-value | Effect Size | Finding |
|-----------|------|---------|-------------|---------|
| Salary vs. Hourly | Mann-Whitney U | < 1e-300 | d=0.674 (Large) | Salaried earn significantly more |
| Across Departments | Kruskal-Wallis | < 1e-300 | η²=0.266 (Large) | Dept. membership explains 26.6% of pay variation |
| Full-Time vs. Part-Time | Mann-Whitney U | < 1e-300 | d=4.41 (Very Large) | Full-time earns dramatically more (hours-driven) |

### 5.2 Full-Time vs. Part-Time Equity Note

The very large Cohen's d (4.41) for full-time vs. part-time is primarily driven by **hours worked**, not hourly rate discrimination. Part-time employees typically work 10–20 hours per week, resulting in low annualized figures. A per-hour comparison reveals hourly rates are generally consistent. No systematic pay rate discrimination is indicated in this dataset.

---

## 6. Top Earners Analysis

- **2,563 employees (8.0%)** earn more than $150,000 annually
- **Maximum individual salary**: $350,000 (senior executive/elected official roles)
- **High earner concentration**: CPD accounts for the largest share of $150K+ earners due to senior officer rank, overtime, and longevity provisions
- **Outlier review**: 729 employees flagged as statistical outliers (IQR method); classified as senior executives, specialized roles, or elected officials — no data quality issues identified

---

## 7. Recommendations

### 7.1 Strategic (Leadership Level)

1. **Public Safety Budget Sensitivity Modeling**: Given CPD and CFD together represent ~55% of payroll, the City Budget Office should model 1%, 2%, and 3% wage increase scenarios for public safety to quantify the multi-year fiscal impact before each contract negotiation cycle.

2. **Part-Time Workforce Review**: The 887 part-time employees — predominantly in library and cultural roles — should be assessed for potential full-time conversion where operationally feasible, to reduce administrative complexity and improve benefits equity.

3. **Compensation Benchmarking Program**: Establish a formal annual benchmarking process comparing city compensation to peer municipalities (Milwaukee, Minneapolis, Indianapolis, Kansas City) and private sector equivalents for hard-to-fill technical roles.

### 7.2 Operational (HR/Finance Level)

4. **Unique Employee Identifier**: The dataset lacks a unique employee ID — a critical gap for tracking tenure, promotions, and year-over-year payroll changes. HR should prioritize adding a persistent employee ID to the public data export.

5. **Hourly Worker Classification Review**: The 21.7% of hourly workers represent variable-cost exposure in the payroll budget. An audit of which hourly roles could be converted to salaried (with predictable cost) versus which genuinely require hourly flexibility would improve budget predictability.

6. **Lower Quartile Compensation Review**: 1,539 employees (4.8%) earning under $50K annually — predominantly part-time — should be reviewed against Chicago's living wage standards and compared to peer city minimum compensation thresholds.

### 7.3 Analytics (Data Team Level)

7. **Build a Live Power BI Dashboard**: Connect the Power BI dashboard to a live data refresh from the Chicago Open Data portal API, enabling real-time workforce monitoring for budget analysts.

8. **Multi-Year Trend Analysis**: When prior-year datasets are available, build a year-over-year compensation trend model to identify which departments and titles have experienced above-market growth.

9. **Predictive Payroll Modeling**: Use historical data to build a regression model predicting total payroll under different headcount and contract scenarios — enabling proactive budget management.

---

## 8. Methodology Summary

| Step | Method | Tool |
|------|--------|------|
| Data Ingestion | pandas read_csv with validation | Python |
| Data Profiling | Column-level null/dtype/cardinality analysis | Python + JSON |
| Data Cleaning | Standardization, feature engineering, outlier flagging | Python |
| Annual Normalization | Hourly Rate × Typical Hours × 52 for hourly workers | Python |
| SQL Analysis | 6 query modules covering KPIs, equity, benchmarking | SQLite |
| Statistical Tests | Mann-Whitney U, Kruskal-Wallis, D'Agostino K² | scipy |
| Effect Sizes | Cohen's d (two-group), Eta-squared (multi-group) | Python |
| Visualization | 13 charts: histograms, boxplots, heatmaps, bars | matplotlib/seaborn |
| Excel Reporting | 6-tab workbook with conditional formatting | openpyxl |
| BI Dashboard | 5-page interactive dashboard | Power BI |
| AI Insights | Anomaly narration, data quality scoring, insight bullets | Python + LLM patterns |

---

## 9. Data Quality Assessment

The dataset received an overall **Data Quality Grade of A (97/100)**:

- ✅ **Completeness** (25/25): Zero unexpected nulls — all nulls are by design
- ✅ **Validity** (20/20): All categorical values conform to expected domains
- ✅ **Consistency** (20/20): Pay type perfectly aligns with compensation columns
- ✅ **Uniqueness** (15/15): 1.1% name duplication is within acceptable threshold for large datasets without unique IDs
- ✅ **Accuracy** (10/10): No impossible values (negative salaries, >168hr/week)
- ⚠️ **Timeliness** (7/10): No record-level timestamp; annual refresh cadence is acceptable for strategic analysis

---

## 10. Appendices

- **Appendix A**: Full department compensation summary table → `data/processed/department_summary.csv`
- **Appendix B**: Top 50 highest-paid employees → `data/processed/top50_earners.csv`
- **Appendix C**: Job title benchmarking table → `data/processed/job_title_benchmarks.csv`
- **Appendix D**: Data profile report (JSON) → `data/processed/data_profile_report.json`
- **Appendix E**: Anomaly detection report → `ai_insights/anomaly_detection_report.csv`
- **Appendix F**: All visualizations → `visualizations/` (13 PNG files)
- **Appendix G**: Power BI dashboard → `powerbi/Chicago_Workforce_Dashboard.pbix`
- **Appendix H**: Excel workbook → `excel/Chicago_Workforce_Analytics.xlsx`

---

*This report was produced as part of an end-to-end Senior Data Analyst portfolio project using publicly available City of Chicago employee data from data.gov. All findings are based on the dataset as published; no supplemental HR records were accessed. This analysis is for professional portfolio demonstration purposes.*

---
**End of Report**  
Chicago City Workforce Analytics | data.gov Open Data | Senior Data Analyst Portfolio Project
