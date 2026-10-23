import pandas as pd
import numpy as np

np.random.seed(42)
data = pd.read_csv("cleaned_data.csv")
data.timestamp = pd.to_datetime(data.timestamp)
data["anomaly"] = 0

n_anomilies = int(len(data) * 0.02)
print("Normal rows :" , len(data) , "anomaly rows add", n_anomilies)

anomaly_rows = []

for i in range(n_anomilies):
    row = data.sample(1).iloc[0].copy()
    kind = np.random.choice(["big_amount", "night_time", "both"])

    if  kind == "big_amount" or kind == "both":
        row.amount = round(row.amount * np.random.uniform(8,20),2)
        row.log_amount = np.log1p(row.amount)

    if kind == "night_time" or kind == "both":
        hour = int(np.random.choice([0,1,2,3,4]))   
        minute = int(np.random.randint(0, 60))
        row.timestamp = row.timestamp.replace(hour = hour , minute = minute)
        row.hour_of_day = hour
        row.time = f"{hour:02d}:{minute:02d}" 

    row.anomaly = 1
    anomaly_rows.append(row)  

anomalies = pd.DataFrame(anomaly_rows)    
data_all = pd.concat([data, anomalies], ignore_index = True)  
data_all = data_all.sample(frac = 1 , random_state = 42).reset_index(drop = True)

data_all.to_csv("data_with_anomalies.csv", index=False)
print(data_all["anomaly"].value_counts())