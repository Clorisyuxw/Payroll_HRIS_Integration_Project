import pandas as pd

payroll_population = pd.read_csv(
    "data_processed/payroll_population.csv"
)

pilot_group = payroll_population.sample(
    n=200,
    random_state=42
)

print("Pilot group shape:")
print(pilot_group.shape)

print("\nEmployee Type:")
print(pilot_group["EmployeeType"].value_counts())

print("\nBusiness Unit:")
print(pilot_group["BusinessUnit"].value_counts())

pilot_group.to_csv(
    "data_processed/pilot_employee_master.csv",
    index=False
)

print("\nPilot employee master created.")