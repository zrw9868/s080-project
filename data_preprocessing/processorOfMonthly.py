import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3 as sql
import pandas as pd
import argparse
import os
#Input:
# 1) Manhattan zones: csv with Location ID, Zone, service_zone. (All Borough= Manhattan so it's omitted)
# 2) Monthly Taxi Ride data: csv
# 3) Date of taxi ride source file: string
#Output:
#1) Monthly Tax Ride (Manhattan Only) data: csv
home_dir=os.environ['HOME']+'/Desktop/s080-project/'
manhattanZones = home_dir+'clean_data/manhattan_taxi_zone.csv'



def helper(monthlyRide):
    date = monthlyRide.split("_")[-1].split(".")[0]
    return date


def manhattanScraper(manhattanZones, monthlyRide, date):

# convert both csvs into dataframes
    manhattanDf = pd. read_csv(manhattanZones)
    rideDf = pd.read_csv(monthlyRide)
    #want PU location and DO location to be within the mahattanZones file
    puFilter= rideDf.PULocationID.isin(manhattanDf.LocationID)
    doFilter= rideDf.DOLocationID.isin(manhattanDf.LocationID)
    manhattanFilter= puFilter & doFilter
    manhattanRideDf= rideDf[manhattanFilter]
    return manhattanRideDf.to_csv(home_dir+'clean_data/rideManhattanOnly'+date+'.csv')


path = home_dir+'source_data/'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if 'yellow' in file :
            files.append(os.path.join(r, file))


for f in files:
    date=helper(f)
    manhattanScraper(manhattanZones,f,date)
