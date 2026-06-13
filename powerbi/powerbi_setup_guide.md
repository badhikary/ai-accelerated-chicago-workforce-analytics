# Power BI Dashboard Setup Guide
## Chicago City Workforce Analytics

---

## Overview

The Power BI dashboard (`Chicago_Workforce_Dashboard.pbix`) provides an interactive, executive-level view of Chicago's workforce compensation data. It features 5 pages, 20+ visuals, slicers, drill-throughs, and custom DAX measures.

---

## Data Connection Setup

### Step 1: Load the Cleaned Dataset

1. Open Power BI Desktop
2. Click **Home → Get Data → Text/CSV**
3. Navigate to: `data/processed/chicago_workforce_cleaned.csv`
4. Click **Transform Data** to open Power Query Editor
5. Verify column types:
   - `annual_equivalent` → Decimal Number
   - `annual_salary` → Decimal Number
   - `hourly_rate` → Decimal Number
   - `typical_hours` → Whole Number
   - `is_public_safety` → Whole Number
   - `is_fulltime` → Whole Number
   - All others → Text

### Step 2: Load Supporting Tables

Also load:
- `data/processed/department_summary.csv`
- `data/processed/job_title_summary.csv`
- `data/processed/dept_payroll_summary.csv`

---

## DAX Measures (Create in Power BI)

Create a dedicated **Measures Table** (blank table named `_Measures`), then add these DAX measures:

### Core Metrics

```dax
[Total Employees] =
COUNTROWS(chicago_workforce_cleaned)

[Total Annual Payroll] =
SUM(chicago_workforce_cleaned[annual_equivalent])

[Average Compensation] =
AVERAGE(chicago_workforce_cleaned[annual_equivalent])

[Median Compensation] =
MEDIAN(chicago_workforce_cleaned[annual_equivalent])

[Highest Compensation] =
MAX(chicago_workforce_cleaned[annual_equivalent])

[Monthly Payroll Run Rate] =
DIVIDE([Total Annual Payroll], 12)

[Weekly Payroll Run Rate] =
DIVIDE([Total Annual Payroll], 52)
```

### Workforce Composition

```dax
[% Full-Time] =
DIVIDE(
    CALCULATE(COUNTROWS(chicago_workforce_cleaned),
              chicago_workforce_cleaned[employment_type] = "F"),
    [Total Employees]
)

[% Salaried] =
DIVIDE(
    CALCULATE(COUNTROWS(chicago_workforce_cleaned),
              chicago_workforce_cleaned[pay_type] = "SALARY"),
    [Total Employees]
)

[% Public Safety] =
DIVIDE(
    CALCULATE(COUNTROWS(chicago_workforce_cleaned),
              chicago_workforce_cleaned[is_public_safety] = 1),
    [Total Employees]
)

[% Part-Time] =
DIVIDE(
    CALCULATE(COUNTROWS(chicago_workforce_cleaned),
              chicago_workforce_cleaned[employment_type] = "P"),
    [Total Employees]
)
```

### Benchmarking

```dax
[Comp vs City Avg] =
DIVIDE([Average Compensation], 
       CALCULATE(AVERAGE(chicago_workforce_cleaned[annual_equivalent]),
                 ALL(chicago_workforce_cleaned)))

[Payroll % of Total] =
DIVIDE(
    [Total Annual Payroll],
    CALCULATE([Total Annual Payroll], ALL(chicago_workforce_cleaned))
)

[Headcount % of Total] =
DIVIDE(
    [Total Employees],
    CALCULATE([Total Employees], ALL(chicago_workforce_cleaned))
)

[Avg Cost Per Employee] =
DIVIDE([Total Annual Payroll], [Total Employees])
```

### Advanced

```dax
[Payroll Rank by Dept] =
RANKX(
    ALL(chicago_workforce_cleaned[department]),
    [Total Annual Payroll],
    ,
    DESC,
    Dense
)

[Compensation Tier Label] =
SWITCH(
    TRUE(),
    AVERAGE(chicago_workforce_cleaned[annual_equivalent]) < 50000,  "< $50K",
    AVERAGE(chicago_workforce_cleaned[annual_equivalent]) < 75000,  "$50K–$75K",
    AVERAGE(chicago_workforce_cleaned[annual_equivalent]) < 100000, "$75K–$100K",
    AVERAGE(chicago_workforce_cleaned[annual_equivalent]) < 125000, "$100K–$125K",
    AVERAGE(chicago_workforce_cleaned[annual_equivalent]) < 150000, "$125K–$150K",
    "$150K+"
)

[Rolling YTD Payroll] =
CALCULATE(
    [Total Annual Payroll],
    DATESYTD('Date'[Date])
)

[Salaried vs Hourly Gap] =
CALCULATE([Median Compensation], chicago_workforce_cleaned[pay_type] = "SALARY")
-
CALCULATE([Median Compensation], chicago_workforce_cleaned[pay_type] = "HOURLY")
```

