import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3 as sql
import pandas as pd
import argparse
import os
#Input:
# 1) Manhattan zones: csv with Location ID, Zone, service_zone. (All Borough= Manhattan so it's omitted)
# 2) Manhattan only Monthly Taxi Ride data: csv
# 3) Date of taxi ride source file: string
#Output:
#1) Monthly Tax Ride (Manhattan Only) data in time intervals[Morning, afternoon, evening, night]: csv
home_dir=os.environ['HOME']+'/Desktop/s080-project/'
manhattanZones = home_dir+'clean_data/manhattan_taxi_zone.csv'

#we definite morning (5-10), afternoon(11-16), evening(17-22), and night (23, 0-4) and label these times

def helper(monthlyRide):
    month = monthlyRide.split("-")[-1].split(".")[0]
    return month

def process(f,month):
    rideDf = pd.read_csv(f)
    date_time=rideDf.tpep_pickup_datetime.str.split(" ", n=1, expand=True)
    rideDf["PickUp_Date"]=date_time[0]
    rideDf["PickUp_Time"]=date_time[1]
    rideDf.drop(columns=["tpep_pickup_datetime"])
    hour_minute_second=rideDf.PickUp_Time.str.split(":", n=-1, expand=True)
    rideDf["PickUp_Hour"]=hour_minute_second[0]

    date_time=rideDf.tpep_dropoff_datetime.str.split(" ", n=1, expand=True)
    rideDf["DropOff_Date"]=date_time[0]
    rideDf["DropOff_Time"]=date_time[1]
    rideDf.drop(columns=["tpep_dropoff_datetime"])
    hour_minute_second=rideDf.DropOff_Time.str.split(":", n=-1, expand=True)
    rideDf["DropOff_Hour"]=hour_minute_second[0]


    rideDf[["VendorID","PickUp_Hour","DropOff_Hour","PULocationID","DOLocationID"]].to_csv(home_dir+'clean_data/ManhattanRidesSmall'+month+'.csv')


def filter_by_time_pickup(f,month):
    rideDf = pd.read_csv(f)
    rideDf.loc[(rideDf["PickUp_Hour"]>=5) & (rideDf["PickUp_Hour"]<=10),"TimeCategory"] = "morning"
    rideDf.loc[(rideDf["PickUp_Hour"]>=11) & (rideDf["PickUp_Hour"]<=16),"TimeCategory"] = "afternoon"
    rideDf.loc[(rideDf["PickUp_Hour"]>=17) & (rideDf["PickUp_Hour"]<=22),"TimeCategory"] = "evening"
    rideDf.loc[((rideDf["PickUp_Hour"]>=0) & (rideDf["PickUp_Hour"]<=4)) | (rideDf["PickUp_Hour"]==23),"TimeCategory"] = "night"
    rideDf = rideDf[["PULocationID", "VendorID","TimeCategory"]].groupby(["TimeCategory","PULocationID"]).agg({"VendorID":"count"}).rename({"VendorID":"Number of PickUps"},axis=1).reset_index()
    print(rideDf.columns)

    rideDf[rideDf["TimeCategory"]=="morning"].to_csv(home_dir+'clean_data/Morning/pickup-2019-'+month+'.csv')
    rideDf[rideDf["TimeCategory"]=="afternoon"].to_csv(home_dir+'clean_data/Afternoon/pickup-2019-'+month+'.csv')
    rideDf[rideDf["TimeCategory"]=="evening"].to_csv(home_dir+'clean_data/Evening/pickup-2019-'+month+'.csv')
    rideDf[rideDf["TimeCategory"]=="night"].to_csv(home_dir+'clean_data/Night/pickup-2019-'+month+'.csv')

def filter_by_time_dropoff(f,month):
    rideDf = pd.read_csv(f)
    rideDf.loc[(rideDf["DropOff_Hour"]>=5) & (rideDf["DropOff_Hour"]<=10),"TimeCategory"] = "morning"
    rideDf.loc[(rideDf["DropOff_Hour"]>=11) & (rideDf["DropOff_Hour"]<=16),"TimeCategory"] = "afternoon"
    rideDf.loc[(rideDf["DropOff_Hour"]>=17) & (rideDf["DropOff_Hour"]<=22),"TimeCategory"] = "evening"
    rideDf.loc[((rideDf["DropOff_Hour"]>=0) & (rideDf["DropOff_Hour"]<=4)) | (rideDf["DropOff_Hour"]==23),"TimeCategory"] = "night"
    rideDf = rideDf[["DOLocationID", "VendorID","TimeCategory"]].groupby(["TimeCategory","DOLocationID"]).agg({"VendorID":"count"}).rename({"VendorID":"Number of PickUps"},axis=1).reset_index()

    rideDf[rideDf["TimeCategory"]=="morning"].to_csv(home_dir+'clean_data/Morning/dropoff-2019-'+month+'.csv')
    rideDf[rideDf["TimeCategory"]=="afternoon"].to_csv(home_dir+'clean_data/Afternoon/dropoff-2019-'+month+'.csv')
    rideDf[rideDf["TimeCategory"]=="evening"].to_csv(home_dir+'clean_data/Evening/dropoff-2019-'+month+'.csv')
    rideDf[rideDf["TimeCategory"]=="night"].to_csv(home_dir+'clean_data/Night/dropoff-2019-'+month+'.csv')
    
  


path = home_dir+'clean_data/'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if 'ManhattanRidesSmall' in file :
            files.append(os.path.join(r, file))


for f in files:
    print (f)
    month=helper(f)
    # process(f, month)
    filter_by_time_pickup(f,month)
    filter_by_time_dropoff(f,month)