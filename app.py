import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from predict import predict_anomalies

st.set_page_config(page_title="Brew & Bean Transactions")
st.title("Brew & Bean Transactions")

base_folder = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_folder, "data", "transactions.csv")

if not os.path.exists(csv_path):
    import data_generator

def highlight_anomaly(row):
    if row["anomaly"] == True:
        return ["background-color: #ffcccc"] * len(row)
    return [""] * len(row)

if os.path.exists(csv_path):
    #data padho aur model se anomaly flags lagwao
    df = pd.read_csv(csv_path)
    result =predict_anomalies(df)

    #sirf tarikh wala column banao (filter ke liye)

    result["date_only"] = result["timestamp"].dt.date
    min_date = result["date_only"].min()
    max_date = result["date_only"].max()
    
    #sidebar filters
    st.sidebar.header("Filters")
    date_range = st.sidebar.date_input(
        "Date Range",
        value = (min_date, max_date),
        min_value = min_date,
        max_value = max_date    )
    hour_range = st.sidebar.slider("Hour of Day", 0, 23 , (0,23))  

    #date_input jab tak dono tarikhen na chuni jayen, sirf ek deta hai
    if len(date_range) != 2:
        st.info("Date Range ki both Dates")
        st.stop()
        
    start_date = date_range[0]
    end_date = date_range[1]
    start_hour = hour_range[0]
    end_hour = hour_range[1] 

     #filters lagao (ek ek karke)
    filtered = result.copy()
    filtered = filtered[filtered["date_only"] >= start_date]
    filtered = filtered[filtered["date_only"] <= end_date]
    filtered = filtered[filtered["hour_of_day"] >= start_hour]
    filtered = filtered[filtered["hour_of_day"] <= end_hour]
    st.write("Rows:" , len(filtered), "| Anomalies", int(filtered["anomaly"].sum()))
    
    #agar filter ke baad koi row na bache to yahin ruk jao
    if len(filtered) == 0:
        st.warning("This filter there is no transaction")
        st.stop()

    show = filtered[["date", "time","item" , "amount", "payment_method", "anomaly", "score"]]
    show = show.reset_index(drop = True)

    st.subheader("Transactions")
    st.dataframe(show.style.apply(highlight_anomaly , axis = 1))
    
    #Plotly chart (anomalies laal)
    sorted_df = filtered.sort_values("timestamp")    # waqt ke hisaab se tarteeb
    anomalies_only = sorted_df[sorted_df.anomaly == True]    # sirf anomaly rows

    fig = go.Figure()

    #neeli line: saari transactions ka amount
    fig.add_trace(go.Scatter(
        x = sorted_df["timestamp"],
        y = sorted_df["amount"],
        mode = "lines",
        name = "Amount",
        line = dict(color = "steelblue")
    ))

    #laal nuqte: sirf anomalies
    fig.add_trace(go.Scatter(
        x = anomalies_only["timestamp"],
        y = anomalies_only["amount"],
        mode = "markers",
        name = "Anomaly", 
        marker = dict(color = "red", size = 9)

    ))

    fig.update_layout(
        title = "Transaction amount over time",
        xaxis_title = "Time",
        yaxis_title = "Amount"
    )
    st.subheader("Amount over time")
    st.plotly_chart(fig)

    #download button
    flagged = show[show["anomaly"] == True]
    csv_data = flagged.to_csv(index = False)

    st.subheader("Download")
    st.download_button(
        label = "Dowanload Flagged Transction (CSV)",
        data = csv_data,
        file_name = "flagged_transactions.csv",
        mime = "text/csv",
    )


else:
    st.error("data/transactions.csv nahi mili.")
