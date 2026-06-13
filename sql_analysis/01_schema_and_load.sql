-- ============================================================
-- Chicago City Workforce Analytics
-- SQL Script 01: Schema Creation & Data Load
-- ============================================================
-- Compatible with: SQLite (portable), PostgreSQL, SQL Server
-- Analyst: Senior Data Analyst Portfolio Project
-- Source:  City of Chicago / data.gov (Public Domain)
-- ============================================================

-- ──────────────────────────────────────────────────────────
-- DROP & RECREATE TABLES (idempotent)
-- ──────────────────────────────────────────────────────────

DROP TABLE IF EXISTS workforce_raw;
DROP TABLE IF EXISTS workforce_clean;
DROP VIEW  IF EXISTS vw_dept_summary;
DROP VIEW  IF EXISTS vw_compensation_bands;
DROP VIEW  IF EXISTS vw_payroll_liability;

-- ──────────────────────────────────────────────────────────
-- TABLE: workforce_raw  (mirrors source CSV 1:1)
-- ──────────────────────────────────────────────────────────

CREATE TABLE workforce_raw (
    employee_name    TEXT,
    job_title        TEXT,
    department       TEXT,
    employment_type  TEXT,         -- 'F' or 'P'
    pay_type         TEXT,         -- 'SALARY' or 'HOURLY'
    typical_hours    INTEGER,      -- NULL for salaried
    annual_salary    REAL,         -- NULL for hourly
    hourly_rate      REAL          -- NULL for salaried
);

-- NOTE: To load from CSV in SQLite:
--   .mode csv
--   .headers on
--   .import data/raw/Current_Employee_Names__Salaries__and_Position_Titles.csv workforce_raw

-- ──────────────────────────────────────────────────────────
-- TABLE: workforce_clean  (transformed, production table)
-- ──────────────────────────────────────────────────────────

CREATE TABLE workforce_clean (
    employee_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name      TEXT NOT NULL,
    job_title          TEXT NOT NULL,
    department         TEXT NOT NULL,
    employment_type    TEXT NOT NULL CHECK (employment_type IN ('F','P')),
    pay_type           TEXT NOT NULL CHECK (pay_type IN ('SALARY','HOURLY')),
    typical_hours      INTEGER,
    annual_salary      REAL,
    hourly_rate        REAL,
    -- Derived columns
    annual_equivalent  REAL,       -- normalized annual pay
    compensation_tier  TEXT,       -- salary band label
    is_public_safety   INTEGER DEFAULT 0 CHECK (is_public_safety IN (0,1)),
    is_fulltime        INTEGER DEFAULT 1 CHECK (is_fulltime IN (0,1)),
    is_outlier_high    INTEGER DEFAULT 0,
    is_outlier_low     INTEGER DEFAULT 0,
    load_date          TEXT DEFAULT (DATE('now'))
);

-- ──────────────────────────────────────────────────────────
-- POPULATE workforce_clean FROM workforce_raw
-- (Run after CSV import into workforce_raw)
-- ──────────────────────────────────────────────────────────

INSERT INTO workforce_clean (
    employee_name,
    job_title,
    department,
    employment_type,
    pay_type,
    typical_hours,
    annual_salary,
    hourly_rate,
    annual_equivalent,
    compensation_tier,
    is_public_safety,
    is_fulltime
)
SELECT
    TRIM(UPPER(employee_name))     AS employee_name,
    TRIM(UPPER(job_title))         AS job_title,
    TRIM(UPPER(department))        AS department,
    TRIM(UPPER(employment_type))   AS employment_type,
    TRIM(UPPER(pay_type))          AS pay_type,
    typical_hours,
    annual_salary,
    hourly_rate,

    -- Annual equivalent: salary as-is; hourly × hours × 52
    CASE
        WHEN TRIM(UPPER(pay_type)) = 'SALARY' THEN annual_salary
        WHEN TRIM(UPPER(pay_type)) = 'HOURLY'
             AND hourly_rate IS NOT NULL
             AND typical_hours IS NOT NULL
             THEN ROUND(hourly_rate * typical_hours * 52, 2)
        ELSE NULL
    END AS annual_equivalent,

    -- Compensation tier bands
    CASE
        WHEN (CASE WHEN TRIM(UPPER(pay_type)) = 'SALARY' THEN annual_salary
                   ELSE hourly_rate * typical_hours * 52 END) < 50000
             THEN '1_Under_50K'
        WHEN (CASE WHEN TRIM(UPPER(pay_type)) = 'SALARY' THEN annual_salary
                   ELSE hourly_rate * typical_hours * 52 END) < 75000
             THEN '2_50K-75K'
        WHEN (CASE WHEN TRIM(UPPER(pay_type)) = 'SALARY' THEN annual_salary
                   ELSE hourly_rate * typical_hours * 52 END) < 100000
             THEN '3_75K-100K'
        WHEN (CASE WHEN TRIM(UPPER(pay_type)) = 'SALARY' THEN annual_salary
                   ELSE hourly_rate * typical_hours * 52 END) < 125000
             THEN '4_100K-125K'
        WHEN (CASE WHEN TRIM(UPPER(pay_type)) = 'SALARY' THEN annual_salary
                   ELSE hourly_rate * typical_hours * 52 END) < 150000
             THEN '5_125K-150K'
        ELSE '6_150K_Plus'
    END AS compensation_tier,

    -- Public safety flag
    CASE
        WHEN TRIM(UPPER(department)) IN (
            'CHICAGO POLICE DEPARTMENT',
            'CHICAGO FIRE DEPARTMENT',
            'OFFICE OF EMERGENCY MANAGEMENT AND COMMUNICATIONS'
        ) THEN 1
        ELSE 0
    END AS is_public_safety,

    -- Full-time flag
    CASE WHEN TRIM(UPPER(employment_type)) = 'F' THEN 1 ELSE 0 END AS is_fulltime

