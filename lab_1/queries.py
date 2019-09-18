import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3 as sql
import pandas as pd
import argparse

candidate = pd.read_csv("data/candidate.txt", delimiter="|")
cand_summary = pd.read_csv("data/cand_summary.txt", delimiter="|")
committee = pd.read_csv("data/committee.txt",delimiter="|")
dist_pop = pd.read_csv("data/dist_pop.txt", delimiter="|")
pac_summary = pd.read_csv("data/pac_summary.txt", delimiter="|")

def runSQL(query_num):
	with sql.connect("lab1.sqlite") as conn, open("queries/q{}.sql".format(query_num)) as in_query:
		cur = conn.cursor()
		df = pd.read_sql_query(in_query.read(), conn)
		return df

def Q1Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    filterr = (candidate.CAND_OFFICE == "P") & ((candidate.CAND_STATUS == "C") | (candidate.CAND_STATUS == "N")) & (candidate.CAND_ELECTION_YR == 2016)
    df = candidate[filterr][["CAND_ID"]].count()
    df.rename({"CAND_ID":"CAND_NUM_2016"})
    return df

def Q2Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    filterr = (candidate.CAND_OFFICE == "S") & ((candidate.CAND_STATUS == "C") | (candidate.CAND_STATUS == "N")) & (candidate.CAND_ELECTION_YR == 2016)
    third_party = (~candidate.CAND_PTY_AFFILIATION.isin(["REP","IND","DEM"]))
    counts = candidate[filterr & third_party][["CAND_ID","CAND_PTY_AFFILIATION"]].groupby(["CAND_PTY_AFFILIATION"]).count().sort_values("CAND_ID",ascending=False)
    return counts.rename({"CAND_ID":"NUM_SENATE_CAND"},axis=1)[:1]

def Q3Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    df = pac_summary[pac_summary.CMTE_TP == "O"][["CMTE_NM","TTL_RECEIPTS"]].sort_values("TTL_RECEIPTS", ascending = False)[:10]
    return df

def Q4Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    filterr = (candidate.CAND_OFFICE == "P") & ((candidate.CAND_STATUS == "C") | (candidate.CAND_STATUS == "N")) & (candidate.CAND_ELECTION_YR == 2016)
    huck = (candidate.CAND_NAME.str.contains("HUCK"))
    president_cand = candidate[filterr & huck][["CAND_NAME","CAND_PCC"]]
    cmte = committee[["CMTE_ID", "CMTE_NM", "CMTE_ST1","CMTE_ST2"]]
    joined = pd.merge(left=president_cand, right=cmte, left_on=["CAND_PCC"], right_on="CMTE_ID")
    return joined[["CAND_NAME", "CMTE_NM","CMTE_ST1","CMTE_ST2"]]

def Q5Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    filterr = (candidate.CAND_OFFICE == "S") & ((candidate.CAND_STATUS == "C") | (candidate.CAND_STATUS == "N")) & (candidate.CAND_ELECTION_YR == 2016)
    cand_info = pd.merge(left=candidate[filterr][["CAND_ID","CAND_PCC","CAND_OFFICE_ST"]],right=cand_summary[["CAND_ID","TTL_RECEIPTS"]],left_on=["CAND_ID"], right_on=["CAND_ID"])
    senate_cmte = pd.merge(left=cand_info, right=committee, left_on=["CAND_PCC"], right_on=["CMTE_ID"])[["CMTE_NM", "CAND_OFFICE_ST", "TTL_RECEIPTS"]]

    state_pop = dist_pop[["state","population"]].groupby("state").sum()
    joined = pd.merge(left=senate_cmte, right=state_pop, left_on=["CAND_OFFICE_ST"], right_on=["state"])

    most_receipt_cmte = joined[["CMTE_NM", "CAND_OFFICE_ST", "TTL_RECEIPTS"]]
    most_receipt_cmte["PER_CAPITA_RECEIPTS"] = joined.TTL_RECEIPTS/joined.population

    return most_receipt_cmte.sort_values("PER_CAPITA_RECEIPTS", ascending=False)[:20]

def Q6Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    filterr = (candidate.CAND_OFFICE == "H") & ((candidate.CAND_STATUS == "C") | (candidate.CAND_STATUS == "N")) & (candidate.CAND_ELECTION_YR == 2016)
    house_cand = candidate[filterr][["CAND_ID"]]
    output = cand_summary[(cand_summary.TTL_RECEIPTS >= 100000) & (cand_summary.CAND_ID.isin(house_cand.CAND_ID))][["CAND_NAME","PTY_AFFILIATION","TTL_INDIV_CONTRIB","TTL_RECEIPTS"]]
    output["TTL_INDIV_RATIO"] = output.TTL_INDIV_CONTRIB / output.TTL_RECEIPTS
    return output.sort_values("TTL_INDIV_RATIO", ascending=True)[:10]

def Q7Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    filterr = (candidate.CAND_OFFICE == "S") & ((candidate.CAND_STATUS == "C") | (candidate.CAND_STATUS == "N")) & (candidate.CAND_ELECTION_YR == 2016)
    senate_cand = candidate[filterr][["CAND_ID","CAND_PTY_AFFILIATION"]]
    output = pd.merge(left=senate_cand, right=cand_summary, left_on=["CAND_ID"], right_on=["CAND_ID"])[["CAND_PTY_AFFILIATION","TTL_INDIV_CONTRIB","TTL_RECEIPTS"]]
    output = output.groupby("CAND_PTY_AFFILIATION").agg({"TTL_INDIV_CONTRIB":"sum","TTL_RECEIPTS":"sum"})
    output["TTL_INDIV_RATIO"] = output.TTL_INDIV_CONTRIB / output.TTL_RECEIPTS
    return output.sort_values("TTL_INDIV_RATIO", ascending=False)[:10]


pandas_queries = [Q1Pandas, Q2Pandas, Q3Pandas, Q4Pandas, Q5Pandas, Q6Pandas, Q7Pandas]
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", help="Run a specific query", type=int)
    args = parser.parse_args()

    queries = range(1, 12)
    if args.query != None:
        queries = [args.query]
    for query in queries:
        print("\nQuery {}".format(query))
        if query <= 7:
            print("\nPandas Output")
            print(pandas_queries[query-1]())
        print("\nSQLite Output")
        # df = runSQL(query)
        print(runSQL(query))

        # df.plot.bar(x="CAND_OFFICE", y="AVG_RECEIPTS")
        # plt.savefig("per_capita_company.png")

    

	
