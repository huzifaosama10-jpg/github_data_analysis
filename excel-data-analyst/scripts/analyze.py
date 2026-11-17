
"""
Excel Data Analyst
A basic data analysis tool for Excel and CSV files.
"""

import argparse
import json
import math
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def to_native(value):
    """Convert NumPy and Pandas values into JSON-compatible values."""
    if isinstance(value, dict):
        return {str(k): to_native(v) for k, v in value.items()}

    if isinstance(value, list):
        return [to_native(v) for v in value]

    if isinstance(value, (np.integer,)):
        return int(value)

    if isinstance(value, (np.floating, float)):
        return float(value) if math.isfinite(float(value)) else None

    if isinstance(value, np.bool_):
        return bool(value)

    if pd.isna(value):
        return None

    return value


def load_data(file_path, sheet=None):
    """Load Excel or CSV data."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    extension = path.suffix.lower()

    if extension == ".csv":
        return pd.read_csv(path)

    if extension in [".xlsx", ".xls"]:
        return pd.read_excel(path, sheet_name=0 if sheet is None else sheet)

    raise ValueError("Only CSV, XLSX and XLS files are supported.")


def analyze_data(df, output_dir):
    """Analyze dataset and create a report."""

    output_dir = Path(output_dir)
    charts_dir = output_dir / "charts"

    output_dir.mkdir(parents=True, exist_ok=True)
    charts_dir.mkdir(parents=True, exist_ok=True)

    numeric_columns = df.select_dtypes(include="number").columns

    # Basic information
    report = {
        "dataset_shape": {
            "rows": len(df),
            "columns": len(df.columns)
        },
        "columns": {
            col: str(dtype)
            for col, dtype in df.dtypes.items()
        },
        "missing_values": df.isna().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_statistics": {},
        "outliers": {},
        "categorical_summary": {},
        "correlations": {},
        "charts": []
    }

    # Descriptive statistics
    if len(numeric_columns) > 0:
        stats = df[numeric_columns].describe().round(3)
        report["numeric_statistics"] = to_native(stats.to_dict())

        # Outlier detection using IQR
        for col in numeric_columns:
            series = df[col].dropna()

            if len(series) == 0:
                continue

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            count = int(((series < lower) | (series > upper)).sum())

            report["outliers"][col] = {
                "lower_bound": float(lower),
                "upper_bound": float(upper),
                "count": count
            }

            # Histogram
            if len(series) >= 2 and len(report["charts"]) < 6:
                plt.figure(figsize=(8, 5))
                plt.hist(series, bins=15)
                plt.title(f"Distribution of {col}")
                plt.xlabel(col)
                plt.ylabel("Frequency")
                plt.tight_layout()

                chart_path = charts_dir / f"{col}_histogram.png"
                plt.savefig(chart_path)
                plt.close()

                report["charts"].append(str(chart_path))

        # Correlation analysis
        if len(numeric_columns) >= 2:
            corr = df[numeric_columns].corr().round(3)
            report["correlations"] = to_native(corr.to_dict())

    # Categorical summaries
    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    for col in categorical_columns:
        report["categorical_summary"][col] = {
            "unique_values": int(df[col].nunique()),
            "top_values": to_native(
                df[col].value_counts().head(5).to_dict()
            )
        }

    # Save report
    report_path = output_dir / "report.json"

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(
            to_native(report),
            file,
            ensure_ascii=False,
            indent=4
        )

    print("\nAnalysis completed successfully!")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Duplicate rows: {report['duplicate_rows']}")
    print(f"Report saved to: {report_path}")
    print(f"Charts saved to: {charts_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Excel and CSV Data Analyst"
    )

    parser.add_argument(
        "file",
        help="Path to Excel or CSV file"
    )

    parser.add_argument(
        "--sheet",
        default=None,
        help="Excel sheet name (optional)"
    )

    parser.add_argument(
        "--output",
        default="analysis_output",
        help="Output folder"
    )

    args = parser.parse_args()

    try:
        df = load_data(args.file, args.sheet)
        analyze_data(df, args.output)

    except Exception as error:
        print(f"Error: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
