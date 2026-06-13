-- ============================================================
-- Chicago City Workforce Analytics
-- SQL Script 05: Pay Equity & Fairness Analysis
-- ============================================================
-- Author  : Senior Data Analyst Portfolio Project
-- Purpose : Identify pay equity patterns, compression,
--           dispersion, and anomalies across groups.
-- ============================================================

-- ──────────────────────────────────────────────────────────
-- Q1: PAY EQUITY RATIO — HOURLY vs SALARIED (ANNUALIZED)
--     Equity ratio: hourly annualized / salaried average
-- ──────────────────────────────────────────────────────────

WITH group_stats AS (
    SELECT
        pay_type,
        COUNT(*)                             AS headcount,
        ROUND(AVG(annual_equivalent), 0)     AS avg_comp,
        ROUND(MIN(annual_equivalent), 0)     AS min_comp,
        ROUND(MAX(annual_equivalent), 0)     AS max_comp,
        ROUND(SUM(annual_equivalent), 0)     AS total_payroll
    FROM workforce_clean
    WHERE annual_equivalent IS NOT NULL
    GROUP BY pay_type
),
salaried_avg AS (
    SELECT avg_comp FROM group_stats WHERE pay_type = 'SALARY'
)
SELECT
    gs.pay_type,
    gs.headcount,
    gs.avg_comp,
    gs.min_comp,
    gs.max_comp,
    gs.total_payroll,
    ROUND(gs.avg_comp / sa.avg_comp, 4) AS equity_ratio_vs_salaried,
    ROUND((1 - gs.avg_comp / sa.avg_comp) * 100, 1) AS pct_gap_vs_salaried
FROM group_stats gs
CROSS JOIN salaried_avg sa
ORDER BY gs.avg_comp DESC;

-- ──────────────────────────────────────────────────────────
-- Q2: SALARY COMPRESSION ANALYSIS
--     (ratio of P90 to P10 within each department)
--     High ratio = wide spread; Low ratio = compressed pay scale
-- ──────────────────────────────────────────────────────────

WITH emp_ranked AS (
    SELECT
        department,
        annual_equivalent,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY annual_equivalent)    AS rn_asc,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY annual_equivalent DESC) AS rn_desc,
        COUNT(*) OVER (PARTITION BY department) AS dept_n
    FROM workforce_clean
    WHERE annual_equivalent IS NOT NULL
),
percentile_approx AS (
    SELECT
        department,
        AVG(CASE WHEN rn_asc  <= dept_n * 0.10 + 1 AND rn_asc  >= dept_n * 0.10 THEN annual_equivalent END) AS p10,
        AVG(CASE WHEN rn_asc  <= dept_n * 0.50 + 1 AND rn_asc  >= dept_n * 0.50 THEN annual_equivalent END) AS p50,
        AVG(CASE WHEN rn_desc <= dept_n * 0.10 + 1 AND rn_desc >= dept_n * 0.10 THEN annual_equivalent END) AS p90,
        MAX(dept_n) AS n
    FROM emp_ranked
    GROUP BY department
)
SELECT
    department,
    n AS headcount,
    ROUND(p10, 0) AS p10_comp,
    ROUND(p50, 0) AS p50_comp,
    ROUND(p90, 0) AS p90_comp,
    ROUND(p90 / NULLIF(p10, 0), 2) AS p90_p10_ratio,
    CASE
        WHEN p90 / NULLIF(p10, 0) < 1.5  THEN 'Highly Compressed'
        WHEN p90 / NULLIF(p10, 0) < 2.0  THEN 'Moderately Compressed'
        WHEN p90 / NULLIF(p10, 0) < 3.0  THEN 'Normal Spread'
        ELSE 'Wide Dispersion'
    END AS compression_label
FROM percentile_approx
WHERE n >= 30 AND p10 IS NOT NULL AND p90 IS NOT NULL
ORDER BY p90_p10_ratio DESC;

-- ──────────────────────────────────────────────────────────
-- Q3: PART-TIME WORKERS — PAY EQUITY CHECK
--     Are part-time hourly rates comparable to full-time?
-- ──────────────────────────────────────────────────────────

SELECT
    employment_type,
    pay_type,
    COUNT(*) AS headcount,
    ROUND(AVG(hourly_rate), 2)       AS avg_hourly_rate,
    ROUND(MIN(hourly_rate), 2)       AS min_hourly_rate,
    ROUND(MAX(hourly_rate), 2)       AS max_hourly_rate,
    ROUND(AVG(typical_hours), 1)     AS avg_weekly_hours,
    ROUND(AVG(annual_equivalent), 0) AS avg_annual_equivalent
FROM workforce_clean
WHERE pay_type = 'HOURLY'
  AND hourly_rate IS NOT NULL
GROUP BY employment_type, pay_type
ORDER BY employment_type;

-- ──────────────────────────────────────────────────────────
-- Q4: INTRA-DEPARTMENT PAY EQUITY
--     Standard deviation within each department (high = less equitable)
-- ──────────────────────────────────────────────────────────

