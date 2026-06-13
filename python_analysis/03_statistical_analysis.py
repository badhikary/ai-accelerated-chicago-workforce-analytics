"""
============================================================
Chicago City Workforce Analytics
Script 03: Statistical Analysis — Pay Equity & Compensation
============================================================
Author  : Senior Data Analyst Portfolio Project
Dataset : City of Chicago – Current Employee Names, Salaries,
          and Position Titles (data.gov)
Purpose : Inferential statistics, pay equity tests, 
          ANOVA, t-tests, effect sizes, normality tests.
============================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
from scipy.stats import f_oneway, ttest_ind, mannwhitneyu, shapiro, kruskal
import warnings
import os
warnings.filterwarnings("ignore")

CLEAN_CSV = "data/processed/chicago_workforce_cleaned.csv"
VIZ_DIR   = "visualizations"
os.makedirs(VIZ_DIR, exist_ok=True)

PALETTE_MAIN  = "#003087"
PALETTE_ACC1  = "#E63946"
PALETTE_ACC2  = "#2A9D8F"

plt.rcParams.update({
    "font.family":    "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "figure.dpi":     150,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

print("=" * 60)
print("  CHICAGO WORKFORCE ANALYTICS — STEP 03: STATISTICAL ANALYSIS")
print("=" * 60)

df = pd.read_csv(CLEAN_CSV)
comp = df["annual_equivalent"].dropna()
print(f"\n[✓] Loaded {len(df):,} employees — {len(comp):,} with annual_equivalent\n")

# ──────────────────────────────────────────────
# 1. DESCRIPTIVE STATISTICS DEEP DIVE
# ──────────────────────────────────────────────
print("=" * 50)
print("[1] DESCRIPTIVE STATISTICS")
print("=" * 50)

desc = comp.describe(percentiles=[.05, .1, .25, .5, .75, .9, .95])
print(f"\n  Count:       {desc['count']:>12,.0f}")
print(f"  Mean:        ${desc['mean']:>12,.2f}")
print(f"  Std Dev:     ${desc['std']:>12,.2f}")
print(f"  Min:         ${desc['min']:>12,.2f}")
print(f"  P5:          ${desc['5%']:>12,.2f}")
print(f"  P10:         ${desc['10%']:>12,.2f}")
print(f"  P25 (Q1):    ${desc['25%']:>12,.2f}")
print(f"  Median:      ${desc['50%']:>12,.2f}")
print(f"  P75 (Q3):    ${desc['75%']:>12,.2f}")
print(f"  P90:         ${desc['90%']:>12,.2f}")
print(f"  P95:         ${desc['95%']:>12,.2f}")
print(f"  Max:         ${desc['max']:>12,.2f}")
print(f"\n  Skewness:    {comp.skew():>12.4f}  (positive = right-skewed)")
print(f"  Kurtosis:    {comp.kurtosis():>12.4f}  (>0 = heavy-tailed)")
cv = comp.std() / comp.mean() * 100
print(f"  Coeff. Var:  {cv:>11.2f}%  (variation relative to mean)")
gini_approx = (2 * np.cov(comp, np.arange(len(comp)))[0][1]) / (len(comp) * comp.mean())
print(f"  IQR:         ${comp.quantile(0.75) - comp.quantile(0.25):>12,.2f}")

# ──────────────────────────────────────────────
# 2. TEST: SALARY vs HOURLY (ANNUALIZED) — t-test & Mann-Whitney
# ──────────────────────────────────────────────
print("\n" + "=" * 50)
print("[2] HYPOTHESIS TEST: Salaried vs Hourly (Annualized)")
print("=" * 50)
print("\n  H₀: No difference in median annual compensation between salaried and hourly employees")
print("  H₁: Salaried employees have higher median annual compensation\n")

sal_group  = df[df["pay_type"] == "SALARY"]["annual_equivalent"].dropna()
hour_group = df[df["pay_type"] == "HOURLY"]["annual_equivalent"].dropna()

# Independent t-test (parametric)
t_stat, t_pval = ttest_ind(sal_group, hour_group, alternative="greater")

# Mann-Whitney U (non-parametric — appropriate given non-normal distribution)
u_stat, u_pval = mannwhitneyu(sal_group, hour_group, alternative="greater")

# Cohen's d effect size
def cohens_d(a, b):
    pooled_std = np.sqrt((np.std(a, ddof=1)**2 + np.std(b, ddof=1)**2) / 2)
    return (np.mean(a) - np.mean(b)) / pooled_std

d = cohens_d(sal_group, hour_group)
effect_label = "small" if abs(d) < 0.2 else "medium" if abs(d) < 0.5 else "large"

print(f"  Salaried  — n={len(sal_group):,}   median=${sal_group.median():,.0f}   mean=${sal_group.mean():,.0f}")
print(f"  Hourly    — n={len(hour_group):,}    median=${hour_group.median():,.0f}   mean=${hour_group.mean():,.0f}")
print(f"\n  Independent t-test:")
print(f"    t-statistic:   {t_stat:.4f}")
print(f"    p-value:       {t_pval:.2e}   {'✓ REJECT H₀ (p<0.05)' if t_pval < 0.05 else '✗ FAIL TO REJECT H₀'}")
print(f"\n  Mann-Whitney U (non-parametric):")
print(f"    U-statistic:   {u_stat:.2f}")
print(f"    p-value:       {u_pval:.2e}   {'✓ REJECT H₀ (p<0.05)' if u_pval < 0.05 else '✗ FAIL TO REJECT H₀'}")
print(f"\n  Cohen's d:     {d:.4f}  →  {effect_label} effect size")
print(f"\n  📌 FINDING: Salaried employees earn ${sal_group.median()-hour_group.median():,.0f} more")
print(f"             (median) annually than hourly workers.")

# ──────────────────────────────────────────────
# 3. ONE-WAY ANOVA: Compensation across Top 10 Departments
# ──────────────────────────────────────────────
print("\n" + "=" * 50)
print("[3] ONE-WAY ANOVA: Compensation Across Departments")
print("=" * 50)
print("\n  H₀: Mean annual compensation is equal across all departments")
print("  H₁: At least one department differs significantly\n")

top10_depts = df.groupby("department").size().nlargest(10).index
dept_groups = [
    df[df["department"] == d]["annual_equivalent"].dropna().values
    for d in top10_depts
]

f_stat, f_pval = f_oneway(*dept_groups)
k_stat, k_pval = kruskal(*dept_groups)   # non-parametric alternative

# Eta-squared (effect size for ANOVA)
grand_mean = np.concatenate(dept_groups).mean()
ss_between = sum(len(g) * (g.mean() - grand_mean)**2 for g in dept_groups)
ss_total   = sum(((x - grand_mean)**2) for g in dept_groups for x in g)
eta_sq = ss_between / ss_total

print(f"  One-Way ANOVA (parametric):")
print(f"    F-statistic:   {f_stat:.4f}")
print(f"    p-value:       {f_pval:.2e}   {'✓ REJECT H₀ (p<0.05)' if f_pval < 0.05 else '✗ FAIL TO REJECT'}")
print(f"\n  Kruskal-Wallis (non-parametric):")
print(f"    H-statistic:   {k_stat:.4f}")
print(f"    p-value:       {k_pval:.2e}   {'✓ REJECT H₀ (p<0.05)' if k_pval < 0.05 else '✗ FAIL TO REJECT'}")
print(f"\n  Eta-squared (η²): {eta_sq:.4f}")
eff = "small (η²<0.06)" if eta_sq < 0.06 else "medium (0.06≤η²<0.14)" if eta_sq < 0.14 else "large (η²≥0.14)"
print(f"    Effect size:   {eff}")
print(f"\n  Department Medians:")
for d in sorted(top10_depts, key=lambda x: df[df['department']==x]['annual_equivalent'].median(), reverse=True):
    med = df[df["department"] == d]["annual_equivalent"].median()
    n   = (df["department"] == d).sum()
    print(f"    {d:<55} ${med:>10,.0f}  (n={n:,})")

# ──────────────────────────────────────────────
# 4. PAY EQUITY: FULL-TIME vs PART-TIME
# ──────────────────────────────────────────────
print("\n" + "=" * 50)
print("[4] PAY EQUITY: Full-Time vs Part-Time")
print("=" * 50)

ft = df[df["employment_type"] == "F"]["annual_equivalent"].dropna()
pt = df[df["employment_type"] == "P"]["annual_equivalent"].dropna()

u2, p2 = mannwhitneyu(ft, pt, alternative="two-sided")
d2 = cohens_d(ft, pt)

print(f"\n  Full-Time — n={len(ft):,}   median=${ft.median():,.0f}   mean=${ft.mean():,.0f}")
print(f"  Part-Time — n={len(pt):,}    median=${pt.median():,.0f}    mean=${pt.mean():,.0f}")
print(f"\n  Mann-Whitney U:")
print(f"    U-statistic:   {u2:.2f}")
print(f"    p-value:       {p2:.2e}   {'✓ Significant' if p2 < 0.05 else '✗ Not significant'}")
print(f"    Cohen's d:     {d2:.4f}")

# ──────────────────────────────────────────────
# 5. NORMALITY TESTS
# ──────────────────────────────────────────────
print("\n" + "=" * 50)
print("[5] NORMALITY TESTS")
print("=" * 50)

# D'Agostino K² for large n (Shapiro limited to 5000)
sample = comp.sample(min(5000, len(comp)), random_state=42)
k2_stat, k2_pval = stats.normaltest(sample)
print(f"\n  D'Agostino K² test (n={len(sample):,} sample):")
print(f"    Statistic:  {k2_stat:.4f}")
print(f"    p-value:    {k2_pval:.2e}")
print(f"    Result:     {'NOT normally distributed (p<0.05)' if k2_pval < 0.05 else 'Cannot reject normality'}")
print(f"\n  📌 This justifies use of non-parametric tests (Mann-Whitney,")
print(f"     Kruskal-Wallis) as primary statistical methods.")

# ──────────────────────────────────────────────
# CHART 9: QQ Plot + Salary vs Hourly Violin
# ──────────────────────────────────────────────
print("\n[6] Generating: Statistical Charts (QQ Plot + Violin)...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("City of Chicago — Statistical Distribution Diagnostics",
             fontsize=14, fontweight="bold")

# QQ Plot
(osm, osr), (slope, intercept, _) = stats.probplot(comp.sample(5000, random_state=42), dist="norm")
axes[0].scatter(osm, osr, color=PALETTE_MAIN, alpha=0.3, s=8, label="Observed")
axes[0].plot(osm, slope * np.array(osm) + intercept, color=PALETTE_ACC1, lw=2, label="Normal Line")
axes[0].set_title("Q-Q Plot: Annual Compensation vs Normal Distribution\n(5,000 random sample)")
axes[0].set_xlabel("Theoretical Quantiles")
axes[0].set_ylabel("Sample Quantiles")
axes[0].legend(fontsize=9)

# Violin plot
vdata = [sal_group.values, hour_group.values]
parts = axes[1].violinplot(vdata, positions=[1, 2], showmedians=True, showextrema=True)
for i, pc in enumerate(parts["bodies"]):
    pc.set_facecolor([PALETTE_MAIN, PALETTE_ACC2][i])
    pc.set_alpha(0.7)
parts["cmedians"].set_color("white")
parts["cmedians"].set_linewidth(2)
axes[1].set_xticks([1, 2])
axes[1].set_xticklabels([f"Salaried\n(n={len(sal_group):,})", f"Hourly (Ann.)\n(n={len(hour_group):,})"])
axes[1].set_title("Violin Plot: Salaried vs Hourly (Annualized)\np-value: " + ("< 1e-300" if u_pval == 0 else f"{u_pval:.2e}") + f"  |  Cohen's d: {d:.3f} (" + str(effect_label) + ")")
axes[1].set_ylabel("Annual Equivalent Compensation (USD)")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${int(x/1000)}K"))

fig.text(0.99, 0.01, "Source: City of Chicago / data.gov", ha="right", fontsize=7, color="gray")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/09_statistical_diagnostics.png", bbox_inches="tight")
plt.close()
print(f"    ✓ Saved → {VIZ_DIR}/09_statistical_diagnostics.png")

# ──────────────────────────────────────────────
# CHART 10: Percentile Ladder
# ──────────────────────────────────────────────
print("[7] Generating: Compensation Percentile Ladder...")

percentiles = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50,
               55, 60, 65, 70, 75, 80, 85, 90, 95, 99]
pct_values = [comp.quantile(p/100) for p in percentiles]

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(percentiles, [v/1000 for v in pct_values], color=PALETTE_MAIN, lw=2.5, marker="o", markersize=4)
ax.fill_between(percentiles, [v/1000 for v in pct_values], alpha=0.15, color=PALETTE_MAIN)

# Annotate key percentiles
for p, v in [(25, comp.quantile(0.25)), (50, comp.quantile(0.50)), (75, comp.quantile(0.75)), (90, comp.quantile(0.90))]:
    ax.annotate(f"P{p}: ${v:,.0f}", xy=(p, v/1000), xytext=(p+1.5, v/1000 + 3),
                fontsize=8.5, arrowprops=dict(arrowstyle="->", color="#666666", lw=0.8))

ax.set_xlabel("Percentile", fontsize=11)
ax.set_ylabel("Annual Compensation ($K)", fontsize=11)
ax.set_title("City of Chicago — Compensation Percentile Ladder\n(All 31,984 Employees)", fontsize=14, fontweight="bold")
ax.set_xticks(percentiles)
ax.tick_params(axis="x", rotation=45)
fig.text(0.99, 0.01, "Source: City of Chicago / data.gov", ha="right", fontsize=7, color="gray")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/10_percentile_ladder.png", bbox_inches="tight")
plt.close()
print(f"    ✓ Saved → {VIZ_DIR}/10_percentile_ladder.png")

print("\n  ✅ Script 03 complete. Statistical analysis done.")
print("  ✅ Proceed to 04_compensation_benchmarking.py\n")
