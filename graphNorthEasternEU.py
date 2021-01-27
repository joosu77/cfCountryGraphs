import matplotlib.pyplot as plt
import requests
import json
import math

contest = "1453"
data = requests.get(url='https://codeforces.com/api/contest.standings?contestId='+contest).json()
allowed = ["Estonia","Latvia","Finland","Norway","Sweden","Poland","Germany","Lithuania","Poland","Belarus","Ukraine","Czechia","Slovakia","Denmark"]

batchSize = 700
handles = list({i["party"]["members"][0]["handle"] for i in data["result"]["rows"]})
handsets = [handles[i*batchSize:(i+1)*batchSize] for i in range(len(handles)//batchSize)]
if len(handles)%batchSize:
    handsets.append(handles[(len(handles)//batchSize)*batchSize:])

users = []
for s in handsets:
    users += requests.get(url='https://codeforces.com/api/user.info?handles='+";".join(s)).json()["result"]
handletocountry = {i["handle"]:i["country"] if "country" in i else "None" for i in users}
countryScores = {}
countryCounts = {}
for i in data["result"]["rows"]:
    c = handletocountry[i["party"]["members"][0]["handle"]]
    if c not in countryScores:
        countryScores[c] = 0
        countryCounts[c] = 0
    countryScores[c] += i["points"]
    countryCounts[c] += 1
countryAves = {c:countryScores[c]/countryCounts[c] for c in countryScores}

fig, axs = plt.subplots(1,2)

countryScores = {k: v for k, v in sorted(countryScores.items(), key=lambda item: -item[1])}
scoreSegs = {k:v for k,v in countryScores.items() if k in allowed}
axs[0].bar(range(len(scoreSegs)), scoreSegs.values())
plt.sca(axs[0])
plt.xticks(range(len(scoreSegs)), scoreSegs.keys(), rotation=45)

countryAves = {k: v for k, v in sorted(countryAves.items(), key=lambda item: -item[1])}
aveSegs = {k:v for k,v in countryAves.items() if k in allowed}
axs[1].bar(range(len(aveSegs)), aveSegs.values())
plt.sca(axs[1])
plt.xticks(range(len(aveSegs)), aveSegs.keys(), rotation=45)

plt.show()