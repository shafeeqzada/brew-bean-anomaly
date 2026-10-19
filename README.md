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