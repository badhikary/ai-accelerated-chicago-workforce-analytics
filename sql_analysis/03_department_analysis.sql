-- ============================================================
-- Chicago City Workforce Analytics
-- SQL Script 03: Department-Level Analysis
-- ============================================================
-- Author  : Senior Data Analyst Portfolio Project
-- Purpose : Deep dive into department compensation, staffing,
--           payroll concentration, benchmarking vs. city average.
-- ============================================================

-- ──────────────────────────────────────────────────────────
-- Q1: FULL DEPARTMENT SCORECARD
-- ──────────────────────────────────────────────────────────

WITH city_stats AS (
    SELECT
        AVG(annual_equivalent)  AS city_avg,
        SUM(annual_equivalent)  AS city_total_payroll
    FROM workforce_clean
    WHERE annual_equivalent IS NOT NULL
)
SELECT
    d.department,
    d.headcount,
    d.salaried_count,
    d.hourly_count,
    d.fulltime_count,
    d.parttime_count,
    ROUND(d.min_comp,  0)  AS min_comp,
    ROUND(d.avg_comp,  0)  AS avg_comp,
    ROUND(d.max_comp,  0)  AS max_comp,
    ROUND(d.total_payroll, 0) AS total_payroll,
    ROUND(d.total_payroll / cs.city_total_payroll * 100, 2) AS pct_of_payroll,
    ROUND(d.avg_comp / cs.city_avg, 3) AS avg_vs_city_ratio,
    CASE
        WHEN d.avg_comp / cs.city_avg > 1.15 THEN '▲▲ Well Above'
        WHEN d.avg_comp / cs.city_avg > 1.05 THEN '▲ Above'
        WHEN d.avg_comp / cs.city_avg > 0.95 THEN '● At Average'
        WHEN d.avg_comp / cs.city_avg > 0.85 THEN '▼ Below'
        ELSE '▼▼ Well Below'
    END AS vs_city_benchmark
FROM vw_dept_summary d
CROSS JOIN city_stats cs
ORDER BY d.headcount DESC;

-- ──────────────────────────────────────────────────────────
-- Q2: PARETO ANALYSIS — 80% OF PAYROLL
-- ──────────────────────────────────────────────────────────

WITH dept_payroll AS (
    SELECT
        department,
        ROUND(SUM(annual_equivalent), 0) AS dept_payroll
    FROM workforce_clean
    WHERE annual_equivalent IS NOT NULL
    GROUP BY department
),
ranked AS (
    SELECT
        department,
        dept_payroll,
        SUM(dept_payroll) OVER ()                                   AS total_payroll,
        SUM(dept_payroll) OVER (ORDER BY dept_payroll DESC)         AS running_total,
        ROUND(SUM(dept_payroll) OVER (ORDER BY dept_payroll DESC) * 100.0
              / SUM(dept_payroll) OVER (), 1)                       AS cumulative_pct,
        ROW_NUMBER() OVER (ORDER BY dept_payroll DESC)              AS rank
    FROM dept_payroll
)
SELECT
    rank,
    department,
    dept_payroll,
    ROUND(dept_payroll * 100.0 / total_payroll, 2) AS pct_of_payroll,
    running_total,
    cumulative_pct,
    CASE WHEN cumulative_pct <= 80 THEN 'Top 80%' ELSE 'Remaining 20%' END AS pareto_segment
FROM ranked
ORDER BY rank;

-- ──────────────────────────────────────────────────────────
-- Q3: DEPARTMENT × JOB TITLE MATRIX
--     Top 5 titles per department by headcount
-- ──────────────────────────────────────────────────────────

WITH ranked_titles AS (
    SELECT
        department,
        job_title,
        COUNT(*) AS headcount,
        ROUND(AVG(annual_equivalent), 0) AS avg_comp,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY COUNT(*) DESC) AS title_rank
    FROM workforce_clean
    WHERE annual_equivalent IS NOT NULL
    GROUP BY department, job_title
)
SELECT
    department,
    title_rank,
    job_title,
    headcount,
    avg_comp
FROM ranked_titles
WHERE title_rank <= 5
ORDER BY department, title_rank;

-- ──────────────────────────────────────────────────────────
-- Q4: DEPARTMENT COMPENSATION RANGE ANALYSIS
--     (spread between min and max within dept — indicates title diversity)
-- ──────────────────────────────────────────────────────────

