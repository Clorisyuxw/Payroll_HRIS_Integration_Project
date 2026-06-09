import pandas as pd
from pathlib import Path

# Define project paths
BASE_DIR = Path(__file__).resolve().parents[1]

EMPLOYEE_PATH = BASE_DIR / "data_processed" / "pilot_employee_master.csv"
HOURS_PATH = BASE_DIR / "data_processed" / "daily_hours_calculated.csv"
OUTPUT_PATH = BASE_DIR / "data_processed" / "daily_hours_with_rates.csv"

# Load employee master data
employees = pd.read_csv(EMPLOYEE_PATH)

# Load daily hours data
daily_hours = pd.read_csv(HOURS_PATH)

# Keep only the employee fields needed for payroll rate assignment
employee_pay_rules = employees[
    ["EmpID", "PayZone", "EmployeeType", "BusinessUnit"]
].copy()

# Define hourly rate rules based on PayZone
# PayZone is used as a simplified payroll pay grade
payzone_rate_map = {
    "Zone A": 28,
    "Zone B": 32,
    "Zone C": 38
}

# Assign hourly rate to each employee
employee_pay_rules["Hourly_Rate"] = employee_pay_rules["PayZone"].map(
    payzone_rate_map
)

# Merge daily hours with employee pay rules
# This adds PayZone and Hourly_Rate to each daily attendance record
payroll_hours = daily_hours.merge(
    employee_pay_rules,
    on="EmpID",
    how="left"
)

# Create rate assignment status
payroll_hours["Rate_Status"] = "Rate Assigned"

# Mark records where PayZone is missing
payroll_hours.loc[
    payroll_hours["PayZone"].isna(),
    "Rate_Status"
] = "Missing PayZone"

# Mark records where Hourly_Rate is missing
payroll_hours.loc[
    payroll_hours["Hourly_Rate"].isna(),
    "Rate_Status"
] = "Missing Hourly Rate"

# Save output file
payroll_hours.to_csv(OUTPUT_PATH, index=False)

# Print summary
print("Step 10 - Hourly Rates Assigned")
print("--------------------------------")
print("Total records:", len(payroll_hours))

print("\nPayZone Distribution:")
print(payroll_hours["PayZone"].value_counts())

print("\nHourly Rate Distribution:")
print(payroll_hours["Hourly_Rate"].value_counts())

print("\nRate Status Summary:")
print(payroll_hours["Rate_Status"].value_counts())

print("\nOutput saved to:")
print(OUTPUT_PATH)