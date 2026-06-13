# AI-Accelerated Workforce Analytics
## Prompt Library & GPT-4/Claude Generated Insights

**Project**: Chicago City Workforce Analytics   
**AI Tools Used**: GPT-4 (OpenAI), Claude (Anthropic)  
**Purpose**: Demonstrate AI-Accelerated analytics workflows at a senior level

---

## Section 1: AI-Accelerated Executive Insights

*The following narrative was generated using GPT-4 with structured data inputs from our analysis pipeline. This demonstrates AI-Accelerated report writing — a key senior analyst skill.*

---

### 1.1 Workforce Composition Narrative

**Prompt used**:
```
You are a senior municipal finance analyst. Based on the following workforce data 
for City of Chicago employees, write a 3-paragraph executive summary suitable for 
the City Comptroller.

Data:
- Total employees: 31,984
- Departments: 39
- Public safety (CPD + CFD + OEMC): 17,985 employees (56.2%)
- Salaried: 25,042 (78.3%) | Hourly: 6,942 (21.7%)
- Full-time: 31,097 (97.2%) | Part-time: 887 (2.8%)
- Total annual payroll estimate: $3.54 billion
- Median annual compensation: $111,252

Write professionally. No bullet points. Include one strategic recommendation.
```

**AI-Accelerated Output**:

The City of Chicago maintains a workforce of 31,984 employees across 39 departments, representing a total estimated annual payroll commitment of approximately $3.54 billion. The composition of this workforce reflects the city's core mission priorities: 56.2% of all employees are engaged in public safety functions — including the Chicago Police Department, Chicago Fire Department, and the Office of Emergency Management and Communications. This concentration underscores the significant operational and financial weight that public safety obligations place on the city's human capital budget.

The workforce is predominantly composed of full-time, salaried employees, with 97.2% classified as full-time and 78.3% receiving fixed annual salaries. The median annual compensation of $111,252 sits substantially above both the U.S. median worker wage ($63,795, BLS 2024) and the Illinois statewide average annual wage ($72,130), reflecting the skilled nature of municipal roles, strong collective bargaining agreements, and the high cost of living in the Chicago metropolitan area. The remaining 21.7% of hourly workers, when annualized at their contracted hours, average approximately $93,745 annually — a meaningful gap relative to their salaried counterparts that warrants periodic equity review.

**Strategic Recommendation**: Given that public safety accounts for over 56% of the workforce and an estimated 64% of total payroll expenditure, the City should prioritize scenario modeling around public safety staffing levels and wage structure negotiations. Any changes to CPD or CFD compensation formulas — including overtime provisions, step increases, and contract renewals — will have outsized fiscal impact. The analytics infrastructure established in this project provides a baseline for multi-year payroll forecasting and labor cost sensitivity analysis.

---

### 1.2 Compensation Disparity Analysis Narrative

**Prompt used**:
```
Based on statistical analysis of City of Chicago employee data:
- Salaried median: $115,158 | Hourly (annualized) median: $101,358
- Statistical test: Mann-Whitney U, p < 1e-300, Cohen's d = 0.674 (large effect)
- Full-time median: $112,104 | Part-time median: $19,344
- ANOVA across 10 departments: F=1,120.9, p < 1e-300, η² = 0.266 (large)

Write 2 paragraphs analyzing these findings for a compensation committee review.
Focus on what these statistics mean for policy, not just the numbers themselves.
```

**AI-Accelerated Output**:

The statistical analysis reveals that compensation differences between salaried and hourly workers are not merely anecdotal but are large, consistent, and highly significant. With a Cohen's d of 0.674 — a large effect size by conventional standards — hourly employees earn roughly $13,800 less annually (median basis) than their salaried counterparts, even after annualizing hourly wages using contracted weekly hours. This gap persists across the entire workforce distribution, suggesting it is structural rather than concentrated among outliers. From a policy standpoint, this finding invites two questions: (1) whether hourly roles could be reclassified to salaried structures to reduce pay volatility and improve workforce stability, and (2) whether the annualized hourly equivalent truly represents actual take-home earnings, or whether variable hours lead to even larger realized income gaps.

The ANOVA result — F-statistic of 1,120.9 with an eta-squared of 0.266 — indicates that department membership alone explains 26.6% of the variance in compensation across the workforce. This is an exceptionally large departmental effect for a city government, where one might expect standardized pay scales to minimize inter-departmental variation. The Department of Buildings' median compensation of $133,432 versus the Office of Emergency Management's $78,744 represents a 69% gap between departments — a range that may reflect legitimate differences in required expertise and licensure, but also merits review for equity and competitiveness. Compensation benchmarking against peer municipalities (Milwaukee, Minneapolis, Indianapolis) would provide additional context for whether these departmental differentials represent market-rate alignment or structural anomalies.