---

## Dashboard Pages

### Page 1: Executive Overview
**Layout**: Header + 6 KPI cards + 3 visuals

**Visuals**:
1. **Card** — Total Employees (`[Total Employees]`)
2. **Card** — Total Annual Payroll (`[Total Annual Payroll]`, format: $#,##0.0,,,"B"`)
3. **Card** — Median Compensation (`[Median Compensation]`, format: $#,##0`)
4. **Card** — % Full-Time (`[% Full-Time]`, format: 0.0%`)
5. **Card** — Total Departments (Count of distinct dept)
6. **Card** — % Public Safety (`[% Public Safety]`)
7. **Donut Chart** — Employees by Pay Type (SALARY vs HOURLY)
8. **Bar Chart** — Top 10 Departments by Headcount
9. **Treemap** — Payroll share by department

**Slicers (header area)**:
- Department (dropdown)
- Pay Type (button)
- Employment Type (button)

---

### Page 2: Department Analysis
**Visuals**:
1. **Clustered Bar Chart** — Headcount by Department (all 39)
2. **Waterfall Chart** — Payroll by Department (sorted desc)
3. **Matrix Table** — Department scorecard (headcount, avg comp, total payroll, % of total)
4. **Gauge Chart** — CPD headcount vs city total

**Drill-through**: Click any department → goes to Page 5 (Department Detail)

---

### Page 3: Compensation Deep Dive
**Visuals**:
1. **Histogram** — Annual compensation distribution (bin size = $10K)
2. **Box Plot** — Compensation by department (top 15)
3. **Scatter Plot** — Headcount vs Average Comp (by department, bubble size = total payroll)
4. **Table** — Compensation percentiles (P10, P25, P50, P75, P90, P99)
5. **Stacked Bar** — Compensation tier distribution by department

**Slicers**:
- Pay Type (SALARY / HOURLY)
- Compensation Tier
- Min Compensation (slider)

---

### Page 4: Pay Equity Analysis
**Visuals**:
1. **KPI Card** — Salaried vs Hourly median gap (`[Salaried vs Hourly Gap]`)
2. **Clustered Column** — Avg comp: Salaried vs Hourly (annualized) by dept
3. **Table** — Department equity ratio (with conditional formatting)
4. **Bar Chart** — Full-time vs part-time compensation comparison
5. **Scatter** — Equity ratio by department (x = headcount, y = equity ratio vs city avg)

---

### Page 5: Top Earners & Job Titles
**Visuals**:
1. **Table** — Top 50 individual earners (name, title, dept, compensation)
2. **Bar Chart** — Top 20 job titles by avg compensation
3. **Treemap** — Job title clusters by total payroll
4. **KPI Card** — Highest single earner compensation

---

## Color Theme

Apply this custom theme JSON in Power BI (View → Themes → Browse for themes):

```json
{
  "name": "Chicago Workforce Analytics",
  "dataColors": [
    "#003087", "#E63946", "#2A9D8F", "#F4A261",
    "#6C3483", "#1A3A5C", "#4A90D9", "#F7DC6F"
  ],
  "background": "#FFFFFF",
  "foreground": "#1A1A2E",
  "tableAccent": "#003087"
}
```

---

## Formatting Guidelines

- **Font**: Segoe UI throughout
- **Title font size**: 16pt bold
- **Body font size**: 10pt
- **KPI cards**: Dark navy background, white text
- **Page background**: Light gray (#F8F9FA)
- **Visual borders**: Subtle shadow, rounded corners

---

## Publishing

1. **Save** the .pbix file locally
2. **Publish to Power BI Service**: Home → Publish → Select workspace
3. **Share**: Generate embed code or share link from Power BI Service
4. **Export**: File → Export → Export to PDF for static version

---

## Screenshots for GitHub

Export each page as PNG:
1. File → Export → Export to PDF, then convert PDF pages to PNG
2. Or use Snipping Tool / PrintScreen on each page
3. Save to `powerbi/dashboard_screenshots/` folder
4. Reference in README.md

---

## Performance Tips

- **Disable auto-refresh** for static dataset
- **Disable cross-filtering** on the histogram for faster rendering
- Use **Aggregation Tables** if connecting to live database (>1M rows)
- Apply **Row-Level Security** if sharing with department heads
