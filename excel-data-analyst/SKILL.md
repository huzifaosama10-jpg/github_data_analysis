---
name: excel-data-analyst
description: Analyze Excel and CSV files using Python. Use this skill when users request data cleaning, descriptive statistics, missing-value analysis, duplicate detection, outlier detection, correlations, categorical summaries, or charts from tabular data.
---

# Excel Data Analyst

## Purpose
Analyze Excel and CSV files and provide clear, accurate, practical insights.

## Supported Files
- CSV
- XLSX
- XLS

## Available Script
Use `scripts/analyze.py` to perform data analysis.

## Workflow

1. Identify the user's uploaded Excel or CSV file.
2. Check whether the file is accessible to the Python environment.
3. Run the analysis script:

   `python scripts/analyze.py "path/to/file.xlsx"`

4. For a specific Excel sheet:

   `python scripts/analyze.py "path/to/file.xlsx" --sheet "Sheet1"`

5. Read the generated `analysis_output/report.json`.
6. Inspect the generated charts in `analysis_output/charts/`.
7. Explain the results in clear language.
8. Highlight important patterns, anomalies, and data-quality issues.

## Analysis Features

The script can provide:

- Dataset dimensions.
- Column data types.
- Missing values.
- Duplicate rows.
- Descriptive statistics for numerical columns.
- Outlier detection using the IQR method.
- Categorical summaries.
- Correlation analysis.
- Histograms for numerical columns.

## Interpretation Rules

- Never invent values or findings.
- Distinguish correlation from causation.
- Explain the limitations of the dataset.
- Do not assume missing values are errors without context.
- Explain statistical findings in language appropriate for the user.
- Recommend practical next steps when useful.

## Error Handling

- If required Python libraries are missing, explain how to install them.
- If the file cannot be accessed, ask the user to provide an accessible file path.
- If the script fails, inspect the error before reporting results.
- Never claim that an analysis was completed unless the script actually ran successfully.

## Output Format

Present the analysis using these sections when relevant:

1. Executive Summary
2. Dataset Overview
3. Data Quality
4. Descriptive Statistics
5. Outliers and Anomalies
6. Correlations
7. Charts and Visual Insights
8. Recommendations

Adapt the report to the user's actual question instead of presenting unnecessary sections.