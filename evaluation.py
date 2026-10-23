import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, roc_auc_score

model = joblib.load("model/isolation_forest.pkl")
test = pd.read_csv("model/test_data.csv")

features = [
    "log_amount",
    "hour_of_day",
    "day_of_week",
    "payment_method_Card",
    "payment_method_Cash",
    "payment_method_Online",
]
X_test = test[features]
y_test = test.anomaly

scores = -model.score_samples(X_test)
auc = roc_auc_score(y_test, scores)
print("ROC AUC:", round(auc, 3))
if auc >= 0.80:
    print("AUC >= 0.80: Yes")
else:
    print("AUC >= 0.80 : No")

raw_pred = model.predict(X_test)
pred = []
for p in raw_pred:
    if p == -1:
        pred.append(1)
    else:
        pred.append(0)

cm = confusion_matrix(y_test, pred)
tn = cm[0][0]
fp = cm[0][1]
fn = cm[1][0]
tp = cm[1][1]

print("True Negative :", tn)
print("False Positive:", fp)
print("False Negative:", fn)
print("True Positive :", tp)


threshold = -model.offset_
print("Contamination", model.contamination)
print("Threshold (score > this = anomaly): ", round(threshold , 4))

disp = ConfusionMatrixDisplay(confusion_matrix = cm , display_labels = ["Normal" , "Anomaly"])
disp.plot()
plt.title("Confusion Matrix (test_set)")
plt.savefig("confusion_matrix.png")
print("Save: confusion matrix.png")