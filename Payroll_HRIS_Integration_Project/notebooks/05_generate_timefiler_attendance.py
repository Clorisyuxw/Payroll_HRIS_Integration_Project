import pandas as pd
import random
from datetime import datetime, timedelta

# Load pilot employee master data
employees = pd.read_csv(
    "data_processed/pilot_employee_master.csv"
)

attendance_records = []

# Start date for attendance generation
start_date = datetime(2025, 1, 1)

# Generate attendance for each employee
for _, employee in employees.iterrows():

    employee_id = employee["EmpID"]

    # Generate 60 calendar days
    for day in range(60):

        work_date = start_date + timedelta(days=day)

        # Monday = 0, Sunday = 6
        weekday = work_date.weekday()

        # Most employees work Monday to Friday
        # Some employees also work weekends to simulate warehouse/operations shifts
        works_today = weekday < 5 or random.random() < 0.25

        if not works_today:
            continue

        # Random clock in time between 6:00 and 9:59
        clock_in_hour = random.randint(6, 9)
        clock_in_minute = random.randint(0, 59)

        # Random shift length between 7.5 and 10 hours
        shift_minutes = random.randint(450, 600)

        clock_in = datetime(
            work_date.year,
            work_date.month,
            work_date.day,
            clock_in_hour,
            clock_in_minute
        )

        clock_out = clock_in + timedelta(minutes=shift_minutes)

        # Add Clock In record
        attendance_records.append([
            employee_id,
            work_date.date(),
            clock_in.strftime("%H:%M"),
            "Clock In"
        ])

        # Add Clock Out record
        attendance_records.append([
            employee_id,
            work_date.date(),
            clock_out.strftime("%H:%M"),
            "Clock Out"
        ])

attendance = pd.DataFrame(
    attendance_records,
    columns=[
        "EmpID",
        "Work_Date",
        "Clock_Time",
        "Attendance_Event"
    ]
)

print("Attendance Shape:")
print(attendance.shape)

print("\nAttendance Events:")
print(attendance["Attendance_Event"].value_counts())

print("\nUnique Employees:")
print(attendance["EmpID"].nunique())

attendance.to_csv(
    "data_processed/timefiler_attendance_generated.csv",
    index=False
)

print("\nTimeFiler attendance created.")