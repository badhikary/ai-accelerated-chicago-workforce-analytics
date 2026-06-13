"""
============================================================
Chicago City Workforce Analytics
Script 01: Data Ingestion, Profiling & Cleaning
============================================================
Author  : Senior Data Analyst Portfolio Project
Dataset : City of Chicago – Current Employee Names, Salaries,
          and Position Titles (data.gov)
Purpose : Load raw data, profile it, clean and transform it,
          and export a production-ready cleaned dataset.
============================================================
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

# ──────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────
RAW_PATH    = "data/raw/Current_Employee_Names__Salaries__and_Position_Titles.csv"
CLEAN_CSV   = "data/processed/chicago_workforce_cleaned.csv"
CLEAN_PARQ  = "data/processed/chicago_workforce_cleaned.parquet"
PROFILE_OUT = "data/processed/data_profile_report.json"

os.makedirs("data/processed", exist_ok=True)

print("=" * 60)
print("  CHICAGO WORKFORCE ANALYTICS — STEP 01: DATA INGESTION")
print("=" * 60)

# ──────────────────────────────────────────────
# 1. LOAD RAW DATA
# ──────────────────────────────────────────────
print("\n[1] Loading raw dataset...")
df_raw = pd.read_csv(RAW_PATH)
print(f"    ✓ Loaded {df_raw.shape[0]:,} rows × {df_raw.shape[1]} columns")

# ──────────────────────────────────────────────
# 2. DATA PROFILING
# ──────────────────────────────────────────────
print("\n[2] Running data profile...")

profile = {
    "profile_generated_at": datetime.now().isoformat(),
    "source_file": RAW_PATH,
    "shape": {"rows": df_raw.shape[0], "columns": df_raw.shape[1]},
    "columns": {}
}

for col in df_raw.columns:
    s = df_raw[col]
    col_profile = {
        "dtype": str(s.dtype),
        "null_count": int(s.isnull().sum()),
        "null_pct": round(s.isnull().mean() * 100, 2),
        "unique_count": int(s.nunique()),
    }
    if s.dtype in [np.float64, np.int64]:
        col_profile.update({
            "min":    round(float(s.min()), 2),
            "max":    round(float(s.max()), 2),
            "mean":   round(float(s.mean()), 2),
            "median": round(float(s.median()), 2),
            "std":    round(float(s.std()), 2),
            "p25":    round(float(s.quantile(0.25)), 2),
            "p75":    round(float(s.quantile(0.75)), 2),
        })
    else:
        col_profile["top_values"] = s.value_counts().head(5).to_dict()
    profile["columns"][col] = col_profile

with open(PROFILE_OUT, "w") as f:
    json.dump(profile, f, indent=2)
print(f"    ✓ Profile saved → {PROFILE_OUT}")

# Print summary
print("\n    Column Summary:")
print(f"    {'Column':<40} {'Dtype':<12} {'Nulls':>8} {'Null%':>7} {'Unique':>8}")
print("    " + "─" * 79)
for col, meta in profile["columns"].items():
    print(f"    {col:<40} {meta['dtype']:<12} {meta['null_count']:>8,} {meta['null_pct']:>6.1f}% {meta['unique_count']:>8,}")

# ──────────────────────────────────────────────
# 3. DATA CLEANING
# ──────────────────────────────────────────────
print("\n[3] Cleaning data...")
df = df_raw.copy()

# 3a. Standardize column names (snake_case)
df.columns = [
    "employee_name",
    "job_title",
    "department",
    "employment_type",   # F / P
    "pay_type",          # SALARY / HOURLY
    "typical_hours",
    "annual_salary",
    "hourly_rate"
]
print("    ✓ Column names standardized to snake_case")

# 3b. Strip whitespace from string columns
str_cols = ["employee_name", "job_title", "department", "employment_type", "pay_type"]
for col in str_cols:
    df[col] = df[col].str.strip().str.upper()
print("    ✓ String columns stripped and uppercased")

# 3c. Validate pay_type / compensation columns alignment
salary_employees = df[df["pay_type"] == "SALARY"]
hourly_employees = df[df["pay_type"] == "HOURLY"]

n_salary_no_val = salary_employees["annual_salary"].isnull().sum()
n_hourly_no_val = hourly_employees["hourly_rate"].isnull().sum()

print(f"    ✓ Salaried employees missing annual_salary: {n_salary_no_val}")
print(f"    ✓ Hourly employees missing hourly_rate: {n_hourly_no_val}")

# ──────────────────────────────────────────────
# 4. FEATURE ENGINEERING
# ──────────────────────────────────────────────
print("\n[4] Engineering derived features...")

# 4a. Annual equivalent compensation (normalize to annual basis)
def compute_annual_equivalent(row):
    if row["pay_type"] == "SALARY":
        return row["annual_salary"]
    elif row["pay_type"] == "HOURLY" and pd.notna(row["hourly_rate"]) and pd.notna(row["typical_hours"]):
        return round(row["hourly_rate"] * row["typical_hours"] * 52, 2)
    return np.nan

df["annual_equivalent"] = df.apply(compute_annual_equivalent, axis=1)
n_annualized = df["annual_equivalent"].notna().sum()
print(f"    ✓ annual_equivalent computed for {n_annualized:,} employees")

# 4b. Compensation tier bands
def compensation_tier(val):
    if pd.isna(val):          return "Unknown"
    elif val < 50_000:         return "1_Under_50K"
    elif val < 75_000:         return "2_50K-75K"
    elif val < 100_000:        return "3_75K-100K"
    elif val < 125_000:        return "4_100K-125K"
    elif val < 150_000:        return "5_125K-150K"
    else:                      return "6_150K_Plus"

df["compensation_tier"] = df["annual_equivalent"].apply(compensation_tier)
print("    ✓ compensation_tier bands created")

# 4c. Compensation quartile (within full dataset)
df["comp_quartile"] = pd.qcut(
    df["annual_equivalent"].dropna(),
    q=4,
    labels=["Q1_Bottom", "Q2_LowMid", "Q3_HighMid", "Q4_Top"]
).reindex(df.index)
print("    ✓ comp_quartile (Q1–Q4) assigned")

# 4d. Public safety flag
PUBLIC_SAFETY_DEPTS = {
    "CHICAGO POLICE DEPARTMENT",
    "CHICAGO FIRE DEPARTMENT",
    "OFFICE OF EMERGENCY MANAGEMENT AND COMMUNICATIONS"
}
df["is_public_safety"] = df["department"].isin(PUBLIC_SAFETY_DEPTS).astype(int)
print(f"    ✓ is_public_safety flag: {df['is_public_safety'].sum():,} employees flagged")

# 4e. Full time flag
df["is_fulltime"] = (df["employment_type"] == "F").astype(int)
print("    ✓ is_fulltime binary flag created")

# 4f. Department short name (for chart labels)
dept_abbrev = {
    "CHICAGO POLICE DEPARTMENT":                           "CPD",
    "CHICAGO FIRE DEPARTMENT":                             "CFD",
    "DEPARTMENT OF WATER MANAGEMENT":                      "Water Mgmt",
    "DEPARTMENT OF STREETS AND SANITATION":                "Streets & San",
    "CHICAGO DEPARTMENT OF AVIATION":                      "Aviation",
    "CHICAGO DEPARTMENT OF TRANSPORTATION":                "CDOT",
    "CHICAGO PUBLIC LIBRARY":                              "Library",
    "DEPARTMENT OF FLEET AND FACILITY MANAGEMENT":         "Fleet & Fac",
    "OFFICE OF EMERGENCY MANAGEMENT AND COMMUNICATIONS":   "OEMC",
    "DEPARTMENT OF FAMILY AND SUPPORT SERVICES":           "Family Services",
    "CHICAGO PARKS DISTRICT":                              "Parks",
    "DEPARTMENT OF FINANCE":                               "Finance",
    "CHICAGO CITY CLERK":                                  "City Clerk",
    "DEPARTMENT OF PUBLIC HEALTH":                         "Public Health",
    "DEPARTMENT OF BUILDINGS":                             "Buildings",
    "CHICAGO ANIMAL CARE AND CONTROL":                     "Animal Control",
    "DEPARTMENT OF CULTURAL AFFAIRS AND SPECIAL EVENTS":   "Cultural Affairs",
    "CHICAGO INSPECTOR GENERAL":                           "Inspector Gen",
    "DEPARTMENT OF PLANNING AND DEVELOPMENT":              "Planning & Dev",
    "OFFICE OF THE MAYOR":                                 "Mayor's Office",
}
df["dept_short"] = df["department"].map(dept_abbrev).fillna(df["department"].str.title().str[:20])
print("    ✓ dept_short abbreviations mapped")

# ──────────────────────────────────────────────
# 5. OUTLIER FLAGGING
# ──────────────────────────────────────────────
print("\n[5] Flagging compensation outliers...")

q1 = df["annual_equivalent"].quantile(0.25)
q3 = df["annual_equivalent"].quantile(0.75)
iqr = q3 - q1
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr

df["is_outlier_low"]  = (df["annual_equivalent"] < lower_fence).astype(int)
df["is_outlier_high"] = (df["annual_equivalent"] > upper_fence).astype(int)

n_low  = df["is_outlier_low"].sum()
n_high = df["is_outlier_high"].sum()
print(f"    ✓ Low outliers  (<${lower_fence:,.0f}): {n_low:,} employees")
print(f"    ✓ High outliers (>${upper_fence:,.0f}): {n_high:,} employees")

# ──────────────────────────────────────────────
# 6. FINAL VALIDATION
# ──────────────────────────────────────────────
print("\n[6] Final validation checks...")

assert df.shape[0] == df_raw.shape[0], "Row count mismatch after cleaning!"
assert df["pay_type"].isin(["SALARY", "HOURLY"]).all(), "Unexpected pay_type values!"
assert df["employment_type"].isin(["F", "P"]).all(), "Unexpected employment_type values!"

pct_annualized = df["annual_equivalent"].notna().mean() * 100
print(f"    ✓ Row count preserved: {df.shape[0]:,}")
print(f"    ✓ annual_equivalent coverage: {pct_annualized:.1f}%")
print(f"    ✓ All pay_type values valid")
print(f"    ✓ All employment_type values valid")

# ──────────────────────────────────────────────
# 7. EXPORT
# ──────────────────────────────────────────────
print("\n[7] Exporting cleaned data...")

df.to_csv(CLEAN_CSV, index=False)
print(f"    ✓ Cleaned CSV  → {CLEAN_CSV}")

try:
    df.to_parquet(CLEAN_PARQ, index=False, engine="pyarrow")
    print(f"    ✓ Cleaned Parquet → {CLEAN_PARQ}")
except ImportError:
    print("    ⚠ pyarrow not installed — skipping Parquet export")

# ──────────────────────────────────────────────
# 8. SUMMARY STATISTICS
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("  CLEANING COMPLETE — SUMMARY")
print("=" * 60)
print(f"  Total employees:        {df.shape[0]:>10,}")
print(f"  Salaried employees:     {(df['pay_type']=='SALARY').sum():>10,}")
print(f"  Hourly employees:       {(df['pay_type']=='HOURLY').sum():>10,}")
print(f"  Full-time:              {(df['employment_type']=='F').sum():>10,}")
print(f"  Part-time:              {(df['employment_type']=='P').sum():>10,}")
print(f"  Unique departments:     {df['department'].nunique():>10,}")
print(f"  Unique job titles:      {df['job_title'].nunique():>10,}")
print(f"  Public safety staff:    {df['is_public_safety'].sum():>10,}")
print(f"  Mean annual equiv:      ${df['annual_equivalent'].mean():>12,.2f}")
print(f"  Median annual equiv:    ${df['annual_equivalent'].median():>12,.2f}")
print(f"  Min annual equiv:       ${df['annual_equivalent'].min():>12,.2f}")
print(f"  Max annual equiv:       ${df['annual_equivalent'].max():>12,.2f}")
print("=" * 60)
print(f"\n  Output columns ({df.shape[1]}):")
for col in df.columns:
    print(f"    • {col}")
print("\n  ✅ Script 01 complete. Proceed to 02_exploratory_data_analysis.py\n")
