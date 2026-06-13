# Data Dictionary — Chicago City Employee Compensation Dataset

**Source**: City of Chicago Open Data Portal / data.gov  
**Dataset Name**: Current Employee Names, Salaries, and Position Titles  
**Last Refreshed**: Current fiscal year (annual update cadence)  
**Record Count**: 31,984 rows  
**Column Count**: 8

---

## Column Definitions

| Column Name | Data Type | Description | Example Values | Notes |
|-------------|-----------|-------------|----------------|-------|
| `Name` | STRING | Employee full name in LAST, FIRST MIDDLE format | `SANFRATELLO, VINCENT A` | No PII beyond name; consistent formatting |
| `Job Titles` | STRING | Official job title as per HR classification | `POLICE OFFICER`, `FIREFIGHTER-EMT`, `LIBRARIAN I` | ~1,200+ unique titles across city |
| `Department` | STRING | City department or agency the employee belongs to | `CHICAGO POLICE DEPARTMENT`, `CHICAGO FIRE DEPARTMENT` | 39 unique departments |
| `Full or Part-Time` | STRING (categorical) | Employment status | `F` = Full-Time, `P` = Part-Time | Binary field; 97.2% Full-Time |
| `Salary or Hourly` | STRING (categorical) | Compensation structure | `SALARY`, `HOURLY` | Mutually exclusive; drives which pay column is populated |
| `Typical Hours` | INTEGER (nullable) | Scheduled weekly hours for hourly employees | `40`, `20`, `10` | NULL for all salaried employees (25,042 NULLs) |
| `Annual Salary` | FLOAT (nullable) | Annual base salary in USD for salaried employees | `115158.00`, `98928.00` | NULL for all hourly employees (6,942 NULLs) |
| `Hourly Rate` | FLOAT (nullable) | Hourly pay rate in USD for hourly employees | `46.30`, `53.06` | NULL for all salaried employees (25,042 NULLs) |

---

## Business Rules & Relationships

1. **Salary XOR Hourly**: Each employee has either `Annual Salary` OR `Hourly Rate` populated — never both. The `Salary or Hourly` flag is the discriminator.
2. **Typical Hours**: Only populated for hourly employees. Used to annualize hourly compensation for apples-to-apples comparison.
3. **Annualized Hourly Formula**: `Annual Equivalent = Hourly Rate × Typical Hours × 52`
4. **Department Hierarchy**: Departments are flat — no sub-department or division hierarchy in source data.
5. **No Employee ID**: The dataset does not include a unique employee identifier. `Name` is the closest proxy but is not guaranteed unique.

---

## Data Quality Notes

| Issue | Severity | Count | Handling |
|-------|----------|-------|----------|
| Employees with $199.20 annual salary | Medium | ~1 | Likely stipend/elected official roles; kept, flagged |
| Very high salaries (>$300K) | Low | <5 | Likely senior elected officials; valid, kept |
| Part-time employees with 40hr/week | Low | ~12 | Valid (some PT classifications are administrative) |
| Duplicate names | Low | ~30 | Common names; not deduped — no UID available |
| Missing Typical Hours for salaried | Expected | 25,042 | By design — NULL means salaried |

---

## Derived Columns (Added During Processing)

| Derived Column | Formula | Purpose |
|----------------|---------|---------|
| `Annual_Equivalent` | `Annual Salary` if salaried; else `Hourly Rate × Typical Hours × 52` | Normalize all pay to annual basis |
| `Compensation_Band` | Quartile buckets: Q1/Q2/Q3/Q4 | Segment analysis |
| `Dept_Short` | Abbreviated department name | Chart label readability |
| `Is_Public_Safety` | 1 if Police/Fire/OEM, else 0 | Public safety vs. civilian split |
| `Salary_Tier` | `<$50K`, `$50K-$100K`, `$100K-$150K`, `$150K+` | Distribution bucketing |

---

## Source Metadata

```
Organization:  City of Chicago
Bureau:        Department of Human Resources
Update Freq:   Annual
License:       Public Domain
Portal URL:    https://data.cityofchicago.org/Administration-Finance/
               Current-Employee-Names-Salaries-and-Position-Title/xzkq-xp2w
data.gov URL:  https://catalog.data.gov/dataset/current-employee-names-salaries-and-position-titles
```
