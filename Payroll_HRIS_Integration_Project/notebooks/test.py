import pandas as pd

employees = pd.read_csv("data_processed/pilot_employee_master.csv")

print(employees["PayZone"].value_counts())