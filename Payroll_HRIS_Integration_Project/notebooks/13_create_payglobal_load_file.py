import pandas as pd
from pathlib import Path

# Define project paths
BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data_processed" / "payroll_calculated.csv"
OUTPUT_PATH = BASE_DIR / "data_processed" / "payglobal_load_file.csv"

# Load calculated payroll data
payroll = pd.read_csv(INPUT_PATH)

# Keep only records approved for payment
payglobal_load = payroll[
    payroll["Payroll_Payment_Status"]
    == "Ready for Payment"
].copy()

# Create payroll period
# In a real payroll project this would normally come
# from payroll calendars or pay cycles
payglobal_load["Pay_Period"] = "2025-01"

# Select fields required for payroll loading
payglobal_load = payglobal_load[
    [
        "EmpID",
        "Pay_Period",
        "Work_Date",
        "Hours_Worked",
        "Hourly_Rate",
        "Gross_Pay"
    ]
]

# Save PayGlobal load file
payglobal_load.to_csv(
    OUTPUT_PATH,
    index=False
)

# Print summary
print("Step 13 - PayGlobal Load File Created")
print("------------------------------------")

print("\nRecords Ready For Payroll Import:")
print(len(payglobal_load))

print("\nTotal Gross Pay Being Loaded:")
print(
    round(
        payglobal_load["Gross_Pay"].sum(),
        2
    )
)

print("\nOutput saved to:")
print(OUTPUT_PATH)