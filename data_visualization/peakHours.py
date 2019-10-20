import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3 as sql
import pandas as pd
import argparse
import os

import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
from altair import datum

#input:
#1) ride_data: csv, rideManhattanOnly for a particular month
#2) date: string, the date of the data
#output:
#) output_Date: csv, number of rides sorted by each hour in a csv identified by month
home_dir=os.environ['HOME']+'/Desktop/s080-project/'
def groupByHour(ride_data, month):
    rideDf = pd.read_csv(ride_data)
    date_time=rideDf.tpep_dropoff_datetime.str.split(" ", n=1, expand=True)
    rideDf["PickUp_Date"]=date_time[0]
    rideDf["PickUp_Time"]=date_time[1]
    rideDf.drop(columns=["tpep_pickup_datetime"])
    hour_minute_second=rideDf.PickUp_Time.str.split(":", n=-1, expand=True)
    rideDf["PickUp_Hour"]=hour_minute_second[0]
    rideDf=rideDf[["PickUp_Hour", "VendorID"]].groupby(["PickUp_Hour"]).count().rename({"VendorID":"Number of PickUps"},axis=1)
    output_Date= rideDf.to_csv(home_dir+'clean_data/peak_hours_dropoff/peakHour-2019-'+month+'.csv')
    return output_Date


def helper(file):
    month = file.split("-")[-1]
    return month

# path = home_dir+'clean_data/'
#
# files = []
# # r=root, d=directories, f = files
# for r, d, f in os.walk(path):
#     for file in f:
#         if 'rideManhattanOnly' in file :
#             files.append(os.path.join(r, file))
#
#
# for f in files:
#     month=helper(f)
#     groupByHour(f,month)

# path2=home_dir+'clean_data/peak_hours_dropoff/'
# peakhour_files=[]
# for r, d, f in os.walk(path2):
#     for file in f:
#         peakhour_files.append(os.path.join(r, file))
#
# dic = {}
# for peakhour_f in peakhour_files:
#     df = pd.read_csv(peakhour_f)
#     records = df.to_dict("records")
#     for row in records:
#         if row["PickUp_Hour"] not in dic:
#             dic[row["PickUp_Hour"]] = 0
#         dic[row["PickUp_Hour"]] += row["Number of PickUps"]
#
# df = pd.DataFrame.from_dict(dic,orient='index')
# df.to_csv(path2+'aggregate_dropoff_by_hour.csv')

# df= pd.read_csv(home_dir+"data_visualization/path2aggregate_pickups_by_hour.csv")
# chart=alt.Chart(df).mark_line(). \
#     encode(x="Hour:Q",
#            y="Pickups:Q")
# chart.save('chart.png', webdriver='chrome')
