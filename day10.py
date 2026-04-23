import random
import pandas as pd
import numpy as np
import math
import copy

roll_number = 19


def generate_data():
    data = []
    for i in range(15):
        record = {
            "zone": i + 1,
            "metrics": {
                "traffic": random.randint(10, 100),
                "pollution": random.randint(20, 300),
                "energy": random.randint(50, 500)
            },
            "history": [random.randint(1, 50) for _ in range(3)]
        }
        data.append(record)
    return data


def personalize(data):
    if roll_number % 2 == 0:
        data.reverse()
    else:
        data = data[3:] + data[:3]
    return data


def replicate(data):
    assignment = data
    shallow = copy.copy(data)
    deep = copy.deepcopy(data)
    return assignment, shallow, deep


def mutate(data):
    for d in data:
        d["metrics"]["traffic"] += 5
        d["history"].append(random.randint(10, 60))
    return data


def custom_risk(data):
    scores = []
    for d in data:
        t = d["metrics"]["traffic"]
        p = d["metrics"]["pollution"]
        e = d["metrics"]["energy"]
        risk = math.log(t + p + e)
        scores.append(risk)
    return scores


def manual_corr(x, y):
    x = np.array(x)
    y = np.array(y)
    xm = np.mean(x)
    ym = np.mean(y)
    num = np.sum((x-xm)*(y-ym))
    den = math.sqrt(np.sum((x-xm)**2)*np.sum((y-ym)**2))
    return num/den


def detect(data, scores):
    arr = np.array(scores)
    mean = np.mean(arr)
    std = np.std(arr)

    anomalies = []
    for i in range(len(arr)):
        if arr[i] > mean + std:
            anomalies.append(data[i]["zone"])

    clusters = []
    temp = []
    for i in range(len(arr)):
        if arr[i] > mean:
            temp.append(data[i]["zone"])
        else:
            if len(temp) >= 2:
                clusters.append(temp)
            temp = []

    stability = 1 / np.var(arr)

    return anomalies, clusters, stability


data = generate_data()

print("BEFORE")
print(data)

data = personalize(data)

assignment, shallow, deep = replicate(data)

mutate(shallow)

scores = custom_risk(data)

zones = []
traffic = []
pollution = []
energy = []

for d in data:
    zones.append(d["zone"])
    traffic.append(d["metrics"]["traffic"])
    pollution.append(d["metrics"]["pollution"])
    energy.append(d["metrics"]["energy"])

df = pd.DataFrame({
    "zone": zones,
    "traffic": traffic,
    "pollution": pollution,
    "energy": energy,
    "risk": scores
})

print("\nDataFrame")
print(df)

print("\nAFTER")
print("Original")
print(data)

print("\nShallow")
print(shallow)

print("\nDeep")
print(deep)

mean = np.mean(scores)
var = np.var(scores)

corr_tp = manual_corr(traffic, pollution)

anomalies, clusters, stability = detect(data, scores)

print("\nAnomaly Zones")
print(anomalies)

result = (max(scores), min(scores), stability)

print("\nTuple")
print(result)

if stability > 1:
    decision = "System Stable"
elif stability > 0.5:
    decision = "Moderate Risk"
elif stability > 0.2:
    decision = "High Corruption Risk"
else:
    decision = "Critical Failure"

print("\nFinal Decision")
print(decision)

print("\nCorrelation Traffic-Pollution")
print(corr_tp)