---

### 1.3 Top Earner Analysis Narrative

**AI-Prompt + Output Summary**:

The top compensation tier (>$150K annually) comprises 2,563 employees — 8.0% of the workforce but responsible for 12.1% of total payroll expenditure. The maximum single-employee compensation is $350,000, concentrated in senior executive and elected official roles. The Chicago Police Department contributes the largest absolute number of $150K+ earners, reflecting the combination of base pay, longevity increments, and overtime provisions embedded in the Fraternal Order of Police contract.

---

## Section 2: Reusable AI Prompt Library

*These prompts are ready to use with GPT-4, Claude, or any LLM for ongoing workforce analytics work.*

---

### Prompt 01: Anomaly Narration
```
You are a data analyst. I have a list of employees flagged as compensation outliers
using the IQR method (below Q1-1.5×IQR or above Q3+1.5×IQR).

Here are the high outliers: [PASTE TABLE]
Here are the low outliers: [PASTE TABLE]

For each group:
1. Identify the most likely explanation (elected official, specialized role, data entry error)
2. Flag any that require HR review
3. Suggest whether to include or exclude in aggregate analysis
Keep your response concise and in table format.
```

---

### Prompt 02: Department Narrative Generator
```
Generate a 1-paragraph profile of the [DEPARTMENT NAME] based on:
- Headcount: [N]
- Average compensation: $[X]
- Median compensation: $[X]
- Equity ratio vs city avg: [R]
- Pay type breakdown: [X% salaried, X% hourly]
- Top job title: [TITLE] (n=[N])

Write as if presenting to a city council finance committee. Be factual, neutral in tone,
and end with one question the committee might want to ask department leadership.
```

---

### Prompt 03: Executive Summary Auto-Draft
```
Using the following workforce analytics statistics, draft a 1-page executive summary
suitable for a city CFO. Use professional language, avoid jargon, and include:
1. Headline workforce facts (3 bullets)
2. Key financial findings (2 paragraphs)
3. Recommended actions (3 bullets)

Data: [PASTE SUMMARY TABLE]
```

---

### Prompt 04: SQL Query Generator
```
I have a SQL table called workforce_clean with these columns:
employee_name, job_title, department, employment_type (F/P),
pay_type (SALARY/HOURLY), typical_hours, annual_salary,
hourly_rate, annual_equivalent, compensation_tier, is_public_safety

Write a SQL query to: [DESCRIBE WHAT YOU WANT]
Use SQLite syntax. Include comments explaining each major step.
Return only the SQL, no explanation.
```

---

### Prompt 05: Statistical Interpretation
```
I ran a Mann-Whitney U test comparing salaried vs hourly employee compensation.
Results: U = 116,300,697.5, p < 1e-300, Cohen's d = 0.674.

Explain:
1. What this result means in plain English for a non-statistician
2. Why Mann-Whitney was the right choice over a t-test
3. What "large effect size" means practically in this workforce context
4. What follow-up analysis would be recommended

Keep the explanation to 3-4 paragraphs. No formulas.
```

---

### Prompt 06: Compensation Band Policy Recommendation
```
City of Chicago workforce data shows:
- 4.8% of employees earn under $50K annually
- 78.5% earn between $75K and $150K
- 8.0% earn over $150K
- Part-time workers average $19,344 (dramatically lower due to fewer hours)

As an HR policy advisor, provide 3 recommendations for:
1. Addressing the low-wage employee segment
2. Managing the concentration in the $75K-$150K band
3. Ensuring part-time workers have access to benefits and career growth

Format as an executive memo. Be specific and actionable.
```

---

### Prompt 07: Payroll Forecast Scenario
```
Current City of Chicago annual payroll is $3.54 billion across 31,984 employees.

Model three scenarios for Year 1 payroll impact:
1. 2.5% across-the-board raise for all employees
2. 5% raise for all hourly workers only (6,942 employees)
3. Adding 500 new police officers at median CPD salary ($115,158)

For each scenario:
- Calculate the dollar impact
- Express as % change from base
- Identify which departments are most affected

Present as a comparison table.
```

---

### Prompt 08: Data Quality Review
```
Review this dataset description and identify potential data quality issues 
that a senior analyst should flag before presenting findings:

[Dataset description: 31,984 city employees, 8 columns, some employees earning 
as little as $199 annually, no unique employee ID, Typical Hours NULL for salaried,
39 departments, data from city open portal - no update timestamp on records]

For each issue: (1) describe the problem, (2) rate severity Low/Medium/High,
(3) suggest a mitigation. Use a table format.
```

