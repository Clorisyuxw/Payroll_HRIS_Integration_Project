import pandas as pd
from pathlib import Path

# Define project paths
BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data_processed" / "payroll_calculated.csv"
OUTPUT_PATH = BASE_DIR / "reports" / "dashboard_employee_summary.csv"

# Load payroll data
payroll = pd.read_csv(INPUT_PATH)

# Employee-level payroll status
employee_summary = (
    payroll
    .groupby("EmpID")
    .agg(
        Review_Count=(
            "Payroll_Payment_Status",
            lambda x: (x == "On Hold - Review Required").sum()
        )
    )
    .reset_index()
)

employee_summary["Employee_Payroll_Status"] = (
    employee_summary["Review_Count"]
    .apply(
        lambda x:
        "Review Required"
        if x > 0
        else "Ready for Payment"
    )
)

dashboard_summary = (
    employee_summary
    .groupby("Employee_Payroll_Status")
    .size()
    .reset_index(name="Employee_Count")
)

dashboard_summary.to_csv(
    OUTPUT_PATH,
    index=False
)

print(dashboard_summary)