import multiprocessing
import queue
import json
import sys
import os
import pandas as pd

home_dir=os.environ['HOME']+'/Desktop/s080-project/'

# Useful for debugging concurrency issues.
def log(msg):
    print(sys.stderr, multiprocessing.current_process().name, msg)


# Each worker reads the json file, computes a sum and a count for the target
# field, then stores both in the output queue.
def groupbyhourperday(fn):
    print(fn)
    rides = pd.read_csv(fn)
    date_time=rides.tpep_pickup_datetime.str.split(" ", n=1, expand=True)

    date = date_time[0].str.split("-",n=-1, expand=True)
    rides["year"] = date[0].astype(int)
    rides["month"] = date[1].astype(int)
    rides["day"] = date[2].astype(int)
    rides["hour"] = date_time[1].str.split(":", n=-1, expand=True)[0]

    rides = rides[["year","month","day","hour","VendorID"]].groupby(["year","month","day","hour"],as_index=False).count().rename({"VendorID":"Number of rides"},axis=1)
    
    #rides.to_csv("yellow_manhattan_rides_2015"+date+".csv")
    return rides



def task(in_q, out_q):
    rides = []
    try:
        while (True):
            f = in_q.get(block=False)
            ride = groupbyhourperday(f)
            rides.append(ride)
    except queue.Empty:
        pass  #print "Done processing"
    out_q.put(rides)


def main_task(nprocs):
    q = multiprocessing.Queue()
    out_q = multiprocessing.Queue()

    # Enqueue filenames to be processed in parallel.
    for i in [1,4,5,8,9,11]:
        f = home_dir + "source_data/yellow_tripdata_2015-%02d.csv" % (i)
        q.put(f)

    procs = []
    for i in range(nprocs):
        p = multiprocessing.Process(target=task, args=(q, out_q))
        p.start()
        procs.append(p)

    # Main task takes partial results and computes the final average.
    output = []

    for p in procs:
        partial = out_q.get()
        output.extend(partial)

    rides= pd.concat(output)

    mean=rides['Number of rides'].mean()
    std=rides["Number of rides"].std()
    rides["normlzed"] = (rides["Number of rides"] - mean)/std
    rides = rides.drop(["Unnamed: 0"],axis=1)
    rides = rides.sort_values(["year","month","day","hour"],ascending=True)
    rides = rides.reset_index(drop=True)
    rides.to_csv("taxi_rides_2015.csv")

# python3 queue_test.py <n_cores>
if __name__ == "__main__":
    main_task(3)
