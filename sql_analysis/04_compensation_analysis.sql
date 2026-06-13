-- ============================================================
-- Chicago City Workforce Analytics
-- SQL Script 04: Compensation Deep-Dive Analysis
-- ============================================================
-- Author  : Senior Data Analyst Portfolio Project
-- Purpose : Salary bands, pay equity, outlier analysis,
--           compensation benchmarking, job title ranking.
-- ============================================================

-- ──────────────────────────────────────────────────────────
-- Q1: TOTAL PAYROLL SUMMARY
-- ──────────────────────────────────────────────────────────

SELECT
    'CITY TOTAL'              AS scope,
    COUNT(*)                  AS total_employees,
    ROUND(SUM(annual_equivalent), 0)         AS total_annual_payroll,
    ROUND(AVG(annual_equivalent), 0)         AS avg_annual_compensation,
    -- SQLite doesn't have PERCENTILE_CONT; use Python for exact median
    ROUND(MIN(annual_equivalent), 0)         AS min_compensation,
    ROUND(MAX(annual_equivalent), 0)         AS max_compensation
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL;

-- ──────────────────────────────────────────────────────────
-- Q2: TOP 20 JOB TITLES BY AVERAGE COMPENSATION
--     (minimum 10 employees per title for statistical validity)
-- ──────────────────────────────────────────────────────────

SELECT
    job_title,
    COUNT(*)                                AS headcount,
    ROUND(AVG(annual_equivalent), 0)        AS avg_annual_comp,
    ROUND(MIN(annual_equivalent), 0)        AS min_comp,
    ROUND(MAX(annual_equivalent), 0)        AS max_comp,
    ROUND(MAX(annual_equivalent) - MIN(annual_equivalent), 0) AS comp_range,
    ROUND(AVG(annual_equivalent) * COUNT(*), 0) AS dept_payroll_contribution
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
GROUP BY job_title
HAVING COUNT(*) >= 10
ORDER BY avg_annual_comp DESC
LIMIT 20;

-- ──────────────────────────────────────────────────────────
-- Q3: COMPENSATION PERCENTILE BANDS
--     (manual percentile buckets for SQLite compatibility)
-- ──────────────────────────────────────────────────────────

WITH ranked AS (
    SELECT
        annual_equivalent,
        ROW_NUMBER() OVER (ORDER BY annual_equivalent)  AS rn,
        COUNT(*) OVER ()                                AS total_n
    FROM workforce_clean
    WHERE annual_equivalent IS NOT NULL
),
percentiles AS (
    SELECT
        ROUND(annual_equivalent, 0) AS comp_value,
        ROUND(rn * 100.0 / total_n, 1) AS approx_percentile
    FROM ranked
    WHERE rn IN (
        CAST(total_n * 0.10 AS INT),
        CAST(total_n * 0.25 AS INT),
        CAST(total_n * 0.50 AS INT),
        CAST(total_n * 0.75 AS INT),
        CAST(total_n * 0.90 AS INT),
        CAST(total_n * 0.95 AS INT),
        CAST(total_n * 0.99 AS INT)
    )
)
SELECT * FROM percentiles ORDER BY approx_percentile;

-- ──────────────────────────────────────────────────────────
-- Q4: SALARY vs HOURLY COMPARISON (ANNUALIZED)
-- ──────────────────────────────────────────────────────────

SELECT
    pay_type,
    COUNT(*)                                AS employee_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct_workforce,
    ROUND(AVG(annual_equivalent), 0)        AS avg_annual_comp,
    ROUND(MIN(annual_equivalent), 0)        AS min_comp,
    ROUND(MAX(annual_equivalent), 0)        AS max_comp,
    ROUND(SUM(annual_equivalent), 0)        AS total_payroll
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
GROUP BY pay_type
ORDER BY avg_annual_comp DESC;

-- ──────────────────────────────────────────────────────────
-- Q5: FULL-TIME vs PART-TIME COMPENSATION COMPARISON
-- ──────────────────────────────────────────────────────────

SELECT
    CASE employment_type WHEN 'F' THEN 'Full-Time' ELSE 'Part-Time' END AS emp_status,
    COUNT(*)                                  AS headcount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM workforce_clean), 1) AS pct_total,
    ROUND(AVG(annual_equivalent), 0)          AS avg_annual_comp,
    ROUND(SUM(annual_equivalent), 0)          AS total_payroll,
    COUNT(DISTINCT department)                AS dept_count
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
GROUP BY employment_type;

-- ──────────────────────────────────────────────────────────
-- Q6: COMPENSATION BAND DISTRIBUTION WITH PAYROLL SHARE
-- ──────────────────────────────────────────────────────────