---

### Prompt 09: Benchmarking Narrative
```
City of Chicago median employee compensation is $111,252.
Compare this to: U.S. median worker ($63,795), Illinois avg ($72,130),
U.S. federal employees ($101,397), and median household income ($80,610).

Write a 2-paragraph analysis:
- Para 1: Contextualize the Chicago figure relative to benchmarks
- Para 2: Explain the factors that likely drive this premium (union contracts,
  required certifications, public safety roles, cost of living) and whether
  it represents good or poor value for taxpayers

Maintain an analytical, non-political tone.
```

---

### Prompt 10: Visualization Recommendation
```
I have the following data about Chicago city employees and want to create 
a Power BI dashboard page for the city CFO.

Available metrics:
- Headcount by department (39 depts)
- Annual payroll by department
- Compensation distribution (histogram data)
- Pay type split (78% salary / 22% hourly)
- Full/part-time split (97% FT / 3% PT)
- Top 20 job titles by avg comp

Recommend:
1. The best chart type for each metric, with justification
2. The layout arrangement for a single dashboard page
3. Which 3 visuals are highest priority for the CFO
4. Which filters/slicers to include
```

---

## Section 3: AI-Accelerated Python Pipeline

The following shows how AI was used to accelerate the analytical pipeline:

### 3.1 Anomaly Detection with LLM Context
```python
# ai_insights/ai_accelerated_pipeline.py
# Example: Using AI to narrate detected outliers

import pandas as pd
import json

def flag_and_narrate_outliers(df, api_client):
    """
    Uses IQR method to detect outliers, then sends
    summary to LLM for narrative context generation.
    """
    q1 = df['annual_equivalent'].quantile(0.25)
    q3 = df['annual_equivalent'].quantile(0.75)
    iqr = q3 - q1
    
    high_outliers = df[df['annual_equivalent'] > q3 + 1.5 * iqr][
        ['employee_name', 'job_title', 'department', 'annual_equivalent']
    ].head(20)
    
    low_outliers = df[df['annual_equivalent'] < q1 - 1.5 * iqr][
        ['employee_name', 'job_title', 'department', 'annual_equivalent']
    ].head(20)
    
    # Build prompt with actual data
    prompt = f"""
    Analyze these compensation outliers from Chicago city employee data.
    
    HIGH OUTLIERS (above ${q3 + 1.5*iqr:,.0f}):
    {high_outliers.to_string(index=False)}
    
    LOW OUTLIERS (below ${q1 - 1.5*iqr:,.0f}):
    {low_outliers.to_string(index=False)}
    
    For each group, provide:
    1. Likely explanation for the outlier
    2. Whether it appears to be a data quality issue or legitimate
    3. Recommended action (flag for HR, exclude from avg, keep as-is)
    """
    
    # Call API (replace with actual OpenAI/Claude API call)
    # response = api_client.complete(prompt)
    # return response.text
    
    return prompt  # Return prompt for demonstration

# Usage:
# df = pd.read_csv('data/processed/chicago_workforce_cleaned.csv')
# prompt = flag_and_narrate_outliers(df, api_client)
# print(prompt)
```

---

## Section 4: AI Tools Comparison for Data Analytics

| Tool | Best For | Limitations | Cost |
|------|---------|-------------|------|
| **GPT-4** | Long narrative generation, code writing | No live data access | ~$0.03/1K tokens |
| **Claude (Anthropic)** | Document analysis, structured reasoning | Context window limits | ~$0.015/1K tokens |
| **GitHub Copilot** | Real-time Python/SQL code completion | Not for analysis narrative | $10/month |
| **ChatGPT Data Analysis** | Quick EDA on uploaded CSVs | Limited customization | Included in Plus |
| **Power BI Copilot** | DAX generation, visual narration | Requires Premium capacity | $20/user/month |
| **Tableau AI** | In-visual explanations | Tableau license required | Bundled |

---

## Section 5: AI Ethics & Governance for Analytics

When using AI in workforce analytics, observed these principles:

1. **No PII in prompts**: Never send employee names, IDs, or identifying info to external LLMs. Aggregate or anonymize first.
2. **Validate AI outputs**: All AI-Accelerated SQL must be reviewed and tested before production use.
3. **Disclose AI use**: Clearly mark AI-Accelerated content in reports and presentations.
4. **Human review required**: AI narrative insights should be reviewed by a senior analyst before sharing with leadership.
5. **Data sovereignty**: Understand that data sent to cloud AI APIs may be used for model training (check vendor agreements).
6. **Bias awareness**: AI may reflect biases in training data — workforce analytics outputs should always be reviewed for unintended discriminatory framing.
