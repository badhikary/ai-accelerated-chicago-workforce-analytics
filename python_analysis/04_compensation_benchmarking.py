"""
============================================================
Chicago City Workforce Analytics
Script 04: Compensation Benchmarking & Payroll Analysis
============================================================
Author  : Senior Data Analyst Portfolio Project
Dataset : City of Chicago – Current Employee Names, Salaries,
          and Position Titles (data.gov)
Purpose : Total payroll liability by department, salary bands,
          benchmarking, top earners analysis, payroll modeling.
============================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

CLEAN_CSV = "data/processed/chicago_workforce_cleaned.csv"
VIZ_DIR   = "visualizations"
os.makedirs(VIZ_DIR, exist_ok=True)

PALETTE_MAIN = "#003087"
PALETTE_ACC1 = "#E63946"
PALETTE_ACC2 = "#2A9D8F"
PALETTE_ACC3 = "#F4A261"

plt.rcParams.update({
    "font.family":    "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "figure.dpi":     150,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

print("=" * 60)
print("  CHICAGO WORKFORCE ANALYTICS — STEP 04: COMPENSATION BENCHMARKING")
print("=" * 60)

df = pd.read_csv(CLEAN_CSV)
print(f"\n[✓] Loaded {len(df):,} employees\n")

# ──────────────────────────────────────────────
# 1. TOTAL PAYROLL LIABILITY BY DEPARTMENT
# ──────────────────────────────────────────────
print("=" * 50)
print("[1] TOTAL PAYROLL LIABILITY")
print("=" * 50)

total_payroll = df["annual_equivalent"].sum()
dept_payroll = (df.groupby("department")
                .agg(
                    headcount=("employee_name", "count"),
                    total_payroll=("annual_equivalent", "sum"),
                    median_comp=("annual_equivalent", "median"),
                    mean_comp=("annual_equivalent", "mean"),
                    max_comp=("annual_equivalent", "max"),
                )
                .sort_values("total_payroll", ascending=False)
                .reset_index())

dept_payroll["payroll_pct"]     = dept_payroll["total_payroll"] / total_payroll * 100
dept_payroll["headcount_pct"]   = dept_payroll["headcount"] / len(df) * 100

print(f"\n  Total City Annual Payroll:   ${total_payroll:>16,.2f}")
print(f"  Monthly Equivalent:          ${total_payroll/12:>16,.2f}")
print(f"  Weekly Equivalent:           ${total_payroll/52:>16,.2f}")

print(f"\n  Top 10 Departments by Payroll:")
print(f"\n  {'Department':<55} {'Headcount':>9} {'Total Payroll':>16} {'% of Total':>10}")
print("  " + "─" * 93)
for _, row in dept_payroll.head(10).iterrows():
    print(f"  {row['department']:<55} {row['headcount']:>9,} ${row['total_payroll']:>15,.0f} {row['payroll_pct']:>9.1f}%")

# Export table
dept_payroll.to_csv("data/processed/dept_payroll_summary.csv", index=False)
print(f"\n  ✓ Full department payroll table saved → data/processed/dept_payroll_summary.csv")

# ──────────────────────────────────────────────
# 2. TOP 50 HIGHEST COMPENSATED EMPLOYEES
# ──────────────────────────────────────────────
print("\n" + "=" * 50)
print("[2] TOP 50 HIGHEST COMPENSATED EMPLOYEES")
print("=" * 50)

top50 = (df.nlargest(50, "annual_equivalent")
         [["employee_name", "job_title", "department", "pay_type", "annual_equivalent"]]
         .reset_index(drop=True))
top50.index += 1
top50.to_csv("data/processed/top50_earners.csv", index_label="rank")
print(f"\n  Top 10 highest earners:")
print(f"\n  {'Rank':<5} {'Name':<35} {'Job Title':<40} {'Annual Comp':>14}")
print("  " + "─" * 96)
for rank, row in top50.head(10).iterrows():
    print(f"  {rank:<5} {row['employee_name']:<35} {row['job_title']:<40} ${row['annual_equivalent']:>13,.2f}")
print(f"\n  ✓ Top 50 earners saved → data/processed/top50_earners.csv")

# ──────────────────────────────────────────────
# 3. JOB TITLE BENCHMARKING TABLE
# ──────────────────────────────────────────────
print("\n" + "=" * 50)
print("[3] JOB TITLE BENCHMARKING")
print("=" * 50)

title_bench = (df.groupby("job_title")["annual_equivalent"]
               .agg(["count", "min", "mean", "median", "max", "std"])
               .query("count >= 10")
               .rename(columns={"count":"headcount","min":"comp_min","mean":"comp_mean",
                                 "median":"comp_median","max":"comp_max","std":"comp_std"})
               .sort_values("comp_median", ascending=False)
               .reset_index())

title_bench["comp_range"] = title_bench["comp_max"] - title_bench["comp_min"]
title_bench.to_csv("data/processed/job_title_benchmarks.csv", index=False)
print(f"\n  Benchmarked {len(title_bench):,} job titles (min 10 employees each)")
print(f"  ✓ Saved → data/processed/job_title_benchmarks.csv")

# ──────────────────────────────────────────────
# 4. SALARY BAND ANALYSIS
# ──────────────────────────────────────────────
print("\n" + "=" * 50)
print("[4] SALARY BAND DISTRIBUTION")
print("=" * 50)

tier_map = {
    "1_Under_50K":    "<$50K",
    "2_50K-75K":      "$50K–$75K",
    "3_75K-100K":     "$75K–$100K",
    "4_100K-125K":    "$100K–$125K",
    "5_125K-150K":    "$125K–$150K",
    "6_150K_Plus":    "$150K+"
}
tier_stats = (df.groupby("compensation_tier")
              .agg(
                  headcount=("employee_name", "count"),
                  total_payroll=("annual_equivalent", "sum"),
                  avg_comp=("annual_equivalent", "mean"),
              )
              .reset_index())
tier_stats["label"]      = tier_stats["compensation_tier"].map(tier_map)
tier_stats["pct_workers"]= tier_stats["headcount"] / len(df) * 100
tier_stats["pct_payroll"]= tier_stats["total_payroll"] / total_payroll * 100

print(f"\n  {'Band':<15} {'Workers':>8} {'% Workers':>10} {'% Payroll':>10} {'Avg Comp':>14}")
print("  " + "─" * 60)
for _, r in tier_stats.iterrows():
    print(f"  {r['label']:<15} {r['headcount']:>8,} {r['pct_workers']:>9.1f}% {r['pct_payroll']:>9.1f}% ${r['avg_comp']:>13,.0f}")

# ──────────────────────────────────────────────
# CHART 11: Payroll Waterfall by Department (Top 15)
# ──────────────────────────────────────────────
print("\n[5] Generating: Payroll Waterfall Chart...")

top15_pay = dept_payroll.head(15).copy()
top15_pay["total_payroll_M"] = top15_pay["total_payroll"] / 1_000_000

fig, ax = plt.subplots(figsize=(14, 8))
colors = [PALETTE_MAIN if i < 3 else ("#1f4e79" if i < 6 else "#4472C4") for i in range(len(top15_pay))]

bars = ax.bar(range(len(top15_pay)), top15_pay["total_payroll_M"], color=colors, edgecolor="white", width=0.75)

for i, (bar, row) in enumerate(zip(bars, top15_pay.itertuples())):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8,
            f"${row.total_payroll_M:.0f}M\n({row.payroll_pct:.1f}%)",
            ha="center", va="bottom", fontsize=7.5, color="#333333")

dept_labels = [d[:20] + "..." if len(d) > 22 else d for d in top15_pay["department"]]
ax.set_xticks(range(len(top15_pay)))
ax.set_xticklabels(dept_labels, rotation=35, ha="right", fontsize=8.5)
ax.set_ylabel("Total Annual Payroll ($M)", fontsize=11)
ax.set_title(f"City of Chicago — Annual Payroll by Department\nTotal Payroll: ${total_payroll/1e9:.2f}B | Top 15 Departments", fontsize=14, fontweight="bold")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}M"))

# Cumulative line
cumsum = np.cumsum(top15_pay["total_payroll_M"].values)
ax2 = ax.twinx()
ax2.plot(range(len(top15_pay)), cumsum / (total_payroll/1e6) * 100, color=PALETTE_ACC1, lw=2, marker="o", markersize=4, label="Cumulative %")
ax2.set_ylabel("Cumulative % of Total Payroll", color=PALETTE_ACC1, fontsize=10)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
ax2.tick_params(axis="y", colors=PALETTE_ACC1)
ax2.spines["right"].set_visible(True)
ax2.legend(loc="lower right", fontsize=9)

fig.text(0.99, 0.01, "Source: City of Chicago / data.gov", ha="right", fontsize=7, color="gray")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/11_payroll_by_department.png", bbox_inches="tight")
plt.close()
print(f"    ✓ Saved → {VIZ_DIR}/11_payroll_by_department.png")

# ──────────────────────────────────────────────
# CHART 12: Compensation Band Workforce Pyramid
# ──────────────────────────────────────────────
print("[6] Generating: Compensation Band Pyramid...")

tier_order  = ["1_Under_50K", "2_50K-75K", "3_75K-100K", "4_100K-125K", "5_125K-150K", "6_150K_Plus"]
tier_labels = ["<$50K", "$50K–$75K", "$75K–$100K", "$100K–$125K", "$125K–$150K", "$150K+"]
tier_colors = ["#d62728", "#ff7f0e", "#ffbb78", "#aec7e8", "#1f77b4", "#003087"]

tier_counts = df["compensation_tier"].value_counts().reindex(tier_order).fillna(0).values
payroll_vals = [tier_stats.loc[tier_stats["compensation_tier"]==t, "total_payroll"].values[0]/1e6
                if t in tier_stats["compensation_tier"].values else 0 for t in tier_order]

fig, axes = plt.subplots(1, 2, figsize=(14, 7))
fig.suptitle("City of Chicago — Compensation Pyramid Analysis", fontsize=14, fontweight="bold")

# Horizontal workforce count
axes[0].barh(tier_labels, tier_counts, color=tier_colors[::-1], edgecolor="white", height=0.65)
for i, (val, lbl) in enumerate(zip(tier_counts, tier_labels)):
    axes[0].text(val + 30, i, f"{int(val):,} ({val/len(df)*100:.1f}%)", va="center", fontsize=9)
axes[0].set_title("Employees by Compensation Band")
axes[0].set_xlabel("Number of Employees")
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

# Payroll contribution
axes[1].barh(tier_labels, payroll_vals, color=tier_colors[::-1], edgecolor="white", height=0.65)
for i, (val, lbl) in enumerate(zip(payroll_vals, tier_labels)):
    axes[1].text(val + 1, i, f"${val:.0f}M ({val/sum(payroll_vals)*100:.1f}%)", va="center", fontsize=9)
axes[1].set_title("Payroll Share by Compensation Band")
axes[1].set_xlabel("Total Annual Payroll ($M)")
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}M"))

fig.text(0.99, 0.01, "Source: City of Chicago / data.gov", ha="right", fontsize=7, color="gray")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/12_compensation_pyramid.png", bbox_inches="tight")
plt.close()
print(f"    ✓ Saved → {VIZ_DIR}/12_compensation_pyramid.png")

# ──────────────────────────────────────────────
# FINAL BENCHMARKING SUMMARY
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("  BENCHMARKING SUMMARY")
print("=" * 60)
print(f"\n  Total Annual Payroll:        ${total_payroll:>14,.0f}")
print(f"  Total Annual Payroll (B):    ${total_payroll/1e9:>14.3f}B")
print(f"  Average Cost Per Employee:   ${total_payroll/len(df):>14,.0f}")
print(f"  Median Cost Per Employee:    ${df['annual_equivalent'].median():>14,.0f}")
print(f"\n  Highest Payroll Dept:        {dept_payroll.iloc[0]['department']}")
print(f"    → ${dept_payroll.iloc[0]['total_payroll']:,.0f} ({dept_payroll.iloc[0]['payroll_pct']:.1f}% of total)")
print(f"\n  Highest Median Salary Dept:  {dept_payroll.sort_values('median_comp', ascending=False).iloc[0]['department']}")
print(f"    → Median ${dept_payroll.sort_values('median_comp', ascending=False).iloc[0]['median_comp']:,.0f}")
print(f"\n  Top Compensation Tier ($150K+):")
top_tier = df[df["compensation_tier"] == "6_150K_Plus"]
print(f"    {len(top_tier):,} employees ({len(top_tier)/len(df)*100:.1f}% of workforce)")
print(f"    Total payroll share: ${top_tier['annual_equivalent'].sum()/1e6:.1f}M")
print("\n  ✅ Script 04 complete. Proceed to 05_visualization_export.py\n")