FROM workforce_raw
WHERE employee_name IS NOT NULL;

-- ──────────────────────────────────────────────────────────
-- VIEWS: Reusable analytical layers
-- ──────────────────────────────────────────────────────────

-- Departmental summary view
CREATE VIEW vw_dept_summary AS
SELECT
    department,
    COUNT(*)                                          AS headcount,
    SUM(CASE WHEN pay_type = 'SALARY' THEN 1 ELSE 0 END)  AS salaried_count,
    SUM(CASE WHEN pay_type = 'HOURLY' THEN 1 ELSE 0 END)  AS hourly_count,
    SUM(CASE WHEN is_fulltime = 1 THEN 1 ELSE 0 END)       AS fulltime_count,
    SUM(CASE WHEN is_fulltime = 0 THEN 1 ELSE 0 END)       AS parttime_count,
    ROUND(MIN(annual_equivalent), 2)                  AS min_comp,
    ROUND(AVG(annual_equivalent), 2)                  AS avg_comp,
    ROUND(MAX(annual_equivalent), 2)                  AS max_comp,
    ROUND(SUM(annual_equivalent), 2)                  AS total_payroll,
    MAX(is_public_safety)                              AS is_public_safety_dept
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
GROUP BY department;

-- Compensation band view
CREATE VIEW vw_compensation_bands AS
SELECT
    compensation_tier,
    COUNT(*)                          AS headcount,
    ROUND(AVG(annual_equivalent), 2)  AS avg_comp,
    ROUND(SUM(annual_equivalent), 2)  AS total_payroll,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM workforce_clean), 2) AS pct_workforce
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
GROUP BY compensation_tier
ORDER BY compensation_tier;

-- Payroll liability view (includes monthly/weekly)
CREATE VIEW vw_payroll_liability AS
SELECT
    department,
    ROUND(SUM(annual_equivalent), 0)       AS annual_payroll,
    ROUND(SUM(annual_equivalent) / 12, 0)  AS monthly_payroll,
    ROUND(SUM(annual_equivalent) / 52, 0)  AS weekly_payroll,
    COUNT(*)                               AS headcount,
    ROUND(SUM(annual_equivalent) * 100.0 /
        (SELECT SUM(annual_equivalent) FROM workforce_clean
         WHERE annual_equivalent IS NOT NULL), 2) AS pct_of_total_payroll
FROM workforce_clean
WHERE annual_equivalent IS NOT NULL
GROUP BY department
ORDER BY annual_payroll DESC;

-- ──────────────────────────────────────────────────────────
-- INDEXES (performance)
-- ──────────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_wc_department     ON workforce_clean(department);
CREATE INDEX IF NOT EXISTS idx_wc_job_title      ON workforce_clean(job_title);
CREATE INDEX IF NOT EXISTS idx_wc_pay_type       ON workforce_clean(pay_type);
CREATE INDEX IF NOT EXISTS idx_wc_annual_equiv   ON workforce_clean(annual_equivalent);
CREATE INDEX IF NOT EXISTS idx_wc_comp_tier      ON workforce_clean(compensation_tier);
CREATE INDEX IF NOT EXISTS idx_wc_is_public_safe ON workforce_clean(is_public_safety);

-- ──────────────────────────────────────────────────────────
-- VERIFICATION QUERIES
-- ──────────────────────────────────────────────────────────

-- Row count check
SELECT 'workforce_raw'   AS tbl, COUNT(*) AS rows FROM workforce_raw
UNION ALL
SELECT 'workforce_clean' AS tbl, COUNT(*) AS rows FROM workforce_clean;

-- Null check on annual_equivalent
SELECT
    pay_type,
    COUNT(*)                                                 AS total,
    SUM(CASE WHEN annual_equivalent IS NULL THEN 1 ELSE 0 END) AS null_annual_equiv,
    ROUND(SUM(CASE WHEN annual_equivalent IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_null
FROM workforce_clean
GROUP BY pay_type;

-- Schema complete
SELECT 'Schema creation complete. Tables: workforce_raw, workforce_clean. Views: vw_dept_summary, vw_compensation_bands, vw_payroll_liability' AS status;
