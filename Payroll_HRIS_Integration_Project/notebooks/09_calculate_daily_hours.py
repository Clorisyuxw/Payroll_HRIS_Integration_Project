import pandas as pd
from pathlib import Path

# Define project paths
BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data_processed" / "timefiler_attendance_with_exceptions.csv"
OUTPUT_PATH = BASE_DIR / "data_processed" / "daily_hours_calculated.csv"
# Load TimeFiler punch transaction data
attendance = pd.read_csv(INPUT_PATH)

# Convert Work_Date to date format
# This helps Python recognise the column as a real date
attendance["Work_Date"] = pd.to_datetime(attendance["Work_Date"], errors="coerce")

# Create separate Clock In table
# Each row represents one clock-in punch
clock_in = attendance[
    attendance["Attendance_Event"] == "Clock In"
].copy()

# Create separate Clock Out table
# Each row represents one clock-out punch
clock_out = attendance[
    attendance["Attendance_Event"] == "Clock Out"
].copy()

# For each employee and work date, keep the earliest Clock In time
# This handles duplicate clock-in punches by using the first clock-in time
daily_clock_in = (
    clock_in
    .groupby(["EmpID", "Work_Date"], as_index=False)
    .agg(
        Clock_In=("Clock_Time", "min"),
        Clock_In_Exception=("Exception_Type", lambda x: ", ".join(sorted(set(x))))
    )
)

# For each employee and work date, keep the latest Clock Out time
# This handles duplicate clock-out punches by using the last clock-out time
daily_clock_out = (
    clock_out
    .groupby(["EmpID", "Work_Date"], as_index=False)
    .agg(
        Clock_Out=("Clock_Time", "max"),
        Clock_Out_Exception=("Exception_Type", lambda x: ", ".join(sorted(set(x))))
    )
)

# Merge Clock In and Clock Out into one daily attendance table
# Each row should now represent one employee on one work date
daily_hours = daily_clock_in.merge(
    daily_clock_out,
    on=["EmpID", "Work_Date"],
    how="outer"
)

# Combine Work_Date and Clock_In into a full datetime value
daily_hours["Clock_In_Datetime"] = pd.to_datetime(
    daily_hours["Work_Date"].astype(str) + " " + daily_hours["Clock_In"],
    errors="coerce"
)

# Combine Work_Date and Clock_Out into a full datetime value
daily_hours["Clock_Out_Datetime"] = pd.to_datetime(
    daily_hours["Work_Date"].astype(str) + " " + daily_hours["Clock_Out"],
    errors="coerce"
)

# Calculate worked hours
# The time difference is calculated in seconds, then converted to hours
daily_hours["Hours_Worked"] = (
    (daily_hours["Clock_Out_Datetime"] - daily_hours["Clock_In_Datetime"])
    .dt.total_seconds()
    / 3600
)

# Round hours to 2 decimal places for payroll calculation
daily_hours["Hours_Worked"] = daily_hours["Hours_Worked"].round(2)

# Create default status
daily_hours["Hours_Status"] = "Valid"

# Mark missing clock-in records
daily_hours.loc[
    daily_hours["Clock_In"].isna(),
    "Hours_Status"
] = "Missing Clock In"

# Mark missing clock-out records
daily_hours.loc[
    daily_hours["Clock_Out"].isna(),
    "Hours_Status"
] = "Missing Clock Out"

# Mark records where hours cannot be calculated
daily_hours.loc[
    daily_hours["Hours_Worked"].isna(),
    "Hours_Status"
] = "Unable to Calculate"

# Mark invalid negative hours
daily_hours.loc[
    daily_hours["Hours_Worked"] < 0,
    "Hours_Status"
] = "Invalid Negative Hours"

# Mark unusually long shifts
daily_hours.loc[
    daily_hours["Hours_Worked"] > 16,
    "Hours_Status"
] = "Unusually Long Shift"

# Mark short shifts for review
daily_hours.loc[
    (daily_hours["Hours_Worked"] > 0) & (daily_hours["Hours_Worked"] < 4),
    "Hours_Status"
] = "Short Shift - Review"

# Default payroll status
daily_hours["Payroll_Calculation_Status"] = "Ready for Payroll Calculation"

# Review if hours calculation failed
daily_hours.loc[
    daily_hours["Hours_Status"] != "Valid",
    "Payroll_Calculation_Status"
] = "Review Required"

# Review if clock-in side contains attendance exceptions
daily_hours.loc[
    daily_hours["Clock_In_Exception"] != "No Exception",
    "Payroll_Calculation_Status"
] = "Review Required"

# Review if clock-out side contains attendance exceptions
daily_hours.loc[
    daily_hours["Clock_Out_Exception"] != "No Exception",
    "Payroll_Calculation_Status"
] = "Review Required"

# Save daily hours output
daily_hours.to_csv(OUTPUT_PATH, index=False)

# Print summary
print("Step 09 - Daily Hours Calculation Completed")
print("------------------------------------------")
print("Total daily attendance records:", len(daily_hours))

print("\nHours Status Summary:")
print(daily_hours["Hours_Status"].value_counts())

print("\nPayroll Calculation Status Summary:")
print(daily_hours["Payroll_Calculation_Status"].value_counts())

print("\nOutput saved to:")
print(OUTPUT_PATH)