![CI](https://github.com/shafeeqzada/brew-bean-anomaly/actions/workflows/ci.yml/badge.svg)

# Brew & Bean Anomaly Detection

Anomaly detection system for cafe transactions using IsolationForest and Streamlit.

## Task 1: Setup and data generator
pip install -r requirements.txt
python data_generator.py
streamlit run app.py

## Task 2: Data cleaning and feature engineering
`clean_data.py` has two functions:
- `clean(df)`: fills missing values, builds `timestamp` from date and time, drops rows with bad dates
- `engineer(df)`: adds `hour_of_day`, `day_of_week`, `log_amount` and one-hot payment method columns

Run the pipeline (creates `cleaned_data.csv`):
python clean_data.py

Run tests:
python -m pytest

Tests also run automatically on every push using GitHub Actions.

## Task 3: Anomaly detection model

**Data:** `inject_anomalies.py` adds 2% synthetic anomalies (very large amounts and/or night-time transactions) to `cleaned_data.csv` and saves `data_with_anomalies.csv` with an `anomaly` label (0 = normal, 1 = anomaly).

**Model:** IsolationForest (scikit-learn, 200 trees) trained on 70% of the data using log_amount, hour_of_day, day_of_week and the payment method one-hot columns. 30% is kept as a test set. The model is saved with joblib at `model/isolation_forest.pkl`.

**Threshold:** I tried contamination values 0.005, 0.01, 0.02, 0.03, 0.05 and 0.10 and picked the one with the best F1 score on the training data (best: **0.02**). Contamination sets the threshold: the model flags the most unusual 2% of training rows, which gives an anomaly score threshold of **0.6515** (score above this = anomaly). The model never saw the labels while training, so labels were only used to choose this value.

**Results (test set):** ROC AUC = **0.XXX**. The confusion matrix is in `confusion_matrix.png`.

**How to run:** `python inject_anomalies.py`, then `python train_model.py`, then `python evaluation.py`.


## Task 4: Streamlit dashboard for anomaly review

`app.py` loads the trained IsolationForest (`model/isolation_forest.pkl`) through `predict.py`, predicts anomalies on the synthetic transactions and shows:
- sidebar filters for date range and hour of day
- a table with an `anomaly` column (True/False), anomalies highlighted in red
- a Plotly line chart of amount over time with red markers for anomalies
- a download button for the flagged transactions (CSV)

Run it:
pip install -r requirements.txt
streamlit run app.py