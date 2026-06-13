"""
============================================================
Chicago City Workforce Analytics
Script 05: Executive Dashboard Export & Final Visualizations
============================================================
Author  : Senior Data Analyst Portfolio Project
Dataset : City of Chicago – Current Employee Names, Salaries,
          and Position Titles (data.gov)
Purpose : Generate multi-panel executive summary dashboard,
          export all processed datasets, print final summary.
============================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.gridspec as gridspec
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
PALETTE_DARK = "#1A1A2E"

plt.rcParams.update({
    "font.family":    "DejaVu Sans",
    "figure.dpi":     150,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

print("=" * 60)
print("  CHICAGO WORKFORCE ANALYTICS — STEP 05: DASHBOARD EXPORT")
print("=" * 60)

df = pd.read_csv(CLEAN_CSV)
total_payroll = df["annual_equivalent"].sum()
print(f"\n[✓] Loaded {len(df):,} employees\n")

# ──────────────────────────────────────────────
# MASTER EXECUTIVE DASHBOARD (Multi-Panel)
# ──────────────────────────────────────────────
print("[1] Generating: Executive Summary Dashboard...")

fig = plt.figure(figsize=(20, 24), facecolor="#F8F9FA")
fig.suptitle(
    "CITY OF CHICAGO — WORKFORCE ANALYTICS EXECUTIVE DASHBOARD",
    fontsize=20, fontweight="bold", color=PALETTE_DARK, y=0.98,
    fontfamily="DejaVu Sans"
)

gs = gridspec.GridSpec(4, 3, figure=fig, hspace=0.45, wspace=0.35,
                       top=0.95, bottom=0.04, left=0.07, right=0.97)

# ── Panel 1: KPI Cards (text-based) ──────────────
ax0 = fig.add_subplot(gs[0, :])
ax0.set_xlim(0, 1)
ax0.set_ylim(0, 1)
ax0.axis("off")

kpis = [
    ("31,984",       "Total Employees",          "#003087"),
    ("$3.64B",       "Est. Annual Payroll",       "#E63946"),
    ("$115,158",     "Median Compensation",       "#2A9D8F"),
    ("39",           "City Departments",          "#F4A261"),
    ("78.5%",        "Full-Time Workforce",       "#6c3483"),
    ("12,315",       "CPD (Largest Dept.)",       "#1a5276"),
]
box_w = 0.148
for i, (val, label, color) in enumerate(kpis):
    x = 0.025 + i * (box_w + 0.013)
    rect = plt.Rectangle((x, 0.05), box_w, 0.88, transform=ax0.transAxes,
                           facecolor=color, edgecolor="white", lw=1.5,
                           clip_on=False, zorder=2, alpha=0.92)
    ax0.add_patch(rect)
    ax0.text(x + box_w/2, 0.62, val,
             transform=ax0.transAxes, ha="center", va="center",
             fontsize=17, fontweight="bold", color="white", zorder=3)
    ax0.text(x + box_w/2, 0.26, label,
             transform=ax0.transAxes, ha="center", va="center",
             fontsize=8.5, color="white", alpha=0.9, zorder=3,
             wrap=True)
ax0.set_title("KEY PERFORMANCE INDICATORS", fontsize=12, fontweight="bold",
              color=PALETTE_DARK, pad=8, loc="left")

# ── Panel 2: Department Headcount ──────────────
ax1 = fig.add_subplot(gs[1, 0])
dept_count = df.groupby("dept_short").size().sort_values(ascending=True).tail(12)
colors_bar = [PALETTE_MAIN] * len(dept_count)
colors_bar[-1] = PALETTE_ACC1   # highlight largest
ax1.barh(dept_count.index, dept_count.values, color=colors_bar, height=0.7, edgecolor="white")
ax1.set_title("Headcount by Department (Top 12)", fontsize=10, fontweight="bold")
ax1.set_xlabel("Employees", fontsize=8)
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1000)}K"))
ax1.tick_params(labelsize=7)

# ── Panel 3: Salary Distribution ──────────────
ax2 = fig.add_subplot(gs[1, 1])
comp_vals = df["annual_equivalent"].dropna()
ax2.hist(comp_vals, bins=70, color=PALETTE_MAIN, edgecolor="white", alpha=0.85)
ax2.axvline(comp_vals.median(), color=PALETTE_ACC1, lw=2, linestyle="--", label=f"Median: ${comp_vals.median():,.0f}")
ax2.axvline(comp_vals.mean(),   color=PALETTE_ACC3, lw=2, linestyle="-",  label=f"Mean: ${comp_vals.mean():,.0f}")
ax2.legend(fontsize=7)
ax2.set_title("Compensation Distribution", fontsize=10, fontweight="bold")
ax2.set_xlabel("Annual Compensation", fontsize=8)
ax2.set_ylabel("Employees", fontsize=8)
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${int(x/1000)}K"))
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax2.tick_params(labelsize=7)

# ── Panel 4: Pay Type Split ──────────────────
ax3 = fig.add_subplot(gs[1, 2])
pay_split = df["pay_type"].value_counts()
wedge_colors = [PALETTE_MAIN, PALETTE_ACC2]
wedges, texts, autotexts = ax3.pie(
    pay_split.values,
    labels=[f"Salaried\n({pay_split['SALARY']:,})", f"Hourly\n({pay_split['HOURLY']:,})"],
    autopct="%1.1f%%", colors=wedge_colors, startangle=90,
    wedgeprops=dict(edgecolor="white", linewidth=2)
)
for t in autotexts: t.set_fontsize(9); t.set_color("white"); t.set_fontweight("bold")
ax3.set_title("Salary vs Hourly Split", fontsize=10, fontweight="bold")

# ── Panel 5: Payroll by Department (Top 10) ──
ax4 = fig.add_subplot(gs[2, :2])
dept_pay = (df.groupby("dept_short")["annual_equivalent"].sum().nlargest(10).sort_values(ascending=True))
dept_pay_M = dept_pay / 1e6
bars = ax4.barh(dept_pay_M.index, dept_pay_M.values, color=PALETTE_MAIN, height=0.7, edgecolor="white")
for bar, val in zip(bars, dept_pay_M.values):
    ax4.text(val + 3, bar.get_y() + bar.get_height()/2, f"${val:.0f}M", va="center", fontsize=8)
ax4.set_title("Total Annual Payroll by Department (Top 10)", fontsize=10, fontweight="bold")
ax4.set_xlabel("Annual Payroll ($M)", fontsize=8)
ax4.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}M"))
ax4.tick_params(labelsize=7.5)

# ── Panel 6: Compensation Tiers Donut ────────
ax5 = fig.add_subplot(gs[2, 2])
tier_order  = ["1_Under_50K","2_50K-75K","3_75K-100K","4_100K-125K","5_125K-150K","6_150K_Plus"]
tier_labels = ["<$50K","$50K-75K","$75K-100K","$100K-125K","$125K-150K","$150K+"]
tier_colors = ["#d62728","#ff7f0e","#ffbb78","#aec7e8","#1f77b4","#003087"]
tier_counts = df["compensation_tier"].value_counts().reindex(tier_order).fillna(0)
ax5.pie(tier_counts.values, labels=tier_labels, colors=tier_colors,
        startangle=140, wedgeprops=dict(edgecolor="white", linewidth=1.5), textprops={"fontsize": 8})
centre_circle = plt.Circle((0,0), 0.60, fc="white")
ax5.add_patch(centre_circle)
ax5.text(0, 0, "Comp\nBands", ha="center", va="center", fontsize=9, fontweight="bold", color=PALETTE_DARK)
ax5.set_title("Compensation Tier Breakdown", fontsize=10, fontweight="bold")

# ── Panel 7: Top 15 Job Titles ───────────────
ax6 = fig.add_subplot(gs[3, :2])
title_med = (df.groupby("job_title")["annual_equivalent"]
             .agg(["median","count"])
             .query("count >= 10")
             .nlargest(15, "median")
             .reset_index())
ax6.barh(title_med["job_title"], title_med["median"]/1000, color=PALETTE_ACC2, height=0.7, edgecolor="white")
ax6.set_title("Top 15 Job Titles by Median Compensation (min 10 employees)", fontsize=10, fontweight="bold")
ax6.set_xlabel("Median Annual Compensation ($K)", fontsize=8)
ax6.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}K"))
ax6.tick_params(labelsize=7.5)

# ── Panel 8: Public Safety vs Civilian ───────
ax7 = fig.add_subplot(gs[3, 2])
ps_data  = [df[df["is_public_safety"]==0]["annual_equivalent"].dropna(),
            df[df["is_public_safety"]==1]["annual_equivalent"].dropna()]
bp = ax7.boxplot(ps_data, patch_artist=True, notch=True, widths=0.45,
                  medianprops=dict(color="white", lw=2))
bp["boxes"][0].set_facecolor(PALETTE_ACC2)
bp["boxes"][1].set_facecolor(PALETTE_MAIN)
ax7.set_xticklabels([f"Civilian\n(n={len(ps_data[0]):,})", f"Public Safety\n(n={len(ps_data[1]):,})"], fontsize=8)
ax7.set_title("Public Safety vs. Civilian Comp", fontsize=10, fontweight="bold")
ax7.set_ylabel("Annual Compensation (USD)", fontsize=8)
ax7.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${int(x/1000)}K"))
ax7.tick_params(labelsize=7.5)

# Watermark
fig.text(0.5, 0.005, "Source: City of Chicago | data.gov  •  Analysis: Chicago Workforce Analytics Project  •  Data: Public Domain",
         ha="center", fontsize=8, color="gray", style="italic")

plt.savefig(f"{VIZ_DIR}/00_EXECUTIVE_DASHBOARD.png", bbox_inches="tight", facecolor="#F8F9FA")
plt.close()
print(f"    ✓ Executive Dashboard → {VIZ_DIR}/00_EXECUTIVE_DASHBOARD.png")

# ──────────────────────────────────────────────
# EXPORT FINAL PROCESSED DATASETS
# ──────────────────────────────────────────────
print("\n[2] Exporting all processed datasets...")

# Summary by department
dept_summary = df.groupby("department").agg(
    headcount=("employee_name","count"),
    salaried=("pay_type", lambda x: (x=="SALARY").sum()),
    hourly=("pay_type", lambda x: (x=="HOURLY").sum()),
    fulltime=("employment_type", lambda x: (x=="F").sum()),
    parttime=("employment_type", lambda x: (x=="P").sum()),
    median_comp=("annual_equivalent","median"),
    mean_comp=("annual_equivalent","mean"),
    total_payroll=("annual_equivalent","sum"),
    public_safety_staff=("is_public_safety","sum"),
).reset_index()
dept_summary.to_csv("data/processed/department_summary.csv", index=False)
print(f"    ✓ Department summary → data/processed/department_summary.csv")

# Summary by job title (full)
title_summary = df.groupby("job_title").agg(
    headcount=("employee_name","count"),
    median_comp=("annual_equivalent","median"),
    mean_comp=("annual_equivalent","mean"),
    min_comp=("annual_equivalent","min"),
    max_comp=("annual_equivalent","max"),
    total_payroll=("annual_equivalent","sum"),
).reset_index().sort_values("median_comp", ascending=False)
title_summary.to_csv("data/processed/job_title_summary.csv", index=False)
print(f"    ✓ Job title summary  → data/processed/job_title_summary.csv")

# Compensation tier breakdown
tier_breakdown = df.groupby(["compensation_tier","pay_type","employment_type"]).agg(
    headcount=("employee_name","count"),
    total_payroll=("annual_equivalent","sum"),
    median_comp=("annual_equivalent","median"),
).reset_index()
tier_breakdown.to_csv("data/processed/tier_breakdown.csv", index=False)
print(f"    ✓ Tier breakdown     → data/processed/tier_breakdown.csv")

print("\n" + "=" * 60)
print("  ✅ ALL SCRIPTS COMPLETE — PIPELINE SUMMARY")
print("=" * 60)
print(f"\n  📊 Visualizations generated:  {len([f for f in os.listdir(VIZ_DIR) if f.endswith('.png')])} PNG charts")
print(f"  📁 Processed datasets:        {len([f for f in os.listdir('data/processed') if f.endswith('.csv')])} CSV files")
print(f"\n  Next Steps:")
print(f"    → Open Excel workbook: excel/Chicago_Workforce_Analytics.xlsx")
print(f"    → Open Power BI file:  powerbi/Chicago_Workforce_Dashboard.pbix")
print(f"    → Review AI insights:  ai_insights/gpt_workforce_insights.md")
print(f"    → Read final report:   reports/Chicago_Workforce_Executive_Report.md")
print(f"\n  ✅ Project ready for GitHub upload!\n")
