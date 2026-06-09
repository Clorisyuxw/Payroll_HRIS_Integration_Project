import pandas as pd
from pathlib import Path

# Define project paths
BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data_processed" / "payroll_calculated.csv"
OUTPUT_PATH = BASE_DIR / "reports" / "payroll_validation_report.csv"

# Load payroll results
payroll = pd.read_csv(INPUT_PATH)

validation_results = []

# Check 1: Missing Gross Pay for records ready to pay
missing_pay = payroll[
    (payroll["Payroll_Payment_Status"] == "Ready for Payment")
    &
    (payroll["Gross_Pay"].isna())
]

validation_results.append({
    "Validation_Check": "Missing Gross Pay",
    "Issue_Count": len(missing_pay)
})

# Check 2: Negative payroll amounts
negative_pay = payroll[
    payroll["Gross_Pay"] < 0
]

validation_results.append({
    "Validation_Check": "Negative Gross Pay",
    "Issue_Count": len(negative_pay)
})

# Check 3: Unusually high payroll amounts
# Threshold can be adjusted based on business rules
high_pay = payroll[
    payroll["Gross_Pay"] > 1000
]

validation_results.append({
    "Validation_Check": "High Gross Pay (>1000)",
    "Issue_Count": len(high_pay)
})

# Check 4: Review records accidentally calculated
review_paid = payroll[
    (payroll["Payroll_Payment_Status"] == "On Hold - Review Required")
    &
    (payroll["Gross_Pay"].notna())
]

validation_results.append({
    "Validation_Check": "Review Records Calculated",
    "Issue_Count": len(review_paid)
})

# Create validation report
validation_report = pd.DataFrame(validation_results)

# Create pass/review status
validation_report["Status"] = validation_report["Issue_Count"].apply(
    lambda x: "Pass" if x == 0 else "Review Required"
)

# Save report
validation_report.to_csv(
    OUTPUT_PATH,
    index=False
)

# Print results
print("Step 12 - Payroll Validation Completed")
print("--------------------------------------")

print(validation_report)

print("\nValidation report saved to:")
print(OUTPUT_PATH)