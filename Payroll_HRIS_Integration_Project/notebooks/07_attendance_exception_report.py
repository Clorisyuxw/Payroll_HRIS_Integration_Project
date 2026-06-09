import pandas as pd

# Load attendance data with injected exceptions
attendance = pd.read_csv(
    "data_processed/timefiler_attendance_with_exceptions.csv"
)

# Keep only records with exceptions
exceptions = attendance[
    attendance["Exception_Type"] != "No Exception"
]

print("Total exception records:")
print(len(exceptions))

print("\nException type distribution:")
print(exceptions["Exception_Type"].value_counts())

# Create employee-level exception summary
exception_report = (
    exceptions
    .groupby("EmpID")
    .agg(
        Exception_Count=("Exception_Type", "count"),
        Exception_Types=("Exception_Type", lambda x: ", ".join(sorted(set(x))))
    )
    .reset_index()
)

print("\nEmployee-level exception report:")
print(exception_report.head(20))

exception_report.to_csv(
    "reports/attendance_exception_report.csv",
    index=False
)

print("\nAttendance exception report created.")