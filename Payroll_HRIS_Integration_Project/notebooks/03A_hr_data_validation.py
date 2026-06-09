import pandas as pd

# Load payroll population data
# This file only includes active employees
hr = pd.read_csv(
    "data_processed/payroll_population.csv"
)

validation_results = []

# Check duplicate employee IDs
duplicate_empid = hr["EmpID"].duplicated().sum()

validation_results.append({
    "Validation_Check": "Duplicate Employee ID",
    "Issue_Count": duplicate_empid
})

# Check missing department / business unit
missing_business_unit = hr["BusinessUnit"].isna().sum()

validation_results.append({
    "Validation_Check": "Missing Business Unit",
    "Issue_Count": missing_business_unit
})

# Check missing job title
missing_title = hr["Title"].isna().sum()

validation_results.append({
    "Validation_Check": "Missing Job Title",
    "Issue_Count": missing_title
})

# Check missing supervisor
missing_supervisor = hr["Supervisor"].isna().sum()

validation_results.append({
    "Validation_Check": "Missing Supervisor",
    "Issue_Count": missing_supervisor
})

# Check missing email
missing_email = hr["ADEmail"].isna().sum()

validation_results.append({
    "Validation_Check": "Missing Email",
    "Issue_Count": missing_email
})

# Check non-active employees accidentally included
non_active = (
    hr["EmployeeStatus"] != "Active"
).sum()

validation_results.append({
    "Validation_Check": "Non-active Employees Included",
    "Issue_Count": non_active
})

# Create validation report
validation_report = pd.DataFrame(validation_results)

# Add pass / review status
validation_report["Status"] = validation_report["Issue_Count"].apply(
    lambda x: "Pass" if x == 0 else "Review Required"
)

print(validation_report)

validation_report.to_csv(
    "reports/hr_master_data_validation_report.csv",
    index=False
)

print("\nHR master data validation report created.")