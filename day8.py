import random
import pandas as pd
import numpy as np
import math

roll_number = 19


# generate data
def generate_data():
    data = []

    for i in range(18):
        record = {
            "zone": i+1,
            "traffic": random.randint(0,100),
            "air_quality": random.randint(0,300),
            "energy": random.randint(0,500)
        }
        data.append(record)

    # test cases
    data[0]["air_quality"] = 280   # extreme pollution
    data[1]["traffic"] = 0         # zero traffic
    data[2]["traffic"] = 95        # spike
    data[2]["energy"] = 450

    # forced safe zone
    data[3]["traffic"] = 10
    data[3]["air_quality"] = 50
    data[3]["energy"] = 200

    return data


# classification
def classify(data):

    for d in data:

        if d["air_quality"] > 200 or d["traffic"] > 80:
            d["category"] = "High Risk"

        elif d["energy"] > 400:
            d["category"] = "Energy Critical"

        elif d["traffic"] < 30 and d["air_quality"] < 100:
            d["category"] = "Safe Zone"

        else:
            d["category"] = "Moderate"

    return data


# risk score
def calculate_risk(df):

    scores = []

    for i in range(len(df)):

        t = df.loc[i,"traffic"]
        a = df.loc[i,"air_quality"]
        e = df.loc[i,"energy"]

        risk = (t*0.4) + (a*0.4) + (e*0.2)

        risk = math.sqrt(risk)

        scores.append(risk)

    df["risk_score"] = scores

    return df


# custom sort
def custom_sort(data):
    return sorted(data, key=lambda x: x["traffic"], reverse=True)


# pattern detection
def detect_patterns(df):

    threshold = df["risk_score"].mean()

    multi = []
    clusters = []
    temp = []

    for i in range(1,len(df)):
        if df.loc[i,"risk_score"] > threshold and df.loc[i,"air_quality"] > df.loc[i-1,"air_quality"]:
            multi.append(df.loc[i,"zone"])

    for i in range(len(df)):
        if df.loc[i,"risk_score"] > threshold:
            temp.append(df.loc[i,"zone"])
        else:
            if len(temp) >= 2:
                clusters.append(temp)
            temp = []

    variance = np.var(df["traffic"])

    if variance < 500:
        stability = "Stable Traffic"
    else:
        stability = "Unstable Traffic"

    return multi, clusters, stability


# main
city_data = generate_data()

# personalization rule
if roll_number % 3 == 0:
    random.shuffle(city_data)
else:
    city_data = sorted(city_data, key=lambda x: x["traffic"])

city_data = classify(city_data)

df = pd.DataFrame(city_data)

df = calculate_risk(df)

# IMPORTANT PRINT (shows safe zone)
print("\nCity Data")
print(df)

# mean values
print("\nMean Values")
print(np.mean(df[["traffic","air_quality","energy"]]))

# top 3
print("\nTop 3 Risk Zones")
top3 = custom_sort(city_data)[:3]
for t in top3:
    print(t)

# patterns
multi, clusters, stability = detect_patterns(df)

print("\nMulti Factor Risk Zones")
print(multi)

print("\nClusters")
print(clusters)

print("\nTraffic Stability")
print(stability)

# tuple
risk_tuple = (
    df["risk_score"].max(),
    df["risk_score"].mean(),
    df["risk_score"].min()
)

print("\nRisk Tuple")
print(risk_tuple)

# decision
avg = risk_tuple[1]

if avg < 8:
    decision = "City Stable"
elif avg < 12:
    decision = "Moderate Risk"
elif avg < 15:
    decision = "High Alert"
else:
    decision = "Critical Emergency"

print("\nFinal Decision")
print(decision)

print("\nSmart City Definition")
print("Smart city means low pollution, balanced traffic and stable energy with fewer high risk zones.")