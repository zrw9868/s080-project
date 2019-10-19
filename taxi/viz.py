import pandas as pd
import numpy as np
import urllib.request
import zipfile
import random
import itertools
import math

import shapefile
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('ggplot')


#green_raw = pd.read_csv("green_tripdata_2019-01.csv")
#print(green_raw)
def get_lat_lon(sf):
	#returns a dataframe with latitude and longitude
	
    content = []
    for sr in sf.shapeRecords():
        shape = sr.shape
        rec = sr.record
        if rec[shp_dic['borough']]=='Manhattan':
	        loc_id = rec[shp_dic['LocationID']]
	        
	        x = (shape.bbox[0]+shape.bbox[2])/2
	        y = (shape.bbox[1]+shape.bbox[3])/2
	        
	        content.append((loc_id, x, y))
    return pd.DataFrame(content, columns=["LocationID", "longitude", "latitude"])


def get_boundaries(sf):
    lat, lon = [], []
    for sr in sf.shapeRecords():
        shape = sr.shape
        rec = sr.record
        if rec[shp_dic['borough']]=='Manhattan':
	        lat.extend([shape.bbox[0], shape.bbox[2]])
        	lon.extend([shape.bbox[1], shape.bbox[3]])

    margin = 1 # buffer to add to the range
    lat_min = min(lat) - margin
    lat_max = max(lat) + margin
    lon_min = min(lon) - margin
    lon_max = max(lon) + margin

    return lat_min, lat_max, lon_min, lon_max

def draw_zone_map(ax, sf):
    continent = [235/256, 151/256, 78/256]
    ocean = (89/256, 171/256, 227/256)
    #ocean = (22/256, 165/256, 217/256)
    ax.set_facecolor(ocean)
       
    for sr in sf.shapeRecords():
        shape = sr.shape
        rec = sr.record
        if rec[shp_dic['borough']]=='Manhattan':
	        loc_id = rec[shp_dic['LocationID']]
	        zone = rec[shp_dic['zone']]
	        
	        col = continent

	        # check number of parts (could use MultiPolygon class of shapely?)
	        nparts = len(shape.parts) # total parts
	        if nparts == 1:
	            polygon = Polygon(shape.points)
	            patch = PolygonPatch(polygon, facecolor=col, alpha=1.0, zorder=2)
	            ax.add_patch(patch)
	        else: # loop over parts of each shape, plot separately
	            for ip in range(nparts): # loop over parts, plot separately
	                i0 = shape.parts[ip]
	                if ip < nparts-1:
	                    i1 = shape.parts[ip+1]-1
	                else:
	                    i1 = len(shape.points)

	                polygon = Polygon(shape.points[i0:i1+1])
	                patch = PolygonPatch(polygon, facecolor=col, alpha=1.0, zorder=2)
	                ax.add_patch(patch)
	        
	        x = (shape.bbox[0]+shape.bbox[2])/2
	        y = (shape.bbox[1]+shape.bbox[3])/2

	        plt.text(x, y, str(loc_id), fontsize=9, horizontalalignment='center', verticalalignment='center')                
    # display

    # lat_lon_df = get_lat_lon(sf)
    # margin = 0.01

    # plt.xlim(min(lat_lon_df['latitude'])/2-margin, 
    # 	max(lat_lon_df['latitude'])*2+margin)
    # plt.ylim(min(lat_lon_df['longitude'])/2-margin,
    # 	max(lat_lon_df['longitude'])*2+margin)

    limits = get_boundaries(sf)
    plt.xlim(limits[0], limits[1])
    plt.ylim(limits[2], limits[3])

sf = shapefile.Reader("taxi_zones/taxi_zones.shp")

'''Record #0: [1, 0.116357453189, 0.0007823067885, 'Newark Airport', 1, 'EWR']
'''
'''
[('DeletionFlag', 'C', 1, 0),
['OBJECTID', 'N', 9, 0], 
['Shape_Leng', 'F', 19, 11], 
['Shape_Area', 'F', 19, 11], 
['zone', 'C', 254, 0], 
['LocationID', 'N', 4, 0], 
['borough', 'C', 254, 0]]
'''
fields_name = [field[0] for field in sf.fields[1:]]
shp_dic = dict(zip(fields_name, list(range(len(fields_name)))))
attributes = sf.records()
shp_attr = [dict(zip(fields_name, attr)) for attr in attributes]

df_loc = pd.DataFrame(shp_attr).join(get_lat_lon(sf).set_index("LocationID"), on="LocationID")
df_loc.head()

fig, ax = plt.subplots(nrows=1, ncols=1) #figsize=(15, 15)
ax = plt.subplot(1, 1, 1)
ax.set_title("Manhattan")
draw_zone_map(ax, sf)
plt.show()