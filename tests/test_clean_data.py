import pandas as pd
import numpy as np
from clean_data import clean , engineer

def make_sample():
    data = {
        "date": ["2026-01-01", "2026-01-02", "2026-01-03"],
        "time": ["08:00", "14:30", "23:15"],
        "item": ["Latte", None, "Mocha"],
        "amount": [10.0, np.nan, 30.0],
        "payment_method": ["Cash", "Card", None],
    }
    return pd.DataFrame(data)

def test_clean_amount():
    df = clean(make_sample())
    assert df.amount.isna().sum() == 0
    assert df.amount.iloc[1] == 20.0

def test_clean_txt():
    df = clean(make_sample())
    assert df.item.iloc[1] == "unknown"
    assert df.payment_method.iloc[2] == "unknown"

def test_clean_drop_timestamp():
    raw = make_sample()
    raw.loc[0 ,"date"] = "wrong date"
    df = clean(raw)
    assert len(df) == 2

def test_enginerr_time_feature():
    df = engineer(clean(make_sample()))
    assert list(df["hour_of_day"]) == [8, 14, 23]
    assert list(df["day_of_week"]) == [3, 4, 5]        

def  test_engineer_log_amount():
    df = engineer(clean(make_sample()))
    assert np.isclose(df["log_amount"].iloc[0], np.log1p(10.0))    

def test_engineer_payment_onehot():
    df = engineer(clean(make_sample()))
    assert "payment_method_Cash" in df.columns
    assert "payment_method_Card" in df.columns
    assert "payment_method_unknown" in df.columns
    assert df["payment_method_Cash"].iloc[0] == 1    