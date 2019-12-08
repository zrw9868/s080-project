import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import os


home_dir = os.environ['HOME']+'/Desktop/s080-project/parking_violation/'

violation15data = pd.read_csv(home_dir+'source/Parking_Violations_2015.csv')

#we exclude the "Base" column
violation15data=violation15data[["Date First Observed", "Street Name"]].rename(columns={"Date First Observed":"Date_Issued","Street Name":"Street"})
#we parse out Time in "Date/Time"
violation15data=violation15data.groupby(["Street"],as_index=False).agg({'Date_Issued': 'count'})
violation15data.to_csv(home_dir+"clean/violation_time_street.csv", index=False)
