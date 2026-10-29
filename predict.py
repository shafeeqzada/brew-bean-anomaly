import joblib
import pandas as pd
from clean_data import clean , engineer

model = joblib.load("model/isolation_forest.pkl")

features = [
    "log_amount",
    "hour_of_day",
    "day_of_week",
    "payment_method_Card",
    "payment_method_Cash",
    "payment_method_Online",
]
def predict_anomalies(df):
    df = clean(df)
    df = engineer(df)

    for col in features:
        if col not in df.columns:
            df[col] = 0

    pred = model.predict(df[features])    

    anomaly_flags = []
    for p in pred:
        if p == -1:
            anomaly_flags.append(True)
        else:
            anomaly_flags.append(False)

    df["anomaly"] = anomaly_flags
    df["score"] = -model.score_samples(df[features])
    return df

if __name__ == "__main__":
    data = pd.read_csv("data_with_anomalies.csv")
    data = data[["date", "time", "item", "amount", "payment_method"]]
    result = predict_anomalies(data)
    print("Data : ", len(result))
    print("anomaly_flags:", int(result["anomaly"].sum()))
    print(result[["date", "time", "amount", "anomaly", "score"]].head())

