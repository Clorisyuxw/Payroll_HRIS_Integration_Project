import pandas as pd
import numpy as np
from pathlib import Path

# Define project paths
BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data_processed" / "daily_hours_with_rates.csv"
OUTPUT_PATH = BASE_DIR / "data_processed" / "payroll_calculated.csv"

# Load payroll source data
payroll = pd.read_csv(INPUT_PATH)

# Create Gross Pay column with numeric missing values
# np.nan is better than None for numeric calculations in pandas
payroll["Gross_Pay"] = np.nan

# Identify records that are ready for payroll calculation
ready_mask = (
    payroll["Payroll_Calculation_Status"]
    == "Ready for Payroll Calculation"
)

# Calculate Gross Pay only for records ready for payroll calculation
payroll.loc[
    ready_mask,
    "Gross_Pay"
] = (
    payroll.loc[ready_mask, "Hours_Worked"]
    *
    payroll.loc[ready_mask, "Hourly_Rate"]
)

# Round payroll amounts to 2 decimal places
payroll["Gross_Pay"] = payroll["Gross_Pay"].round(2)

# Create default payment status
payroll["Payroll_Payment_Status"] = "Ready for Payment"

# Put exception records on hold
payroll.loc[
    payroll["Payroll_Calculation_Status"] == "Review Required",
    "Payroll_Payment_Status"
] = "On Hold - Review Required"

# Keep gross pay empty for records under review
# These records should not be paid until manual review is completed
payroll.loc[
    payroll["Payroll_Payment_Status"] == "On Hold - Review Required",
    "Gross_Pay"
] = np.nan

# Save output
payroll.to_csv(
    OUTPUT_PATH,
    index=False
)

# Print summary
print("Step 11 - Payroll Calculation Completed")
print("--------------------------------------")

print("\nPayment Status Summary:")
print(
    payroll["Payroll_Payment_Status"].value_counts()
)

print("\nTotal Gross Pay:")
print(
    round(
        payroll["Gross_Pay"].fillna(0).sum(),
        2
    )
)

print("\nAverage Daily Gross Pay:")
print(
    round(
        payroll["Gross_Pay"].fillna(0).mean(),
        2
    )
)

print("\nOutput saved to:")
print(OUTPUT_PATH)