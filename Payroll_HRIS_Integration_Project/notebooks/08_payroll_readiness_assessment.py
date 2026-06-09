import pandas as pd

# Load pilot employee master data
employees = pd.read_csv(
    "data_processed/pilot_employee_master.csv"
)

# Load attendance exception report
exceptions = pd.read_csv(
    "reports/attendance_exception_report.csv"
)

# Merge employee data with exception data
payroll_readiness = employees.merge(
    exceptions,
    on="EmpID",
    how="left"
)

# If an employee has no exception record, fill Exception_Count with 0
payroll_readiness["Exception_Count"] = (
    payroll_readiness["Exception_Count"]
    .fillna(0)
    .astype(int)
)

# If an employee has no exception record, fill Exception_Types with No Exception
payroll_readiness["Exception_Types"] = (
    payroll_readiness["Exception_Types"]
    .fillna("No Exception")
)

# Create payroll readiness status
payroll_readiness["Payroll_Status"] = payroll_readiness["Exception_Count"].apply(
    lambda x: "Ready for Payroll" if x == 0 else "Review Required"
)

# Create summary table
summary = (
    payroll_readiness["Payroll_Status"]
    .value_counts()
    .reset_index()
)

summary.columns = [
    "Payroll_Status",
    "Employee_Count"
]

summary["Percentage"] = (
    summary["Employee_Count"]
    / summary["Employee_Count"].sum()
    * 100
).round(2)

print("\nPayroll Readiness Summary:")
print(summary)

# Save detailed report
payroll_readiness.to_csv(
    "reports/payroll_readiness_report.csv",
    index=False
)

# Save summary report
summary.to_csv(
    "reports/payroll_readiness_summary.csv",
    index=False
)

print("\nPayroll readiness reports created.")