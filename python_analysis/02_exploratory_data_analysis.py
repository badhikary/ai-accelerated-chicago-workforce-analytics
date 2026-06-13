"""
============================================================
Chicago City Workforce Analytics
Script 02: Exploratory Data Analysis (EDA)
============================================================
Author  : Senior Data Analyst Portfolio Project
Dataset : City of Chicago – Current Employee Names, Salaries,
          and Position Titles (data.gov)
Purpose : Comprehensive EDA — distributions, correlations,
          department analysis, job title analysis.
============================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for script mode
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────
CLEAN_CSV   = "data/processed/chicago_workforce_cleaned.csv"
VIZ_DIR     = "visualizations"
os.makedirs(VIZ_DIR, exist_ok=True)

# Corporate color palette
PALETTE_MAIN  = "#003087"   # navy blue
PALETTE_ACC1  = "#E63946"   # accent red
PALETTE_ACC2  = "#2A9D8F"   # teal
PALETTE_ACC3  = "#F4A261"   # amber
PALETTE_LIGHT = "#E9ECEF"

DEPT_PALETTE = sns.color_palette("Blues_r", 15)

plt.rcParams.update({
    "font.family":    "DejaVu Sans",
    "axes.titlesize": 14,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi":     150,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

print("=" * 60)
print("  CHICAGO WORKFORCE ANALYTICS — STEP 02: EDA")
print("=" * 60)

# ──────────────────────────────────────────────
# LOAD DATA
# ──────────────────────────────────────────────
df = pd.read_csv(CLEAN_CSV)
print(f"\n[✓] Loaded {df.shape[0]:,} rows × {df.shape[1]} columns\n")

# ──────────────────────────────────────────────
# CHART 1: Department Headcount (Top 20)
# ──────────────────────────────────────────────
print("[1] Generating: Department Headcount Bar Chart...")

dept_count = df.groupby("dept_short").size().sort_values(ascending=True).tail(20)

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(dept_count.index, dept_count.values, color=PALETTE_MAIN, edgecolor="white", height=0.7)

for bar, val in zip(bars, dept_count.values):
    ax.text(val + 80, bar.get_y() + bar.get_height() / 2,
            f"{val:,}", va="center", ha="left", fontsize=8.5, color="#333333")

ax.set_xlabel("Number of Employees", fontsize=11)
ax.set_title("City of Chicago — Employee Headcount by Department\n(Top 20 Departments)", fontsize=14, fontweight="bold", pad=15)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_xlim(0, dept_count.max() * 1.12)
fig.text(0.99, 0.01, "Source: City of Chicago / data.gov", ha="right", fontsize=7, color="gray")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/01_department_headcount.png", bbox_inches="tight")
plt.close()
print(f"    ✓ Saved → {VIZ_DIR}/01_department_headcount.png")

# ──────────────────────────────────────────────
# CHART 2: Salary Distribution Histogram
# ──────────────────────────────────────────────
print("[2] Generating: Annual Equivalent Salary Distribution...")

sal = df["annual_equivalent"].dropna()

fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(sal, bins=80, color=PALETTE_MAIN, edgecolor="white", alpha=0.88)
ax.axvline(sal.median(), color=PALETTE_ACC1, linewidth=2, linestyle="--", label=f"Median: ${sal.median():,.0f}")
ax.axvline(sal.mean(),   color=PALETTE_ACC3, linewidth=2, linestyle="-",  label=f"Mean:   ${sal.mean():,.0f}")

ax.set_xlabel("Annualized Compensation (USD)", fontsize=11)
ax.set_ylabel("Number of Employees", fontsize=11)
ax.set_title("City of Chicago — Annual Compensation Distribution\n(All 31,984 Employees)", fontsize=14, fontweight="bold")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${int(x/1000)}K"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.legend(fontsize=10)
fig.text(0.99, 0.01, "Source: City of Chicago / data.gov", ha="right", fontsize=7, color="gray")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/02_salary_distribution.png", bbox_inches="tight")
plt.close()
print(f"    ✓ Saved → {VIZ_DIR}/02_salary_distribution.png")

# ──────────────────────────────────────────────
# CHART 3: Salary vs Hourly (Annualized) Comparison
# ──────────────────────────────────────────────
print("[3] Generating: Salary vs Hourly Comparison...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("City of Chicago — Salaried vs Hourly Employees (Annualized Comparison)",
             fontsize=14, fontweight="bold", y=1.01)

salary_vals = df[df["pay_type"] == "SALARY"]["annual_equivalent"].dropna()
hourly_vals = df[df["pay_type"] == "HOURLY"]["annual_equivalent"].dropna()

# Distribution overlay
axes[0].hist(salary_vals, bins=60, color=PALETTE_MAIN, alpha=0.6, label=f"Salaried (n={len(salary_vals):,})", density=True)
axes[0].hist(hourly_vals, bins=60, color=PALETTE_ACC2, alpha=0.6, label=f"Hourly (n={len(hourly_vals):,})", density=True)
axes[0].set_title("Compensation Distribution Overlay")
axes[0].set_xlabel("Annualized Compensation (USD)")
axes[0].set_ylabel("Density")
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${int(x/1000)}K"))
axes[0].legend()

# Box plot comparison
bp_data = [salary_vals, hourly_vals]
bp = axes[1].boxplot(bp_data, patch_artist=True, notch=True, widths=0.5,
                      medianprops=dict(color="white", linewidth=2.5))
bp["boxes"][0].set_facecolor(PALETTE_MAIN)
bp["boxes"][1].set_facecolor(PALETTE_ACC2)
axes[1].set_xticklabels(["Salaried", "Hourly (Annualized)"])
axes[1].set_title("Compensation Boxplot by Pay Type")
axes[1].set_ylabel("Annualized Compensation (USD)")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${int(x/1000)}K"))

stats_text = (
    f"Salaried Median:  ${salary_vals.median():>10,.0f}\n"
    f"Hourly Median:    ${hourly_vals.median():>10,.0f}\n"
    f"Difference:       ${salary_vals.median() - hourly_vals.median():>10,.0f}"
)
axes[1].text(0.97, 0.97, stats_text, transform=axes[1].transAxes,
             verticalalignment="top", horizontalalignment="right",
             fontsize=8.5, fontfamily="monospace",
             bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="#cccccc"))

fig.text(0.99, -0.01, "Source: City of Chicago / data.gov", ha="right", fontsize=7, color="gray")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/03_salary_vs_hourly.png", bbox_inches="tight")
plt.close()
print(f"    ✓ Saved → {VIZ_DIR}/03_salary_vs_hourly.png")

# ──────────────────────────────────────────────
# CHART 4: Compensation Boxplot by Top 15 Departments
# ──────────────────────────────────────────────
print("[4] Generating: Department Compensation Boxplot...")

top15_depts = df.groupby("dept_short")["annual_equivalent"].median().nlargest(15).index
df_top15 = df[df["dept_short"].isin(top15_depts)].copy()

order = df_top15.groupby("dept_short")["annual_equivalent"].median().sort_values(ascending=False).index

fig, ax = plt.subplots(figsize=(14, 8))
sns.boxplot(
    data=df_top15, x="annual_equivalent", y="dept_short",
    order=order, palette="Blues_r", ax=ax, width=0.6,
    flierprops=dict(marker="o", markersize=2, alpha=0.3)
)
ax.set_title("City of Chicago — Compensation Distribution by Department\n(Top 15 Departments by Median Salary)", fontsize=14, fontweight="bold")
ax.set_xlabel("Annualized Compensation (USD)", fontsize=11)
ax.set_ylabel("")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${int(x/1000)}K"))
fig.text(0.99, 0.01, "Source: City of Chicago / data.gov", ha="right", fontsize=7, color="gray")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/04_dept_compensation_boxplot.png", bbox_inches="tight")
plt.close()
print(f"    ✓ Saved → {VIZ_DIR}/04_dept_compensation_boxplot.png")

# ──────────────────────────────────────────────
# CHART 5: Top 20 Job Titles by Average Compensation
# ──────────────────────────────────────────────
print("[5] Generating: Top 20 Job Titles by Average Pay...")

title_avg = (df.groupby("job_title")["annual_equivalent"]
             .agg(["mean", "count"])
             .query("count >= 5")   # at least 5 employees in title
             .nlargest(20, "mean")
             .reset_index())

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(title_avg["job_title"], title_avg["mean"],
               color=[PALETTE_MAIN if i < 10 else PALETTE_ACC2 for i in range(len(title_avg))],
               edgecolor="white", height=0.7)

for bar, val, cnt in zip(bars, title_avg["mean"], title_avg["count"]):
    ax.text(val + 1500, bar.get_y() + bar.get_height() / 2,
            f"${val:,.0f}  (n={cnt})", va="center", ha="left", fontsize=8)

ax.set_xlabel("Average Annualized Compensation (USD)", fontsize=11)
ax.set_title("City of Chicago — Top 20 Highest-Paid Job Titles\n(Min. 5 employees per title)", fontsize=14, fontweight="bold")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${int(x/1000)}K"))
ax.set_xlim(0, title_avg["mean"].max() * 1.22)
fig.text(0.99, 0.01, "Source: City of Chicago / data.gov", ha="right", fontsize=7, color="gray")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/05_top20_job_titles.png", bbox_inches="tight")
plt.close()
print(f"    ✓ Saved → {VIZ_DIR}/05_top20_job_titles.png")

# ──────────────────────────────────────────────
# CHART 6: Payroll Heatmap — Department × Employment Type
# ──────────────────────────────────────────────
print("[6] Generating: Department × Employment Type Heatmap...")

top12 = df.groupby("dept_short").size().nlargest(12).index
df_heat = df[df["dept_short"].isin(top12)]

heat_pivot = df_heat.pivot_table(
    index="dept_short",
    columns="employment_type",
    values="annual_equivalent",
    aggfunc="median"
).fillna(0)

heat_pivot.columns = ["Full-Time Median", "Part-Time Median"] if set(heat_pivot.columns) == {"F", "P"} else heat_pivot.columns
heat_pivot.columns = [c.replace("F", "Full-Time Median").replace("P", "Part-Time Median") for c in heat_pivot.columns]

# Sort by full-time median
if "Full-Time Median" in heat_pivot.columns:
    heat_pivot = heat_pivot.sort_values("Full-Time Median", ascending=False)

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(
    heat_pivot / 1000, annot=True, fmt=".0f", cmap="Blues",
    linewidths=0.5, ax=ax, cbar_kws={"label": "Median Compensation ($K)"}
)
ax.set_title("City of Chicago — Median Annual Compensation Heatmap\nDepartment × Employment Type (Top 12 Depts, $K)", fontsize=13, fontweight="bold")
ax.set_xlabel("Employment Type", fontsize=10)
ax.set_ylabel("")
plt.xticks(rotation=15)
plt.yticks(rotation=0)
fig.text(0.99, 0.01, "Source: City of Chicago / data.gov", ha="right", fontsize=7, color="gray")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/06_heatmap_dept_employment.png", bbox_inches="tight")
plt.close()
print(f"    ✓ Saved → {VIZ_DIR}/06_heatmap_dept_employment.png")

# ──────────────────────────────────────────────
# CHART 7: Compensation Tier Distribution (Stacked Bar)
# ──────────────────────────────────────────────
print("[7] Generating: Compensation Tier Distribution...")

tier_order = ["1_Under_50K", "2_50K-75K", "3_75K-100K", "4_100K-125K", "5_125K-150K", "6_150K_Plus"]
tier_labels = ["<$50K", "$50K–$75K", "$75K–$100K", "$100K–$125K", "$125K–$150K", "$150K+"]
tier_colors = ["#d62728", "#ff7f0e", "#ffbb78", "#aec7e8", "#1f77b4", "#003087"]

tier_counts = df["compensation_tier"].value_counts().reindex(tier_order).fillna(0)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("City of Chicago — Workforce Compensation Tier Analysis", fontsize=14, fontweight="bold")

# Bar chart
bars = axes[0].bar(tier_labels, tier_counts.values, color=tier_colors, edgecolor="white", width=0.65)
for bar, val in zip(bars, tier_counts.values):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                 f"{int(val):,}", ha="center", va="bottom", fontsize=9)
axes[0].set_title("Employee Count by Compensation Tier")
axes[0].set_xlabel("Annual Compensation Band")
axes[0].set_ylabel("Number of Employees")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
axes[0].tick_params(axis="x", rotation=25)

# Pie chart
pct = tier_counts.values / tier_counts.sum() * 100
wedge_labels = [f"{lbl}\n{p:.1f}%" for lbl, p in zip(tier_labels, pct)]
axes[1].pie(tier_counts.values, labels=wedge_labels, colors=tier_colors,
             startangle=140, wedgeprops=dict(edgecolor="white", linewidth=1.5))
axes[1].set_title("Proportion of Workforce by Compensation Tier")

fig.text(0.99, 0.01, "Source: City of Chicago / data.gov", ha="right", fontsize=7, color="gray")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/07_compensation_tiers.png", bbox_inches="tight")
plt.close()
print(f"    ✓ Saved → {VIZ_DIR}/07_compensation_tiers.png")

# ──────────────────────────────────────────────
# CHART 8: Public Safety vs Civilian Comparison
# ──────────────────────────────────────────────
print("[8] Generating: Public Safety vs Civilian Comparison...")

ps_group = df.groupby("is_public_safety")["annual_equivalent"].describe()
ps_group.index = ["Civilian", "Public Safety"]

fig, ax = plt.subplots(figsize=(10, 6))
ps_data = [
    df[df["is_public_safety"] == 0]["annual_equivalent"].dropna(),
    df[df["is_public_safety"] == 1]["annual_equivalent"].dropna(),
]
bp = ax.boxplot(ps_data, patch_artist=True, notch=True, widths=0.45,
                 medianprops=dict(color="white", linewidth=2.5))
bp["boxes"][0].set_facecolor(PALETTE_ACC2)
bp["boxes"][1].set_facecolor(PALETTE_MAIN)

ax.set_xticklabels([
    f"Civilian Staff\n(n={len(ps_data[0]):,})",
    f"Public Safety\n(n={len(ps_data[1]):,})"
], fontsize=11)
ax.set_title("City of Chicago — Compensation: Public Safety vs. Civilian Roles",
             fontsize=14, fontweight="bold")
ax.set_ylabel("Annualized Compensation (USD)", fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${int(x/1000)}K"))

for i, data in enumerate(ps_data, 1):
    ax.text(i, data.max() * 1.02,
            f"Median: ${data.median():,.0f}\nMean: ${data.mean():,.0f}",
            ha="center", fontsize=9, color="#333333",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.7, edgecolor="#cccccc"))

fig.text(0.99, 0.01, "Source: City of Chicago / data.gov", ha="right", fontsize=7, color="gray")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/08_public_safety_vs_civilian.png", bbox_inches="tight")
plt.close()
print(f"    ✓ Saved → {VIZ_DIR}/08_public_safety_vs_civilian.png")

# ──────────────────────────────────────────────
# PRINT EDA SUMMARY STATISTICS
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("  EDA KEY STATISTICS SUMMARY")
print("=" * 60)

total = len(df)
sal_med = df["annual_equivalent"].median()
sal_mean = df["annual_equivalent"].mean()
sal_max = df["annual_equivalent"].max()

print(f"\n  Workforce Overview:")
print(f"    Total employees:        {total:>10,}")
print(f"    Unique departments:     {df['department'].nunique():>10}")
print(f"    Unique job titles:      {df['job_title'].nunique():>10}")

print(f"\n  Compensation:")
print(f"    Mean annual equiv:      ${sal_mean:>12,.2f}")
print(f"    Median annual equiv:    ${sal_med:>12,.2f}")
print(f"    Highest paid employee:  ${sal_max:>12,.2f}")
print(f"    P10 (10th percentile):  ${df['annual_equivalent'].quantile(0.10):>12,.2f}")
print(f"    P25 (25th percentile):  ${df['annual_equivalent'].quantile(0.25):>12,.2f}")
print(f"    P75 (75th percentile):  ${df['annual_equivalent'].quantile(0.75):>12,.2f}")
print(f"    P90 (90th percentile):  ${df['annual_equivalent'].quantile(0.90):>12,.2f}")

largest_dept = df.groupby("department").size().idxmax()
highest_med  = df.groupby("department")["annual_equivalent"].median().idxmax()

print(f"\n  Departments:")
print(f"    Largest department:     {largest_dept}")
print(f"    Highest median salary:  {highest_med}")

print(f"\n  Total annual payroll liability estimate:")
total_payroll = df["annual_equivalent"].sum()
print(f"    ${total_payroll:>15,.2f}")

print("\n  ✅ Script 02 complete. All charts saved to /visualizations/")
print("  ✅ Proceed to 03_statistical_analysis.py\n")
