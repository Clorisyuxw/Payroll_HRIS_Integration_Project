import pandas as pd

hr = pd.read_csv(
    "data_raw/employee_data.csv"
)

print("Rows and Columns:")
print(hr.shape)

print("\nColumns:")
print(hr.columns)

print("\nMissing Values:")
print(hr.isnull().sum())

print("\nEmployee Status:")
print(
    hr["EmployeeStatus"].value_counts()
)

print("\nEmployee Type:")
print(
    hr["EmployeeType"].value_counts()
)