import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

p1 = pd.read_csv("pickup-2019-01.csv.csv")
p2 = pd.read_csv("pickup-2019-02.csv.csv")
p3 = pd.read_csv("pickup-2019-03.csv.csv")
p4 = pd.read_csv("pickup-2019-04.csv.csv")
p5 = pd.read_csv("pickup-2019-05.csv.csv")
p6 = pd.read_csv("pickup-2019-06.csv.csv")

p_all = pd.merge(left=p1,
	right=p2,
	right_on=["PULocationID"],
	left_on=["PULocationID"]).rename({"Number of PickUps_x":"01", "Number of PickUps_y":"02"}, axis=1)
p_all = p_all.merge(p3,
	right_on=["PULocationID"],
	left_on=["PULocationID"])
p_all = p_all.merge(p4,
	right_on=["PULocationID"],
	left_on=["PULocationID"]).rename({"Number of PickUps_x":"03", "Number of PickUps_y":"04"}, axis=1)
p_all = p_all.merge(p5,
	right_on=["PULocationID"],
	left_on=["PULocationID"])
p_all = p_all.merge(p6,
	right_on=["PULocationID"],
	left_on=["PULocationID"]).rename({"Number of PickUps_x":"05", "Number of PickUps_y":"06"}, axis=1)
p_all["Half Year Sum"]=p_all["01"]+p_all["02"]+p_all["03"]+p_all["04"]+p_all["05"]+p_all["06"]
#print(p_all)
#p_all.to_csv("pickup-all.csv")

def consecutive(n):
	return sum([p_all["0{}".format(i)] for i in range(1, n+1)])

colors = sns.color_palette("RdBu",6)
sns.barplot(p_all["PULocationID"], consecutive(6), color=colors[0], label="Jun")
sns.barplot(p_all["PULocationID"], consecutive(5), color=colors[1], label="May")
sns.barplot(p_all["PULocationID"], consecutive(4), color=colors[2], label="Apr")
sns.barplot(p_all["PULocationID"], consecutive(3), color=colors[3], label="Mar")
sns.barplot(p_all["PULocationID"], consecutive(2), color=colors[4], label="Feb")
sns.barplot(p_all["PULocationID"], consecutive(1), color=colors[5], label="Jan")
plt.title("Number of Pick Ups at Different Locations (2019 Jan. to Jun.)")
plt.xticks(rotation=45)
plt.xlabel("Pick Up Location")
plt.ylabel("Number of Pick Ups")
plt.legend()
plt.show()