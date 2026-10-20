import pandas as pd
import numpy as np

def clean(df):
    """Clean the data: fill missing values, build timestamp, drop bad rows."""
    df = df.copy()
    df.amount = df.amount.fillna(df.amount.median())
    df.payment_method = df.payment_method.fillna("unknown")
    df.item = df.item.fillna("unknown")
    df["timestamp"] = pd.to_datetime(df.date + " " + df.time , errors = "coerce")
    df = df.dropna(subset = ["timestamp"])
    return df
def engineer(df):
    """Add features: hour_of_day, day_of_week, log_amount, payment one-hot."""
    df = df.copy()   
    df["hour_of_day"] = df.timestamp.dt.hour
    df["day_of_week"] = df.timestamp.dt.dayofweek
    df["log_amount"] = np.log1p(df.amount)
    payment_dummies = pd.get_dummies(df["payment_method"], prefix="payment_method", dtype=int)
    df = pd.concat([df, payment_dummies], axis=1) 
    return df

if __name__ == "__main__":
    df = pd.read_csv("data/transactions.csv")
    df = clean(df)
    df = engineer(df)
    df.to_csv("cleaned_data.csv", index=False)
    print(df.columns.tolist())
    print(df[["amount", "log_amount"]].head())