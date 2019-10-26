import pandas as pd
import numpy as np

do = pd.read_csv("dropoff-all.csv")
do["scale"]=np.log(do["Half Year Sum"])
l,u = min(do["scale"]), max(do["scale"])
do["scale"] = (do["scale"]-l)/(u-l)


pu = pd.read_csv("pickup-all.csv")
pu["scale"]=np.log(pu["Half Year Sum"])
l, u = min(pu["scale"]), max(pu["scale"])
pu["scale"] = (pu["scale"]-l)/(u-l)

loc_id = 12

a = pu[pu.PULocationID==loc_id].iloc[-1]["scale"]
print(a)
print(l,u)