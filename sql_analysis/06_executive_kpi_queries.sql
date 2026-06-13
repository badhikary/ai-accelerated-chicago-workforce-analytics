-- ============================================================
-- Chicago City Workforce Analytics
-- SQL Script 06: Executive KPI Dashboard Queries
-- ============================================================
-- Author  : Senior Data Analyst Portfolio Project
-- Purpose : Power BI / Tableau ready KPI queries — all the
--           measures needed to drive an executive dashboard.
--           Each query returns a single, presentation-ready result.
-- ============================================================

-- ──────────────────────────────────────────────────────────
-- KPI 01: HEADLINE METRICS (Single-row summary for scorecards)
-- ──────────────────────────────────────────────────────────

SELECT
    COUNT(*)                                                              AS kpi_total_employees,
    COUNT(DISTINCT department)                                            AS kpi_total_departments,
    COUNT(DISTINCT job_title)                                             AS kpi_unique_job_titles,
    ROUND(SUM(annual_equivalent), 0)                                      AS kpi_total_annual_payroll,
    ROUND(AVG(annual_equivalent), 0)                                      AS kpi_avg_compensation,
    ROUND(MAX(annual_equivalent), 0)                                      AS kpi_highest_salary,
    ROUND(SUM(CASE WHEN is_fulltime = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS kpi_pct_fulltime,
    ROUND(SUM(CASE WHEN pay_type = 'SALARY' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS kpi_pct_salaried,
    ROUND(SUM(CASE WHEN is_public_safety = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS kpi_pct_public_safety,
    ROUND(SUM(annual_equivalent) / 12, 0)                                 AS kpi_monthly_payroll_run_rate,
    ROUND(SUM(annual_equivalent) / COUNT(*), 0)                           AS kpi_avg_cost_per_employee
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL;

-- ──────────────────────────────────────────────────────────
-- KPI 02: DEPARTMENT PERFORMANCE TABLE (Power BI Table Visual)
-- ──────────────────────────────────────────────────────────

SELECT
    department                                                             AS "Department",
    COUNT(*)                                                               AS "Headcount",
    ROUND(SUM(annual_equivalent) / 1000000.0, 2)                           AS "Payroll ($M)",
    ROUND(AVG(annual_equivalent), 0)                                       AS "Avg Comp ($)",
    ROUND(MAX(annual_equivalent), 0)                                       AS "Max Comp ($)",
    ROUND(SUM(CASE WHEN is_public_safety=1 THEN 1.0 ELSE 0 END)/COUNT(*)*100,0) AS "% Public Safety",
    ROUND(SUM(CASE WHEN is_fulltime=1 THEN 1.0 ELSE 0 END)/COUNT(*)*100,0) AS "% Full-Time",
    ROUND(SUM(annual_equivalent)/SUM(SUM(annual_equivalent)) OVER ()*100,2) AS "% of Total Payroll"
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
GROUP BY department
ORDER BY SUM(annual_equivalent) DESC;

-- ──────────────────────────────────────────────────────────
-- KPI 03: COMPENSATION BAND FUNNEL (for funnel/waterfall visual)
-- ──────────────────────────────────────────────────────────

SELECT
    CASE compensation_tier
        WHEN '1_Under_50K'  THEN 'Under $50K'
        WHEN '2_50K-75K'    THEN '$50K–$75K'
        WHEN '3_75K-100K'   THEN '$75K–$100K'
        WHEN '4_100K-125K'  THEN '$100K–$125K'
        WHEN '5_125K-150K'  THEN '$125K–$150K'
        WHEN '6_150K_Plus'  THEN '$150K+'
    END                                                  AS "Compensation Band",
    COUNT(*)                                             AS "Employee Count",
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1)  AS "% of Workforce",
    ROUND(SUM(annual_equivalent)/1000000.0, 1)           AS "Payroll ($M)",
    ROUND(SUM(annual_equivalent)*100.0
          / SUM(SUM(annual_equivalent)) OVER (), 1)      AS "% of Payroll"
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
GROUP BY compensation_tier
ORDER BY compensation_tier;

-- ──────────────────────────────────────────────────────────
-- KPI 04: MONTHLY PAYROLL RUN RATE BY DEPARTMENT (Bar/column chart data)
-- ──────────────────────────────────────────────────────────

SELECT
    department                                              AS "Department",
    ROUND(SUM(annual_equivalent) / 12, 0)                  AS "Monthly Payroll ($)",
    ROUND(SUM(annual_equivalent) / 52, 0)                  AS "Weekly Payroll ($)",
    ROUND(SUM(annual_equivalent) / 260, 0)                 AS "Daily Payroll ($)",
    COUNT(*)                                               AS "Headcount",
    ROUND(AVG(annual_equivalent) / 12, 0)                  AS "Avg Monthly Cost/Employee ($)"
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
GROUP BY department
ORDER BY SUM(annual_equivalent) DESC
LIMIT 15;

-- ──────────────────────────────────────────────────────────
-- KPI 05: TOP 10 HIGHEST-PAYING JOB TITLES (Table visual)
-- ──────────────────────────────────────────────────────────

SELECT
    job_title                                             AS "Job Title",
    COUNT(*)                                              AS "Headcount",
    ROUND(AVG(annual_equivalent), 0)                      AS "Avg Annual Comp ($)",
    ROUND(MAX(annual_equivalent), 0)                      AS "Max Annual Comp ($)",
    ROUND(SUM(annual_equivalent) / 1000000.0, 2)          AS "Total Payroll ($M)"
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
GROUP BY job_title
HAVING COUNT(*) >= 5
ORDER BY AVG(annual_equivalent) DESC
LIMIT 10;

-- ──────────────────────────────────────────────────────────
-- KPI 06: WORKFORCE COMPOSITION PIE DATA
-- ──────────────────────────────────────────────────────────

-- By Pay Type
SELECT 'Pay Type' AS dimension, pay_type AS segment, COUNT(*) AS value
FROM workforce_clean GROUP BY pay_type
UNION ALL
-- By Employment Type
SELECT 'Employment Type', 
    CASE employment_type WHEN 'F' THEN 'Full-Time' ELSE 'Part-Time' END,
    COUNT(*) FROM workforce_clean GROUP BY employment_type
UNION ALL
-- By Workforce Segment
SELECT 'Workforce Segment',
    CASE is_public_safety WHEN 1 THEN 'Public Safety' ELSE 'Civilian' END,
    COUNT(*) FROM workforce_clean GROUP BY is_public_safety;

-- ──────────────────────────────────────────────────────────
-- KPI 07: COMPENSATION BENCHMARK vs. U.S. AVERAGES
--         (U.S. benchmarks hardcoded from BLS 2024 data)
-- ──────────────────────────────────────────────────────────

WITH city_stats AS (
    SELECT
        AVG(annual_equivalent) AS chicago_avg,
        COUNT(*) AS chicago_n
    FROM workforce_clean WHERE annual_equivalent IS NOT NULL
)
SELECT
    'Chicago City Employees'        AS entity,
    ROUND(cs.chicago_avg, 0)        AS avg_annual_comp,
    cs.chicago_n                    AS employee_count,
    ROUND(cs.chicago_avg / 63795 - 1, 3) * 100 AS pct_above_us_median_worker
FROM city_stats cs
UNION ALL
SELECT 'U.S. Median Worker (BLS 2024)', 63795,  NULL, NULL UNION ALL
SELECT 'U.S. Median Household Income',  80610,  NULL, NULL UNION ALL
SELECT 'U.S. Federal Employee Avg',    101397,  NULL, NULL UNION ALL
SELECT 'Illinois Avg Annual Wage',      72130,  NULL, NULL;

-- ──────────────────────────────────────────────────────────
-- KPI 08: PAYROLL CONCENTRATION INDEX (Herfindahl-inspired)
--         Measures how concentrated payroll is across departments
-- ──────────────────────────────────────────────────────────

WITH dept_shares AS (
    SELECT
        department,
        SUM(annual_equivalent) AS dept_payroll,
        SUM(annual_equivalent) / SUM(SUM(annual_equivalent)) OVER () AS share
    FROM workforce_clean
    WHERE annual_equivalent IS NOT NULL
    GROUP BY department
)
SELECT
    ROUND(SUM(share * share), 4)            AS payroll_hhi,
    ROUND(SUM(share * share) * 10000, 1)    AS payroll_hhi_scaled,
    COUNT(*)                                AS dept_count,
    CASE
        WHEN SUM(share * share) > 0.25 THEN 'Highly Concentrated'
        WHEN SUM(share * share) > 0.15 THEN 'Moderately Concentrated'
        ELSE 'Diversified'
    END AS concentration_level,
    'Higher HHI = more payroll in fewer departments' AS interpretation
FROM dept_shares;
