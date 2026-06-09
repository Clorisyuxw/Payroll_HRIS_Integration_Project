import pandas as pd

# Load the original TimeFiler attendance sample
attendance = pd.read_csv(
    "data_raw/timefiler_attendance.csv"
)

# Show basic dataset size
print("Rows and Columns:")
print(attendance.shape)

# Show column names
print("\nColumns:")
print(attendance.columns)

# Check missing values
print("\nMissing Values:")
print(attendance.isnull().sum())

# Count unique employees
print("\nUnique Employees:")
print(attendance["id_empleado"].nunique())

# Count attendance event types
print("\nAttendance Event Distribution:")
print(attendance["etiqueta"].value_counts())

# Calculate total records
total_records = len(attendance)

# Calculate exception records
exception_events = [
    "incompleto",
    "confusion",
    "fallo dispositivo"
]

exception_count = attendance[
    attendance["etiqueta"].isin(exception_events)
].shape[0]

# Calculate exception rate
exception_rate = exception_count / total_records * 100

print("\nException Count:")
print(exception_count)

print("\nException Rate (%):")
print(round(exception_rate, 2))

# Count average records per employee
records_per_employee = (
    attendance
    .groupby("id_empleado")
    .size()
    .reset_index(name="Record_Count")
)

print("\nAverage Records per Employee:")
print(round(records_per_employee["Record_Count"].mean(), 2))

# Save the employee-level record summary
records_per_employee.to_csv(
    "reports/timefiler_records_per_employee.csv",
    index=False
)

print("\nAttendance pattern assessment completed.")