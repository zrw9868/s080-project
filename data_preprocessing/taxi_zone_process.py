import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import os 

home_dir = os.environ['HOME']+'/Desktop/s080-project/'

taxi_zone = pd.read_csv(home_dir+'source_data/taxi+_zone_lookup.csv')


taxi_zone = taxi_zone[taxi_zone.Borough == "Manhattan"][["LocationID", "Zone", "service_zone"]]

print (taxi_zone)

taxi_zone.to_csv(home_dir+"clean_data/manhattan_taxi_zone.csv",index=False)

