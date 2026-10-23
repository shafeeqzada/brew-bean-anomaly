import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import f1_score

data = pd.read_csv("data_with_anomalies.csv")
print(data.head())

feature = [
        "log_amount",
    "hour_of_day",
    "day_of_week",
    "payment_method_Card",
    "payment_method_Cash",
    "payment_method_Online"
]
X = data[feature]
y = data["anomaly"]

X_train , X_test, y_train , y_test = train_test_split(X , y , random_state = 42, test_size = 0.3 , stratify = y)
print("Train rows:", len(X_train), "| anomalies:", int(y_train.sum()))
print("Test rows :", len(X_test), "| anomalies:", int(y_test.sum()))

best_combination = None
best_f1 = -1
for c in [0.01, 0.02, 0.05]:

    model = IsolationForest(
        n_estimators=200,
        contamination=c,
        random_state=42
    )

    model.fit(X_train)
    raw_pred = model.predict(X_train)
    pred = []
    for p in raw_pred:
        if p == -1:
            pred.append(1)
        else:
            pred.append(0)
    f1 = f1_score(y_train, pred)
    print("contamination ", c, "F1", round(f1, 3))
    if f1 > best_f1:
        best_f1 = f1
        best_combination = c
print("Best contamination", best_combination)

final_model = IsolationForest(n_estimators = 200 , contamination = best_combination, random_state = 42)
final_model.fit(X_train)

os.makedirs("model", exist_ok =True )
joblib.dump(final_model, "model/isolation_forest.pkl")

test_data = X_test.copy()
test_data["anomaly"] = y_test

test_data.to_csv("model/test_data.csv ", index=False)

print("Model saved: model/isolation_forest.pkl")
print("Test data saved: model/test_data.csv")



