import pandas as pd
import numpy as np
from pathlib import Path
np.random.seed(42)
N= 5000
menu = {
    "Espresso": 3.0,
    "Americano": 3.5, 
    "Latte": 4.5,
    "Cappuccino": 4.5,
    "Mocha": 5.0,
    "Cold Brew": 4.8,
    "Croissant": 3.2,
    "Muffin": 2.8,
    "Sandwich": 6.5,
}
items = list(menu.keys())
dates = pd.to_datetime("2026-01-01") + pd.to_timedelta(
np.random.randint(0, 270, N),
unit = "D"
)
p = np.array([8, 10, 9, 6, 4, 8, 9, 5, 4, 4, 5, 6, 5, 3])
p = p / p.sum()        
hours = np.random.choice(range(7, 21), N, p=p)
minutes = np.random.randint(0 , 60 , N)
times = []
for h , m in zip(hours, minutes):
    times.append(f"{h:02d}:{m:02d}")
item_col = np.random.choice(items , N)
qty = np.random.choice([1,2,3], N , p =[0.7, 0.2,0.1])
amount =[]
for i , q in zip(item_col, qty):
    amount.append(round(menu[i] * q, 2))
payment = np.random.choice(["Cash", "Card", "Online"], 
N, p = [0.4, 0.45, 0.15])
df = pd.DataFrame({
    "date": dates.date,
    "time": times,
    "item": item_col,
    "amount": amount,
    "payment_method": payment,
}).sort_values(["date", "time"]).reset_index(drop=True)
Path("data").mkdir(exist_ok = True)
df.to_csv("data/transactions.csv", index=False)
print(f"Saved {len(df)} rows to data/transactions.csv")

