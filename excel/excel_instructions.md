# Excel Workbook Instructions
## Chicago_Workforce_Analytics.xlsx

---

## Overview

The Excel workbook contains **6 professionally formatted tabs** covering every dimension of the workforce analysis. It is designed for business stakeholders who prefer Excel over code or dashboards.

---

## Tabs Guide

### Tab 1: 📊 Overview Dashboard
- **KPI Cards** (rows 6–9): Six color-coded KPI tiles — Total Employees, Annual Payroll, Median Comp, Departments, Full-Time Rate, CPD Headcount
- **Department Table** (rows 13+): All 39 departments with headcount, pay split, compensation stats, and total payroll
- **Color Scale**: Blue gradient on headcount column — darker = larger department
- **Tip**: Sort column B (Headcount) descending to rank departments by size

### Tab 2: 💰 Compensation Analysis
- **Section A**: Compensation band distribution with data bars
- **Section B**: Salaried vs Hourly annualized comparison
- **Section C**: Full workforce percentile table (P1–P99)
- **Tip**: The data bar in Section A visually shows where most employees cluster ($100K–$125K band)

### Tab 3: 🏆 Top Job Titles
- **Top 50 job titles** by median compensation (minimum 10 employees per title)
- **Color scale** on Average Comp column (white → blue gradient)
- Shows headcount, min/avg/median/max, and total payroll contribution per title
- **Tip**: Use Excel's filter (row 3) to search for specific job titles

### Tab 4: 👑 Top 50 Earners
- Individual employee-level view of the 50 highest-compensated city employees
- **Gold/Silver/Bronze** highlighting on ranks 1, 2, 3
- **Red data bars** on compensation column for visual ranking
- **Tip**: This tab is useful for audit/oversight review of high-compensation roles

### Tab 5: ⚖️ Pay Equity
- **Hypothesis test results**: All statistical tests with p-values and effect sizes
- **Department equity ratios**: Each department's average vs. city average with status flags
- Color-coded status: Green = above average, Red = below average
- **Tip**: Filter the equity ratio column to identify departments most at risk of retention issues

### Tab 6: 📋 Methodology
- Data source, transformation logic, statistical methods, key findings
- Useful as a reference when presenting to non-technical stakeholders

---

## How to Refresh Data

When a new dataset version is available from data.gov:

1. Download the new CSV to `data/raw/`
2. Run: `python python_analysis/01_data_ingestion_cleaning.py`
3. Run: `python python_analysis/04_compensation_benchmarking.py`
4. Re-run the Excel generation:
   ```bash
   python3 -c "exec(open('scripts/generate_excel.py').read())"
   ```
   *(Or re-run Script 05 which calls the Excel builder)*
5. The workbook will be overwritten with fresh data

---

## Printing / Sharing Tips

- **Print area**: Each tab is formatted for landscape A4/Letter printing
- **PDF export**: File → Export → Create PDF/XPS for sharing without Excel
- **Presentation mode**: Zoom to 120% for screen sharing
- **Freeze panes**: Header rows are frozen on all data tabs (scroll down without losing headers)

---

## Compatibility

- Tested on: Microsoft Excel 365, Excel 2021, Excel 2019
- Compatible with: LibreOffice Calc (most formatting preserved)
- Google Sheets: Import via File → Import (some conditional formatting may not render)
