import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import os
home_dir = os.environ['HOME']+'/Desktop/s080-project/parking_violation/'

violation_clean_data = pd.read_csv(home_dir+'clean/violation_cleaned_addr.csv')
uber_clean_data=pd.read_csv(home_dir+'clean/uber_cleaned.csv')
violation_clean_data=violation_clean_data.rename(columns={"Date_Issued":"Violation_Count"})
uber_clean_data=uber_clean_data.rename(columns={"Base":"Ride_Count"}).sort_values(by='Ride_Count',ascending=False)
#merged=uber_clean_data.merge(violation_clean_data, left_on="Street",right_on="Street")

merged_inner = pd.merge(left=uber_clean_data,right=violation_clean_data, left_on='Street', right_on='Street')
merged_inner=merged_inner[["Street","Ride_Count","Violation_Count"]]
merged_inner.to_csv(home_dir+"clean/uber_violations_merged.csv", index=False)
correlation=merged_inner['Ride_Count'].corr(merged_inner['Violation_Count'])
print(correlation)
