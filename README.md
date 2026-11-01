![CI](https://github.com/shafeeqzada/brew-bean-anomaly/actions/workflows/ci.yml/badge.svg)

## Project Overview

Brew & Bean is a small cafe. This project finds unusual (anomalous) transactions, for example a very large amount or a sale in the middle of the night, so that staff can review them.

It has four parts:
1. **Data:** a generator creates synthetic cafe transactions (`data/transactions.csv`).
2. **Cleaning:** `clean_data.py` fills missing values and adds features (hour, weekday, log amount, payment method columns).
3. **Model:** an IsolationForest model (`model/isolation_forest.pkl`) scores every transaction.
4. **Dashboard:** a Streamlit app (`app.py`) where staff filter by date and hour, see anomalies in a table and chart, and download them as CSV.

All data is synthetic. No real customer information is used.

## Setup

1. Clone the repository and open the folder.
2. Install the libraries: `pip install -r requirements.txt`
3. Create the data (only needed once): `python data_generator.py`
4. Start the dashboard: `streamlit run app.py`

Optional: rebuild the model with `python inject_anomalies.py`, then `python train_model.py`, then `python evaluation.py`.
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

## Deployment

**Live app:** https://brew-bean-anomaly.streamlit.app/ (opens without any login)

The app is hosted for free on Streamlit Community Cloud:
1. Push all code, data and the model file to this public GitHub repository.
2. Sign in at share.streamlit.io with GitHub.
3. Click **Create app**, choose this repository, branch `main` and main file `app.py`.
4. In **Advanced settings** choose the same Python version as local (3.13).
5. Click **Deploy**. Every `git push` to `main` updates the live app.

`requirements.txt` pins the library versions (including scikit-learn 1.6.1, the version the model was saved with), so the live app uses the same versions as local development.

## Test Plan

The full plan is in [test_plan.pdf](test_plan.pdf). It covers unit, integration, UI (functional) and performance tests.

- **Unit tests (automated):** `python -m pytest` runs the tests in `tests/`. GitHub Actions runs them on every push (see the CI badge at the top).
- **Integration tests:** run `python predict.py` and `python evaluation.py` (ROC AUC must be at least 0.80).
- **UI and performance tests:** manual checklist in the PDF, to run on the live URL.

## Security Checklist

Data privacy
- [x] All data is synthetic, no real customer or staff information.
- [x] The downloadable CSV only contains synthetic transactions.
- [ ] For real cafe data, add a login to the app and check privacy rules before use.

Secrets
- [x] No passwords, API keys or tokens in the code or repository.
- [x] The app needs no secrets. If secrets are added later they go in Streamlit's secrets settings, never in Git.
- [x] `.gitignore` excludes `.env`, `.streamlit/secrets.toml`, `__pycache__/` and `.pytest_cache/`.

Code and dependencies
- [x] Library versions are pinned in `requirements.txt`.
- [x] GitHub Actions runs the tests on every push and uses no secrets.
- [x] The model file is only loaded from this repository. Pickle model files can run code when loaded, so never load files from unknown sources.
- [x] The live app is served over HTTPS by Streamlit Community Cloud.

Access
- [x] The app is public on purpose (read-only, synthetic data) so it can be opened without login.

## Usage (for cafe staff)

You do not need to install anything. Open the live link above in your browser.

1. **Choose dates:** in the left panel, click **Date Range** and pick a start and an end date (click both).
2. **Choose hours:** move the **Hour of Day** slider, for example 0 to 6 for night-time sales.
3. **Read the table:** the column `anomaly` says True for transactions that look unusual. Those rows are shaded red.
4. **Look at the chart:** the blue line shows amounts over time, red dots are the unusual transactions.
5. **Download:** click **Download flagged transactions (CSV)** to save only the unusual rows, for example to check them against the till.

If the app shows a message that it has gone to sleep, click the button to wake it up and wait a few seconds. Free apps sleep when nobody uses them.