SELECT
    department,
    COUNT(*) AS headcount,
    ROUND(MIN(annual_equivalent), 0) AS min_comp,
    ROUND(MAX(annual_equivalent), 0) AS max_comp,
    ROUND(MAX(annual_equivalent) - MIN(annual_equivalent), 0) AS comp_spread,
    ROUND(AVG(annual_equivalent), 0) AS avg_comp,
    ROUND((MAX(annual_equivalent) - MIN(annual_equivalent)) / AVG(annual_equivalent), 3) AS spread_to_avg_ratio
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
GROUP BY department
HAVING COUNT(*) >= 20
ORDER BY comp_spread DESC;

-- ──────────────────────────────────────────────────────────
-- Q5: INTER-DEPARTMENT COMPARISON — PUBLIC SAFETY TRIO
-- ──────────────────────────────────────────────────────────

SELECT
    department,
    COUNT(*)                                    AS headcount,
    ROUND(AVG(annual_equivalent), 0)            AS avg_comp,
    ROUND(MIN(annual_equivalent), 0)            AS min_comp,
    ROUND(MAX(annual_equivalent), 0)            AS max_comp,
    ROUND(SUM(annual_equivalent), 0)            AS total_payroll,
    COUNT(DISTINCT job_title)                   AS unique_titles,
    SUM(CASE WHEN employment_type = 'F' THEN 1 ELSE 0 END) AS fulltime,
    SUM(CASE WHEN pay_type = 'HOURLY' THEN 1 ELSE 0 END)   AS hourly_workers
FROM workforce_clean
WHERE department IN (
    'CHICAGO POLICE DEPARTMENT',
    'CHICAGO FIRE DEPARTMENT',
    'OFFICE OF EMERGENCY MANAGEMENT AND COMMUNICATIONS'
)
AND annual_equivalent IS NOT NULL
GROUP BY department
ORDER BY total_payroll DESC;

-- ──────────────────────────────────────────────────────────
-- Q6: DEPARTMENTS RANKED BY MEDIAN COMPENSATION
--     (uses approximation via ntile for SQLite compatibility)
-- ──────────────────────────────────────────────────────────

WITH ranked_emp AS (
    SELECT
        department,
        annual_equivalent,
        ROW_NUMBER()  OVER (PARTITION BY department ORDER BY annual_equivalent) AS rn,
        COUNT(*)      OVER (PARTITION BY department)                            AS dept_n
    FROM workforce_clean
    WHERE annual_equivalent IS NOT NULL
),
dept_medians AS (
    SELECT
        department,
        AVG(annual_equivalent) AS median_approx   -- median of middle rows
    FROM ranked_emp
    WHERE rn IN (
        CAST((dept_n + 1) / 2 AS INT),
        CAST((dept_n + 2) / 2 AS INT)
    )
    GROUP BY department
)
SELECT
    dm.department,
    ROUND(dm.median_approx, 0)  AS median_comp,
    COUNT(wc.employee_id)       AS headcount
FROM dept_medians dm
JOIN workforce_clean wc ON wc.department = dm.department
WHERE wc.annual_equivalent IS NOT NULL
GROUP BY dm.department, dm.median_approx
ORDER BY median_approx DESC;

-- ──────────────────────────────────────────────────────────
-- Q7: HOURLY WORKERS BY DEPARTMENT — EXPOSURE ANALYSIS
--     (Hourly staff = variable cost; more = higher budget volatility)
-- ──────────────────────────────────────────────────────────

SELECT
    department,
    COUNT(*) AS total_staff,
    SUM(CASE WHEN pay_type = 'HOURLY' THEN 1 ELSE 0 END) AS hourly_count,
    ROUND(SUM(CASE WHEN pay_type = 'HOURLY' THEN 1.0 ELSE 0 END)
          / COUNT(*) * 100, 1) AS pct_hourly,
    ROUND(AVG(CASE WHEN pay_type = 'HOURLY' THEN hourly_rate END), 2) AS avg_hourly_rate,
    ROUND(AVG(CASE WHEN pay_type = 'HOURLY' THEN typical_hours END), 1) AS avg_weekly_hours
FROM workforce_clean
GROUP BY department
HAVING SUM(CASE WHEN pay_type = 'HOURLY' THEN 1 ELSE 0 END) > 0
ORDER BY pct_hourly DESC;
