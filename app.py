import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Brew & Bean Transactions")
st.title("Brew & Bean Transactions")

base_folder = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_folder, "data", "transactions.csv")

if not os.path.exists(csv_path):
    import data_generator

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.dataframe(df.head(10))
else:
    st.error("data/transactions.csv nahi mili.")
