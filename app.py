import pandas as pd
import streamlit as st

st.set_page_config(page_title="Brew & Bean Transactions")
st.title("Brew & Bean Transactions")

df = pd.read_csv("data/transactions.csv")
st.dataframe(df.head(10))