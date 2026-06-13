-- ============================================================
-- Chicago City Workforce Analytics
-- SQL Script 02: Workforce Summary Queries
-- ============================================================
-- Author  : Senior Data Analyst Portfolio Project
-- Purpose : High-level workforce KPIs, headcount breakdowns,
--           employment composition, department rankings.
-- ============================================================

-- ──────────────────────────────────────────────────────────
-- Q1: CITY-WIDE WORKFORCE SNAPSHOT (EXECUTIVE KPI ROW)
-- ──────────────────────────────────────────────────────────

SELECT
    COUNT(*)                                                      AS total_employees,
    COUNT(DISTINCT department)                                    AS total_departments,
    COUNT(DISTINCT job_title)                                     AS unique_job_titles,
    SUM(CASE WHEN employment_type = 'F' THEN 1 ELSE 0 END)       AS fulltime_count,
    SUM(CASE WHEN employment_type = 'P' THEN 1 ELSE 0 END)       AS parttime_count,
    ROUND(SUM(CASE WHEN employment_type = 'F' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_fulltime,
    SUM(CASE WHEN pay_type = 'SALARY' THEN 1 ELSE 0 END)         AS salaried_count,
    SUM(CASE WHEN pay_type = 'HOURLY' THEN 1 ELSE 0 END)         AS hourly_count,
    SUM(CASE WHEN is_public_safety = 1 THEN 1 ELSE 0 END)        AS public_safety_count,
    ROUND(SUM(CASE WHEN is_public_safety = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS pct_public_safety
FROM workforce_clean;

-- ──────────────────────────────────────────────────────────
-- Q2: HEADCOUNT BY DEPARTMENT (ALL 39 DEPARTMENTS)
-- ──────────────────────────────────────────────────────────

SELECT
    department,
    COUNT(*)                                                        AS headcount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM workforce_clean), 2) AS pct_of_workforce,
    SUM(CASE WHEN employment_type = 'F' THEN 1 ELSE 0 END)          AS fulltime,
    SUM(CASE WHEN employment_type = 'P' THEN 1 ELSE 0 END)          AS parttime,
    SUM(CASE WHEN pay_type = 'SALARY'   THEN 1 ELSE 0 END)          AS salaried,
    SUM(CASE WHEN pay_type = 'HOURLY'   THEN 1 ELSE 0 END)          AS hourly,
    COUNT(DISTINCT job_title)                                        AS unique_titles
FROM workforce_clean
GROUP BY department
ORDER BY headcount DESC;

-- ──────────────────────────────────────────────────────────
-- Q3: EMPLOYMENT TYPE BREAKDOWN WITH CUMULATIVE %
-- ──────────────────────────────────────────────────────────

WITH dept_counts AS (
    SELECT
        department,
        COUNT(*) AS headcount
    FROM workforce_clean
    GROUP BY department
    ORDER BY headcount DESC
)
SELECT
    department,
    headcount,
    ROUND(headcount * 100.0 / SUM(headcount) OVER (), 2) AS pct_workforce,
    SUM(headcount) OVER (ORDER BY headcount DESC) AS cumulative_headcount,
    ROUND(SUM(headcount) OVER (ORDER BY headcount DESC) * 100.0 /
          SUM(headcount) OVER (), 1) AS cumulative_pct
FROM dept_counts;

-- ──────────────────────────────────────────────────────────
-- Q4: TOP 20 MOST COMMON JOB TITLES
-- ──────────────────────────────────────────────────────────

SELECT
    job_title,
    COUNT(*)                                                      AS headcount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM workforce_clean), 2) AS pct_of_workforce,
    COUNT(DISTINCT department)                                    AS departments_present,
    SUM(CASE WHEN employment_type = 'F' THEN 1 ELSE 0 END)       AS fulltime_count,
    SUM(CASE WHEN pay_type = 'SALARY'   THEN 1 ELSE 0 END)       AS salaried_count
FROM workforce_clean
GROUP BY job_title
ORDER BY headcount DESC
LIMIT 20;

-- ──────────────────────────────────────────────────────────
-- Q5: WORKFORCE MIX — 2×2 CROSS-TAB (Pay Type × Employment Type)
-- ──────────────────────────────────────────────────────────

SELECT
    pay_type,
    SUM(CASE WHEN employment_type = 'F' THEN 1 ELSE 0 END)  AS fulltime_count,
    SUM(CASE WHEN employment_type = 'P' THEN 1 ELSE 0 END)  AS parttime_count,
    COUNT(*)                                                  AS total,
    ROUND(SUM(CASE WHEN employment_type = 'F' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS pct_fulltime
FROM workforce_clean
GROUP BY pay_type
UNION ALL
SELECT
    'TOTAL' AS pay_type,
    SUM(CASE WHEN employment_type = 'F' THEN 1 ELSE 0 END),
    SUM(CASE WHEN employment_type = 'P' THEN 1 ELSE 0 END),
    COUNT(*),
    ROUND(SUM(CASE WHEN employment_type = 'F' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1)
FROM workforce_clean;

-- ──────────────────────────────────────────────────────────
-- Q6: PUBLIC SAFETY vs. CIVILIAN WORKFORCE SPLIT
-- ──────────────────────────────────────────────────────────

SELECT
    CASE is_public_safety WHEN 1 THEN 'Public Safety' ELSE 'Civilian' END AS workforce_segment,
    COUNT(*)                                                     AS headcount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM workforce_clean), 1) AS pct_of_total,
    COUNT(DISTINCT department)                                   AS departments,
    COUNT(DISTINCT job_title)                                    AS unique_titles,
    ROUND(AVG(annual_equivalent), 0)                             AS avg_annual_comp,
    ROUND(SUM(annual_equivalent), 0)                             AS total_payroll
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
GROUP BY is_public_safety
ORDER BY is_public_safety DESC;

-- ──────────────────────────────────────────────────────────
-- Q7: DEPARTMENTS WITH ONLY ONE EMPLOYMENT TYPE
--     (fully hourly or fully salaried departments)
-- ──────────────────────────────────────────────────────────

SELECT
    department,
    COUNT(*) AS headcount,
    COUNT(DISTINCT pay_type) AS pay_type_variety,
    MAX(pay_type) AS pay_type_used,
    ROUND(AVG(annual_equivalent), 0) AS avg_comp
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
GROUP BY department
HAVING COUNT(DISTINCT pay_type) = 1
ORDER BY headcount DESC;

-- ──────────────────────────────────────────────────────────
-- Q8: SMALL DEPARTMENTS (< 50 EMPLOYEES)
-- ──────────────────────────────────────────────────────────

SELECT
    department,
    COUNT(*) AS headcount,
    COUNT(DISTINCT job_title) AS unique_titles,
    ROUND(AVG(annual_equivalent), 0) AS avg_comp,
    ROUND(MAX(annual_equivalent), 0) AS max_comp
FROM workforce_clean
GROUP BY department
HAVING COUNT(*) < 50
ORDER BY headcount DESC;
