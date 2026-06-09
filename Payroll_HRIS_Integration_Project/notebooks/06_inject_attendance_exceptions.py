import pandas as pd
import random

# Load generated attendance data
attendance = pd.read_csv(
    "data_processed/timefiler_attendance_generated.csv"
)

# Add a new column to mark whether a record is normal or exception
attendance["Exception_Type"] = "No Exception"

# Set random seed so results are reproducible
random.seed(42)

# Decide how many exceptions to create
total_records = len(attendance)
exception_count = round(total_records * 0.0022)

print("Total records:", total_records)
print("Target exception count:", exception_count)

# Randomly select records for exceptions
exception_indices = random.sample(
    list(attendance.index),
    exception_count
)

# Split exceptions into three types
missing_clock_out_indices = exception_indices[:20]
device_failure_indices = exception_indices[20:30]
duplicate_punch_indices = exception_indices[30:]

# Create Missing Clock Out exceptions
attendance.loc[
    missing_clock_out_indices,
    "Exception_Type"
] = "Missing Clock Out"

# Create Device Failure exceptions
attendance.loc[
    device_failure_indices,
    "Exception_Type"
] = "Device Failure"

# Create Duplicate Punch exceptions
attendance.loc[
    duplicate_punch_indices,
    "Exception_Type"
] = "Duplicate Punch"

print("\nException Type Distribution:")
print(attendance["Exception_Type"].value_counts())

attendance.to_csv(
    "data_processed/timefiler_attendance_with_exceptions.csv",
    index=False
)

print("\nAttendance exceptions injected.")