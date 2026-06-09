import pandas as pd

hr = pd.read_csv(
    "data_raw/employee_data.csv"
)

payroll_population = hr[
    hr["EmployeeStatus"] == "Active"
]

print(
    payroll_population.shape
)

print(
    payroll_population["EmployeeStatus"]
    .value_counts()
)

payroll_population.to_csv(
    "data_processed/payroll_population.csv",
    index=False
)

print(
    "\nPayroll population created."
)