WITH totals AS (
    SELECT
        COUNT(*) AS grand_headcount,
        SUM(annual_equivalent) AS grand_payroll
    FROM workforce_clean
    WHERE annual_equivalent IS NOT NULL
)
SELECT
    wc.compensation_tier,
    CASE wc.compensation_tier
        WHEN '1_Under_50K'   THEN 'Under $50,000'
        WHEN '2_50K-75K'     THEN '$50,000 – $74,999'
        WHEN '3_75K-100K'    THEN '$75,000 – $99,999'
        WHEN '4_100K-125K'   THEN '$100,000 – $124,999'
        WHEN '5_125K-150K'   THEN '$125,000 – $149,999'
        WHEN '6_150K_Plus'   THEN '$150,000 and above'
    END AS band_label,
    COUNT(*)                                                  AS headcount,
    ROUND(COUNT(*) * 100.0 / t.grand_headcount, 2)           AS pct_of_workforce,
    ROUND(SUM(wc.annual_equivalent), 0)                       AS total_payroll,
    ROUND(SUM(wc.annual_equivalent) * 100.0 / t.grand_payroll, 2) AS pct_of_payroll,
    ROUND(AVG(wc.annual_equivalent), 0)                       AS avg_comp
FROM workforce_clean wc
CROSS JOIN totals t
WHERE wc.annual_equivalent IS NOT NULL
GROUP BY wc.compensation_tier, t.grand_headcount, t.grand_payroll
ORDER BY wc.compensation_tier;

-- ──────────────────────────────────────────────────────────
-- Q7: HIGH EARNER CONCENTRATION (>$200K Analysis)
-- ──────────────────────────────────────────────────────────

SELECT
    department,
    COUNT(*) AS high_earner_count,
    ROUND(AVG(annual_equivalent), 0) AS avg_high_earner_comp,
    ROUND(MAX(annual_equivalent), 0) AS max_comp,
    job_title
FROM workforce_clean
WHERE annual_equivalent > 200000
GROUP BY department, job_title
ORDER BY high_earner_count DESC, avg_high_earner_comp DESC
LIMIT 25;

-- ──────────────────────────────────────────────────────────
-- Q8: OUTLIER ANALYSIS — IQR METHOD
-- ──────────────────────────────────────────────────────────

WITH quartiles AS (
    SELECT
        -- Approximate Q1 and Q3 using ntile buckets
        MIN(CASE WHEN tile = 1 THEN annual_equivalent END) AS approx_q1,
        MAX(CASE WHEN tile = 3 THEN annual_equivalent END) AS approx_q3
    FROM (
        SELECT
            annual_equivalent,
            NTILE(4) OVER (ORDER BY annual_equivalent) AS tile
        FROM workforce_clean
        WHERE annual_equivalent IS NOT NULL
    )
),
fences AS (
    SELECT
        approx_q1,
        approx_q3,
        approx_q3 - approx_q1 AS iqr,
        approx_q1 - 1.5 * (approx_q3 - approx_q1) AS lower_fence,
        approx_q3 + 1.5 * (approx_q3 - approx_q1) AS upper_fence
    FROM quartiles
)
SELECT
    f.lower_fence,
    f.upper_fence,
    SUM(CASE WHEN wc.annual_equivalent < f.lower_fence THEN 1 ELSE 0 END) AS outlier_low_count,
    SUM(CASE WHEN wc.annual_equivalent > f.upper_fence THEN 1 ELSE 0 END) AS outlier_high_count,
    ROUND(SUM(CASE WHEN wc.annual_equivalent < f.lower_fence THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_low_outliers,
    ROUND(SUM(CASE WHEN wc.annual_equivalent > f.upper_fence THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_high_outliers
FROM workforce_clean wc
CROSS JOIN fences f
WHERE wc.annual_equivalent IS NOT NULL;

-- ──────────────────────────────────────────────────────────
-- Q9: DEPARTMENT COMPENSATION EQUITY RATIO
--     (How does each dept's avg compare to city average?)
-- ──────────────────────────────────────────────────────────

WITH city_avg AS (
    SELECT AVG(annual_equivalent) AS city_mean
    FROM workforce_clean
    WHERE annual_equivalent IS NOT NULL
)
SELECT
    department,
    COUNT(*) AS headcount,
    ROUND(AVG(wc.annual_equivalent), 0) AS dept_avg_comp,
    ROUND(ca.city_mean, 0) AS city_avg_comp,
    ROUND(AVG(wc.annual_equivalent) / ca.city_mean, 3) AS equity_ratio,
    CASE
        WHEN AVG(wc.annual_equivalent) / ca.city_mean > 1.15 THEN 'Well Above Average'
        WHEN AVG(wc.annual_equivalent) / ca.city_mean > 1.05 THEN 'Above Average'
        WHEN AVG(wc.annual_equivalent) / ca.city_mean > 0.95 THEN 'At Average'
        WHEN AVG(wc.annual_equivalent) / ca.city_mean > 0.85 THEN 'Below Average'
        ELSE 'Well Below Average'
    END AS equity_status
FROM workforce_clean wc
CROSS JOIN city_avg ca
WHERE wc.annual_equivalent IS NOT NULL
GROUP BY department, ca.city_mean
HAVING COUNT(*) >= 20
ORDER BY equity_ratio DESC;

-- ──────────────────────────────────────────────────────────
-- Q10: TOP 50 INDIVIDUAL EARNERS
-- ──────────────────────────────────────────────────────────

SELECT
    ROW_NUMBER() OVER (ORDER BY annual_equivalent DESC) AS rank,
    employee_name,
    job_title,
    department,
    pay_type,
    ROUND(annual_equivalent, 0) AS annual_equivalent
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
ORDER BY annual_equivalent DESC
LIMIT 50;
