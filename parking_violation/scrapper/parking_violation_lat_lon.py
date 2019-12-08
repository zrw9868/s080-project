import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import os
import re
import copy

def clean_number_suffix(street):
    l=street.upper().split()
    str1=l[0]
    newl=[]
    if str1[0].isdigit() and str1[-1].isalpha():
        newstr=str1[:-2]
        newl=[newstr]+l[1:]
        return ' '.join(newl)
    if (not str1[0].isdigit()) and (not str1[0].isalpha()):
        newstr=str1[1:]
        newl=[newstr]+l[1:]
        return ' '.join(newl)
    return ' '.join(l)

def clean_street(street):
    l=street.upper().split()
    number_endings=["TH","RD"]
    key_street_endings=["ST","STR","STREET","AVE","AV","BLVD","BLV"]
    trivial_descriptors=["C/O", "FROM", "E/O","W/O","S/O","N/O", "S/E" "OF", "FEET","FT"]
    for number_ending in number_endings:
        if number_ending in l:
            pos=l.index(number_ending)
            l=l[:pos]+l[pos+1:]
    for key_ending in key_street_endings:
        if key_ending in l:
            pos=l.index(key_ending)
            return l[pos-1]+" "+key_ending
    for trivial_part in trivial_descriptors:
        if trivial_part in l:
            pos=l.index(trivial_part)
            new=' '.join(l[pos+1:])
            return new
    #print("We are returning l here: ", l)
    return ' '.join(l)
def match_street_to_lat_lon(violations, map):
    violations_street=violations["Street"].tolist()
    violations_number=violations["Date_Issued"].tolist()
    violations_lat_result=[]
    violations_lon_result=[]
    map_street=map["Street"].tolist()
    map_lon=map["Lon"].tolist()
    map_lat=map["Lat"].tolist()
    for i in range(len(violations_street)):
        street_to_match=violations_street[i]
        if street_to_match in map_street:
            map_index=map_street.index(street_to_match)
            lon=map_lon[map_index]
            lat=map_lat[map_index]
            violations_lat_result.append(lat)
            violations_lon_result.append(lon)
        else:
            for i in range(1,5):
                if street_to_match[:-i] in map_street:
                    map_index=map_street.index(street_to_match[:-i])
                    lon=map_lon[map_index]
                    lat=map_lat[map_index]
                    violations_lat_result.append(lat)
                    violations_lon_result.append(lon)
                    break
            else:
                violations_lat_result.append(None)
                violations_lon_result.append(None)
    return [violations_lat_result,violations_lon_result]

home_dir = os.environ['HOME']+'/Desktop/s080-project/parking_violation/'

violation_street_data = pd.read_csv(home_dir+'clean/violation_time_street.csv')
street_dict=pd.read_csv(home_dir+'source/Address_Point.csv')
#entity resolution for street names to latitude and longitudes
street_dict=street_dict[["the_geom", "FULL_STREE"]].rename(columns={"FULL_STREE":"Street"})
coords=street_dict.the_geom.str.split("(",n=1, expand=True)
lat_lon=coords[1].str.split(" ",n=1,expand=True)
lat=lat_lon[0]
lon=lat_lon[1]
street_dict["Lat"]=lat.astype(float)
street_dict["Lon"]=lon.str.slice(0,-1).astype(float)
street_dict=street_dict[["Street", "Lat","Lon"]]
street_dict=street_dict.groupby(["Street"],as_index=False).agg({'Lat': 'mean', 'Lon':'mean'})
#street_dict.to_csv(home_dir+"clean/street_dict_clean.csv", index=False)
street_dict["Street"]=street_dict["Street"].str.upper()
violation_street_data["Street"]=violation_street_data["Street"].apply(clean_street)
violation_street_data=violation_street_data[violation_street_data.Street!=""]
violation_street_data["Street"]=violation_street_data["Street"].apply(clean_number_suffix)
violation_street_data=violation_street_data[violation_street_data.Street!=""]
violation_street_data=violation_street_data.groupby(["Street"],as_index=False).agg({'Date_Issued':'sum'})
lat_lon_match=match_street_to_lat_lon(violation_street_data, street_dict)
violation_street_data["Lat"]=lat_lon_match[1]
violation_street_data["Lon"]=lat_lon_match[0]
violation_street_data=violation_street_data.groupby(["Lat","Lon"],as_index=False).agg({'Street':'first','Date_Issued':'sum'}).sort_values(by='Date_Issued',ascending=False)
total_rows=len(violation_street_data.index)
violation_street_data=violation_street_data.head(300)
violation_street_data.to_csv(home_dir+"clean/violation_cleaned_addr.csv", index=False)
