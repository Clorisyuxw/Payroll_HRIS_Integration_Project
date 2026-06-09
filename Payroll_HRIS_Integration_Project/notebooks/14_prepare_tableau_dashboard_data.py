import pandas as pd
from pathlib import Path

# Define project paths
BASE_DIR = Path(__file__).resolve().parents[1]

PAYROLL_PATH = BASE_DIR / "data_processed" / "payroll_calculated.csv"

SUMMARY_OUTPUT = BASE_DIR / "reports" / "dashboard_payroll_summary.csv"
EXCEPTION_OUTPUT = BASE_DIR / "reports" / "dashboard_exception_summary.csv"
PAYZONE_OUTPUT = BASE_DIR / "reports" / "dashboard_payzone_summary.csv"

# Load payroll calculated data
payroll = pd.read_csv(PAYROLL_PATH)

# -------------------------------
# 1. Payroll summary for dashboard
# -------------------------------

# Create high-level payroll summary by payment status
payroll_summary = (
    payroll
    .groupby("Payroll_Payment_Status")
    .agg(
        Record_Count=("EmpID", "count"),
        Total_Hours=("Hours_Worked", "sum"),
        Total_Gross_Pay=("Gross_Pay", "sum")
    )
    .reset_index()
)

# Round numeric values for reporting
payroll_summary["Total_Hours"] = payroll_summary["Total_Hours"].round(2)
payroll_summary["Total_Gross_Pay"] = payroll_summary["Total_Gross_Pay"].round(2)

# -------------------------------
# 2. Exception summary for dashboard
# -------------------------------

# Create exception summary using payroll calculation status
exception_summary = (
    payroll
    .groupby("Payroll_Calculation_Status")
    .agg(
        Record_Count=("EmpID", "count")
    )
    .reset_index()
)

# -------------------------------
# 3. PayZone summary for dashboard
# -------------------------------

# Create PayZone-level payroll summary
payzone_summary = (
    payroll
    .groupby("PayZone")
    .agg(
        Record_Count=("EmpID", "count"),
        Total_Hours=("Hours_Worked", "sum"),
        Average_Hourly_Rate=("Hourly_Rate", "mean"),
        Total_Gross_Pay=("Gross_Pay", "sum")
    )
    .reset_index()
)

# Round numeric values for reporting
payzone_summary["Total_Hours"] = payzone_summary["Total_Hours"].round(2)
payzone_summary["Average_Hourly_Rate"] = payzone_summary["Average_Hourly_Rate"].round(2)
payzone_summary["Total_Gross_Pay"] = payzone_summary["Total_Gross_Pay"].round(2)

# Save dashboard files
payroll_summary.to_csv(SUMMARY_OUTPUT, index=False)
exception_summary.to_csv(EXCEPTION_OUTPUT, index=False)
payzone_summary.to_csv(PAYZONE_OUTPUT, index=False)

# Print summary
print("Step 14 - Tableau Dashboard Data Prepared")
print("----------------------------------------")

print("\nPayroll Summary:")
print(payroll_summary)

print("\nException Summary:")
print(exception_summary)

print("\nPayZone Summary:")
print(payzone_summary)

print("\nDashboard files saved to reports folder.")