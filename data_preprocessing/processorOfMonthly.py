import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3 as sql
import pandas as pd
import argparse

#Input:
# 1) Manhattan zones: csv with Location ID, Zone, service_zone. (All Borough= Manhattan so it's omitted)
# 2) Monthly Taxi Ride data: csv
#Output:
#1) Monthly Tax Ride (Manhattan Only) data: csv

def manhattanScraper(manhattanZones, monthlyRide):
    # convert both csvs into dataframes
    manhattanDf = pd. read_csv(manhattanZones)
    rideDf = pd.read_csv(monthlyRide)
    #want PU location and DO location to be within the mahattanZones file
    puFilter= rideDF.PULocationID.isin(manhattanDf.LocationID)
    doFilter= rideDF.DOLocationID.isin(manhattanDf.LocationID)
    manhattanFilter= puFilter & doFilter
    manhattanRideDf= rideDF[manhattanFilter]
    return manhattanRideDf.to_csv()
