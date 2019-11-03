import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

p1 = pd.read_csv("dropoff-2019-01.csv")
p2 = pd.read_csv("dropoff-2019-02.csv")
p3 = pd.read_csv("dropoff-2019-03.csv")
p4 = pd.read_csv("dropoff-2019-04.csv")
p5 = pd.read_csv("dropoff-2019-05.csv")
p6 = pd.read_csv("dropoff-2019-06.csv")

p_all = pd.merge(left=p1,
	right=p2,
	right_on=["DOLocationID"],
	left_on=["DOLocationID"]).rename({"Number of PickUps_x":"01", "Number of PickUps_y":"02"}, axis=1)
p_all = p_all.merge(p3,
	right_on=["DOLocationID"],
	left_on=["DOLocationID"])
p_all = p_all.merge(p4,
	right_on=["DOLocationID"],
	left_on=["DOLocationID"]).rename({"Number of PickUps_x":"03", "Number of PickUps_y":"04"}, axis=1)
p_all = p_all.merge(p5,
	right_on=["DOLocationID"],
	left_on=["DOLocationID"])
p_all = p_all.merge(p6,
	right_on=["DOLocationID"],
	left_on=["DOLocationID"]).rename({"Number of PickUps_x":"05", "Number of PickUps_y":"06"}, axis=1)
p_all["Half Year Sum"]=p_all["01"]+p_all["02"]+p_all["03"]+p_all["04"]+p_all["05"]+p_all["06"]

p_all=p_all[["DOLocationID", "Half Year Sum", "01", "02", "03", "04","05", "06"]]
dp_all.to_csv("dropoff-all.csv")

def consecutive(n):
	return sum([p_all["0{}".format(i)] for i in range(1, n+1)])

colors = sns.color_palette("PuOr",6)
sns.barplot(p_all["DOLocationID"], consecutive(6), color=colors[0], label="Jun")
sns.barplot(p_all["DOLocationID"], consecutive(5), color=colors[1], label="May")
sns.barplot(p_all["DOLocationID"], consecutive(4), color=colors[2], label="Apr")
sns.barplot(p_all["DOLocationID"], consecutive(3), color=colors[3], label="Mar")
sns.barplot(p_all["DOLocationID"], consecutive(2), color=colors[4], label="Feb")
sns.barplot(p_all["DOLocationID"], consecutive(1), color=colors[5], label="Jan")
plt.title("Morning (5am-10am) Dropoffs at Different Locations (2019 Jan. to Jun.)")
plt.xticks(rotation=45)
plt.xlabel("Dropoff Location")
plt.ylabel("Number of Dropoffs")
plt.ylim(top=750000)
plt.legend()
plt.show()

