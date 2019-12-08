import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import os

def min_distance(lat_target,lon_target,lat_list,lon_list):
    min_dist=50000
    min_index=0
    for i in range(len(lat_list)):
        current_dist=(lon_list[i]-lon_target)**2+(lat_list[i]-lat_target)**2
        if current_dist<min_dist:
            min_dist=current_dist
            min_index=i
    return min_index

def match_street_to_lat_lon(violations, uber):
    violations_street=violations["Street"].tolist()
    violations_lat_result=violations["Lat"].tolist()
    violations_lon_result=violations["Lon"].tolist()
    uber_street=[]
    uber_lon=uber["Lon"].tolist()
    uber_lat=uber["Lat"].tolist()
    for i in range(len(uber_lon)):
        lon_to_match=uber_lon[i]
        lat_to_match=uber_lat[i]
        index_match=min_distance(lat_to_match,lon_to_match,violations_lat_result,violations_lon_result)
        street_match=violations_street[index_match]
        uber_street.append(street_match)
    return uber_street

home_dir = os.environ['HOME']+'/Desktop/s080-project/parking_violation/'

violation_clean_data = pd.read_csv(home_dir+'clean/violation_cleaned_addr.csv')
uber_data=pd.read_csv(home_dir+'source/uber-raw-data-aug14.csv')
uberdata=uber_data[["Lat","Lon","Base"]]
uber_data=uber_data.groupby(["Lat","Lon"],as_index=False).agg({'Base':'count'})
street_list=match_street_to_lat_lon(violation_clean_data,uber_data)
uber_data["Street"]=street_list
uber_data=uber_data[["Street","Base"]]
uber_data=uber_data.groupby(["Street"],as_index=False).agg({'Base':'sum'})
uber_data.to_csv(home_dir+"clean/uber_cleaned.csv", index=False)