SELECT
    department,
    COUNT(*) AS headcount,
    ROUND(AVG(annual_equivalent), 0) AS avg_comp,
    -- SQLite approximation: manual variance
    ROUND(
        SQRT(AVG(annual_equivalent * annual_equivalent) - AVG(annual_equivalent) * AVG(annual_equivalent))
    , 0) AS std_dev_comp,
    ROUND(
        SQRT(AVG(annual_equivalent * annual_equivalent) - AVG(annual_equivalent) * AVG(annual_equivalent))
        / AVG(annual_equivalent) * 100
    , 1) AS coeff_of_variation_pct,
    CASE
        WHEN SQRT(AVG(annual_equivalent * annual_equivalent) - AVG(annual_equivalent) * AVG(annual_equivalent))
             / AVG(annual_equivalent) * 100 < 15 THEN 'Low Dispersion (Equitable)'
        WHEN SQRT(AVG(annual_equivalent * annual_equivalent) - AVG(annual_equivalent) * AVG(annual_equivalent))
             / AVG(annual_equivalent) * 100 < 30 THEN 'Moderate Dispersion'
        ELSE 'High Dispersion (Review Recommended)'
    END AS equity_flag
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
GROUP BY department
HAVING COUNT(*) >= 50
ORDER BY coeff_of_variation_pct DESC;

-- ──────────────────────────────────────────────────────────
-- Q5: ANOMALY DETECTION — UNUSUALLY LOW SALARIES
--     Employees earning below $30,000 annually (potential data issues
--     or genuine low-wage roles requiring attention)
-- ──────────────────────────────────────────────────────────

SELECT
    employee_name,
    job_title,
    department,
    pay_type,
    employment_type,
    ROUND(annual_equivalent, 0) AS annual_equivalent,
    CASE
        WHEN annual_equivalent < 10000 THEN 'Stipend / Elected Official'
        WHEN annual_equivalent < 20000 THEN 'Very Low — Review Required'
        ELSE 'Low Wage Role'
    END AS anomaly_category
FROM workforce_clean
WHERE annual_equivalent < 30000
  AND annual_equivalent IS NOT NULL
ORDER BY annual_equivalent ASC;

-- ──────────────────────────────────────────────────────────
-- Q6: SAME TITLE, DIFFERENT DEPARTMENTS — EQUITY CHECK
--     Do identical job titles pay differently across departments?
-- ──────────────────────────────────────────────────────────

WITH title_cross AS (
    SELECT
        job_title,
        department,
        COUNT(*) AS headcount,
        ROUND(AVG(annual_equivalent), 0) AS avg_comp
    FROM workforce_clean
    WHERE annual_equivalent IS NOT NULL
    GROUP BY job_title, department
),
title_stats AS (
    SELECT
        job_title,
        COUNT(DISTINCT department) AS dept_count,
        MIN(avg_comp) AS min_dept_avg,
        MAX(avg_comp) AS max_dept_avg,
        ROUND(MAX(avg_comp) - MIN(avg_comp), 0) AS pay_gap_across_depts,
        ROUND(MAX(avg_comp) / NULLIF(MIN(avg_comp), 0) - 1, 3) AS pay_gap_pct
    FROM title_cross
    GROUP BY job_title
    HAVING COUNT(DISTINCT department) >= 2  -- title exists in 2+ departments
)
SELECT
    ts.job_title,
    ts.dept_count,
    ts.min_dept_avg,
    ts.max_dept_avg,
    ts.pay_gap_across_depts,
    ROUND(ts.pay_gap_pct * 100, 1) AS pay_gap_pct,
    CASE
        WHEN ts.pay_gap_pct > 0.25 THEN '⚠ Significant Cross-Dept Pay Gap'
        WHEN ts.pay_gap_pct > 0.10 THEN '↗ Moderate Gap — Monitor'
        ELSE '✓ Consistent Pay'
    END AS equity_flag
FROM title_stats ts
ORDER BY ts.pay_gap_across_depts DESC
LIMIT 30;

-- ──────────────────────────────────────────────────────────
-- Q7: HIGH EARNER vs LOW EARNER RATIO BY DEPARTMENT
--     (Top 10% earners vs bottom 10% earners — inequality metric)
-- ──────────────────────────────────────────────────────────

WITH deciles AS (
    SELECT
        department,
        annual_equivalent,
        NTILE(10) OVER (PARTITION BY department ORDER BY annual_equivalent) AS decile
    FROM workforce_clean
    WHERE annual_equivalent IS NOT NULL
)
SELECT
    department,
    ROUND(AVG(CASE WHEN decile = 10 THEN annual_equivalent END), 0)  AS top_10pct_avg,
    ROUND(AVG(CASE WHEN decile = 1  THEN annual_equivalent END), 0)  AS bot_10pct_avg,
    ROUND(
        AVG(CASE WHEN decile = 10 THEN annual_equivalent END) /
        NULLIF(AVG(CASE WHEN decile = 1 THEN annual_equivalent END), 0),
        2
    ) AS d10_d1_ratio,
    COUNT(*) AS headcount
FROM deciles
GROUP BY department
HAVING COUNT(*) >= 50
   AND AVG(CASE WHEN decile = 1 THEN annual_equivalent END) > 0
ORDER BY d10_d1_ratio DESC;
